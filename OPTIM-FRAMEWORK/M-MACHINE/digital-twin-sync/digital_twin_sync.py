#!/usr/bin/env python3
"""
AMPEL360 Digital Twin Synchronization Engine
Real-time synchronization between physical and digital aircraft models
"""

import json
import time
import logging
import asyncio
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from abc import ABC, abstractmethod


class SyncMode(Enum):
    """Digital twin synchronization modes"""
    REAL_TIME = "real_time"
    BATCH = "batch"
    EVENT_DRIVEN = "event_driven"
    HYBRID = "hybrid"


class DataSource(Enum):
    """Data source types"""
    PHYSICAL_SENSORS = "physical_sensors"
    SIMULATION = "simulation"
    CAD_MODEL = "cad_model"
    FLIGHT_TEST = "flight_test"
    WIND_TUNNEL = "wind_tunnel"
    USER_INPUT = "user_input"


@dataclass
class SensorData:
    """Sensor data structure"""
    sensor_id: str
    sensor_type: str
    timestamp: float
    value: Any
    unit: str
    quality: float = 1.0  # Data quality score 0-1
    location: Dict[str, float] = None  # 3D position
    metadata: Dict[str, Any] = None


@dataclass
class ModelState:
    """Digital twin model state"""
    timestamp: float
    configuration: Dict[str, Any]
    performance_metrics: Dict[str, float]
    structural_state: Dict[str, Any]
    aerodynamic_state: Dict[str, Any]
    propulsion_state: Dict[str, Any]
    environmental_conditions: Dict[str, Any]
    confidence_scores: Dict[str, float]


@dataclass
class SyncEvent:
    """Synchronization event"""
    event_id: str
    event_type: str
    timestamp: float
    source: DataSource
    data: Any
    priority: int = 0  # 0=low, 1=normal, 2=high, 3=critical


class DataProcessor(ABC):
    """Abstract data processor for different data types"""
    
    @abstractmethod
    def process(self, raw_data: Any) -> SensorData:
        """Process raw data into standardized sensor data"""
        pass
    
    @abstractmethod
    def validate(self, data: SensorData) -> bool:
        """Validate sensor data quality"""
        pass


class StructuralDataProcessor(DataProcessor):
    """Processor for structural sensor data"""
    
    def process(self, raw_data: Any) -> SensorData:
        """Process structural measurements"""
        return SensorData(
            sensor_id=raw_data.get("id", "unknown"),
            sensor_type="structural",
            timestamp=time.time(),
            value=raw_data.get("strain", 0.0),
            unit="microstrain",
            quality=self._calculate_quality(raw_data),
            location=raw_data.get("position", {}),
            metadata={"temperature": raw_data.get("temp", 20.0)}
        )
    
    def validate(self, data: SensorData) -> bool:
        """Validate structural data"""
        if data.sensor_type != "structural":
            return False
        
        # Check reasonable strain values
        strain = data.value
        if not isinstance(strain, (int, float)):
            return False
        
        # Typical aerospace strain limits
        return -10000 <= strain <= 10000
    
    def _calculate_quality(self, raw_data: Dict) -> float:
        """Calculate data quality score"""
        quality = 1.0
        
        # Reduce quality for missing temperature compensation
        if "temp" not in raw_data:
            quality *= 0.9
        
        # Reduce quality for noisy data
        if "noise_level" in raw_data and raw_data["noise_level"] > 0.1:
            quality *= 0.8
        
        return quality


