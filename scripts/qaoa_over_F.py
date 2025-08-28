#!/usr/bin/env python3
"""
QAOA Selector over Feasible Set F for AMPEL360 H₂-BWB-Q
CVaR Risk-Aware Optimization with Quantum Approximate Optimization Algorithm

Implementation of the ecosystem cost optimization:
QNNN = argmin_N E[H_s(N)] + β·CVaR_α(H_s(N))

This is a stub implementation that can be replaced with full QAOA one-hot encoding.
Enhanced with CAD-AI Convert integration for parametric design optimization.
"""

import json
import yaml
import numpy as np
from typing import Dict, List, Tuple, Optional
import argparse
from pathlib import Path
import sys
import os

# Add current directory to path for CAD-AI Convert import
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from app.CQEA_Classical_Quantum_Extensible_Applications.CAD_AI_CONVERT import CADAIConvert, ConstraintLayer
    CAD_AI_AVAILABLE = True
except ImportError:
    CAD_AI_AVAILABLE = False
    print("Warning: CAD-AI Convert not available. Running in legacy mode.")


class CVaROptimizer:
    """Conditional Value at Risk optimizer for aircraft configuration selection"""
    
    def __init__(self, alpha: float = 0.8, beta: float = 0.25):
        self.alpha = alpha  # CVaR confidence level
        self.beta = beta    # Risk preference parameter
        
    def calculate_cvar(self, cost_scenarios: np.ndarray) -> float:
        """Calculate CVaR_α for given cost scenarios"""
        sorted_costs = np.sort(cost_scenarios)
        var_index = int(np.ceil(len(sorted_costs) * self.alpha))
        cvar = np.mean(sorted_costs[var_index:])
        return cvar
    
    def ecosystem_cost(self, config: Dict, scenario: Dict) -> float:
        """Calculate ecosystem cost H_s(N) for a configuration in a scenario"""
        # Cost components: RD + MFG_INV + CERT_TIME·CAPITAL + INFRA + TRAIN + MAINT·FLEET·LIFE + FUEL·BLOCK_HRS·PRICE
        
        # Simplified cost model (would be replaced with detailed engineering models)
        rd_cost = config.get('complexity_factor', 1.0) * scenario.get('rd_multiplier', 1.0) * 1e6
        mfg_cost = config.get('manufacturing_complexity', 1.0) * scenario.get('mfg_multiplier', 1.0) * 2e6
        cert_cost = config.get('certification_risk', 1.0) * scenario.get('cert_multiplier', 1.0) * 0.5e6
        infra_cost = config.get('infrastructure_need', 1.0) * scenario.get('infra_multiplier', 1.0) * 3e6
        train_cost = config.get('training_complexity', 1.0) * 0.2e6
        
        # Operational costs
        fleet_size = scenario.get('fleet_size', 50)
        lifetime_years = scenario.get('lifetime', 25)
        maint_cost = config.get('maintenance_factor', 1.0) * fleet_size * lifetime_years * 0.1e6
        
        block_hours = scenario.get('annual_block_hours', 3000) * fleet_size * lifetime_years
        fuel_price = scenario.get('h2_price_per_kg', 5.0)  # $/kg H₂
        fuel_consumption = config.get('h2_consumption_kg_per_hour', 150)
        fuel_cost = fuel_consumption * block_hours * fuel_price
        
        total_cost = rd_cost + mfg_cost + cert_cost + infra_cost + train_cost + maint_cost + fuel_cost
        return total_cost


