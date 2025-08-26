#!/usr/bin/env python3
"""
AMPEL360 Artifact Validation Script
Validates CI artifacts for compliance with phase requirements
"""

import os
import sys
import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

class AMPEL360Validator:
    """Validator for AMPEL360 CI artifacts"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_phase_data(self, phase_data_path: Path) -> Dict[str, Any]:
        """Validate phase-data.yaml file"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        if not phase_data_path.exists():
            result['valid'] = False
            result['errors'].append(f"phase-data.yaml not found at {phase_data_path}")
            return result
            
        try:
            with open(phase_data_path, 'r') as f:
                data = yaml.safe_load(f)
                
            # Required fields validation
            required_fields = ['utcs_phase', 'component_id', 'status', 'date', 'doc_id', 'owner']
            for field in required_fields:
                if field not in data:
                    result['errors'].append(f"Missing required field: {field}")
                    result['valid'] = False
                    
            # Check if status is FROZEN (for v1.5)
            if data.get('status') == 'FROZEN':
                if 'v1.5' in data.get('doc_id', ''):
                    result['info'].append("Status: FROZEN - compliant with v1.5")
                else:
                    result['info'].append("Status: FROZEN - version needs verification")
            else:
                result['warnings'].append(f"Status is '{data.get('status')}' - expected 'FROZEN'")
                
            # Check links
            if 'links' in data and isinstance(data['links'], list):
                result['info'].append(f"Found {len(data['links'])} evidence links")
            else:
                result['warnings'].append("No evidence links found")
                
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Error parsing phase-data.yaml: {str(e)}")
            
        return result
        
    def validate_phase_md(self, phase_md_path: Path) -> Dict[str, Any]:
        """Validate phase.md file"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        if not phase_md_path.exists():
            result['valid'] = False
            result['errors'].append(f"phase.md not found at {phase_md_path}")
            return result
            
        try:
            with open(phase_md_path, 'r') as f:
                content = f.read()
                
            # Check for v1.5 FROZEN indicator
            if 'v1.5 FROZEN' in content:
                result['info'].append("Document marked as v1.5 FROZEN")
            elif 'v1.3 FROZEN' in content:
                result['info'].append("Document marked as v1.3 FROZEN (older version)")
            else:
                result['warnings'].append("Document not marked as FROZEN")
                
            # Check for requirements sections
            required_sections = [
                'REQUIREMENTS INDEX (MANDATORY)',
                'STANDARDS MAPPING (MANDATORY)', 
                'TECHNICAL REQUIREMENTS SECTIONS',
                'VERIFICATION MATRIX (MANDATORY)'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
                    
            if missing_sections:
                result['warnings'].append(f"Missing sections: {', '.join(missing_sections)}")
            else:
                result['info'].append("All required sections present")
                
            # Count requirements
            import re
            req_pattern = r'REQ-[A-Z]{3}-\d{3}[a-z]?'
            requirements = re.findall(req_pattern, content)
            unique_reqs = list(set(requirements))
            result['info'].append(f"Found {len(unique_reqs)} unique requirements")
            
        except Exception as e:
            result['valid'] = False
            result['errors'].append(f"Error reading phase.md: {str(e)}")
            
        return result
        
    def validate_evidence_links(self, ci_path: Path, phase_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate evidence file links"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        if 'links' not in phase_data:
            result['warnings'].append("No evidence links to validate")
            return result
            
        evidence_path = ci_path / '01-Requirements'
        missing_files = []
        existing_files = []
        
        for link in phase_data['links']:
            file_path = evidence_path / link
            if file_path.exists():
                existing_files.append(link)
                # Check if it's a placeholder (0 bytes)
                if file_path.stat().st_size == 0:
                    result['warnings'].append(f"Evidence file is placeholder: {link}")
            else:
                missing_files.append(link)
                result['errors'].append(f"Missing evidence file: {link}")
                
        if missing_files:
            result['valid'] = False
            
        result['info'].append(f"Evidence files: {len(existing_files)} existing, {len(missing_files)} missing")
        
        return result
        
    def validate_ci(self, ci_path: Path) -> Dict[str, Any]:
        """Validate complete CI"""
        result = {
            'ci_path': str(ci_path),
            'overall_valid': True,
            'phase_data': {},
            'phase_md': {},
            'evidence_links': {}
        }
        
        # Validate phase-data.yaml
        phase_data_path = ci_path / '01-Requirements' / 'phase-data.yaml'
        result['phase_data'] = self.validate_phase_data(phase_data_path)
        
        # Validate phase.md
        phase_md_path = ci_path / '01-Requirements' / 'phase.md'
        result['phase_md'] = self.validate_phase_md(phase_md_path)
        
        # Load phase data for evidence validation
        phase_data = {}
        if phase_data_path.exists():
            try:
                with open(phase_data_path, 'r') as f:
                    phase_data = yaml.safe_load(f)
            except:
                pass
                
        # Validate evidence links
        result['evidence_links'] = self.validate_evidence_links(ci_path, phase_data)
        
        # Overall validity
        result['overall_valid'] = (
            result['phase_data']['valid'] and 
            result['phase_md']['valid'] and 
            result['evidence_links']['valid']
        )
        
        return result
        
    def generate_report(self, validation_result: Dict[str, Any], output_format: str = 'text') -> str:
        """Generate validation report"""
        if output_format == 'json':
            return json.dumps(validation_result, indent=2)
            
        # Text format
        lines = []
        lines.append("="*60)
        lines.append("AMPEL360 CI Validation Report")
        lines.append("="*60)
        lines.append(f"CI Path: {validation_result['ci_path']}")
        lines.append(f"Overall Valid: {'✅ YES' if validation_result['overall_valid'] else '❌ NO'}")
        lines.append("")
        
        # Phase Data validation
        lines.append("Phase Data (phase-data.yaml):")
        pd = validation_result['phase_data']
        lines.append(f"  Valid: {'✅' if pd['valid'] else '❌'}")
        for error in pd['errors']:
            lines.append(f"  ❌ Error: {error}")
        for warning in pd['warnings']:
            lines.append(f"  ⚠️  Warning: {warning}")
        for info in pd['info']:
            lines.append(f"  ℹ️  Info: {info}")
        lines.append("")
        
        # Phase MD validation
        lines.append("Phase Documentation (phase.md):")
        pm = validation_result['phase_md']
        lines.append(f"  Valid: {'✅' if pm['valid'] else '❌'}")
        for error in pm['errors']:
            lines.append(f"  ❌ Error: {error}")
        for warning in pm['warnings']:
            lines.append(f"  ⚠️  Warning: {warning}")
        for info in pm['info']:
            lines.append(f"  ℹ️  Info: {info}")
        lines.append("")
        
        # Evidence Links validation
        lines.append("Evidence Links:")
        el = validation_result['evidence_links']
        lines.append(f"  Valid: {'✅' if el['valid'] else '❌'}")
        for error in el['errors']:
            lines.append(f"  ❌ Error: {error}")
        for warning in el['warnings']:
            lines.append(f"  ⚠️  Warning: {warning}")
        for info in el['info']:
            lines.append(f"  ℹ️  Info: {info}")
        
        lines.append("")
        lines.append("="*60)
        
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Validate AMPEL360 CI artifacts')
    parser.add_argument('--path', required=True, help='Path to CI directory')
    parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--check-links', action='store_true', help='Check evidence file links')
    
    args = parser.parse_args()
    
    ci_path = Path(args.path)
    if not ci_path.exists():
        print(f"Error: CI path does not exist: {ci_path}")
        return 1
        
    validator = AMPEL360Validator()
    result = validator.validate_ci(ci_path)
    
    report = validator.generate_report(result, args.output_format)
    print(report)
    
    return 0 if result['overall_valid'] else 1

if __name__ == "__main__":
    sys.exit(main())