class AerodynamicDataProcessor(DataProcessor):
    """Processor for aerodynamic sensor data"""
    
    def process(self, raw_data: Any) -> SensorData:
        """Process aerodynamic measurements"""
        return SensorData(
            sensor_id=raw_data.get("id", "unknown"),
            sensor_type="aerodynamic",
            timestamp=time.time(),
            value=raw_data.get("pressure", 0.0),
            unit="Pa",
            quality=self._calculate_quality(raw_data),
            location=raw_data.get("position", {}),
            metadata={
                "mach_number": raw_data.get("mach", 0.0),
                "reynolds_number": raw_data.get("reynolds", 0.0)
            }
        )
    
    def validate(self, data: SensorData) -> bool:
        """Validate aerodynamic data"""
        if data.sensor_type != "aerodynamic":
            return False
        
        pressure = data.value
        if not isinstance(pressure, (int, float)):
            return False
        
        # Reasonable pressure range for aerospace applications
        return 0 <= pressure <= 200000  # Up to ~2 atm


    def _calculate_quality(self, raw_data: Dict) -> float:
        """Calculate aerodynamic data quality"""
        quality = 1.0
        
        # Higher quality for calibrated sensors
        if raw_data.get("calibrated", False):
            quality *= 1.1
        
        # Account for flow conditions
        mach = raw_data.get("mach", 0.0)
        if mach > 0.8:  # Transonic effects reduce measurement quality
            quality *= 0.9
        
        return min(quality, 1.0)


