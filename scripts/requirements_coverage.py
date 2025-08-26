#!/usr/bin/env python3
"""
Requirements Coverage Analysis for AMPEL360 CI artifacts
Generate requirements coverage and traceability report
"""

import yaml
import re
from pathlib import Path
import argparse
import sys

def analyze_requirements_coverage(phase_md_path):
    """Analyze requirements coverage from phase.md."""
    
    if not phase_md_path.exists():
        print(f"❌ phase.md not found at {phase_md_path}")
        return None
        
    try:
        with open(phase_md_path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading phase.md: {e}")
        return None
    
    # Extract requirements index
    req_pattern = r'(REQ-[A-Z]{3}-\d{3}[a-z]?):\s*"([^"]+)"'
    requirements = dict(re.findall(req_pattern, content))
    
    # Extract verification matrix entries
    verification_section = re.search(r'### \d+\. Verification Matrix(.*?)(?=###|\Z)', content, re.DOTALL)
    
    coverage = {}
    verification_methods = {}
    
    if verification_section:
        matrix_content = verification_section.group(1)
        
        # Parse verification matrix table
        table_pattern = r'\|\s*(REQ-[A-Z]{3}-\d{3}[a-z]?)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        matrix_entries = re.findall(table_pattern, matrix_content)
        
        for req_id, method, medium, evidence, criterion in matrix_entries:
            req_id = req_id.strip()
            coverage[req_id] = 'Covered'
            verification_methods[req_id] = {
                'method': method.strip(),
                'medium': medium.strip(),
                'evidence': evidence.strip(),
                'criterion': criterion.strip()
            }
    
    # Check coverage
    for req_id in requirements:
        if req_id not in coverage:
            coverage[req_id] = 'NOT COVERED'
    
    return {
        'requirements': requirements,
        'coverage': coverage,
        'verification_methods': verification_methods
    }

def generate_coverage_report(ci_path):
    """Generate comprehensive requirements coverage report."""
    
    phase_md_path = Path(ci_path) / '01-Requirements' / 'phase.md'
    result = analyze_requirements_coverage(phase_md_path)
    
    if not result:
        return 1
        
    requirements = result['requirements']
    coverage = result['coverage']
    verification_methods = result['verification_methods']
    
    print("Requirements Coverage Report")
    print("="*80)
    print(f"CI: {Path(ci_path).name}")
    print(f"Total Requirements: {len(requirements)}")
    
    covered = sum(1 for s in coverage.values() if s == 'Covered')
    total = len(requirements)
    print(f"Coverage: {covered}/{total} ({covered/total*100:.1f}%)")
    print()
    
    # Detailed coverage
    print("📋 Requirements Coverage Details:")
    print("-" * 80)
    
    for req_id in sorted(requirements.keys()):
        description = requirements[req_id]
        status = coverage.get(req_id, 'UNKNOWN')
        symbol = '✅' if status == 'Covered' else '❌'
        
        print(f"{symbol} {req_id}")
        print(f"    Description: {description}")
        
        if req_id in verification_methods:
            vm = verification_methods[req_id]
            print(f"    Method: {vm['method']}")
            print(f"    Medium: {vm['medium']}")
            print(f"    Evidence: {vm['evidence']}")
            print(f"    Criterion: {vm['criterion']}")
        else:
            print("    ⚠️ No verification method defined")
        print()
    
    # Coverage by category
    print("📊 Coverage by Category:")
    print("-" * 40)
    
    categories = {
        'Structural': [req for req in requirements.keys() if req.startswith('REQ-STR-')],
        'Thermal': [req for req in requirements.keys() if req.startswith('REQ-THR-')],
        'Interface': [req for req in requirements.keys() if req.startswith('REQ-IFC-')],
        'Material': [req for req in requirements.keys() if req.startswith('REQ-MAT-')],
        'Environmental/EMC': [req for req in requirements.keys() if req.startswith('REQ-ENV-')]
    }
    
    for category, reqs in categories.items():
        if reqs:
            covered_cat = sum(1 for req in reqs if coverage.get(req) == 'Covered')
            total_cat = len(reqs)
            print(f"{category}: {covered_cat}/{total_cat} ({covered_cat/total_cat*100:.0f}%)")
    
    print()
    
    # Verification methods summary
    methods_count = {}
    for vm in verification_methods.values():
        method = vm['method']
        methods_count[method] = methods_count.get(method, 0) + 1
    
    if methods_count:
        print("🔬 Verification Methods Used:")
        print("-" * 40)
        for method, count in sorted(methods_count.items()):
            print(f"  {method}: {count} requirements")
    
    print()
    print("="*80)
    
    return 0 if covered == total else 1

def generate_traceability_matrix(ci_path, output_file=None):
    """Generate requirements traceability matrix."""
    
    phase_md_path = Path(ci_path) / '01-Requirements' / 'phase.md'
    result = analyze_requirements_coverage(phase_md_path)
    
    if not result:
        return
        
    requirements = result['requirements']
    verification_methods = result['verification_methods']
    
    lines = []
    lines.append("# Requirements Traceability Matrix")
    lines.append(f"**CI:** {Path(ci_path).name}")
    lines.append("")
    lines.append("| Requirement ID | Description | Verification Method | Evidence | Status |")
    lines.append("|---|---|---|---|---|")
    
    for req_id in sorted(requirements.keys()):
        description = requirements[req_id][:50] + "..." if len(requirements[req_id]) > 50 else requirements[req_id]
        
        if req_id in verification_methods:
            vm = verification_methods[req_id]
            method = vm['method']
            evidence = vm['evidence']
            status = "✅ Covered"
        else:
            method = "TBD"
            evidence = "TBD"
            status = "❌ Not Covered"
            
        lines.append(f"| {req_id} | {description} | {method} | {evidence} | {status} |")
    
    content = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(content)
        print(f"📊 Traceability matrix written to {output_file}")
    else:
        print(content)

def main():
    parser = argparse.ArgumentParser(description='Analyze requirements coverage')
    parser.add_argument('ci_path', help='Path to CI directory')
    parser.add_argument('--traceability', help='Generate traceability matrix to file')
    
    args = parser.parse_args()
    
    ci_path = Path(args.ci_path)
    if not ci_path.exists():
        print(f"❌ CI path does not exist: {ci_path}")
        return 1
    
    # Generate coverage report
    result = generate_coverage_report(ci_path)
    
    # Generate traceability matrix if requested
    if args.traceability:
        generate_traceability_matrix(ci_path, args.traceability)
    
    return result

if __name__ == "__main__":
    sys.exit(main())