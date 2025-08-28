#!/usr/bin/env python3
"""
Test suite for configuration index validation system
"""

import unittest
import tempfile
import pathlib
import yaml
import json
from tools.validate_config_index import main as validate_main
import sys
import os

class TestConfigurationIndexValidation(unittest.TestCase):
    """Test configuration index validation functionality"""

    def setUp(self):
        """Set up test environment"""
        self.original_dir = pathlib.Path.cwd()
        
    def test_existing_configuration_validates(self):
        """Test that the existing configuration passes validation"""
        # Change to repo root for test
        os.chdir('/home/runner/work/AMPEL360-BWB-Q/AMPEL360-BWB-Q')
        
        # Capture stdout/stderr
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                result = validate_main()
            
            self.assertEqual(result, 0, f"Validation failed. stderr: {stderr_capture.getvalue()}")
            output = stdout_capture.getvalue()
            self.assertIn("Schema validation passed", output)
            self.assertIn("All validations passed", output)
            
        finally:
            os.chdir(self.original_dir)
    
    def test_configuration_has_required_fields(self):
        """Test that configuration contains all required fields"""
        config_path = pathlib.Path('/home/runner/work/AMPEL360-BWB-Q/AMPEL360-BWB-Q/OPTIM-FRAMEWORK/O-ORGANIZATIONAL/artifacts/configuration-index.yaml')
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check required top-level fields
        required_fields = ['meta', 'configurations', 'configuration_parameters', 
                          'validation_gates', 'key_decisions', 'traceability', 'audit_trail']
        
        for field in required_fields:
            self.assertIn(field, data, f"Required field '{field}' missing from configuration")
    
    def test_utcs_mi_header_format(self):
        """Test that UTCS-MI header has correct format"""
        config_path = pathlib.Path('/home/runner/work/AMPEL360-BWB-Q/AMPEL360-BWB-Q/OPTIM-FRAMEWORK/O-ORGANIZATIONAL/artifacts/configuration-index.yaml')
        
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Check UTCS-MI header exists and starts correctly
        self.assertIn('utcs_mi_header', data)
        header = data['utcs_mi_header']
        self.assertTrue(header.startswith('EstándarUniversal:'), 
                       "UTCS-MI header should start with 'EstándarUniversal:'")
        
        # Check header has expected number of fields (14 as shown in example)
        fields = header.split(':')
        self.assertGreaterEqual(len(fields), 13, 
                               f"UTCS-MI header should have at least 13 fields, found {len(fields)}")
        self.assertLessEqual(len(fields), 14, 
                            f"UTCS-MI header should have at most 14 fields, found {len(fields)}")

def run_tests():
    """Run all tests"""
    print("🧪 Running Configuration Index Validation Tests")
    print("=" * 60)
    
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConfigurationIndexValidation))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All configuration index tests passed!")
        return True
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)