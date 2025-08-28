# GAIA AIR-RTOS Kernel
# MOS Tri-Modal (Kernel) — GAIA AIR-RTOS

"""
GAIA AIR-RTOS: Kernel principal para AQUA-BRIDGE-OS v22.0
Arquitectura Computacional Triádica (ACT) con soporte ARINC 653
"""

import threading
import time
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
import logging

class PartitionType(Enum):
    FLIGHT_CRITICAL = "flight_critical"
    NON_FLIGHT = "non_flight"
    ORGANIC_RND = "organic_rnd"

class TaskPriority(Enum):
    DAL_A = 0  # Highest priority
    DAL_B = 1
    DAL_C = 2
    DAL_D = 3
    NON_CRITICAL = 4

@dataclass
class ARINCPartition:
    """ARINC 653 Partition"""
    id: str
    partition_type: PartitionType
    memory_base: int
    memory_size: int
    cpu_budget_us: int
    period_us: int
    enabled: bool = True

@dataclass
class Task:
    """Task definition for HTS scheduler"""
    id: str
    priority: TaskPriority
    wcet_us: int  # Worst Case Execution Time
    period_us: int
    partition_id: str
    substrate: str  # "cpu", "fpga", "dsp"

class GAIAAIRRTOSKernel:
    """
    GAIA AIR-RTOS Kernel
    Microkernel design with ARINC 653 partitioning
    """
    
    def __init__(self):
        self.partitions: Dict[str, ARINCPartition] = {}
        self.tasks: Dict[str, Task] = {}
        self.running = False
        self.major_frame_us = 50000  # 50ms major frame
        self.minor_frame_us = 1000   # 1ms minor frame
        self.current_time_us = 0
        
        # HTS (Hybrid Task Scheduler) components
        self.cpu_queue = []
        self.fpga_queue = []
        self.dsp_queue = []
        
        self.logger = logging.getLogger("GAIA-AIR-RTOS")
        
    def create_partition(self, partition: ARINCPartition) -> bool:
        """Create ARINC 653 partition"""
        try:
            if partition.id in self.partitions:
                self.logger.error(f"Partition {partition.id} already exists")
                return False
                
            # Validate memory bounds and non-overlap
            if not self._validate_memory_allocation(partition):
                return False
                
            self.partitions[partition.id] = partition
            self.logger.info(f"Created partition {partition.id} type {partition.partition_type.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create partition {partition.id}: {e}")
            return False
    
    def _validate_memory_allocation(self, partition: ARINCPartition) -> bool:
        """Validate memory allocation for spatial isolation"""
        # Check for memory overlap with existing partitions
        for existing_partition in self.partitions.values():
            existing_end = existing_partition.memory_base + existing_partition.memory_size
            new_end = partition.memory_base + partition.memory_size
            
            if not (partition.memory_base >= existing_end or 
                   new_end <= existing_partition.memory_base):
                self.logger.error(f"Memory overlap detected with partition {existing_partition.id}")
                return False
        return True
    
    def create_task(self, task: Task) -> bool:
        """Create and register task"""
        try:
            if task.id in self.tasks:
                self.logger.error(f"Task {task.id} already exists")
                return False
                
            if task.partition_id not in self.partitions:
                self.logger.error(f"Partition {task.partition_id} does not exist")
                return False
                
            self.tasks[task.id] = task
            
            # Route to appropriate queue based on substrate
            if task.substrate == "cpu":
                self.cpu_queue.append(task)
            elif task.substrate == "fpga":
                self.fpga_queue.append(task)
            elif task.substrate == "dsp":
                self.dsp_queue.append(task)
            else:
                self.logger.error(f"Unknown substrate {task.substrate}")
                return False
                
            self.logger.info(f"Created task {task.id} on {task.substrate} substrate")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create task {task.id}: {e}")
            return False
    
    def hts_dispatch_loop(self):
        """Hybrid Task Scheduler dispatch loop"""
        self.logger.info("Starting HTS dispatch loop")
        
        while self.running:
            frame_start = time.time() * 1000000  # Convert to microseconds
            
            # Execute tasks in priority order within each substrate
            self._execute_substrate_tasks("CPU", self.cpu_queue)
            self._execute_substrate_tasks("FPGA", self.fpga_queue) 
            self._execute_substrate_tasks("DSP", self.dsp_queue)
            
            # Wait for end of minor frame
            frame_duration = (time.time() * 1000000) - frame_start
            if frame_duration < self.minor_frame_us:
                time.sleep((self.minor_frame_us - frame_duration) / 1000000)
            
            self.current_time_us += self.minor_frame_us
    
    def _execute_substrate_tasks(self, substrate_name: str, task_queue: List[Task]):
        """Execute tasks for a specific substrate"""
        # Sort by priority (DAL-A highest)
        sorted_tasks = sorted(task_queue, key=lambda t: t.priority.value)
        
        for task in sorted_tasks:
            if self._should_execute_task(task):
                self._execute_task(task)
    
    def _should_execute_task(self, task: Task) -> bool:
        """Check if task should execute in current time slot"""
        return (self.current_time_us % task.period_us) == 0
    
    def _execute_task(self, task: Task):
        """Execute individual task with WCET monitoring"""
        start_time = time.time() * 1000000
        
        try:
            # Simulate task execution
            self.logger.debug(f"Executing task {task.id} (WCET: {task.wcet_us}μs)")
            
            # TODO: Actual task execution would go here
            # For now, simulate execution time
            time.sleep(task.wcet_us / 2000000)  # Simulate half of WCET
            
            execution_time = (time.time() * 1000000) - start_time
            
            if execution_time > task.wcet_us:
                self.logger.warning(f"Task {task.id} exceeded WCET: {execution_time}μs > {task.wcet_us}μs")
                # Trigger FDI (Fault Detection & Isolation)
                self._signal_fdi_event(task, "WCET_BREACH")
            
        except Exception as e:
            self.logger.error(f"Task {task.id} execution failed: {e}")
            self._signal_fdi_event(task, "EXECUTION_ERROR")
    
    def _signal_fdi_event(self, task: Task, event_type: str):
        """Signal FDI (Fault Detection & Isolation) event"""
        self.logger.critical(f"FDI Event: {event_type} for task {task.id}")
        # TODO: Implement proper FDI response
    
    def start(self):
        """Start the GAIA AIR-RTOS kernel"""
        self.running = True
        self.logger.info("GAIA AIR-RTOS Kernel started")
        
        # Start HTS in separate thread
        hts_thread = threading.Thread(target=self.hts_dispatch_loop)
        hts_thread.daemon = True
        hts_thread.start()
    
    def stop(self):
        """Stop the kernel"""
        self.running = False
        self.logger.info("GAIA AIR-RTOS Kernel stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get kernel status"""
        return {
            "running": self.running,
            "partitions": len(self.partitions),
            "tasks": len(self.tasks),
            "current_time_us": self.current_time_us,
            "major_frame_us": self.major_frame_us,
            "substrate_queues": {
                "cpu": len(self.cpu_queue),
                "fpga": len(self.fpga_queue),
                "dsp": len(self.dsp_queue)
            }
        }

# Factory function for creating default flight partitions
def create_default_flight_partitions() -> List[ARINCPartition]:
    """Create default ARINC 653 partitions for flight operations"""
    return [
        ARINCPartition(
            id="FLIGHT_CONTROL",
            partition_type=PartitionType.FLIGHT_CRITICAL,
            memory_base=0x10000000,
            memory_size=0x1000000,  # 16MB
            cpu_budget_us=10000,    # 10ms
            period_us=50000         # 50ms
        ),
        ARINCPartition(
            id="NAVIGATION",
            partition_type=PartitionType.FLIGHT_CRITICAL,
            memory_base=0x11000000,
            memory_size=0x800000,   # 8MB
            cpu_budget_us=5000,     # 5ms
            period_us=50000         # 50ms
        ),
        ARINCPartition(
            id="HEALTH_MONITORING",
            partition_type=PartitionType.NON_FLIGHT,
            memory_base=0x12000000,
            memory_size=0x400000,   # 4MB
            cpu_budget_us=2000,     # 2ms
            period_us=100000        # 100ms
        )
    ]

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    kernel = GAIAAIRRTOSKernel()
    
    # Create default partitions
    for partition in create_default_flight_partitions():
        kernel.create_partition(partition)
    
    # Create example tasks
    flight_control_task = Task(
        id="AILERON_CONTROL",
        priority=TaskPriority.DAL_A,
        wcet_us=500,
        period_us=10000,
        partition_id="FLIGHT_CONTROL",
        substrate="cpu"
    )
    
    kernel.create_task(flight_control_task)
    
    print("GAIA AIR-RTOS Kernel Status:", kernel.get_status())