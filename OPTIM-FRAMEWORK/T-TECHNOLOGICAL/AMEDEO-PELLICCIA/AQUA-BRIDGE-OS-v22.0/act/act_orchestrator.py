# ACT - Arquitectura Computacional Triádica
# Triadic Computational Architecture

"""
ACT Core: Orchestrates computation across Electronic, Photonic, and Organic substrates
Implements 2oo3 redundancy with heterogeneous voting (CPU+FPGA+DSP)
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import logging
import hashlib

class SubstrateType(Enum):
    ELECTRONIC = "electronic"
    PHOTONIC = "photonic" 
    ORGANIC = "organic"

class ComputeLane(Enum):
    CPU = "cpu"
    FPGA = "fpga"
    DSP = "dsp"

class VoteResult(Enum):
    UNANIMOUS = "unanimous"
    MAJORITY = "majority"
    SPLIT = "split"
    ERROR = "error"

@dataclass
class ComputeJob:
    """Job for heterogeneous compute lanes"""
    id: str
    function_name: str
    input_data: bytes
    expected_output_size: int
    timeout_us: int
    priority: int = 0

@dataclass
class ComputeResult:
    """Result from compute lane"""
    job_id: str
    lane: ComputeLane
    output_data: bytes
    execution_time_us: int
    status: str  # "success", "timeout", "error"
    checksum: str

class VoterLogic:
    """2oo3 Voter for heterogeneous redundancy"""
    
    def __init__(self):
        self.logger = logging.getLogger("ACT-Voter")
        
    def vote(self, cpu_result: ComputeResult, 
             fpga_result: ComputeResult, 
             dsp_result: ComputeResult) -> Tuple[VoteResult, bytes, str]:
        """
        Perform 2oo3 voting on results from CPU, FPGA, DSP
        Returns: (vote_result, winning_output, reasoning)
        """
        
        # Check if all three are successful
        results = [cpu_result, fpga_result, dsp_result]
        successful_results = [r for r in results if r.status == "success"]
        
        if len(successful_results) < 2:
            return VoteResult.ERROR, b"", "Insufficient successful results for voting"
        
        # Compare checksums for exact matches
        checksum_groups = {}
        for result in successful_results:
            checksum = result.checksum
            if checksum not in checksum_groups:
                checksum_groups[checksum] = []
            checksum_groups[checksum].append(result)
        
        # Find groups with at least 2 members (2oo3)
        majority_groups = [group for group in checksum_groups.values() if len(group) >= 2]
        
        if len(majority_groups) == 1:
            # Clear majority
            winning_group = majority_groups[0]
            if len(winning_group) == 3:
                return VoteResult.UNANIMOUS, winning_group[0].output_data, "All three results match"
            else:
                return VoteResult.MAJORITY, winning_group[0].output_data, f"2oo3 majority from {[r.lane.value for r in winning_group]}"
        
        elif len(majority_groups) == 0:
            # All different - split vote
            return VoteResult.SPLIT, b"", "All results differ - no 2oo3 majority"
        
        else:
            # Multiple majority groups - should not happen with 3 inputs
            return VoteResult.ERROR, b"", "Invalid voting state"
    
    def log_vote_result(self, vote_result: VoteResult, job_id: str, reasoning: str):
        """Log voting result for DET (Digital Evidence Twin)"""
        timestamp = time.time()
        log_entry = {
            "timestamp": timestamp,
            "job_id": job_id,
            "vote_result": vote_result.value,
            "reasoning": reasoning
        }
        
        if vote_result == VoteResult.SPLIT:
            self.logger.critical(f"SPLIT VOTE for job {job_id}: {reasoning}")
        elif vote_result == VoteResult.ERROR:
            self.logger.error(f"VOTE ERROR for job {job_id}: {reasoning}")
        else:
            self.logger.info(f"Vote result for job {job_id}: {vote_result.value}")

class ElectronicSubstrate:
    """Electronic substrate manager (CPU, FPGA, DSP)"""
    
    def __init__(self):
        self.cpu_available = True
        self.fpga_available = True
        self.dsp_available = True
        self.logger = logging.getLogger("ACT-Electronic")
        
    async def execute_on_cpu(self, job: ComputeJob) -> ComputeResult:
        """Execute job on CPU lane"""
        start_time = time.time() * 1000000
        
        try:
            # Simulate CPU computation
            await asyncio.sleep(0.001)  # 1ms simulation
            
            # Generate deterministic output based on input
            output = hashlib.sha256(job.input_data + b"cpu").digest()
            checksum = hashlib.md5(output).hexdigest()
            
            execution_time = int((time.time() * 1000000) - start_time)
            
            return ComputeResult(
                job_id=job.id,
                lane=ComputeLane.CPU,
                output_data=output,
                execution_time_us=execution_time,
                status="success",
                checksum=checksum
            )
            
        except Exception as e:
            self.logger.error(f"CPU execution failed for job {job.id}: {e}")
            return ComputeResult(
                job_id=job.id,
                lane=ComputeLane.CPU,
                output_data=b"",
                execution_time_us=0,
                status="error",
                checksum=""
            )
    
    async def execute_on_fpga(self, job: ComputeJob) -> ComputeResult:
        """Execute job on FPGA lane"""
        start_time = time.time() * 1000000
        
        try:
            # Simulate FPGA computation
            await asyncio.sleep(0.0008)  # 800μs simulation
            
            # Generate same deterministic output (for voting)
            output = hashlib.sha256(job.input_data + b"cpu").digest()  # Same as CPU for testing
            checksum = hashlib.md5(output).hexdigest()
            
            execution_time = int((time.time() * 1000000) - start_time)
            
            return ComputeResult(
                job_id=job.id,
                lane=ComputeLane.FPGA,
                output_data=output,
                execution_time_us=execution_time,
                status="success",
                checksum=checksum
            )
            
        except Exception as e:
            self.logger.error(f"FPGA execution failed for job {job.id}: {e}")
            return ComputeResult(
                job_id=job.id,
                lane=ComputeLane.FPGA,
                output_data=b"",
                execution_time_us=0,
                status="error",
                checksum=""
            )
    
    async def execute_on_dsp(self, job: ComputeJob) -> ComputeResult:
        """Execute job on DSP lane"""
        start_time = time.time() * 1000000
        
        try:
            # Simulate DSP computation
            await asyncio.sleep(0.0012)  # 1.2ms simulation
            
            # Generate same deterministic output (for voting)
            output = hashlib.sha256(job.input_data + b"cpu").digest()  # Same as CPU for testing
            checksum = hashlib.md5(output).hexdigest()
            
            execution_time = int((time.time() * 1000000) - start_time)
            
            return ComputeResult(
                job_id=job.id,
                lane=ComputeLane.DSP,
                output_data=output,
                execution_time_us=execution_time,
                status="success",
                checksum=checksum
            )
            
        except Exception as e:
            self.logger.error(f"DSP execution failed for job {job.id}: {e}")
            return ComputeResult(
                job_id=job.id,
                lane=ComputeLane.DSP,
                output_data=b"",
                execution_time_us=0,
                status="error",
                checksum=""
            )

class PhotonicSubstrate:
    """Photonic substrate with TSN networking"""
    
    def __init__(self):
        self.tsn_available = True
        self.latency_target_us = 200  # 200μs target latency
        self.logger = logging.getLogger("ACT-Photonic")
        
    async def route_data(self, source: str, destination: str, data: bytes) -> bool:
        """Route data through photonic TSN backplane"""
        start_time = time.time() * 1000000
        
        try:
            # Simulate photonic routing
            await asyncio.sleep(0.0002)  # 200μs simulation
            
            routing_time = int((time.time() * 1000000) - start_time)
            
            if routing_time <= self.latency_target_us:
                self.logger.debug(f"Photonic routing {source}->{destination}: {routing_time}μs")
                return True
            else:
                self.logger.warning(f"Photonic routing exceeded target: {routing_time}μs > {self.latency_target_us}μs")
                return False
                
        except Exception as e:
            self.logger.error(f"Photonic routing failed: {e}")
            return False

class OrganicSubstrate:
    """Organic substrate (R&D, NO-FLIGHT)"""
    
    def __init__(self):
        self.flight_mode = False  # Always NO-FLIGHT
        self.logger = logging.getLogger("ACT-Organic")
        
    def execute_research_task(self, task_description: str) -> Dict[str, Any]:
        """Execute research task (NO-FLIGHT only)"""
        if self.flight_mode:
            raise RuntimeError("Organic substrate is NO-FLIGHT only")
            
        self.logger.info(f"Executing R&D task: {task_description}")
        
        # Simulate bio-inspired computation
        return {
            "task": task_description,
            "status": "completed",
            "research_data": "Bio-inspired optimization results",
            "flight_approved": False
        }

class ACTOrchestrator:
    """Main ACT orchestrator"""
    
    def __init__(self):
        self.electronic = ElectronicSubstrate()
        self.photonic = PhotonicSubstrate()
        self.organic = OrganicSubstrate()
        self.voter = VoterLogic()
        self.logger = logging.getLogger("ACT-Orchestrator")
        
    async def execute_redundant_computation(self, job: ComputeJob) -> Tuple[VoteResult, bytes]:
        """Execute job with 2oo3 redundancy"""
        
        self.logger.info(f"Starting redundant computation for job {job.id}")
        
        # Execute on all three lanes in parallel
        tasks = [
            self.electronic.execute_on_cpu(job),
            self.electronic.execute_on_fpga(job),
            self.electronic.execute_on_dsp(job)
        ]
        
        cpu_result, fpga_result, dsp_result = await asyncio.gather(*tasks)
        
        # Route results through photonic backplane
        await self.photonic.route_data("compute_lanes", "voter", b"results")
        
        # Perform voting
        vote_result, winning_output, reasoning = self.voter.vote(cpu_result, fpga_result, dsp_result)
        
        # Log vote for DET
        self.voter.log_vote_result(vote_result, job.id, reasoning)
        
        return vote_result, winning_output
    
    def get_act_status(self) -> Dict[str, Any]:
        """Get ACT system status"""
        return {
            "electronic": {
                "cpu_available": self.electronic.cpu_available,
                "fpga_available": self.electronic.fpga_available,
                "dsp_available": self.electronic.dsp_available
            },
            "photonic": {
                "tsn_available": self.photonic.tsn_available,
                "latency_target_us": self.photonic.latency_target_us
            },
            "organic": {
                "flight_mode": self.organic.flight_mode,
                "research_capabilities": "bio-inspired optimization"
            }
        }

# Example usage
async def main():
    logging.basicConfig(level=logging.INFO)
    
    orchestrator = ACTOrchestrator()
    
    # Create test job
    test_job = ComputeJob(
        id="flight_control_001",
        function_name="aileron_control",
        input_data=b"sensor_data_12345",
        expected_output_size=32,
        timeout_us=5000,
        priority=1
    )
    
    # Execute with redundancy
    vote_result, output = await orchestrator.execute_redundant_computation(test_job)
    
    print(f"Vote result: {vote_result}")
    print(f"Output length: {len(output)} bytes")
    print(f"ACT Status: {orchestrator.get_act_status()}")

if __name__ == "__main__":
    asyncio.run(main())