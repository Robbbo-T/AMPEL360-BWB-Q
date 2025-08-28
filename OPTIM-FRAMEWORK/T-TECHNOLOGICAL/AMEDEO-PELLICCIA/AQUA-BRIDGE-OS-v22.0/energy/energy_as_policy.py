# Energy-as-Policy Framework
# Executable energy and carbon budgets as runtime policies

"""
Energy-as-Policy (EaP): Implements energy and carbon constraints as executable
policies at the RTOS partition level. Ensures no operation violates
sustainability budgets defined in kJ and gCO₂.
"""

import time
import threading
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
import logging
import json
from abc import ABC, abstractmethod

class EnergyPolicyLevel(Enum):
    SYSTEM = "system"
    PARTITION = "partition"
    TASK = "task"
    COMPONENT = "component"

class PolicyViolationSeverity(Enum):
    WARNING = "warning"
    THROTTLE = "throttle"
    DENY = "deny"
    EMERGENCY_SHUTDOWN = "emergency_shutdown"

class CarbonAccountingMethod(Enum):
    DIRECT_MEASUREMENT = "direct"
    GRID_FACTOR = "grid_factor"
    LIFECYCLE_ASSESSMENT = "lca"

@dataclass
class EnergyBudget:
    """Energy budget definition"""
    id: str
    name: str
    max_energy_kj: float
    max_carbon_gco2: float
    time_window_seconds: float
    priority: int = 1
    accounting_method: CarbonAccountingMethod = CarbonAccountingMethod.GRID_FACTOR
    
    # Current consumption tracking
    current_energy_kj: float = 0.0
    current_carbon_gco2: float = 0.0
    window_start_time: float = field(default_factory=time.time)
    
    # Violation handling
    violation_callback: Optional[Callable] = None
    escalation_threshold: float = 0.9  # Trigger warnings at 90%

@dataclass
class EnergyConsumptionEvent:
    """Energy consumption event"""
    timestamp: float
    source_component: str
    partition_id: str
    energy_kj: float
    carbon_gco2: float
    operation_description: str
    duration_seconds: float

@dataclass
class PolicyViolation:
    """Energy policy violation"""
    timestamp: float
    budget_id: str
    severity: PolicyViolationSeverity
    current_consumption: float
    budget_limit: float
    violation_type: str  # "energy" or "carbon"
    action_taken: str

