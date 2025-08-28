#!/usr/bin/env python3
"""
AMPEL360 H₂-BWB-Q Execution Monitor

Real-time monitoring and metrics collection for the AMPEL360 optimization pipeline.
Tracks performance, resource utilization, and execution health.

Part of the E-EXECUTING pillar of the OPTIME framework.
"""

import time
import json
import yaml
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    timestamp: str
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_io_bytes: int
    active_workflows: int
    throughput_configs_per_hour: float
    avg_latency_seconds: float
    success_rate_percent: float
    error_rate_percent: float
    queue_depth: int

@dataclass
class HealthStatus:
    """System health status"""
    timestamp: str
    overall_status: str  # healthy, degraded, critical
    component_status: Dict[str, str]
    alerts: List[str]
    uptime_hours: float

class ExecutionMonitor:
    """Real-time monitoring system for AMPEL360 execution"""
    
    def __init__(self, config_file: str = "config/monitor-config.yaml"):
        """Initialize the execution monitor"""
        self.config = self._load_config(config_file)
        self.metrics_history: List[PerformanceMetrics] = []
        self.health_history: List[HealthStatus] = []
        self.start_time = datetime.now()
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Initialize component health tracking
        self.component_health = {
            'orchestrator': 'healthy',
            'quantum_backend': 'healthy',
            'classical_solver': 'healthy',
            'storage': 'healthy',
            'network': 'healthy'
        }
        
        # Workflow tracking
        self.workflow_metrics = {
            'total_workflows': 0,
            'completed_workflows': 0,
            'failed_workflows': 0,
            'active_workflows': 0,
            'avg_completion_time': 0.0
        }
    
    def _load_config(self, config_file: str) -> Dict:
        """Load monitoring configuration"""
        try:
            config_path = Path(__file__).parent / config_file
            if config_path.exists():
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                return {
                    'monitoring': {
                        'collection_interval': 10,
                        'retention_hours': 24,
                        'alert_thresholds': {
                            'cpu_percent': 80,
                            'memory_percent': 85,
                            'disk_percent': 90,
                            'error_rate_percent': 5,
                            'latency_seconds': 300
                        }
                    }
                }
        except Exception as e:
            logger.error(f"Error loading monitor config: {e}")
            return {}
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        logger.info("📊 AMPEL360 Execution Monitor started")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        logger.info("📊 AMPEL360 Execution Monitor stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        interval = self.config.get('monitoring', {}).get('collection_interval', 10)
        
        while self.monitoring_active:
            try:
                # Collect performance metrics
                metrics = self._collect_performance_metrics()
                self.metrics_history.append(metrics)
                
                # Collect health status
                health = self._collect_health_status()
                self.health_history.append(health)
                
                # Clean old data
                self._cleanup_old_data()
                
                # Check for alerts
                self._check_alerts(metrics, health)
                
                # Save metrics to file
                self._save_metrics()
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            time.sleep(interval)
    
    def _collect_performance_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics"""
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Calculate derived metrics
        uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        throughput = self._calculate_throughput()
        latency = self._calculate_avg_latency()
        success_rate = self._calculate_success_rate()
        error_rate = self._calculate_error_rate()
        
        return PerformanceMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_usage_percent=cpu_percent,
            memory_usage_percent=memory.percent,
            disk_usage_percent=disk.percent,
            network_io_bytes=network.bytes_sent + network.bytes_recv,
            active_workflows=self.workflow_metrics['active_workflows'],
            throughput_configs_per_hour=throughput,
            avg_latency_seconds=latency,
            success_rate_percent=success_rate,
            error_rate_percent=error_rate,
            queue_depth=0  # Would be implemented with actual queue system
        )
    
    def _collect_health_status(self) -> HealthStatus:
        """Collect current health status"""
        uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        
        # Determine overall status
        component_statuses = list(self.component_health.values())
        if 'critical' in component_statuses:
            overall_status = 'critical'
        elif 'degraded' in component_statuses:
            overall_status = 'degraded'
        else:
            overall_status = 'healthy'
        
        # Generate alerts
        alerts = []
        if self.metrics_history:
            latest_metrics = self.metrics_history[-1]
            thresholds = self.config.get('monitoring', {}).get('alert_thresholds', {})
            
            if latest_metrics.cpu_usage_percent > thresholds.get('cpu_percent', 80):
                alerts.append(f"High CPU usage: {latest_metrics.cpu_usage_percent:.1f}%")
            
            if latest_metrics.memory_usage_percent > thresholds.get('memory_percent', 85):
                alerts.append(f"High memory usage: {latest_metrics.memory_usage_percent:.1f}%")
            
            if latest_metrics.error_rate_percent > thresholds.get('error_rate_percent', 5):
                alerts.append(f"High error rate: {latest_metrics.error_rate_percent:.1f}%")
        
        return HealthStatus(
            timestamp=datetime.now().isoformat(),
            overall_status=overall_status,
            component_status=self.component_health.copy(),
            alerts=alerts,
            uptime_hours=uptime_hours
        )
    
    def _calculate_throughput(self) -> float:
        """Calculate configurations processed per hour"""
        if self.workflow_metrics['completed_workflows'] == 0:
            return 0.0
        
        uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        if uptime_hours == 0:
            return 0.0
        
        return self.workflow_metrics['completed_workflows'] / uptime_hours
    
    def _calculate_avg_latency(self) -> float:
        """Calculate average workflow latency"""
        return self.workflow_metrics['avg_completion_time']
    
    def _calculate_success_rate(self) -> float:
        """Calculate workflow success rate"""
        total = self.workflow_metrics['total_workflows']
        if total == 0:
            return 100.0
        
        completed = self.workflow_metrics['completed_workflows']
        return (completed / total) * 100.0
    
    def _calculate_error_rate(self) -> float:
        """Calculate workflow error rate"""
        total = self.workflow_metrics['total_workflows']
        if total == 0:
            return 0.0
        
        failed = self.workflow_metrics['failed_workflows']
        return (failed / total) * 100.0
    
    def _cleanup_old_data(self):
        """Remove old metrics data"""
        retention_hours = self.config.get('monitoring', {}).get('retention_hours', 24)
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)
        
        # Clean metrics history
        self.metrics_history = [
            m for m in self.metrics_history 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        # Clean health history
        self.health_history = [
            h for h in self.health_history
            if datetime.fromisoformat(h.timestamp) > cutoff_time
        ]
    
    def _check_alerts(self, metrics: PerformanceMetrics, health: HealthStatus):
        """Check for alert conditions"""
        if health.alerts:
            for alert in health.alerts:
                logger.warning(f"🚨 ALERT: {alert}")
    
    def _save_metrics(self):
        """Save metrics to files"""
        try:
            # Save latest metrics
            if self.metrics_history:
                with open('monitoring/latest_metrics.json', 'w') as f:
                    json.dump(asdict(self.metrics_history[-1]), f, indent=2)
            
            if self.health_history:
                with open('monitoring/latest_health.json', 'w') as f:
                    json.dump(asdict(self.health_history[-1]), f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")
    
    def record_workflow_start(self, workflow_id: str):
        """Record workflow start"""
        self.workflow_metrics['total_workflows'] += 1
        self.workflow_metrics['active_workflows'] += 1
        logger.info(f"📊 Workflow started: {workflow_id}")
    
    def record_workflow_completion(self, workflow_id: str, duration_seconds: float):
        """Record workflow completion"""
        self.workflow_metrics['completed_workflows'] += 1
        self.workflow_metrics['active_workflows'] -= 1
        
        # Update average completion time
        total_completed = self.workflow_metrics['completed_workflows']
        current_avg = self.workflow_metrics['avg_completion_time']
        self.workflow_metrics['avg_completion_time'] = (
            (current_avg * (total_completed - 1) + duration_seconds) / total_completed
        )
        
        logger.info(f"📊 Workflow completed: {workflow_id} ({duration_seconds:.1f}s)")
    
    def record_workflow_failure(self, workflow_id: str, error: str):
        """Record workflow failure"""
        self.workflow_metrics['failed_workflows'] += 1
        self.workflow_metrics['active_workflows'] -= 1
        logger.error(f"📊 Workflow failed: {workflow_id} - {error}")
    
    def get_current_metrics(self) -> Optional[Dict]:
        """Get current performance metrics"""
        if not self.metrics_history:
            return None
        return asdict(self.metrics_history[-1])
    
    def get_current_health(self) -> Optional[Dict]:
        """Get current health status"""
        if not self.health_history:
            return None
        return asdict(self.health_history[-1])
    
    def get_metrics_summary(self, hours: int = 1) -> Dict:
        """Get metrics summary for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
        
        return {
            'period_hours': hours,
            'total_samples': len(recent_metrics),
            'avg_cpu_percent': sum(m.cpu_usage_percent for m in recent_metrics) / len(recent_metrics),
            'avg_memory_percent': sum(m.memory_usage_percent for m in recent_metrics) / len(recent_metrics),
            'avg_throughput': sum(m.throughput_configs_per_hour for m in recent_metrics) / len(recent_metrics),
            'avg_latency': sum(m.avg_latency_seconds for m in recent_metrics) / len(recent_metrics),
            'workflow_metrics': self.workflow_metrics.copy()
        }

def main():
    """Main execution for standalone monitoring"""
    print("📊 AMPEL360 H₂-BWB-Q Execution Monitor")
    print("=" * 50)
    
    monitor = ExecutionMonitor()
    monitor.start_monitoring()
    
    try:
        # Demo monitoring for 30 seconds
        time.sleep(30)
        
        # Print current status
        metrics = monitor.get_current_metrics()
        health = monitor.get_current_health()
        summary = monitor.get_metrics_summary(hours=1)
        
        print("\nCurrent Status:")
        print(f"  Overall Health: {health['overall_status'] if health else 'Unknown'}")
        print(f"  CPU Usage: {metrics['cpu_usage_percent']:.1f}%" if metrics else "  CPU Usage: Unknown")
        print(f"  Memory Usage: {metrics['memory_usage_percent']:.1f}%" if metrics else "  Memory Usage: Unknown")
        print(f"  Active Workflows: {metrics['active_workflows']}" if metrics else "  Active Workflows: Unknown")
        
        if summary:
            print(f"\nLast Hour Summary:")
            print(f"  Avg CPU: {summary['avg_cpu_percent']:.1f}%")
            print(f"  Avg Memory: {summary['avg_memory_percent']:.1f}%")
            print(f"  Total Workflows: {summary['workflow_metrics']['total_workflows']}")
        
    except KeyboardInterrupt:
        print("\n\nShutting down monitor...")
    finally:
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()