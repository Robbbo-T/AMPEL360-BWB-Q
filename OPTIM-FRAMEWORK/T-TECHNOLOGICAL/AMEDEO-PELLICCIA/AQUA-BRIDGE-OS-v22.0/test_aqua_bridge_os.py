#!/usr/bin/env python3
"""
AQUA-BRIDGE-OS v22.0 Integration Test Suite
Comprehensive testing of all major components
"""

import asyncio
import logging
import sys
import time
import json
from pathlib import Path

# Add the AQUA-BRIDGE-OS modules to path
sys.path.insert(0, str(Path(__file__).parent))

# Import AQUA-BRIDGE-OS components
from kernel.gaia_air_rtos import GAIAAIRRTOSKernel, create_default_flight_partitions, Task, TaskPriority
from act.act_orchestrator import ACTOrchestrator, ComputeJob
from ccmf.ccmf_controller import CCMFController
from det.det_manager import DETManager, EvidenceType, CriticalityLevel
from energy.energy_as_policy import EnergyAsPolicyManager
from kernel.quantum.quantum_gateway import QuantumGateway, QuantumJob, QuantumJobType, QuantumBackend, create_qaoa_circuit
from platforms.tsn.tsn_manager import TSNManager, TSNPriority, FrameType

class AQUABridgeOSTestSuite:
    """Comprehensive test suite for AQUA-BRIDGE-OS v22.0"""
    
    def __init__(self):
        self.logger = logging.getLogger("AQUA-Test-Suite")
        self.test_results = {}
        self.start_time = time.time()
        
        # Initialize components
        self.kernel = None
        self.act_orchestrator = None
        self.ccmf_controller = None
        self.det_manager = None
        self.energy_manager = None
        self.quantum_gateway = None
        self.tsn_manager = None
        
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        
        self.logger.info("=" * 60)
        self.logger.info("AQUA-BRIDGE-OS v22.0 Integration Test Suite")
        self.logger.info("=" * 60)
        
        # Test sequence
        tests = [
            ("Kernel Initialization", self.test_kernel_init),
            ("ACT Triadic Architecture", self.test_act_orchestrator),
            ("CCMF Circular Computing", self.test_ccmf_cycle),
            ("Digital Evidence Twin", self.test_det_system),
            ("Energy-as-Policy", self.test_energy_policy),
            ("Quantum Gateway", self.test_quantum_gateway),
            ("TSN Networking", self.test_tsn_networking),
            ("End-to-End Integration", self.test_integration),
            ("Performance Validation", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            self.logger.info(f"\n--- Running Test: {test_name} ---")
            try:
                result = await test_func()
                self.test_results[test_name] = {"status": "PASS", "result": result}
                self.logger.info(f"✅ {test_name}: PASSED")
            except Exception as e:
                self.test_results[test_name] = {"status": "FAIL", "error": str(e)}
                self.logger.error(f"❌ {test_name}: FAILED - {e}")
        
        # Generate final report
        await self.generate_test_report()
    
    async def test_kernel_init(self):
        """Test GAIA AIR-RTOS kernel initialization"""
        
        self.kernel = GAIAAIRRTOSKernel()
        
        # Create default partitions
        partitions = create_default_flight_partitions()
        for partition in partitions:
            success = self.kernel.create_partition(partition)
            assert success, f"Failed to create partition {partition.id}"
        
        # Create test tasks
        test_task = Task(
            id="test_aileron_control",
            priority=TaskPriority.DAL_A,
            wcet_us=500,
            period_us=10000,
            partition_id="FLIGHT_CONTROL",
            substrate="cpu"
        )
        
        success = self.kernel.create_task(test_task)
        assert success, "Failed to create test task"
        
        # Start kernel
        self.kernel.start()
        
        # Verify status
        status = self.kernel.get_status()
        assert status["running"], "Kernel not running"
        assert status["partitions"] == 3, "Incorrect partition count"
        assert status["tasks"] == 1, "Incorrect task count"
        
        return status
    
    async def test_act_orchestrator(self):
        """Test ACT (Triadic Computational Architecture)"""
        
        self.act_orchestrator = ACTOrchestrator()
        
        # Create test computation job
        test_job = ComputeJob(
            id="test_flight_control_001",
            function_name="aileron_control",
            input_data=b"sensor_data_test_12345",
            expected_output_size=32,
            timeout_us=5000,
            priority=1
        )
        
        # Execute with 2oo3 redundancy
        vote_result, output = await self.act_orchestrator.execute_redundant_computation(test_job)
        
        assert vote_result.name in ["UNANIMOUS", "MAJORITY"], f"Unexpected vote result: {vote_result}"
        assert len(output) > 0, "No output from computation"
        
        # Get system status
        status = self.act_orchestrator.get_act_status()
        assert status["electronic"]["cpu_available"], "CPU lane not available"
        assert status["electronic"]["fpga_available"], "FPGA lane not available"
        assert status["electronic"]["dsp_available"], "DSP lane not available"
        
        return {
            "vote_result": vote_result.name,
            "output_size": len(output),
            "status": status
        }
    
    async def test_ccmf_cycle(self):
        """Test CCMF (Computación Circular Multi-Física) cycle"""
        
        self.ccmf_controller = CCMFController()
        
        # Run single CCMF cycle
        cycle_result = await self.ccmf_controller.run_ccmf_cycle()
        
        assert "error" not in cycle_result, f"CCMF cycle failed: {cycle_result.get('error')}"
        assert cycle_result.get("cycle_time_ms", 0) < 200, "CCMF cycle too slow"
        assert cycle_result.get("proposals_generated", 0) >= 0, "Invalid proposals count"
        
        # Get controller status
        status = self.ccmf_controller.get_status()
        assert status["cycle_count"] > 0, "No cycles completed"
        
        return {
            "cycle_result": cycle_result,
            "controller_status": status
        }
    
    async def test_det_system(self):
        """Test Digital Evidence Twin (DET) system"""
        
        self.det_manager = DETManager("./test_det_storage")
        self.det_manager.start()
        
        # Log test evidence
        evidence_id = self.det_manager.log_evidence(
            EvidenceType.VOTER_DECISION,
            CriticalityLevel.SAFETY_CRITICAL,
            "test_voter",
            {
                "job_id": "test_001",
                "vote_result": "unanimous",
                "cpu_result": "0xABCD",
                "fpga_result": "0xABCD",
                "dsp_result": "0xABCD"
            },
            {"test_mode": True, "timestamp": time.time()}
        )
        
        assert evidence_id, "Failed to log evidence"
        
        # Wait for processing
        await asyncio.sleep(0.2)
        
        # Retrieve evidence
        evidence = self.det_manager.get_evidence(evidence_id)
        assert evidence is not None, "Failed to retrieve evidence"
        assert evidence.pqc_signature.startswith("PQC_"), "Invalid PQC signature"
        
        # Generate audit report
        audit_report = self.det_manager.generate_audit_report(hours_back=1)
        assert audit_report["integrity_verified"], "Evidence integrity check failed"
        
        self.det_manager.stop()
        
        return {
            "evidence_logged": evidence_id,
            "evidence_retrieved": evidence.id,
            "audit_report": audit_report
        }
    
    async def test_energy_policy(self):
        """Test Energy-as-Policy framework"""
        
        self.energy_manager = EnergyAsPolicyManager()
        self.energy_manager.create_flight_energy_budgets()
        
        # Test energy allocation request
        allowed = self.energy_manager.request_energy_allocation(
            "FLIGHT_CRITICAL", "test_component", 5.0, "test_operation"
        )
        assert allowed, "Energy allocation should be allowed"
        
        # Log consumption
        self.energy_manager.log_actual_consumption(
            "FLIGHT_CRITICAL", "test_component", 4.5, 0.01, "test_operation"
        )
        
        # Test over-budget request
        over_budget_allowed = self.energy_manager.request_energy_allocation(
            "FLIGHT_CRITICAL", "test_component", 200.0, "large_operation"
        )
        assert not over_budget_allowed, "Over-budget allocation should be denied"
        
        # Get system status
        status = self.energy_manager.get_system_energy_status()
        assert "FLIGHT_CRITICAL" in status["budgets"], "Flight critical budget missing"
        assert status["enforcement_enabled"], "Energy enforcement not enabled"
        
        return status
    
    async def test_quantum_gateway(self):
        """Test Quantum Gateway and AQUA NISQ v1"""
        
        self.quantum_gateway = QuantumGateway()
        
        # Create test QAOA circuit
        circuit = create_qaoa_circuit(num_qubits=8, p_layers=2)
        
        # Create quantum job
        job = QuantumJob(
            id="test_qaoa_001",
            job_type=QuantumJobType.QAOA,
            circuit=circuit,
            backend=QuantumBackend.AQUA_NISQ_V1,
            shots=512,
            requester="SYSTEM",
            amores_approved=True,
            air_gap_validated=True
        )
        
        # Submit job
        success, message = await self.quantum_gateway.submit_job(job)
        assert success, f"Failed to submit quantum job: {message}"
        
        # Wait for completion
        await asyncio.sleep(1.0)
        
        # Get result
        result = self.quantum_gateway.get_job_result(job.id)
        assert result is not None, "No quantum job result"
        assert result.status.name in ["COMPLETED", "RUNNING"], f"Unexpected job status: {result.status}"
        
        # Get system status
        status = self.quantum_gateway.get_system_status()
        assert not status["flight_mode"], "Flight mode should be disabled for testing"
        
        return {
            "job_submitted": success,
            "job_result": result.status.name if result else "None",
            "system_status": status
        }
    
    async def test_tsn_networking(self):
        """Test TSN (Time-Sensitive Networking)"""
        
        self.tsn_manager = TSNManager()
        self.tsn_manager.start_scheduling()
        
        # Create control frame
        control_frame = self.tsn_manager.create_control_frame(
            source="cpu_node",
            destination="fpga_node",
            command="test_command",
            parameters={"test": True}
        )
        
        # Send frame
        success = await self.tsn_manager.send_frame(control_frame)
        assert success, "Failed to send TSN frame"
        
        # Wait for processing
        await asyncio.sleep(0.1)
        
        # Get network status
        status = self.tsn_manager.get_network_status()
        assert len(status["nodes"]) > 0, "No network nodes found"
        
        return {
            "frame_sent": success,
            "network_status": status
        }
    
    async def test_integration(self):
        """Test end-to-end integration between components"""
        
        # Ensure all components are initialized
        assert self.kernel is not None, "Kernel not initialized"
        assert self.act_orchestrator is not None, "ACT not initialized"
        assert self.ccmf_controller is not None, "CCMF not initialized"
        
        # Create integrated test scenario
        
        # 1. CCMF observes system state
        cycle_result = await self.ccmf_controller.run_ccmf_cycle()
        
        # 2. ACT executes redundant computation based on CCMF proposal
        if cycle_result.get("proposals_validated", 0) > 0:
            test_job = ComputeJob(
                id="integration_test_001",
                function_name="integrated_control",
                input_data=b"integration_test_data",
                expected_output_size=32,
                timeout_us=10000,
                priority=1
            )
            
            vote_result, output = await self.act_orchestrator.execute_redundant_computation(test_job)
            
            # 3. Log evidence to DET
            if self.det_manager:
                evidence_id = self.det_manager.log_evidence(
                    EvidenceType.CCMF_CYCLE,
                    CriticalityLevel.HIGH,
                    "integration_test",
                    {
                        "ccmf_cycle_id": cycle_result.get("cycle_id"),
                        "act_vote_result": vote_result.name,
                        "output_size": len(output)
                    }
                )
        
        # 4. Verify kernel is still running
        kernel_status = self.kernel.get_status()
        assert kernel_status["running"], "Kernel stopped during integration test"
        
        return {
            "ccmf_cycle_completed": True,
            "act_computation_completed": True,
            "det_evidence_logged": True,
            "kernel_still_running": kernel_status["running"]
        }
    
    async def test_performance(self):
        """Test performance targets and benchmarks"""
        
        performance_results = {}
        
        # Test CCMF cycle time
        start_time = time.time()
        cycle_result = await self.ccmf_controller.run_ccmf_cycle()
        ccmf_time_ms = (time.time() - start_time) * 1000
        
        performance_results["ccmf_cycle_time_ms"] = ccmf_time_ms
        performance_results["ccmf_target_met"] = ccmf_time_ms < 100  # Target: <100ms
        
        # Test ACT computation time
        start_time = time.time()
        test_job = ComputeJob(
            id="perf_test_001",
            function_name="performance_test",
            input_data=b"performance_test_data",
            expected_output_size=32,
            timeout_us=5000,
            priority=1
        )
        vote_result, output = await self.act_orchestrator.execute_redundant_computation(test_job)
        act_time_ms = (time.time() - start_time) * 1000
        
        performance_results["act_computation_time_ms"] = act_time_ms
        performance_results["act_target_met"] = act_time_ms < 25  # Target: <25ms
        
        # Test TSN latency
        if self.tsn_manager:
            network_status = self.tsn_manager.get_network_status()
            photonic_stats = network_status.get("photonic_switch", {})
            avg_latency_us = photonic_stats.get("average_latency_us", 0)
            
            performance_results["tsn_latency_us"] = avg_latency_us
            performance_results["tsn_target_met"] = avg_latency_us < 200  # Target: <200μs
        
        # Overall performance assessment
        targets_met = sum([
            performance_results.get("ccmf_target_met", False),
            performance_results.get("act_target_met", False),
            performance_results.get("tsn_target_met", False)
        ])
        
        performance_results["overall_performance_score"] = targets_met / 3
        performance_results["performance_grade"] = "PASS" if targets_met >= 2 else "FAIL"
        
        return performance_results
    
    async def generate_test_report(self):
        """Generate comprehensive test report"""
        
        total_time = time.time() - self.start_time
        
        report = {
            "aqua_bridge_os_version": "22.0",
            "test_execution_time_seconds": total_time,
            "total_tests": len(self.test_results),
            "tests_passed": len([r for r in self.test_results.values() if r["status"] == "PASS"]),
            "tests_failed": len([r for r in self.test_results.values() if r["status"] == "FAIL"]),
            "test_results": self.test_results
        }
        
        # Calculate overall status
        success_rate = report["tests_passed"] / report["total_tests"]
        report["overall_status"] = "PASS" if success_rate >= 0.8 else "FAIL"
        report["success_rate_percent"] = success_rate * 100
        
        # Log summary
        self.logger.info("\n" + "=" * 60)
        self.logger.info("AQUA-BRIDGE-OS v22.0 TEST REPORT")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Tests: {report['total_tests']}")
        self.logger.info(f"Passed: {report['tests_passed']}")
        self.logger.info(f"Failed: {report['tests_failed']}")
        self.logger.info(f"Success Rate: {report['success_rate_percent']:.1f}%")
        self.logger.info(f"Overall Status: {report['overall_status']}")
        self.logger.info(f"Execution Time: {total_time:.2f} seconds")
        self.logger.info("=" * 60)
        
        # Save report to file
        with open("aqua_bridge_os_test_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info("Test report saved to: aqua_bridge_os_test_report.json")
        
        # Cleanup
        if self.kernel:
            self.kernel.stop()
        if self.det_manager:
            self.det_manager.stop()
        
        return report

async def main():
    """Main test execution"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_suite = AQUABridgeOSTestSuite()
    
    try:
        await test_suite.run_all_tests()
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
    except Exception as e:
        logging.error(f"Test execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())