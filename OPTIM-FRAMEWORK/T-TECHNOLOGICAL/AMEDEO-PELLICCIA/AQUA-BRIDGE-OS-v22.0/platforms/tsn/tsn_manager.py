# TSN (Time-Sensitive Networking) Manager
# Photonic backplane and deterministic networking for AQUA-BRIDGE-OS

"""
TSN Manager: Implements Time-Sensitive Networking with photonic backplane
Provides deterministic, low-latency communication for real-time systems
Target latency: ≤ 200μs for photonic routes
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass, field
import logging
import threading
import heapq
from collections import defaultdict
import struct

class TSNPriority(Enum):
    """TSN traffic priorities (IEEE 802.1Q)"""
    EMERGENCY = 7      # Network control, emergency
    VOICE = 6          # Voice traffic
    VIDEO = 5          # Video < 100ms latency
    CONTROLLED_LOAD = 4 # Controlled load
    EXCELLENT_EFFORT = 3 # Excellent effort
    BEST_EFFORT = 1     # Best effort
    BACKGROUND = 0      # Background

class NetworkInterface(Enum):
    ELECTRONIC_ETH = "eth_electronic"
    PHOTONIC_OPT = "opt_photonic"
    WIRELESS_RF = "rf_wireless"

class FrameType(Enum):
    CONTROL = "control"
    DATA = "data"
    TELEMETRY = "telemetry"
    SYNCHRONIZATION = "sync"
    EMERGENCY = "emergency"

@dataclass
class TSNFrame:
    """TSN frame with timing constraints"""
    id: str
    source: str
    destination: str
    frame_type: FrameType
    priority: TSNPriority
    payload: bytes
    
    # Timing requirements
    max_latency_us: int
    max_jitter_us: int
    deadline_time_us: int
    
    # Routing
    interface: NetworkInterface
    path: List[str] = field(default_factory=list)
    
    # Timing tracking
    created_time_us: int = field(default_factory=lambda: int(time.time() * 1000000))
    transmitted_time_us: int = 0
    received_time_us: int = 0
    
    # Quality of Service
    bandwidth_required_mbps: float = 0.0
    reliability_required: float = 0.999

@dataclass
class NetworkNode:
    """Network node in TSN topology"""
    id: str
    name: str
    interface: NetworkInterface
    coordinates: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # 3D position
    capabilities: Set[str] = field(default_factory=set)
    connected_nodes: Set[str] = field(default_factory=set)
    
    # Performance characteristics
    processing_delay_us: int = 10
    transmission_delay_us: int = 5
    buffer_size_frames: int = 1000
    
    # State
    online: bool = True
    load_percent: float = 0.0
    temperature_celsius: float = 25.0

@dataclass
class PhotonicRoute:
    """Photonic network route"""
    route_id: str
    source_node: str
    destination_node: str
    wavelength_nm: int
    path_nodes: List[str]
    
    # Performance characteristics
    propagation_delay_us: float
    loss_db: float
    snr_db: float
    bandwidth_gbps: float
    
    # State
    active: bool = True
    reserved_bandwidth_mbps: float = 0.0

class PhotonicSwitchFabric:
    """Photonic switch fabric for ultra-low latency routing"""
    
    def __init__(self):
        self.logger = logging.getLogger("TSN-PhotonicSwitch")
        self.wavelengths = [1310, 1550, 1490, 1625]  # nm
        self.ports = 24
        self.switching_time_us = 0.1  # 100ns switching
        
        # Routing table: (source, dest) -> route
        self.routing_table: Dict[Tuple[str, str], PhotonicRoute] = {}
        self.wavelength_allocation: Dict[int, Set[str]] = {w: set() for w in self.wavelengths}
        
        # Performance tracking
        self.frames_switched = 0
        self.total_latency_us = 0.0
        
    def add_route(self, route: PhotonicRoute) -> bool:
        """Add photonic route to switch fabric"""
        
        # Check wavelength availability
        if route.route_id in self.wavelength_allocation[route.wavelength_nm]:
            self.logger.error(f"Wavelength {route.wavelength_nm}nm already allocated for route {route.route_id}")
            return False
        
        # Calculate propagation delay based on path
        total_distance_km = self._calculate_path_distance(route.path_nodes)
        route.propagation_delay_us = total_distance_km * 5.0  # ~5μs/km for fiber
        
        # Add to routing table
        key = (route.source_node, route.destination_node)
        self.routing_table[key] = route
        self.wavelength_allocation[route.wavelength_nm].add(route.route_id)
        
        self.logger.info(f"Added photonic route {route.route_id}: {route.source_node} -> {route.destination_node} "
                        f"via wavelength {route.wavelength_nm}nm, delay {route.propagation_delay_us:.1f}μs")
        
        return True
    
    def _calculate_path_distance(self, path_nodes: List[str]) -> float:
        """Calculate physical distance for path (simplified)"""
        # Simplified: assume 1km between nodes
        return len(path_nodes) * 1.0
    
    async def route_frame(self, frame: TSNFrame) -> Tuple[bool, float]:
        """Route frame through photonic fabric"""
        
        start_time = time.time() * 1000000  # μs
        
        # Find route
        route_key = (frame.source, frame.destination)
        route = self.routing_table.get(route_key)
        
        if not route or not route.active:
            return False, 0.0
        
        # Check bandwidth availability
        frame_bandwidth_mbps = len(frame.payload) * 8 / 1000  # Rough estimate
        if route.reserved_bandwidth_mbps + frame_bandwidth_mbps > route.bandwidth_gbps * 1000:
            self.logger.warning(f"Insufficient bandwidth on route {route.route_id}")
            return False, 0.0
        
        # Simulate photonic switching and transmission
        switching_delay = self.switching_time_us
        propagation_delay = route.propagation_delay_us
        transmission_delay = len(frame.payload) * 8 / (route.bandwidth_gbps * 1e9) * 1e6  # μs
        
        total_delay_us = switching_delay + propagation_delay + transmission_delay
        
        # Simulate actual transmission time
        await asyncio.sleep(total_delay_us / 1000000)
        
        # Update statistics
        self.frames_switched += 1
        self.total_latency_us += total_delay_us
        
        actual_delay = (time.time() * 1000000) - start_time
        
        return True, actual_delay
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get photonic switch performance statistics"""
        
        avg_latency_us = self.total_latency_us / self.frames_switched if self.frames_switched > 0 else 0
        
        return {
            "frames_switched": self.frames_switched,
            "average_latency_us": avg_latency_us,
            "active_routes": len([r for r in self.routing_table.values() if r.active]),
            "wavelength_utilization": {
                f"{wl}nm": len(routes) for wl, routes in self.wavelength_allocation.items()
            }
        }

