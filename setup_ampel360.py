#!/usr/bin/env python3
"""
AMPEL360 H₂-BWB-Q Setup and Demonstration Script
Complete setup and execution of the aircraft configuration optimization framework
"""

import subprocess
import sys
from pathlib import Path
import json


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n📋 {description}")
    print(f"🔧 Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"✅ Output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False


def main():
    """Main setup and demonstration"""
    print("=" * 60)
    print("🚁 AMPEL360 H₂-BWB-Q Aircraft Configuration Framework")
    print("   Optimized BWB with Hydrogen Propulsion & Quantum Optimization")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("ampel360_config.json").exists():
        print("❌ Error: ampel360_config.json not found. Run from repository root.")
        sys.exit(1)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Continuing without dependency installation...")
    
    # Step 2: Validate configuration
    if not run_command("python3 ampel360_utils.py --status --validate", 
                      "Validating configuration and file paths"):
        sys.exit(1)
    
    # Step 3: Generate feasible set and optimize
    if not run_command("python3 scripts/qaoa_over_F.py --optimize", 
                      "Running QAOA optimization to determine QNNN"):
        sys.exit(1)
    
    # Step 4: Load optimization results
    try:
        with open("qnnn_optimization_result.json", 'r') as f:
            optimization_result = json.load(f)
        
        qnnn = optimization_result['QNNN']
        
        # Step 5: Update configuration with optimal QNNN
        if not run_command(f"python3 ampel360_utils.py --set-qnnn {qnnn}", 
                          f"Updating configuration with optimal QNNN={qnnn}"):
            sys.exit(1)
        
    except FileNotFoundError:
        print("❌ Optimization result file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error reading optimization results")
        sys.exit(1)
    
    # Step 6: Final validation
    if not run_command("python3 ampel360_utils.py --status", 
                      "Final configuration status"):
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 AMPEL360 H₂-BWB-Q Framework Setup Complete!")
    print("=" * 60)
    
    print("\n📊 Optimization Results:")
    print(f"   • Optimal passenger capacity (QNNN): {optimization_result['QNNN']}")
    print(f"   • Selected configuration: {optimization_result['selected_config']['id']}")
    print("   • Architecture type: BWB with H₂ propulsion")
    print(f"   • Objective value: ${optimization_result['objective_value']:,.0f}")
    
    selected_config = optimization_result['selected_config']['config']
    print("\n🏗️  Architecture Details:")
    for component, donor_id in selected_config.items():
        print(f"   • {component}: Donor {donor_id}")
    
    print("\n📁 Generated Files:")
    print("   • constraints/hard_constraints.yaml - TRL gates & compatibility rules")
    print(f"   • data/candidates.yaml - AMPEL donor database")
    print(f"   • feasible_set.json - Feasible configurations")
    print(f"   • qnnn_optimization_result.json - Optimization results")
    print(f"   • ampel360_config.json - Main configuration (updated)")
    
    print(f"\n🚀 Next Steps:")
    print("   • Review optimization results in qnnn_optimization_result.json")
    print(f"   • Customize constraints in constraints/hard_constraints.yaml")
    print(f"   • Add more candidates to data/candidates.yaml")
    print(f"   • Run detailed geometric integration analysis")
    print("   • Proceed to P3 phase with BLI/DP and morphing capabilities")


if __name__ == "__main__":
    main()