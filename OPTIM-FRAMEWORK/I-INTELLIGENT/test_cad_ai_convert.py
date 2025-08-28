#!/usr/bin/env python3
"""
Test suite for CAD-AI Convert integration with AMPEL360 BWB Q
Validates the complete workflow from AI conceptualization to parametric model generation
"""

import unittest
import json
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cad_ai_convert import (
    CADAIConvert, ConstraintLayer, ParametricVolume, AircraftConcept,
    MultiModalConceptualizer, QuantumParametricGenerator, DesignPhase
)


class TestCADAIConvert(unittest.TestCase):
    """Test suite for CAD-AI Convert core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.converter = CADAIConvert()
        self.conceptualizer = MultiModalConceptualizer()
        self.parametric_generator = QuantumParametricGenerator()
        
        # Test constraint layer
        self.test_constraints = ConstraintLayer(
            propulsion_system="H2_FuelCell_Hybrid_Electric",
            energy_storage="Cryo_H2_Tanks + Li-S_Battery_Buffer",
            structural_paradigm="Quantum_Optimized_Lattice",
            material_base="Carbon-Metamaterial_Composite",
            flight_envelope={"max_mach": 0.95, "service_ceiling": 41000},
            target_laminar_flow=0.85
        )
    
    def test_constraint_layer_creation(self):
        """Test ConstraintLayer creation and serialization"""
        constraints_dict = self.test_constraints.to_dict()
        
        self.assertEqual(constraints_dict['propulsion_system'], "H2_FuelCell_Hybrid_Electric")
        self.assertEqual(constraints_dict['target_laminar_flow'], 0.85)
        self.assertIn('max_mach', constraints_dict['flight_envelope'])
    
    def test_parametric_volume_scaling(self):
        """Test ParametricVolume scaling functionality"""
        volume = ParametricVolume(
            name="test_h2_tank",
            volume_type="h2_tank",
            base_volume=25.0,
            position=(10.0, 0.0, 2.0),
            scaling_factors={"capacity": 1.0, "safety": 1.2},
            constraints=["cryogenic_temperature", "pressure_rating"]
        )
        
        scaled_volume = volume.scale_volume(1.1)
        self.assertAlmostEqual(scaled_volume, 25.0 * 1.1, places=6)
    
    def test_multi_modal_prompt_generation(self):
        """Test AI prompt generation with technical constraints"""
        prompt = self.conceptualizer.generate_prompt("blueprint_schematic", self.test_constraints)
        
        self.assertIn("hydrogen fuel cell integration", prompt)
        self.assertIn("quantum-optimized lattice structure", prompt)
        self.assertIn("high laminar flow surface design", prompt)
    
    def test_aircraft_concept_creation(self):
        """Test AircraftConcept creation with team member assignment"""
        concept = self.conceptualizer.create_concept(
            "quantum_structure", self.test_constraints, "Dr. Thorne"
        )
        
        self.assertTrue(concept.concept_id.startswith("AMPEL360_quantum_structure"))
        self.assertEqual(concept.team_member, "Dr. Thorne")
        self.assertEqual(concept.ai_generator, "DALLE-3")
        self.assertIn("quantum-optimized isogrid structure", concept.description)
    
    def test_quantum_lattice_generation(self):
        """Test quantum-optimized structural lattice generation"""
        volumes = [
            ParametricVolume(
                name="h2_tank_test",
                volume_type="h2_tank",
                base_volume=25.0,
                position=(10.0, 0.0, 2.0),
                scaling_factors={"capacity": 1.0},
                constraints=["cryogenic_temperature"]
            )
        ]
        
        lattice_config = self.parametric_generator.generate_structural_lattice(
            self.test_constraints, volumes
        )
        
        self.assertEqual(lattice_config['lattice_type'], "quantum_optimized_isogrid")
        self.assertIn('zone_h2_tank_test', lattice_config['density_gradient'])
        self.assertEqual(lattice_config['density_gradient']['zone_h2_tank_test'], 1.8)
        self.assertIn('primary', lattice_config['beam_thickness'])
    
    def test_beam_thickness_optimization(self):
        """Test material-based beam thickness optimization"""
        beam_thickness = self.parametric_generator._optimize_beam_thickness(self.test_constraints)
        
        # Should use carbon-metamaterial settings
        self.assertEqual(beam_thickness['primary'], 3.2)
        self.assertEqual(beam_thickness['secondary'], 2.1)
        self.assertEqual(beam_thickness['tertiary'], 1.4)
    
    def test_phase1_conceptualization(self):
        """Test Phase 1: Multi-Modal AI Conceptualization"""
        team_constraints = {
            "Chloe": self.test_constraints,
            "Dr. Thorne": ConstraintLayer(
                propulsion_system="H2_FuelCell_Hybrid_Electric",
                energy_storage="Cryo_H2_Tanks + Li-S_Battery_Buffer",
                structural_paradigm="Integration_Optimized",
                material_base="Thermal_Conductive_Composite",
                flight_envelope={"max_mach": 0.95, "cruise_altitude": 35000},
                target_laminar_flow=0.80
            )
        }
        
        concepts = self.converter.phase1_conceptualization(team_constraints)
        
        # Should generate 6 concepts (3 types × 2 team members)
        self.assertEqual(len(concepts), 6)
        self.assertEqual(self.converter.current_phase, DesignPhase.CONVERSION)
        
        # Check concept distribution
        chloe_concepts = [c for c in concepts if c.team_member == "Chloe"]
        thorne_concepts = [c for c in concepts if c.team_member == "Dr. Thorne"]
        self.assertEqual(len(chloe_concepts), 3)
        self.assertEqual(len(thorne_concepts), 3)
    
    def test_phase2_conversion(self):
        """Test Phase 2: Quantum Conversion Bridge"""
        # Create a test concept
        concept = AircraftConcept(
            concept_id="TEST_CONCEPT_001",
            image_path="test/concept.png",
            description="Test BWB concept",
            technical_constraints="{}",
            ai_generator="TEST",
            creation_timestamp="2025-01-01 00:00:00",
            team_member="TestUser"
        )
        
        constraint_layers = {
            "physics": self.test_constraints.to_dict(),
            "integration": {"manufacturing_complexity": 1.3}
        }
        
        parametric_model = self.converter.phase2_conversion(concept, constraint_layers)
        
        self.assertEqual(parametric_model['concept_id'], "TEST_CONCEPT_001")
        self.assertIn('surface_model', parametric_model)
        self.assertIn('structural_lattice', parametric_model)
        self.assertIn('parametric_volumes', parametric_model)
        self.assertTrue(parametric_model['optimization_metadata']['convergence_achieved'])
    
    def test_phase3_collaboration(self):
        """Test Phase 3: Collaborative Engineering"""
        test_model = {
            "concept_id": "TEST_001",
            "surface_model": {"wing_span": 52.0},
            "structural_lattice": {"lattice_type": "quantum_optimized_isogrid"},
            "parametric_volumes": []
        }
        
        collaborative_model = self.converter.phase3_collaboration(test_model)
        
        self.assertIn('collaboration_log', collaborative_model)
        self.assertIn('real_time_updates', collaborative_model)
        
        # Check that all three engineers contributed
        log = collaborative_model['collaboration_log']
        engineers = [entry['engineer'] for entry in log]
        self.assertIn('Dr. Rostova', engineers)
        self.assertIn('Dr. Thorne', engineers)
        self.assertIn('Ben', engineers)
    
    def test_phase4_problem_solving(self):
        """Test Phase 4: Multi-Domain Problem Solving"""
        test_model = {
            "concept_id": "TEST_001",
            "collaboration_log": [{"engineer": "Dr. Thorne", "action": "test"}]
        }
        
        final_model = self.converter.phase4_problem_solving(test_model)
        
        self.assertIn('problem_solving', final_model)
        self.assertEqual(final_model['design_status'], "quantum_optimized_baseline")
        
        problem_solving = final_model['problem_solving']
        self.assertIn('thermal output 7% higher', problem_solving['problem']['issue'])
        self.assertEqual(problem_solving['resolution_time'], "0.8 hours")
        self.assertEqual(problem_solving['net_impact'], "Positive - crisis turned into efficiency gain")
    
    def test_complete_workflow_execution(self):
        """Test complete CAD-AI Convert workflow"""
        # This test simulates the complete workflow without external dependencies
        self.converter.load_existing_config("ampel360_config.json")
        
        # The workflow should complete without errors
        try:
            result = self.converter.run_complete_workflow()
            self.assertIsNotNone(result)
            self.assertEqual(result.get('design_status'), 'quantum_optimized_baseline')
            self.assertIn('collaboration_log', result)
            self.assertIn('problem_solving', result)
        except Exception as e:
            self.fail(f"Complete workflow failed: {e}")
    
    def test_session_save_and_load(self):
        """Test session save functionality"""
        # Create a simple test session
        self.converter.design_session = {
            "test_data": "value",
            "phase": DesignPhase.CONCEPTUALIZATION
        }
        
        test_filepath = "/tmp/test_session.json"
        self.converter.save_session(test_filepath)
        
        # Verify file was created and contains expected data
        self.assertTrue(Path(test_filepath).exists())
        
        with open(test_filepath, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['test_data'], "value")
        
        # Clean up
        Path(test_filepath).unlink()


class TestQAOAIntegration(unittest.TestCase):
    """Test QAOA integration with CAD-AI Convert"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Import here to avoid import errors if QAOA module is not available
        try:
            from scripts.qaoa_over_F import QAOASelector
            self.qaoa_available = True
        except ImportError:
            self.qaoa_available = False
    
    def test_qaoa_cad_ai_integration_available(self):
        """Test that QAOA-CAD-AI integration is available"""
        if not self.qaoa_available:
            self.skipTest("QAOA module not available")
        
        # Test that integration is properly detected
        from scripts.qaoa_over_F import CAD_AI_AVAILABLE
        self.assertTrue(CAD_AI_AVAILABLE, "CAD-AI Convert should be available for QAOA integration")
    
    def test_constraint_conversion(self):
        """Test conversion from QAOA config to CAD-AI constraints"""
        if not self.qaoa_available:
            self.skipTest("QAOA module not available")
        
        from scripts.qaoa_over_F import QAOASelector
        
        # Create test QAOA selector (will fail gracefully if files don't exist)
        try:
            selector = QAOASelector("../../constraints/hard_constraints.yaml", "data/candidates.yaml")
            
            test_config = {
                "id": "TEST_BWB_H2", 
                "config": {"propulsion": 37, "energy": 38, "wing": 34},
                "manufacturing_complexity": 1.3,
                "certification_risk": 1.4,
                "infrastructure_need": 1.5
            }
            
            constraints = selector._convert_config_to_constraints(test_config)
            
            self.assertIn("physics", constraints)
            self.assertIn("integration", constraints)
            self.assertEqual(constraints["physics"]["propulsion_system"], "H2_FuelCell_Hybrid_Electric")
            self.assertEqual(constraints["physics"]["target_laminar_flow"], 0.85)  # Advanced wing
            
        except FileNotFoundError:
            self.skipTest("QAOA configuration files not available")


def run_validation_tests():
    """Run all validation tests for CAD-AI Convert"""
    print("🧪 Running CAD-AI Convert Validation Tests")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add CAD-AI Convert tests
    suite.addTest(unittest.makeSuite(TestCADAIConvert))
    suite.addTest(unittest.makeSuite(TestQAOAIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed! CAD-AI Convert is ready for use.")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        print("   Please review and fix issues before proceeding.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_validation_tests()
    sys.exit(0 if success else 1)