#!/usr/bin/env python3
"""
Evidence Tracker for AMPEL360 CI artifacts
Track evidence document status and completeness
"""

import os
import yaml
from pathlib import Path
import argparse
import sys
from datetime import datetime

def check_evidence_status(ci_path):
    """Check evidence document status for a CI."""
    phase_data_path = Path(ci_path) / '01-Requirements' / 'phase-data.yaml'
    
    if not phase_data_path.exists():
        print(f"❌ phase-data.yaml not found at {phase_data_path}")
        return None
        
    try:
        with open(phase_data_path, 'r') as f:
            phase_data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error reading phase-data.yaml: {e}")
        return None
        
    evidence_status = []
    evidence_base_path = Path(ci_path) / '01-Requirements' / 'evidence'
    
    for link in phase_data.get('links', []):
        file_path = evidence_base_path / link
        status = {
            'file': link,
            'exists': file_path.exists(),
            'size': file_path.stat().st_size if file_path.exists() else 0,
            'is_placeholder': file_path.stat().st_size == 0 if file_path.exists() else None,
            'is_symlink': file_path.is_symlink() if file_path.exists() else False,
            'target': str(file_path.readlink()) if file_path.exists() and file_path.is_symlink() else None
        }
        evidence_status.append(status)
    
    # Generate report
    total_files = len(evidence_status)
    existing_files = sum(1 for s in evidence_status if s['exists'])
    real_files = sum(1 for s in evidence_status if s['exists'] and s['size'] > 0)
    placeholder_files = sum(1 for s in evidence_status if s['exists'] and s['size'] == 0)
    
    print(f"Evidence Status Report for {Path(ci_path).name}")
    print(f"{'='*60}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Expected Files: {total_files}")
    print(f"Existing Files: {existing_files}")
    print(f"Real Files (non-placeholder): {real_files}")
    print(f"Placeholder Files: {placeholder_files}")
    print(f"Completion: {real_files/total_files*100:.1f}% real, {existing_files/total_files*100:.1f}% total")
    print()
    
    # Missing files
    missing_files = [s for s in evidence_status if not s['exists']]
    if missing_files:
        print("❌ Missing Files:")
        for status in missing_files:
            print(f"  - {status['file']}")
        print()
    
    # Placeholder files
    placeholder_files_list = [s for s in evidence_status if s['exists'] and s['size'] == 0]
    if placeholder_files_list:
        print("⚠️ Placeholder Files (0 bytes):")
        for status in placeholder_files_list:
            target_info = f" -> {status['target']}" if status['is_symlink'] else ""
            print(f"  - {status['file']}{target_info}")
        print()
    
    # Real files
    real_files_list = [s for s in evidence_status if s['exists'] and s['size'] > 0]
    if real_files_list:
        print("✅ Real Files (with content):")
        for status in real_files_list:
            size_info = f" ({status['size']} bytes)"
            target_info = f" -> {status['target']}" if status['is_symlink'] else ""
            print(f"  - {status['file']}{size_info}{target_info}")
        print()
    
    # Summary by category
    print("📊 Summary by Evidence Type:")
    
    categories = {
        "Analysis": [s for s in evidence_status if 'AN-' in s['file']],
        "Test": [s for s in evidence_status if 'TST-' in s['file']],
        "Calculations": [s for s in evidence_status if 'CALC-' in s['file']],
        "Compliance": [s for s in evidence_status if any(x in s['file'] for x in ['LOAD-', 'AEL-', 'FDT-', 'EMC-', 'LPS-', 'IFX-', 'MAT-', 'BVID-', 'THR-'])]
    }
    
    for category, files in categories.items():
        if files:
            existing = sum(1 for f in files if f['exists'])
            real = sum(1 for f in files if f['exists'] and f['size'] > 0)
            total = len(files)
            print(f"  {category}: {real}/{total} real ({real/total*100:.0f}%), {existing}/{total} exist ({existing/total*100:.0f}%)")
    
    print("="*60)
    
    return evidence_status

def generate_evidence_checklist(ci_path, output_file=None):
    """Generate a checklist for evidence completion."""
    phase_data_path = Path(ci_path) / '01-Requirements' / 'phase-data.yaml'
    
    if not phase_data_path.exists():
        print("❌ phase-data.yaml not found")
        return
        
    with open(phase_data_path, 'r') as f:
        phase_data = yaml.safe_load(f)
        
    lines = []
    lines.append("# Evidence Completion Checklist")
    lines.append(f"**CI:** {phase_data.get('component_id', 'Unknown')}")
    lines.append(f"**Document:** {phase_data.get('doc_id', 'Unknown')}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    evidence_base_path = Path(ci_path) / '01-Requirements' / 'evidence'
    
    # Group by type
    analysis_files = []
    test_files = []
    calc_files = []
    other_files = []
    
    for link in phase_data.get('links', []):
        file_path = evidence_base_path / link
        exists = file_path.exists()
        has_content = exists and file_path.stat().st_size > 0
        
        status = "✅" if has_content else ("📄" if exists else "❌")
        item = f"- [{status}] {link}"
        
        if 'AN-' in link:
            analysis_files.append(item)
        elif 'TST-' in link:
            test_files.append(item)
        elif 'CALC-' in link:
            calc_files.append(item)
        else:
            other_files.append(item)
    
    # Add sections
    if analysis_files:
        lines.append("## Analysis Evidence")
        lines.extend(analysis_files)
        lines.append("")
        
    if test_files:
        lines.append("## Test Evidence") 
        lines.extend(test_files)
        lines.append("")
        
    if calc_files:
        lines.append("## Calculation Evidence")
        lines.extend(calc_files)
        lines.append("")
        
    if other_files:
        lines.append("## Other Evidence")
        lines.extend(other_files)
        lines.append("")
    
    lines.append("## Legend")
    lines.append("- ✅ Complete (file exists with content)")
    lines.append("- 📄 Placeholder (file exists but empty)")
    lines.append("- ❌ Missing (file does not exist)")
    
    content = "\n".join(lines)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(content)
        print(f"📋 Checklist written to {output_file}")
    else:
        print(content)

def main():
    parser = argparse.ArgumentParser(description='Track evidence document status')
    parser.add_argument('ci_path', help='Path to CI directory')
    parser.add_argument('--checklist', help='Generate checklist to file')
    parser.add_argument('--export-csv', help='Export status to CSV file')
    
    args = parser.parse_args()
    
    ci_path = Path(args.ci_path)
    if not ci_path.exists():
        print(f"❌ CI path does not exist: {ci_path}")
        return 1
    
    # Generate status report
    evidence_status = check_evidence_status(ci_path)
    
    # Generate checklist if requested
    if args.checklist:
        generate_evidence_checklist(ci_path, args.checklist)
    
    # Export CSV if requested
    if args.export_csv and evidence_status is not None:
        with open(args.export_csv, 'w') as f:
            f.write("file,exists,size,is_placeholder,is_symlink,target\n")
            for status in evidence_status:
                f.write(f"{status['file']},{status['exists']},{status['size']},{status['is_placeholder']},{status['is_symlink']},{status['target'] or ''}\n")
        print(f"📊 Status exported to {args.export_csv}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())