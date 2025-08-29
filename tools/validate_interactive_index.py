#!/usr/bin/env python3
"""
AMPEL360 Interactive Index Validation Script
Validates the interactive index deployment and structure.
"""

import os
import sys
import json
from pathlib import Path

def validate_interactive_index():
    """Validate the interactive index files and structure."""
    
    framework_dir = Path("OPTIM-FRAMEWORK")
    
    print("🔍 Validating AMPEL360 Interactive Framework Index...")
    print("=" * 60)
    
    # Check required files
    required_files = [
        "index.html",
        "styles.css", 
        "script.js",
        "DEPLOYMENT.md",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = framework_dir / file
        if file_path.exists():
            print(f"✅ {file} - Found ({file_path.stat().st_size} bytes)")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Missing required files: {missing_files}")
        return False
    
    # Check technological domains
    tech_dir = framework_dir / "T-TECHNOLOGICAL" / "AMEDEO-PELLICCIA" / "INTEGRATED" / "AMPEL360-H2-BWB-QNNN"
    
    expected_domains = [
        "A-ARCHITECTURE",
        "A2-AIRPORTS", 
        "C-CONTROL",
        "C2-CRYOGENICS",
        "D-DIGITAL",
        "E-ENVIRONMENTAL",
        "E2-ENERGY",
        "E3-ELECTRONICS",
        "I-INFRASTRUCTURES",
        "I2-INTELLIGENCE",
        "L-LOGISTICS",
        "L2-LINKS",
        "M-MECHANICAL",
        "O-OPERATING_SYSTEMS",
        "P-PROPULSION"
    ]
    
    print(f"\n🔧 Validating technological domains in {tech_dir}...")
    missing_domains = []
    
    for domain in expected_domains:
        domain_path = tech_dir / domain
        if domain_path.exists() and domain_path.is_dir():
            print(f"✅ {domain}")
        else:
            print(f"❌ {domain} - Missing or not a directory")
            missing_domains.append(domain)
    
    if missing_domains:
        print(f"\n⚠️  Missing domains: {missing_domains}")
    
    # Check framework sections
    framework_sections = [
        "O-ORGANIZATIONAL",
        "P-PROCEDURAL", 
        "T-TECHNOLOGICAL",
        "I-INTELLIGENT",
        "M-MACHINE",
        "E-EXECUTING"
    ]
    
    print(f"\n📁 Validating framework sections...")
    missing_sections = []
    
    for section in framework_sections:
        section_path = framework_dir / section
        if section_path.exists() and section_path.is_dir():
            print(f"✅ {section}")
        else:
            print(f"❌ {section} - Missing or not a directory")
            missing_sections.append(section)
    
    if missing_sections:
        print(f"\n⚠️  Missing sections: {missing_sections}")
    
    # Validate HTML structure
    print(f"\n📄 Validating index.html structure...")
    index_file = framework_dir / "index.html"
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key elements
        checks = [
            ('DOCTYPE html', 'HTML5 doctype'),
            ('Interactive OPTIM Framework Index', 'Page title'),
            ('searchInput', 'Search functionality'),
            ('nav-item', 'Navigation items'),
            ('overview-card', 'Overview cards'),
            ('domains-grid', 'Domains grid'),
            ('script.js', 'JavaScript file reference'),
            ('styles.css', 'CSS file reference')
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - Not found")
                
    except Exception as e:
        print(f"❌ Error reading index.html: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    total_issues = len(missing_files) + len(missing_domains) + len(missing_sections)
    
    if total_issues == 0:
        print("🎉 Interactive Index Validation PASSED!")
        print("✅ All required files and directories are present")
        print("✅ HTML structure is valid")
        print("✅ Ready for deployment")
        return True
    else:
        print(f"⚠️  Interactive Index Validation completed with {total_issues} issues")
        print("📝 Review the missing items above before deployment")
        return False

if __name__ == "__main__":
    success = validate_interactive_index()
    sys.exit(0 if success else 1)