class EnergyMonitor:
    """Real-time energy consumption monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger("EaP-Monitor")
        self.consumption_history: List[EnergyConsumptionEvent] = []
        self.power_measurement_callbacks: Dict[str, Callable] = {}
        
        # Grid carbon intensity (gCO₂/kWh) - would be updated from external source
        self.grid_carbon_intensity = 400  # Example value
        
    def register_power_meter(self, component_id: str, callback: Callable[[], float]):
        """Register power measurement callback for component"""
        self.power_measurement_callbacks[component_id] = callback
        self.logger.info(f"Registered power meter for {component_id}")
    
    def measure_current_power(self) -> Dict[str, float]:
        """Measure current power consumption across all components"""
        measurements = {}
        
        for component_id, callback in self.power_measurement_callbacks.items():
            try:
                power_watts = callback()
                measurements[component_id] = power_watts
            except Exception as e:
                self.logger.error(f"Failed to measure power for {component_id}: {e}")
                measurements[component_id] = 0.0
        
        return measurements
    
    def calculate_carbon_emission(self, energy_kwh: float, 
                                 method: CarbonAccountingMethod = CarbonAccountingMethod.GRID_FACTOR) -> float:
        """Calculate carbon emission for energy consumption"""
        
        if method == CarbonAccountingMethod.GRID_FACTOR:
            return energy_kwh * self.grid_carbon_intensity
        elif method == CarbonAccountingMethod.DIRECT_MEASUREMENT:
            # Would integrate with direct emission sensors
            return energy_kwh * self.grid_carbon_intensity
        elif method == CarbonAccountingMethod.LIFECYCLE_ASSESSMENT:
            # Includes manufacturing, transport, disposal
            lca_factor = self.grid_carbon_intensity * 1.2  # 20% overhead
            return energy_kwh * lca_factor
        
        return 0.0
    
    def log_consumption(self, source_component: str, partition_id: str,
                       energy_kj: float, duration_seconds: float,
                       operation_description: str = ""):
        """Log energy consumption event"""
        
        energy_kwh = energy_kj / 3600  # Convert kJ to kWh
        carbon_gco2 = self.calculate_carbon_emission(energy_kwh)
        
        event = EnergyConsumptionEvent(
            timestamp=time.time(),
            source_component=source_component,
            partition_id=partition_id,
            energy_kj=energy_kj,
            carbon_gco2=carbon_gco2,
            operation_description=operation_description,
            duration_seconds=duration_seconds
        )
        
        self.consumption_history.append(event)
        self.logger.debug(f"Logged consumption: {energy_kj:.2f}kJ, {carbon_gco2:.2f}gCO₂ from {source_component}")
        
        return event

class EnergyPolicyEngine:
    """Energy policy enforcement engine"""
    
    def __init__(self, monitor: EnergyMonitor):
        self.monitor = monitor
        self.budgets: Dict[str, EnergyBudget] = {}
        self.violations: List[PolicyViolation] = []
        
        self.policy_lock = threading.Lock()
        self.enforcement_enabled = True
        
        self.logger = logging.getLogger("EaP-PolicyEngine")
    
    def create_budget(self, budget: EnergyBudget) -> bool:
        """Create energy budget policy"""
        with self.policy_lock:
            if budget.id in self.budgets:
                self.logger.error(f"Budget {budget.id} already exists")
                return False
            
            self.budgets[budget.id] = budget
            self.logger.info(f"Created energy budget {budget.id}: {budget.max_energy_kj}kJ, {budget.max_carbon_gco2}gCO₂")
            return True
    
    def check_consumption_allowed(self, budget_id: str, requested_energy_kj: float) -> bool:
        """Check if energy consumption is allowed under policy"""
        
        if not self.enforcement_enabled:
            return True
        
        with self.policy_lock:
            budget = self.budgets.get(budget_id)
            if not budget:
                self.logger.warning(f"Unknown budget {budget_id} - allowing consumption")
                return True
            
            # Check if we need to reset the time window
            current_time = time.time()
            if current_time - budget.window_start_time > budget.time_window_seconds:
                self._reset_budget_window(budget, current_time)
            
            # Calculate projected consumption
            projected_energy = budget.current_energy_kj + requested_energy_kj
            
            # Convert to carbon
            energy_kwh = requested_energy_kj / 3600
            additional_carbon = self.monitor.calculate_carbon_emission(energy_kwh, budget.accounting_method)
            projected_carbon = budget.current_carbon_gco2 + additional_carbon
            
            # Check budget limits
            energy_violation = projected_energy > budget.max_energy_kj
            carbon_violation = projected_carbon > budget.max_carbon_gco2
            
            if energy_violation or carbon_violation:
                violation_type = "energy" if energy_violation else "carbon"
                severity = self._determine_violation_severity(budget, projected_energy, projected_carbon)
                
                violation = PolicyViolation(
                    timestamp=current_time,
                    budget_id=budget_id,
                    severity=severity,
                    current_consumption=projected_energy if energy_violation else projected_carbon,
                    budget_limit=budget.max_energy_kj if energy_violation else budget.max_carbon_gco2,
                    violation_type=violation_type,
                    action_taken="denied"
                )
                
                self.violations.append(violation)
                self._handle_violation(budget, violation)
                
                return False
            
            # Check escalation threshold for warnings
            energy_usage_ratio = projected_energy / budget.max_energy_kj
            carbon_usage_ratio = projected_carbon / budget.max_carbon_gco2
            
            if energy_usage_ratio > budget.escalation_threshold or carbon_usage_ratio > budget.escalation_threshold:
                self.logger.warning(f"Budget {budget_id} approaching limit: {energy_usage_ratio:.1%} energy, {carbon_usage_ratio:.1%} carbon")
            
            return True
    
    def update_consumption(self, budget_id: str, energy_kj: float, carbon_gco2: float):
        """Update actual consumption for budget tracking"""
        with self.policy_lock:
            budget = self.budgets.get(budget_id)
            if budget:
                budget.current_energy_kj += energy_kj
                budget.current_carbon_gco2 += carbon_gco2
                
                self.logger.debug(f"Updated budget {budget_id}: {budget.current_energy_kj:.2f}/{budget.max_energy_kj}kJ")
    
    def _reset_budget_window(self, budget: EnergyBudget, current_time: float):
        """Reset budget consumption window"""
        budget.current_energy_kj = 0.0
        budget.current_carbon_gco2 = 0.0
        budget.window_start_time = current_time
        
        self.logger.debug(f"Reset budget window for {budget.id}")
    
    def _determine_violation_severity(self, budget: EnergyBudget, 
                                    projected_energy: float, 
                                    projected_carbon: float) -> PolicyViolationSeverity:
        """Determine violation severity based on overage"""
        
        energy_overage = (projected_energy - budget.max_energy_kj) / budget.max_energy_kj
        carbon_overage = (projected_carbon - budget.max_carbon_gco2) / budget.max_carbon_gco2
        
        max_overage = max(energy_overage, carbon_overage)
        
        if max_overage > 2.0:  # 200% over budget
            return PolicyViolationSeverity.EMERGENCY_SHUTDOWN
        elif max_overage > 0.5:  # 50% over budget
            return PolicyViolationSeverity.DENY
        elif max_overage > 0.1:  # 10% over budget
            return PolicyViolationSeverity.THROTTLE
        else:
            return PolicyViolationSeverity.WARNING
    
    def _handle_violation(self, budget: EnergyBudget, violation: PolicyViolation):
        """Handle policy violation"""
        
        self.logger.error(f"Energy policy violation: {violation.violation_type} budget {violation.budget_id} "
                         f"({violation.current_consumption:.2f} > {violation.budget_limit:.2f}) - {violation.severity.value}")
        
        # Call budget-specific violation handler
        if budget.violation_callback:
            try:
                budget.violation_callback(violation)
            except Exception as e:
                self.logger.error(f"Budget violation callback failed: {e}")
        
        # Take system-level action based on severity
        if violation.severity == PolicyViolationSeverity.EMERGENCY_SHUTDOWN:
            self.logger.critical("EMERGENCY SHUTDOWN triggered by energy policy violation")
            # Would trigger emergency shutdown sequence
        elif violation.severity == PolicyViolationSeverity.DENY:
            # Already denied - log for audit
            pass
        elif violation.severity == PolicyViolationSeverity.THROTTLE:
            self.logger.warning("System throttling due to energy policy")
            # Would trigger performance throttling
    
    def get_budget_status(self, budget_id: str) -> Optional[Dict[str, Any]]:
        """Get current budget status"""
        with self.policy_lock:
            budget = self.budgets.get(budget_id)
            if not budget:
                return None
            
            current_time = time.time()
            window_remaining = budget.time_window_seconds - (current_time - budget.window_start_time)
            
            return {
                "budget_id": budget.id,
                "name": budget.name,
                "energy_usage": {
                    "current_kj": budget.current_energy_kj,
                    "max_kj": budget.max_energy_kj,
                    "usage_percent": (budget.current_energy_kj / budget.max_energy_kj) * 100
                },
                "carbon_usage": {
                    "current_gco2": budget.current_carbon_gco2,
                    "max_gco2": budget.max_carbon_gco2,
                    "usage_percent": (budget.current_carbon_gco2 / budget.max_carbon_gco2) * 100
                },
                "time_window": {
                    "total_seconds": budget.time_window_seconds,
                    "remaining_seconds": max(0, window_remaining),
                    "progress_percent": ((budget.time_window_seconds - window_remaining) / budget.time_window_seconds) * 100
                }
            }

class EnergyOptimizer:
    """Energy optimization engine"""
    
    def __init__(self, monitor: EnergyMonitor, policy_engine: EnergyPolicyEngine):
        self.monitor = monitor
        self.policy_engine = policy_engine
        self.logger = logging.getLogger("EaP-Optimizer")
        
        self.optimization_strategies = [
            self._cpu_frequency_scaling,
            self._workload_scheduling,
            self._component_power_gating,
            self._thermal_management
        ]
    
    def suggest_optimizations(self, budget_id: str) -> List[Dict[str, Any]]:
        """Suggest energy optimizations for budget"""
        
        budget_status = self.policy_engine.get_budget_status(budget_id)
        if not budget_status:
            return []
        
        suggestions = []
        
        # Analyze current consumption patterns
        recent_consumption = self._analyze_recent_consumption()
        
        # Apply optimization strategies
        for strategy in self.optimization_strategies:
            strategy_suggestions = strategy(budget_status, recent_consumption)
            suggestions.extend(strategy_suggestions)
        
        # Sort by potential energy savings
        suggestions.sort(key=lambda s: s.get('energy_savings_kj', 0), reverse=True)
        
        return suggestions
    
    def _analyze_recent_consumption(self) -> Dict[str, Any]:
        """Analyze recent energy consumption patterns"""
        
        recent_events = [e for e in self.monitor.consumption_history 
                        if time.time() - e.timestamp < 300]  # Last 5 minutes
        
        if not recent_events:
            return {}
        
        total_energy = sum(e.energy_kj for e in recent_events)
        avg_power = (total_energy / 300) * 1000 if recent_events else 0  # Average watts
        
        component_usage = {}
        for event in recent_events:
            if event.source_component not in component_usage:
                component_usage[event.source_component] = 0
            component_usage[event.source_component] += event.energy_kj
        
        return {
            "total_energy_kj": total_energy,
            "average_power_w": avg_power,
            "component_usage": component_usage,
            "event_count": len(recent_events)
        }
    
    def _cpu_frequency_scaling(self, budget_status: Dict[str, Any], 
                              consumption_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """CPU frequency scaling optimization"""
        
        suggestions = []
        
        if budget_status["energy_usage"]["usage_percent"] > 80:
            suggestions.append({
                "strategy": "cpu_frequency_scaling",
                "description": "Reduce CPU frequency to save energy",
                "parameters": {
                    "target_frequency_mhz": 1800,  # Down from 2400
                    "expected_performance_impact": "5-10%"
                },
                "energy_savings_kj": 12.5,
                "carbon_savings_gco2": 4.2,
                "implementation_complexity": "low"
            })
        
        return suggestions
    
    def _workload_scheduling(self, budget_status: Dict[str, Any], 
                            consumption_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Workload scheduling optimization"""
        
        suggestions = []
        
        if consumption_analysis.get("average_power_w", 0) > 1000:
            suggestions.append({
                "strategy": "workload_scheduling",
                "description": "Defer non-critical tasks to reduce peak power",
                "parameters": {
                    "defer_tasks": ["health_monitoring", "log_rotation"],
                    "defer_duration_seconds": 300
                },
                "energy_savings_kj": 8.3,
                "carbon_savings_gco2": 2.8,
                "implementation_complexity": "medium"
            })
        
        return suggestions
    
    def _component_power_gating(self, budget_status: Dict[str, Any], 
                               consumption_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Component power gating optimization"""
        
        suggestions = []
        
        # Find underutilized components
        component_usage = consumption_analysis.get("component_usage", {})
        for component, usage_kj in component_usage.items():
            if usage_kj < 1.0:  # Very low usage
                suggestions.append({
                    "strategy": "component_power_gating",
                    "description": f"Power gate unused component {component}",
                    "parameters": {
                        "component": component,
                        "gate_duration_seconds": 60
                    },
                    "energy_savings_kj": 5.2,
                    "carbon_savings_gco2": 1.7,
                    "implementation_complexity": "high"
                })
        
        return suggestions
    
    def _thermal_management(self, budget_status: Dict[str, Any], 
                           consumption_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Thermal management optimization"""
        
        suggestions = []
        
        # Simulate thermal analysis
        if consumption_analysis.get("average_power_w", 0) > 800:
            suggestions.append({
                "strategy": "thermal_management",
                "description": "Optimize thermal management to reduce cooling energy",
                "parameters": {
                    "fan_speed_reduction": "20%",
                    "thermal_throttling_threshold": "75°C"
                },
                "energy_savings_kj": 6.8,
                "carbon_savings_gco2": 2.3,
                "implementation_complexity": "medium"
            })
        
        return suggestions

class EnergyAsPolicyManager:
    """Main Energy-as-Policy manager"""
    
    def __init__(self):
        self.monitor = EnergyMonitor()
        self.policy_engine = EnergyPolicyEngine(self.monitor)
        self.optimizer = EnergyOptimizer(self.monitor, self.policy_engine)
        
        self.logger = logging.getLogger("EaP-Manager")
        
    def create_flight_energy_budgets(self):
        """Create default energy budgets for flight operations"""
        
        # Flight-critical partition budget
        flight_budget = EnergyBudget(
            id="FLIGHT_CRITICAL",
            name="Flight Critical Systems",
            max_energy_kj=100.0,  # 100kJ per hour
            max_carbon_gco2=33.3,  # Corresponding carbon
            time_window_seconds=3600,  # 1 hour window
            priority=1,
            accounting_method=CarbonAccountingMethod.GRID_FACTOR
        )
        
        # Non-flight partition budget
        non_flight_budget = EnergyBudget(
            id="NON_FLIGHT",
            name="Non-Flight Systems",
            max_energy_kj=50.0,   # 50kJ per hour
            max_carbon_gco2=16.7,  # Corresponding carbon
            time_window_seconds=3600,  # 1 hour window
            priority=2,
            accounting_method=CarbonAccountingMethod.GRID_FACTOR
        )
        
        self.policy_engine.create_budget(flight_budget)
        self.policy_engine.create_budget(non_flight_budget)
        
        self.logger.info("Created default flight energy budgets")
    
    def request_energy_allocation(self, budget_id: str, component: str, 
                                 estimated_energy_kj: float, operation: str) -> bool:
        """Request energy allocation for operation"""
        
        # Check policy compliance
        allowed = self.policy_engine.check_consumption_allowed(budget_id, estimated_energy_kj)
        
        if allowed:
            self.logger.debug(f"Energy allocation approved: {estimated_energy_kj:.2f}kJ for {component}")
            return True
        else:
            self.logger.warning(f"Energy allocation denied: {estimated_energy_kj:.2f}kJ for {component} - budget violation")
            return False
    
    def log_actual_consumption(self, budget_id: str, component: str, 
                              actual_energy_kj: float, duration_seconds: float, 
                              operation: str):
        """Log actual energy consumption"""
        
        # Log consumption event
        event = self.monitor.log_consumption(component, budget_id, actual_energy_kj, duration_seconds, operation)
        
        # Update budget tracking
        self.policy_engine.update_consumption(budget_id, actual_energy_kj, event.carbon_gco2)
    
    def get_system_energy_status(self) -> Dict[str, Any]:
        """Get comprehensive energy system status"""
        
        budgets_status = {}
        for budget_id in self.policy_engine.budgets:
            budgets_status[budget_id] = self.policy_engine.get_budget_status(budget_id)
        
        recent_violations = [v for v in self.policy_engine.violations 
                           if time.time() - v.timestamp < 3600]  # Last hour
        
        return {
            "budgets": budgets_status,
            "recent_violations": len(recent_violations),
            "total_consumption_events": len(self.monitor.consumption_history),
            "grid_carbon_intensity": self.monitor.grid_carbon_intensity,
            "enforcement_enabled": self.policy_engine.enforcement_enabled
        }

# Example usage
def main():
    logging.basicConfig(level=logging.INFO)
    
    eap_manager = EnergyAsPolicyManager()
    
    # Create default budgets
    eap_manager.create_flight_energy_budgets()
    
    # Simulate power meter registration
    def cpu_power_meter():
        return 120.0  # 120W
    
    def fpga_power_meter():
        return 80.0   # 80W
    
    eap_manager.monitor.register_power_meter("CPU", cpu_power_meter)
    eap_manager.monitor.register_power_meter("FPGA", fpga_power_meter)
    
    # Request energy allocation
    allowed = eap_manager.request_energy_allocation("FLIGHT_CRITICAL", "flight_control", 5.0, "aileron_control")
    print(f"Energy allocation allowed: {allowed}")
    
    if allowed:
        # Log actual consumption
        eap_manager.log_actual_consumption("FLIGHT_CRITICAL", "flight_control", 4.8, 0.01, "aileron_control")
    
    # Get optimizations
    optimizations = eap_manager.optimizer.suggest_optimizations("FLIGHT_CRITICAL")
    print(f"Optimization suggestions: {len(optimizations)}")
    
    # Get system status
    status = eap_manager.get_system_energy_status()
    print(f"System energy status: {json.dumps(status, indent=2, default=str)}")

if __name__ == "__main__":
    main()