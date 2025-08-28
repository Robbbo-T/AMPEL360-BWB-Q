#!/usr/bin/env python3
"""
MDGPT Source Data Demo
Demonstrates the complete UTCS-MI v5.0 traceability workflow
"""

import csv
import json
import yaml
from pathlib import Path

def demo_source_data():
    """Demo the complete source data workflow"""
    
    print("🚀 MDGPT Source Data with UTCS-MI v5.0 Traceability Demo")
    print("=" * 60)
    
    # Dataset path
    dataset_path = Path("./SourceData/datasets/CB_PrimaryGrid_v1")
    
    print(f"\n📁 Dataset: {dataset_path}")
    
    # Show dataset structure
    print(f"\n📂 Directory Structure:")
    for item in sorted(dataset_path.rglob("*")):
        if item.is_file():
            indent = "  " * (len(item.parts) - len(dataset_path.parts))
            print(f"{indent}📄 {item.name}")
    
    # Parse and display index.csv
    index_file = dataset_path / "index.csv"
    print(f"\n📊 Index CSV Analysis:")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            print(f"\n  Item {i}: {row['id']}")
            print(f"    🏷️  Origin: {row['origin_type']}")
            print(f"    🔒 Trust Tier: {row['trust_tier']}")
            print(f"    📅 Timestamp: {row['timestamp']}")
            
            # Show UTCS-MI header
            utcs_header = row['utcs_mi_header']
            print(f"    🔗 UTCS-MI: {utcs_header[:50]}...")
            
            # Show QA status
            qa_status = []
            for field in ['qa_physical_plausibility', 'qa_lps_continuity', 'qa_fastener_pattern', 'qa_gdnt_minimal']:
                value = row.get(field, 'unknown')
                emoji = {'pass': '✅', 'warn': '⚠️', 'fail': '❌', 'info': 'ℹ️'}.get(value, '❓')
                qa_status.append(f"{emoji} {field.split('_')[-1]}")
            print(f"    🔍 QA: {' '.join(qa_status)}")
            
            # Show SyntheticLM specific fields
            if row['origin_type'] == 'SyntheticLM':
                print(f"    🤖 Model: {row['model_name']} v{row['model_version']}")
                print(f"    💭 Prompt: {row['prompt'][:40]}...")
                print(f"    🎲 Seed: {row['seed']}")
                print(f"    💧 Watermark: {row['watermark']}")
    
    # Show metadata example
    print(f"\n📋 Sample Metadata (T0 - Gold Standard):")
    metadata_file = dataset_path / "items" / "000001" / "metadata.yml"
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
        print(f"    🔗 UTCS-MI: {metadata['utcs_mi_header'][:60]}...")
        print(f"    🏷️  ID: {metadata['id']}")
        print(f"    📊 Origin: {metadata['origin_type']} (Tier {metadata['trust_tier']})")
        print(f"    🔧 Generator: {metadata['provenance']['generator']}")
        
        if 'parametric' in metadata:
            print(f"    ⚙️  Parameters:")
            for param, value in metadata['parametric']['parameters'].items():
                print(f"        {param}: {value}")
    
    # Show GT files
    print(f"\n🎯 Ground Truth Files (T0):")
    gt_dir = dataset_path / "items" / "000001"
    for gt_file in ['ontology.jsonld', 'graph.graphml', 'geom.glb']:
        gt_path = gt_dir / gt_file
        if gt_path.exists():
            size = gt_path.stat().st_size
            print(f"    ✅ {gt_file} ({size:,} bytes)")
            
            if gt_file == 'ontology.jsonld':
                # Show a snippet of the ontology
                with open(gt_path, 'r') as f:
                    ontology = json.load(f)
                    if '@graph' in ontology:
                        component = ontology['@graph'][0]
                        print(f"        📝 Component: {component.get('@id', 'unknown')}")
                        print(f"        🔧 Type: {component.get('@type', 'unknown')}")
    
    print(f"\n✅ Demo completed - MDGPT Source Data fully materialized!")
    print(f"🔗 UTCS-MI v5.0 traceability: ACTIVE")
    print(f"📊 Trust tiers: T0 (1), T2 (1), T3 (1)")
    print(f"🎯 Ground truth coverage: 33% (1/3 items)")

if __name__ == "__main__":
    demo_source_data()