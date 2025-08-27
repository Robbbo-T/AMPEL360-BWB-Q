#!/usr/bin/env python3
"""
AMPEL360 H₂-BWB-Q Decision Flow Model
Digital Twin component for organizational decision modeling

Features:
- Real-time decision tracking
- Decision pattern analysis
- Bottleneck identification
- Optimization recommendations
"""

import networkx as nx
import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class DecisionNode:
    id: str
    name: str
    authority_level: str
    decision_time_limit: int  # hours
    current_load: int
    max_capacity: int

@dataclass
class DecisionFlow:
    id: str
    source: str
    target: str
    decision_type: str
    priority: str
    estimated_duration: int
    
class OrganizationalDecisionModel:
    def __init__(self):
        self.decision_graph = nx.DiGraph()
        self.active_decisions = {}
        self.decision_history = []
        self.setup_decision_network()
        
    def setup_decision_network(self):
        """Initialize the organizational decision network"""
        # Executive level
        self.add_decision_node("PB", "Program Board", "Executive", 72, 0, 5)
        
        # Senior management
        self.add_decision_node("CA", "Chief Architect", "Senior", 48, 0, 8)
        self.add_decision_node("CSE", "CSE Office", "Senior", 24, 0, 10)
        
        # Operational
        self.add_decision_node("H2L", "H2 Lead", "Operational", 24, 0, 6)
        self.add_decision_node("CL", "Cert Lead", "Operational", 48, 0, 4)
        
        # Create decision flows
        self.add_decision_flow("H2L", "CSE", "technical", 24)
        self.add_decision_flow("CSE", "CA", "architecture", 48)
        self.add_decision_flow("CA", "PB", "strategic", 72)
        
    def add_decision_node(self, id: str, name: str, level: str, 
                         time_limit: int, load: int, capacity: int):
        """Add a decision node to the network"""
        node = DecisionNode(id, name, level, time_limit, load, capacity)
        self.decision_graph.add_node(id, node=node)
        
    def add_decision_flow(self, source: str, target: str, 
                         decision_type: str, duration: int):
        """Add a decision flow between nodes"""
        self.decision_graph.add_edge(source, target, 
                                   type=decision_type, duration=duration)
        
    def route_decision(self, decision_id: str, decision_type: str, 
                      priority: str, origin: str) -> List[str]:
        """Route a decision through the organizational network"""
        if decision_type == "operational":
            return [origin]
        elif decision_type == "technical":
            return [origin, "CSE", "CA"]
        elif decision_type == "strategic":
            return [origin, "CSE", "CA", "PB"]
        else:
            return [origin, "CSE"]
            
    def simulate_decision_flow(self, decision_id: str, 
                             decision_type: str, priority: str):
        """Simulate decision flow through organization"""
        route = self.route_decision(decision_id, decision_type, priority, "H2L")
        
        total_time = 0
        bottlenecks = []
        
        for node_id in route:
            node = self.decision_graph.nodes[node_id]['node']
            
            # Check capacity
            if node.current_load >= node.max_capacity:
                bottlenecks.append(node_id)
                
            # Add decision time
            if priority == "High":
                time_factor = 0.5
            elif priority == "Low":
                time_factor = 1.5
            else:
                time_factor = 1.0
                
            total_time += node.decision_time_limit * time_factor
            
        return {
            'route': route,
            'estimated_time': total_time,
            'bottlenecks': bottlenecks,
            # Average time spent per node in the route; lower is more efficient.
            'average_time_per_node': total_time / len(route) if len(route) > 0 else 0
        }
        
    def analyze_organizational_performance(self) -> Dict:
        """Analyze overall organizational decision performance"""
        # Calculate network metrics
        centrality = nx.betweenness_centrality(self.decision_graph)
        
        # Identify bottlenecks
        bottleneck_nodes = [node for node, score in centrality.items() 
                          if score > 0.3]
                          
        # Performance metrics
        if len(self.decision_graph.nodes) > 0:
            avg_decision_time = sum(node['node'].decision_time_limit 
                                  for node in self.decision_graph.nodes.values()) / len(self.decision_graph.nodes)
        else:
            avg_decision_time = 0
                              
        return {
            'network_efficiency': nx.efficiency(self.decision_graph),
            'average_decision_time': avg_decision_time,
            'bottleneck_nodes': bottleneck_nodes,
            'centrality_scores': centrality,
            'optimization_recommendations': self.generate_optimization_recommendations(bottleneck_nodes)
        }
        
    def generate_optimization_recommendations(self, bottlenecks: List[str]) -> List[str]:
        """Generate recommendations for organizational optimization"""
        recommendations = []
        
        if "CSE" in bottlenecks:
            recommendations.append("Consider adding deputy CSE for decision load balancing")
            
        if "CA" in bottlenecks:
            recommendations.append("Implement architectural decision delegation framework")
            
        if len(bottlenecks) > 2:
            recommendations.append("Review overall decision authority distribution")
            
        return recommendations

# Example usage
if __name__ == "__main__":
    model = OrganizationalDecisionModel()
    
    # Simulate a technical decision
    result = model.simulate_decision_flow("DEC-001", "technical", "High")
    print(f"Decision flow simulation: {result}")
    
    # Analyze organizational performance
    performance = model.analyze_organizational_performance()
    print(f"Organizational performance: {performance}")