class TSNScheduler:
    """TSN time-aware scheduler for deterministic transmission"""
    
    def __init__(self):
        self.logger = logging.getLogger("TSN-Scheduler")
        
        # Time windows (Gate Control List)
        self.schedule_cycle_us = 1000  # 1ms cycle
        self.current_time_us = 0
        
        # Priority queues for each traffic class
        self.priority_queues: Dict[TSNPriority, List[TSNFrame]] = {
            priority: [] for priority in TSNPriority
        }
        
        # Transmission gates (open/closed for each priority)
        self.transmission_gates: Dict[TSNPriority, bool] = {
            priority: True for priority in TSNPriority
        }
        
        # Statistics
        self.frames_transmitted = defaultdict(int)
        self.frames_dropped = defaultdict(int)
        self.latency_measurements = []
        
    def schedule_frame(self, frame: TSNFrame) -> bool:
        """Schedule frame for transmission"""
        
        # Check deadline
        current_time = int(time.time() * 1000000)
        if current_time > frame.deadline_time_us:
            self.logger.warning(f"Frame {frame.id} missed deadline")
            self.frames_dropped[frame.priority] += 1
            return False
        
        # Add to appropriate priority queue
        heapq.heappush(self.priority_queues[frame.priority], 
                      (frame.deadline_time_us, frame))
        
        return True
    
    async def transmission_loop(self):
        """Main transmission scheduling loop"""
        
        while True:
            cycle_start = time.time() * 1000000
            
            # Process each priority level
            for priority in TSNPriority:
                if self.transmission_gates[priority] and self.priority_queues[priority]:
                    
                    # Transmit frames from this priority queue
                    frames_to_transmit = []
                    current_time = int(time.time() * 1000000)
                    
                    while (self.priority_queues[priority] and 
                           len(frames_to_transmit) < 10):  # Batch size limit
                        
                        deadline, frame = heapq.heappop(self.priority_queues[priority])
                        
                        if current_time <= frame.deadline_time_us:
                            frames_to_transmit.append(frame)
                        else:
                            self.frames_dropped[priority] += 1
                            self.logger.warning(f"Dropped frame {frame.id} due to deadline miss")
                    
                    # Transmit frames
                    for frame in frames_to_transmit:
                        await self._transmit_frame(frame)
            
            # Wait for next cycle
            cycle_duration = (time.time() * 1000000) - cycle_start
            sleep_time = max(0, (self.schedule_cycle_us - cycle_duration) / 1000000)
            await asyncio.sleep(sleep_time)
    
    async def _transmit_frame(self, frame: TSNFrame):
        """Transmit individual frame"""
        
        transmission_start = time.time() * 1000000
        
        # Simulate transmission delay
        transmission_time_us = len(frame.payload) * 8 / 1000  # Assume 1Gbps
        await asyncio.sleep(transmission_time_us / 1000000)
        
        frame.transmitted_time_us = int(time.time() * 1000000)
        
        # Calculate latency
        latency_us = frame.transmitted_time_us - frame.created_time_us
        self.latency_measurements.append(latency_us)
        
        # Keep only recent measurements
        if len(self.latency_measurements) > 10000:
            self.latency_measurements = self.latency_measurements[-5000:]
        
        self.frames_transmitted[frame.priority] += 1
        
        self.logger.debug(f"Transmitted frame {frame.id}, latency: {latency_us}μs")
    
    def update_gate_schedule(self, schedule: Dict[TSNPriority, bool]):
        """Update transmission gate schedule"""
        self.transmission_gates.update(schedule)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        
        if self.latency_measurements:
            latencies = sorted(self.latency_measurements)
            p50 = latencies[len(latencies) // 2]
            p95 = latencies[int(len(latencies) * 0.95)]
            p99 = latencies[int(len(latencies) * 0.99)]
            avg_latency = sum(latencies) / len(latencies)
        else:
            p50 = p95 = p99 = avg_latency = 0
        
        return {
            "frames_transmitted": dict(self.frames_transmitted),
            "frames_dropped": dict(self.frames_dropped),
            "latency_stats": {
                "average_us": avg_latency,
                "p50_us": p50,
                "p95_us": p95,
                "p99_us": p99
            },
            "queue_depths": {
                priority.name: len(queue) for priority, queue in self.priority_queues.items()
            }
        }

class TSNManager:
    """Main TSN Manager coordinating photonic and electronic networks"""
    
    def __init__(self):
        self.logger = logging.getLogger("TSN-Manager")
        
        self.photonic_switch = PhotonicSwitchFabric()
        self.scheduler = TSNScheduler()
        
        # Network topology
        self.nodes: Dict[str, NetworkNode] = {}
        self.electronic_routes: Dict[Tuple[str, str], List[str]] = {}
        
        # Performance targets
        self.target_latency_us = 200
        self.target_jitter_us = 50
        
        # Initialize default topology
        self._initialize_default_topology()
        
    def _initialize_default_topology(self):
        """Initialize default network topology"""
        
        # Electronic nodes
        self.add_node(NetworkNode(
            id="cpu_node",
            name="CPU Compute Node",
            interface=NetworkInterface.ELECTRONIC_ETH,
            capabilities={"compute", "control"}
        ))
        
        self.add_node(NetworkNode(
            id="fpga_node",
            name="FPGA Accelerator Node",
            interface=NetworkInterface.ELECTRONIC_ETH,
            capabilities={"accelerate", "parallel"}
        ))
        
        self.add_node(NetworkNode(
            id="dsp_node",
            name="DSP Signal Processing Node",
            interface=NetworkInterface.ELECTRONIC_ETH,
            capabilities={"signal_processing", "fft"}
        ))
        
        # Photonic nodes
        self.add_node(NetworkNode(
            id="optical_switch",
            name="Photonic Switch Fabric",
            interface=NetworkInterface.PHOTONIC_OPT,
            capabilities={"switching", "routing"}
        ))
        
        # Create photonic routes
        for wavelength, source_dest in zip([1310, 1550, 1490], 
                                         [("cpu_node", "fpga_node"),
                                          ("fpga_node", "dsp_node"),
                                          ("dsp_node", "cpu_node")]):
            route = PhotonicRoute(
                route_id=f"route_{source_dest[0]}_{source_dest[1]}",
                source_node=source_dest[0],
                destination_node=source_dest[1],
                wavelength_nm=wavelength,
                path_nodes=["optical_switch"],
                propagation_delay_us=5.0,
                loss_db=1.5,
                snr_db=45.0,
                bandwidth_gbps=25.0
            )
            self.photonic_switch.add_route(route)
        
    def add_node(self, node: NetworkNode):
        """Add network node"""
        self.nodes[node.id] = node
        self.logger.info(f"Added node {node.id} ({node.interface.value})")
    
    async def send_frame(self, frame: TSNFrame) -> bool:
        """Send frame through TSN network"""
        
        # Validate nodes
        if frame.source not in self.nodes or frame.destination not in self.nodes:
            self.logger.error(f"Unknown source or destination: {frame.source} -> {frame.destination}")
            return False
        
        source_node = self.nodes[frame.source]
        dest_node = self.nodes[frame.destination]
        
        # Route selection based on interface and priority
        if (frame.interface == NetworkInterface.PHOTONIC_OPT and 
            frame.priority in [TSNPriority.EMERGENCY, TSNPriority.VOICE, TSNPriority.VIDEO]):
            
            # Use photonic route for critical traffic
            success, latency_us = await self.photonic_switch.route_frame(frame)
            
            if success:
                frame.received_time_us = int(time.time() * 1000000)
                
                if latency_us <= self.target_latency_us:
                    self.logger.debug(f"Photonic transmission successful: {latency_us:.1f}μs")
                else:
                    self.logger.warning(f"Photonic transmission exceeded target: {latency_us:.1f}μs > {self.target_latency_us}μs")
                
                return True
            else:
                self.logger.warning(f"Photonic transmission failed, falling back to electronic")
        
        # Electronic network fallback or primary path
        return await self._send_electronic(frame)
    
    async def _send_electronic(self, frame: TSNFrame) -> bool:
        """Send frame through electronic network"""
        
        # Schedule with TSN scheduler
        scheduled = self.scheduler.schedule_frame(frame)
        
        if not scheduled:
            return False
        
        # Electronic routing is handled by scheduler
        return True
    
    def start_scheduling(self):
        """Start TSN scheduling"""
        asyncio.create_task(self.scheduler.transmission_loop())
        self.logger.info("TSN scheduling started")
    
    def configure_gate_schedule(self, priority: TSNPriority, 
                               gate_pattern: List[bool], 
                               window_duration_us: int):
        """Configure time-aware gate schedule"""
        
        # Simplified gate configuration
        # In practice, this would be much more complex
        schedule = {priority: any(gate_pattern)}
        self.scheduler.update_gate_schedule(schedule)
        
        self.logger.info(f"Updated gate schedule for {priority.name}: {any(gate_pattern)}")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get comprehensive network status"""
        
        return {
            "nodes": {
                node_id: {
                    "online": node.online,
                    "load_percent": node.load_percent,
                    "interface": node.interface.value
                } for node_id, node in self.nodes.items()
            },
            "photonic_switch": self.photonic_switch.get_performance_stats(),
            "scheduler": self.scheduler.get_statistics(),
            "performance_targets": {
                "target_latency_us": self.target_latency_us,
                "target_jitter_us": self.target_jitter_us
            }
        }
    
    def create_control_frame(self, source: str, destination: str, 
                           command: str, parameters: Dict[str, Any]) -> TSNFrame:
        """Create control frame for system communication"""
        
        payload_data = {
            "command": command,
            "parameters": parameters,
            "timestamp": time.time()
        }
        
        payload_bytes = str(payload_data).encode('utf-8')
        
        return TSNFrame(
            id=f"ctrl_{int(time.time() * 1000000)}",
            source=source,
            destination=destination,
            frame_type=FrameType.CONTROL,
            priority=TSNPriority.VOICE,  # High priority for control
            payload=payload_bytes,
            max_latency_us=100,  # 100μs max latency
            max_jitter_us=10,    # 10μs max jitter
            deadline_time_us=int(time.time() * 1000000) + 500,  # 500μs deadline
            interface=NetworkInterface.PHOTONIC_OPT,
            bandwidth_required_mbps=1.0,
            reliability_required=0.9999
        )

# Example usage
async def main():
    logging.basicConfig(level=logging.INFO)
    
    tsn_manager = TSNManager()
    tsn_manager.start_scheduling()
    
    # Create and send control frame
    control_frame = tsn_manager.create_control_frame(
        source="cpu_node",
        destination="fpga_node",
        command="load_bitstream",
        parameters={"bitstream_id": "flight_control_v2.0"}
    )
    
    success = await tsn_manager.send_frame(control_frame)
    print(f"Control frame sent: {success}")
    
    # Wait for some processing
    await asyncio.sleep(0.1)
    
    # Get network status
    status = tsn_manager.get_network_status()
    print(f"Network status: {status}")

if __name__ == "__main__":
    asyncio.run(main())