class DigitalTwinSynchronizer:
    """
    Core synchronization engine for digital twin operations
    """
    
    def __init__(self, sync_mode: SyncMode = SyncMode.REAL_TIME):
        self.sync_mode = sync_mode
        self.logger = logging.getLogger(__name__)
        
        # Data processors
        self.processors = {
            "structural": StructuralDataProcessor(),
            "aerodynamic": AerodynamicDataProcessor()
        }
        
        # Synchronization state
        self.current_state = None
        self.sync_history = []
        self.event_queue = asyncio.Queue()
        self.subscribers = []
        
        # Performance metrics
        self.sync_frequency = 10.0  # Hz
        self.latency_threshold = 0.1  # seconds
        self.quality_threshold = 0.8
        
        # Threading for real-time operation
        self.sync_thread = None
        self.running = False
    
    def add_data_processor(self, data_type: str, processor: DataProcessor):
        """Add custom data processor"""
        self.processors[data_type] = processor
        self.logger.info(f"Added data processor for {data_type}")
    
    def subscribe(self, callback: Callable[[ModelState], None]):
        """Subscribe to state updates"""
        self.subscribers.append(callback)
    
    async def ingest_data(self, source: DataSource, raw_data: Any):
        """Ingest data from various sources"""
        try:
            # Determine data type and process
            data_type = self._detect_data_type(raw_data)
            
            if data_type in self.processors:
                sensor_data = self.processors[data_type].process(raw_data)
                
                # Validate data
                if self.processors[data_type].validate(sensor_data):
                    # Create sync event
                    event = SyncEvent(
                        event_id=f"evt_{int(time.time()*1000)}",
                        event_type="data_update",
                        timestamp=time.time(),
                        source=source,
                        data=sensor_data,
                        priority=self._calculate_priority(sensor_data)
                    )
                    
                    # Queue for processing
                    await self.event_queue.put(event)
                    self.logger.debug(f"Ingested {data_type} data from {source.value}")
                else:
                    self.logger.warning(f"Invalid {data_type} data rejected")
            else:
                self.logger.warning(f"No processor available for data type: {data_type}")
        
        except Exception as e:
            self.logger.error(f"Data ingestion failed: {e}")
    
    def _detect_data_type(self, raw_data: Any) -> str:
        """Auto-detect data type from raw data"""
        if isinstance(raw_data, dict):
            if "strain" in raw_data or "stress" in raw_data:
                return "structural"
            elif "pressure" in raw_data or "velocity" in raw_data:
                return "aerodynamic"
        
        return "unknown"
    
    def _calculate_priority(self, sensor_data: SensorData) -> int:
        """Calculate event priority based on sensor data"""
        # High priority for critical structural measurements
        if sensor_data.sensor_type == "structural":
            strain = abs(sensor_data.value)
            if strain > 5000:  # High strain
                return 3  # Critical
            elif strain > 2000:
                return 2  # High
        
        # Normal priority for aerodynamic data
        if sensor_data.sensor_type == "aerodynamic":
            return 1
        
        return 0  # Low priority by default
    
    async def process_events(self):
        """Process events from the queue"""
        while self.running:
            try:
                # Get event with timeout
                event = await asyncio.wait_for(
                    self.event_queue.get(), 
                    timeout=1.0
                )
                
                # Process based on event type
                if event.event_type == "data_update":
                    await self._process_data_update(event)
                elif event.event_type == "model_update":
                    await self._process_model_update(event)
                
                # Mark event as processed
                self.event_queue.task_done()
                
            except asyncio.TimeoutError:
                # No events to process, continue
                continue
            except Exception as e:
                self.logger.error(f"Event processing failed: {e}")
    
    async def _process_data_update(self, event: SyncEvent):
        """Process data update event"""
        sensor_data = event.data
        
        # Update model state based on sensor data
        if self.current_state is None:
            self.current_state = self._create_initial_state()
        
        # Update relevant state components
        if sensor_data.sensor_type == "structural":
            self._update_structural_state(sensor_data)
        elif sensor_data.sensor_type == "aerodynamic":
            self._update_aerodynamic_state(sensor_data)
        
        # Update timestamp and confidence
        self.current_state.timestamp = time.time()
        self._update_confidence_scores()
        
        # Notify subscribers
        for callback in self.subscribers:
            try:
                callback(self.current_state)
            except Exception as e:
                self.logger.error(f"Subscriber notification failed: {e}")
        
        # Store in history
        self.sync_history.append(self.current_state)
        
        # Limit history size
        if len(self.sync_history) > 1000:
            self.sync_history = self.sync_history[-500:]
    
    async def _process_model_update(self, event: SyncEvent):
        """Process model update event"""
        # Handle model configuration changes
        model_data = event.data
        
        if self.current_state:
            self.current_state.configuration.update(model_data)
            self.current_state.timestamp = time.time()
    
    def _create_initial_state(self) -> ModelState:
        """Create initial model state"""
        return ModelState(
            timestamp=time.time(),
            configuration={
                "wingspan": 60.0,
                "chord_root": 15.0,
                "chord_tip": 4.0,
                "sweep_angle": 25.0
            },
            performance_metrics={
                "lift_coefficient": 0.0,
                "drag_coefficient": 0.0,
                "lift_to_drag": 0.0
            },
            structural_state={
                "max_strain": 0.0,
                "max_stress": 0.0,
                "safety_factor": 1.0
            },
            aerodynamic_state={
                "surface_pressure": {},
                "velocity_field": {},
                "flow_separation": False
            },
            propulsion_state={
                "thrust": 0.0,
                "fuel_flow": 0.0,
                "efficiency": 0.0
            },
            environmental_conditions={
                "altitude": 0.0,
                "airspeed": 0.0,
                "temperature": 288.15,
                "pressure": 101325.0
            },
            confidence_scores={
                "structural": 1.0,
                "aerodynamic": 1.0,
                "overall": 1.0
            }
        )
    
    def _update_structural_state(self, sensor_data: SensorData):
        """Update structural state with sensor data"""
        strain = sensor_data.value
        
        # Update maximum strain if higher
        current_max = self.current_state.structural_state.get("max_strain", 0)
        if abs(strain) > abs(current_max):
            self.current_state.structural_state["max_strain"] = strain
        
        # Estimate stress (simplified)
        elastic_modulus = 230e9  # Pa for carbon fiber
        stress = strain * 1e-6 * elastic_modulus  # Convert microstrain to stress
        
        current_max_stress = self.current_state.structural_state.get("max_stress", 0)
        if abs(stress) > abs(current_max_stress):
            self.current_state.structural_state["max_stress"] = stress
        
        # Update safety factor
        yield_strength = 1500e6  # Pa
        if abs(stress) > 0:
            safety_factor = yield_strength / abs(stress)
            self.current_state.structural_state["safety_factor"] = safety_factor
    
    def _update_aerodynamic_state(self, sensor_data: SensorData):
        """Update aerodynamic state with sensor data"""
        pressure = sensor_data.value
        location = sensor_data.location or {}
        
        # Store pressure at location
        loc_key = f"{location.get('x', 0):.2f}_{location.get('y', 0):.2f}"
        self.current_state.aerodynamic_state["surface_pressure"][loc_key] = pressure
        
        # Estimate coefficients (simplified)
        dynamic_pressure = 0.5 * 1.225 * (self.current_state.environmental_conditions.get("airspeed", 0)**2)
        
        if dynamic_pressure > 0:
            # Simplified lift coefficient estimation
            pressure_diff = pressure - 101325.0  # Difference from standard pressure
            cl_contribution = pressure_diff / dynamic_pressure / 100  # Simplified
            
            current_cl = self.current_state.performance_metrics.get("lift_coefficient", 0)
            self.current_state.performance_metrics["lift_coefficient"] = current_cl + cl_contribution
    
    def _update_confidence_scores(self):
        """Update confidence scores based on data quality and recency"""
        current_time = time.time()
        
        # Decay confidence over time
        time_decay = min(1.0, (current_time - self.current_state.timestamp) / 10.0)
        
        for key in self.current_state.confidence_scores:
            if key != "overall":
                self.current_state.confidence_scores[key] *= (1.0 - time_decay)
        
        # Overall confidence is minimum of all subsystems
        subsystem_scores = [v for k, v in self.current_state.confidence_scores.items() if k != "overall"]
        self.current_state.confidence_scores["overall"] = min(subsystem_scores) if subsystem_scores else 0.0
    
    def start_synchronization(self):
        """Start real-time synchronization"""
        if self.running:
            self.logger.warning("Synchronization already running")
            return
        
        self.running = True
        self.logger.info("Starting digital twin synchronization")
        
        # Start event processing loop
        asyncio.create_task(self.process_events())
    
    def stop_synchronization(self):
        """Stop synchronization"""
        self.running = False
        self.logger.info("Digital twin synchronization stopped")
    
    def get_current_state(self) -> Optional[ModelState]:
        """Get current model state"""
        return self.current_state
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get synchronization performance statistics"""
        if not self.sync_history:
            return {"error": "No sync history available"}
        
        # Calculate statistics
        recent_states = self.sync_history[-100:]  # Last 100 states
        
        timestamps = [state.timestamp for state in recent_states]
        if len(timestamps) > 1:
            intervals = np.diff(timestamps)
            avg_frequency = 1.0 / np.mean(intervals) if np.mean(intervals) > 0 else 0
            max_latency = np.max(intervals)
        else:
            avg_frequency = 0
            max_latency = 0
        
        confidence_scores = [state.confidence_scores["overall"] for state in recent_states]
        avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
        
        return {
            "sync_frequency_hz": avg_frequency,
            "max_latency_s": max_latency,
            "average_confidence": avg_confidence,
            "total_updates": len(self.sync_history),
            "queue_size": self.event_queue.qsize() if hasattr(self.event_queue, 'qsize') else 0
        }


class BWBDigitalTwin:
    """
    Complete digital twin implementation for BWB aircraft
    """
    
    def __init__(self):
        self.synchronizer = DigitalTwinSynchronizer(SyncMode.REAL_TIME)
        self.logger = logging.getLogger(__name__)
        
        # Subscribe to state updates
        self.synchronizer.subscribe(self._on_state_update)
        
        # Performance monitoring
        self.update_count = 0
        self.last_performance_log = time.time()
    
    def _on_state_update(self, state: ModelState):
        """Handle state updates"""
        self.update_count += 1
        
        # Log performance periodically
        current_time = time.time()
        if current_time - self.last_performance_log > 10.0:  # Every 10 seconds
            stats = self.synchronizer.get_sync_statistics()
            self.logger.info(f"Digital twin stats: {stats}")
            self.last_performance_log = current_time
    
    async def simulate_flight_test(self, duration: float = 60.0):
        """Simulate a flight test with synthetic sensor data"""
        self.logger.info(f"Starting simulated flight test for {duration} seconds")
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Generate synthetic structural data
            strain_data = {
                "id": "strain_001",
                "strain": np.random.normal(1000, 200),  # Microstrain
                "temp": np.random.normal(20, 5),
                "position": {"x": 15.0, "y": 5.0, "z": 0.0}
            }
            
            await self.synchronizer.ingest_data(
                DataSource.PHYSICAL_SENSORS,
                strain_data
            )
            
            # Generate synthetic aerodynamic data
            pressure_data = {
                "id": "pressure_001", 
                "pressure": np.random.normal(101325, 1000),  # Pa
                "mach": 0.8,
                "position": {"x": 10.0, "y": 3.0, "z": 0.0}
            }
            
            await self.synchronizer.ingest_data(
                DataSource.PHYSICAL_SENSORS,
                pressure_data
            )
            
            # Update environmental conditions
            airspeed = 200 + 50 * np.sin((time.time() - start_time) / 10.0)  # Varying airspeed
            env_data = {
                "airspeed": airspeed,
                "altitude": 10000,
                "temperature": 223.15,  # Temperature at 10km
                "pressure": 26500  # Pressure at 10km
            }
            
            await self.synchronizer.ingest_data(
                DataSource.FLIGHT_TEST,
                env_data
            )
            
            # Wait for next update
            await asyncio.sleep(0.1)  # 10 Hz updates
        
        self.logger.info("Simulated flight test completed")
    
    def get_twin_status(self) -> Dict[str, Any]:
        """Get comprehensive digital twin status"""
        state = self.synchronizer.get_current_state()
        stats = self.synchronizer.get_sync_statistics()
        
        if state is None:
            return {"error": "Digital twin not initialized"}
        
        return {
            "current_state": asdict(state),
            "sync_statistics": stats,
            "update_count": self.update_count,
            "running": self.synchronizer.running
        }


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    async def main():
        print("🌐 AMPEL360 Digital Twin Synchronization Engine")
        print("=" * 60)
        
        # Create BWB digital twin
        bwb_twin = BWBDigitalTwin()
        
        # Start synchronization
        bwb_twin.synchronizer.start_synchronization()
        
        print("🚀 Starting digital twin synchronization...")
        
        # Run simulated flight test
        print("✈️  Running simulated flight test...")
        await bwb_twin.simulate_flight_test(duration=30.0)
        
        # Get final status
        status = bwb_twin.get_twin_status()
        
        print("\n📊 Digital Twin Status:")
        print(f"   Updates processed: {status['update_count']}")
        print(f"   Sync frequency: {status['sync_statistics']['sync_frequency_hz']:.1f} Hz")
        print(f"   Average confidence: {status['sync_statistics']['average_confidence']:.2f}")
        
        current_state = status['current_state']
        print(f"\n🏗️  Current State:")
        print(f"   Max strain: {current_state['structural_state']['max_strain']:.0f} μɛ")
        print(f"   Safety factor: {current_state['structural_state']['safety_factor']:.2f}")
        print(f"   Lift coefficient: {current_state['performance_metrics']['lift_coefficient']:.3f}")
        print(f"   Overall confidence: {current_state['confidence_scores']['overall']:.2%}")
        
        # Stop synchronization
        bwb_twin.synchronizer.stop_synchronization()
        
        print("\n🎯 Digital twin synchronization demonstration complete!")
    
    # Run the async main function
    asyncio.run(main())