class QAOASelector:
    """QAOA-based selector for optimal aircraft configuration"""
    
    def __init__(self, constraints_path: str, candidates_path: str):
        self.constraints = self._load_constraints(constraints_path)
        self.candidates = self._load_candidates(candidates_path)
        self.cvar_optimizer = CVaROptimizer()
        # Initialize CAD-AI Convert integration
        self.cad_ai_converter = None
        if CAD_AI_AVAILABLE:
            self.cad_ai_converter = CADAIConvert()
            print("✅ CAD-AI Convert integration enabled")
        
    def _load_constraints(self, path: str) -> Dict:
        """Load hard constraints from YAML file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_candidates(self, path: str) -> Dict:
        """Load candidate configurations from YAML file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def check_trl_gates(self, config: Dict) -> bool:
        """Check if configuration meets TRL gate requirements"""
        trl_gates = self.constraints['trl_gates']
        
        for subsystem, min_trl in trl_gates.items():
            if subsystem in config:
                candidate_id = config[subsystem]
                # Find candidate and check TRL
                for candidate in self.candidates['candidates']:
                    if candidate['id'] == candidate_id and subsystem in candidate['subsystems']:
                        if candidate['subsystems'][subsystem]['trl'] < min_trl:
                            return False
        return True
    
    def check_compatibility(self, config: Dict) -> bool:
        """Check structural compatibility and forbidden pairs"""
        # Check allowed pairs
        allowed_pairs = self.constraints['allowed_pairs']
        
        if 'wing' in config and 'fuselage' in config:
            wing_id, fuselage_id = config['wing'], config['fuselage']
            if [wing_id, fuselage_id] not in allowed_pairs['wing_fuselage']:
                return False
                
        if 'energy' in config and 'fuselage' in config:
            energy_id, fuselage_id = config['energy'], config['fuselage']
            if [energy_id, fuselage_id] not in allowed_pairs['energy_fuselage']:
                return False
        
        # Check forbidden pairs
        forbidden_pairs = self.constraints['forbidden_pairs']
        for subsystem_a, subsystem_b in [('wing', 'fuselage'), ('wing', 'energy')]:
            if subsystem_a in config and subsystem_b in config:
                pair = [config[subsystem_a], config[subsystem_b]]
                if pair in forbidden_pairs:
                    return False
        
        return True
    
    def check_hydrogen_policy(self, config: Dict) -> bool:
        """Check hydrogen policy compliance"""
        # Both propulsion and energy must use hydrogen
        prop_id = config.get('propulsion')
        energy_id = config.get('energy')
        
        if prop_id and energy_id:
            # Check if both use hydrogen (simplified check)
            return prop_id == 37 and energy_id == 38  # H₂ turbofan and H₂ storage
        
        return True
    
    def generate_feasible_set(self) -> List[Dict]:
        """Generate feasible configuration set F"""
        feasible_configs = []
        
        # Reference configuration from README
        reference_config = {
            'fuselage': 24,
            'wing': 24,
            'primary_structure': 24,
            'flight_controls': 24,
            'propulsion': 37,
            'energy': 38,
            'avionics': 1,
            'landing_gear': 1,
            'cabin': 1
        }
        
        # Add reference configuration if feasible
        if (self.check_trl_gates(reference_config) and 
            self.check_compatibility(reference_config) and
            self.check_hydrogen_policy(reference_config)):
            feasible_configs.append({
                'id': 'REF_BWB_H2',
                'config': reference_config,
                'complexity_factor': 1.2,  # BWB complexity
                'manufacturing_complexity': 1.3,
                'certification_risk': 1.4,  # New configuration
                'infrastructure_need': 1.5,  # H₂ infrastructure
                'training_complexity': 1.1,
                'maintenance_factor': 0.9,   # BWB efficiency
                'h2_consumption_kg_per_hour': 145
            })
        
        # Generate alternative configurations (simplified for demonstration)
        # Alternative with advanced wing (34)
        alt_config = reference_config.copy()
        alt_config['wing'] = 34
        
        if (self.check_trl_gates(alt_config) and 
            self.check_compatibility(alt_config) and
            self.check_hydrogen_policy(alt_config)):
            feasible_configs.append({
                'id': 'ADV_WING_BWB_H2',
                'config': alt_config,
                'complexity_factor': 1.4,  # Advanced wing complexity
                'manufacturing_complexity': 1.5,
                'certification_risk': 1.6,
                'infrastructure_need': 1.5,
                'training_complexity': 1.2,
                'maintenance_factor': 0.85,  # Better efficiency
                'h2_consumption_kg_per_hour': 138
            })
        
        return feasible_configs
    
    def optimize_qnnn(self, passenger_range: Tuple[int, int] = (150, 220)) -> Dict:
        """Optimize QNNN passenger capacity using CVaR"""
        feasible_configs = self.generate_feasible_set()
        passenger_bins = self.candidates['passenger_binning']['bins']
        
        best_qnnn = None
        best_objective = float('inf')
        best_config = None
        
        # Generate scenarios for Monte Carlo evaluation
        scenarios = self._generate_scenarios()
        
        for pax_bin in passenger_bins:
            if passenger_range[0] <= pax_bin['capacity'] <= passenger_range[1]:
                for config_data in feasible_configs:
                    # Calculate costs across scenarios
                    costs = []
                    for scenario in scenarios:
                        cost = self.cvar_optimizer.ecosystem_cost(config_data, scenario)
                        costs.append(cost)
                    
                    costs = np.array(costs)
                    expected_cost = np.mean(costs)
                    cvar_cost = self.cvar_optimizer.calculate_cvar(costs)
                    
                    # Objective: E[cost] + β·CVaR_α(cost)
                    objective = expected_cost + self.cvar_optimizer.beta * cvar_cost
                    
                    if objective < best_objective:
                        best_objective = objective
                        best_qnnn = pax_bin['capacity']
                        best_config = config_data
        
        return {
            'QNNN': best_qnnn,
            'objective_value': best_objective,
            'selected_config': best_config,
            'feasible_set_size': len(feasible_configs)
        }
    
    def _generate_scenarios(self, n_scenarios: int = 100) -> List[Dict]:
        """Generate Monte Carlo scenarios for cost evaluation"""
        np.random.seed(42)  # For reproducible results
        
        scenarios = []
        for _ in range(n_scenarios):
            scenario = {
                'rd_multiplier': np.random.uniform(0.8, 1.3),
                'mfg_multiplier': np.random.uniform(0.9, 1.2),
                'cert_multiplier': np.random.uniform(0.7, 1.5),
                'infra_multiplier': np.random.uniform(0.8, 1.4),
                'fleet_size': int(np.random.uniform(30, 80)),
                'lifetime': int(np.random.uniform(20, 30)),
                'annual_block_hours': int(np.random.uniform(2500, 3500)),
                'h2_price_per_kg': np.random.uniform(3.0, 8.0)
            }
            scenarios.append(scenario)
        
        return scenarios
    
    def run_cad_ai_workflow(self, selected_config: Dict) -> Optional[Dict]:
        """Run CAD-AI Convert workflow with selected configuration"""
        if not self.cad_ai_converter:
            print("❌ CAD-AI Convert not available")
            return None
        
        print("\n🎨 Initializing CAD-AI Convert workflow for selected configuration")
        
        # Convert QAOA config to CAD-AI constraints
        constraint_layers = self._convert_config_to_constraints(selected_config)
        
        # Run CAD-AI workflow
        try:
            result = self.cad_ai_converter.run_complete_workflow()
            
            # Integrate results back into QAOA optimization
            integration_data = {
                "qaoa_config": selected_config,
                "cad_ai_result": result,
                "parametric_model": result.get('parametric_model'),
                "collaboration_metrics": {
                    "design_iterations": len(result.get('collaboration_log', [])),
                    "problem_resolution_time": result.get('problem_solving', {}).get('resolution_time'),
                    "optimization_status": result.get('design_status')
                }
            }
            
            return integration_data
            
        except Exception as e:
            print(f"❌ CAD-AI workflow failed: {e}")
            return None
    
    def _convert_config_to_constraints(self, config: Dict) -> Dict:
        """Convert QAOA configuration to CAD-AI constraint layers"""
        # Map QAOA donor IDs to CAD-AI constraint specifications
        propulsion_systems = {
            37: "H2_FuelCell_Hybrid_Electric",
            38: "Battery_Electric_Enhanced",
            39: "Hybrid_Turbofan_Electric"
        }
        
        energy_storage = {
            37: "Cryo_H2_Tanks + Li-S_Battery_Buffer",
            38: "Li-Ion_Battery_Primary",
            39: "Hybrid_Battery_Fuel"
        }
        
        wing_types = {
            24: "Conventional_BWB_Optimized",
            34: "Advanced_BWB_Morphing",
            44: "Ultra_Efficient_Laminar"
        }
        
        # Create constraint layers based on configuration
        propulsion_id = config['config'].get('propulsion', 37)
        energy_id = config['config'].get('energy', 38)
        wing_id = config['config'].get('wing', 24)
        
        constraints = {
            "physics": {
                "propulsion_system": propulsion_systems.get(propulsion_id, "H2_FuelCell_Hybrid_Electric"),
                "energy_storage": energy_storage.get(energy_id, "Cryo_H2_Tanks + Li-S_Battery_Buffer"),
                "structural_paradigm": "Quantum_Optimized_Lattice",
                "material_base": "Carbon-Metamaterial_Composite",
                "flight_envelope": {"max_mach": 0.95, "service_ceiling": 41000},
                "target_laminar_flow": 0.85 if wing_id >= 34 else 0.80
            },
            "integration": {
                "manufacturing_complexity": config.get('manufacturing_complexity', 1.3),
                "certification_risk": config.get('certification_risk', 1.4),
                "infrastructure_need": config.get('infrastructure_need', 1.5),
                "passenger_capacity": config.get('id', 'UNKNOWN').split('_')[-1] if 'passengers' in str(config.get('id', '')) else 150
            }
        }
        
        return constraints
    
    def optimize_with_cad_ai(self) -> Dict:
        """Enhanced optimization with CAD-AI Convert integration"""
        print("🚀 Running Enhanced QAOA + CAD-AI Optimization")
        
        # Run standard QAOA optimization first
        qaoa_result = self.optimize_qnnn()
        
        # Run CAD-AI workflow with optimal configuration
        if self.cad_ai_converter:
            cad_ai_result = self.run_cad_ai_workflow(qaoa_result['selected_config'])
            
            if cad_ai_result:
                # Enhanced result with CAD-AI integration
                enhanced_result = qaoa_result.copy()
                enhanced_result['cad_ai_integration'] = cad_ai_result
                enhanced_result['workflow_status'] = 'integrated'
                
                # Safely extract design artifacts
                parametric_model = cad_ai_result.get('cad_ai_result', {}) if cad_ai_result else {}
                enhanced_result['design_artifacts'] = {
                    "parametric_model": "cad_ai_session.json",
                    "quantum_lattice": parametric_model.get('structural_lattice', {}),
                    "collaboration_log": parametric_model.get('collaboration_log', [])
                }
                
                print("✅ Enhanced optimization with CAD-AI integration complete")
                return enhanced_result
            else:
                print("⚠️  CAD-AI integration failed, returning QAOA-only result")
                qaoa_result['workflow_status'] = 'qaoa_only'
                return qaoa_result
        else:
            print("ℹ️  CAD-AI not available, using QAOA-only optimization")
            qaoa_result['workflow_status'] = 'qaoa_only'
            return qaoa_result


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='QAOA Selector for AMPEL360 H₂-BWB-Q')
    parser.add_argument('--constraints', default='constraints/hard_constraints.yaml',
                       help='Path to hard constraints file')
    parser.add_argument('--candidates', default='data/candidates.yaml',
                       help='Path to candidates file')
    parser.add_argument('--output', default='feasible_set.json',
                       help='Output file for feasible set')
    parser.add_argument('--optimize', action='store_true',
                       help='Run QNNN optimization')
    parser.add_argument('--enhanced', action='store_true',
                       help='Run enhanced optimization with CAD-AI Convert')
    parser.add_argument('--cad-ai-only', action='store_true',
                       help='Run CAD-AI Convert workflow only')
    
    args = parser.parse_args()
    
    # Initialize selector
    selector = QAOASelector(args.constraints, args.candidates)
    
    if args.cad_ai_only:
        # Run CAD-AI workflow only
        if CAD_AI_AVAILABLE:
            converter = CADAIConvert()
            result = converter.run_complete_workflow()
            print("✅ CAD-AI Convert workflow completed independently")
        else:
            print("❌ CAD-AI Convert not available")
        return
    
    # Generate feasible set
    feasible_set = selector.generate_feasible_set()
    
    # Save feasible set
    with open(args.output, 'w') as f:
        json.dump(feasible_set, f, indent=2)
    
    print(f"Generated feasible set with {len(feasible_set)} configurations")
    print(f"Saved to {args.output}")
    
    if args.enhanced:
        # Run enhanced optimization with CAD-AI integration
        result = selector.optimize_with_cad_ai()
        
        print("\n=== Enhanced QAOA + CAD-AI Optimization Results ===")
        print(f"Optimal QNNN: {result['QNNN']} passengers")
        print(f"Objective value: ${result['objective_value']:,.0f}")
        print(f"Selected configuration: {result['selected_config']['id']}")
        print(f"Workflow status: {result.get('workflow_status', 'standard')}")
        
        if 'cad_ai_integration' in result:
            cad_metrics = result['cad_ai_integration']['collaboration_metrics']
            print(f"Design iterations: {cad_metrics['design_iterations']}")
            print(f"Problem resolution: {cad_metrics['problem_resolution_time']}")
            print(f"Design status: {cad_metrics['optimization_status']}")
        
        # Save enhanced result
        result_file = 'enhanced_optimization_result.json'
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Enhanced result saved to {result_file}")
        
    elif args.optimize:
        # Run standard QNNN optimization
        result = selector.optimize_qnnn()
        
        print("\n=== QNNN Optimization Results ===")
        print(f"Optimal QNNN: {result['QNNN']} passengers")
        print(f"Objective value: ${result['objective_value']:,.0f}")
        print(f"Selected configuration: {result['selected_config']['id']}")
        print(f"Architecture: {result['selected_config']['config']}")
        
        # Save optimization result
        result_file = 'qnnn_optimization_result.json'
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"Optimization result saved to {result_file}")


if __name__ == "__main__":
    main()