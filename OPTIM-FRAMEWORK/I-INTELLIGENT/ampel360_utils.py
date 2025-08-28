#!/usr/bin/env python3
"""
AMPEL360 H₂-BWB-Q Configuration Management
Utilities for working with the aircraft configuration framework
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class AMPEL360Config:
    """Configuration manager for AMPEL360 H₂-BWB-Q framework"""
    
    def __init__(self, config_path: str = "ampel360_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load main configuration file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def get_architecture(self) -> Dict[str, Any]:
        """Get the current architecture configuration"""
        return self.config.get('architecture', {})
    
    def get_constraints_paths(self) -> Dict[str, str]:
        """Get file paths for constraints and data"""
        return self.config.get('constraints_paths', {})
    
    def get_risk_parameters(self) -> Dict[str, float]:
        """Get risk management parameters"""
        return self.config.get('risk', {})
    
    def is_bwb_config(self) -> bool:
        """Check if this is a BWB (Blended Wing Body) configuration"""
        arch = self.get_architecture()
        return (arch.get('fuselage') == 24 and 
                arch.get('wing') == 24 and
                arch.get('tail') == "N/A-BWB")
    
    def is_hydrogen_config(self) -> bool:
        """Check if this is a hydrogen propulsion configuration"""
        arch = self.get_architecture()
        return (arch.get('propulsion') == 37 and 
                arch.get('energy') == 38)
    
    def get_passenger_range(self) -> tuple:
        """Get passenger capacity range for optimization"""
        capacity = self.config.get('capacity', {})
        return tuple(capacity.get('binning_range_pax', [150, 220]))
    
    def update_qnnn(self, qnnn_value: int) -> None:
        """Update the QNNN passenger capacity value"""
        if 'capacity' not in self.config:
            self.config['capacity'] = {}
        self.config['capacity']['QNNN'] = qnnn_value
        self._save_config()
    
    def _save_config(self) -> None:
        """Save configuration back to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def validate_paths(self) -> Dict[str, bool]:
        """Validate that all required files exist"""
        paths = self.get_constraints_paths()
        validation = {}
        
        for name, path in paths.items():
            file_path = Path(path)
            validation[name] = file_path.exists()
            
        return validation
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary"""
        arch = self.get_architecture()
        validation = self.validate_paths()
        
        return {
            'utcs_version': self.config.get('utcs_mi', {}).get('version'),
            'status': self.config.get('utcs_mi', {}).get('status'),
            'configuration_type': 'BWB-H₂' if self.is_bwb_config() and self.is_hydrogen_config() else 'Other',
            'qnnn_status': 'Pending' if self.config.get('capacity', {}).get('QNNN') is None else 'Determined',
            'qnnn_value': self.config.get('capacity', {}).get('QNNN'),
            'files_validation': validation,
            'all_files_present': all(validation.values())
        }


def main():
    """Main function for standalone usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AMPEL360 Configuration Manager')
    parser.add_argument('--config', default='ampel360_config.json',
                       help='Path to configuration file')
    parser.add_argument('--status', action='store_true',
                       help='Show configuration status')
    parser.add_argument('--validate', action='store_true',
                       help='Validate file paths')
    parser.add_argument('--set-qnnn', type=int,
                       help='Set QNNN passenger capacity value')
    
    args = parser.parse_args()
    
    try:
        config_mgr = AMPEL360Config(args.config)
        
        if args.status:
            status = config_mgr.get_status_summary()
            print("=== AMPEL360 H₂-BWB-Q Configuration Status ===")
            for key, value in status.items():
                print(f"{key}: {value}")
        
        if args.validate:
            validation = config_mgr.validate_paths()
            print("\n=== File Path Validation ===")
            for name, exists in validation.items():
                status_icon = "✓" if exists else "✗"
                print(f"{status_icon} {name}: {config_mgr.get_constraints_paths()[name]}")
        
        if args.set_qnnn:
            config_mgr.update_qnnn(args.set_qnnn)
            print(f"Updated QNNN to {args.set_qnnn} passengers")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())