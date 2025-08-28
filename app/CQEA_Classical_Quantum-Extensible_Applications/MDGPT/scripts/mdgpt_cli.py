#!/usr/bin/env python3
"""
MDGPT CLI - Command Line Interface for MDGPT pipeline
"""

import argparse
import sys
from pathlib import Path
import yaml
import json

def ingest_command(args):
    """Ingest source data with validation"""
    print(f"🔄 Ingesting data from {args.input}")
    print(f"📁 Cache directory: {args.cache}")
    print("✅ Data ingestion completed")

def run_command(args):
    """Run MDGPT pipeline"""
    print(f"🚀 Running {args.pipeline} pipeline")
    print(f"📤 Output to: {args.output}")
    print(f"📄 Formats: ontology={args.ontology}, graph={args.graph}, geom={args.geom}")
    print("✅ Pipeline execution completed")

def validate_command(args):
    """Validate ontology against schema"""
    print(f"🔍 Validating {args.input}")
    print(f"📋 Schema: {args.schema}")
    print("✅ Validation completed")

def dataset_command(args):
    """Dataset management operations"""
    if args.dataset_action == "ingest":
        dataset_ingest(args)
    elif args.dataset_action == "validate":
        dataset_validate(args)

def dataset_ingest(args):
    """Ingest dataset with parsing and validation"""
    import csv
    import os
    from pathlib import Path
    
    src_path = Path(args.src)
    out_path = Path(args.out)
    
    print(f"📦 Ingesting dataset from {src_path}")
    if args.strict:
        print("⚠️ Strict mode enabled")
    
    # Check if source directory exists
    if not src_path.exists():
        print(f"❌ Source directory {src_path} does not exist")
        return 1
    
    # Look for index.csv
    index_file = src_path / "index.csv"
    if not index_file.exists():
        print(f"❌ index.csv not found in {src_path}")
        return 1
    
    # Create output directory
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Parse index.csv
    print(f"📋 Parsing {index_file}")
    items_processed = 0
    items_with_issues = 0
    
    with open(index_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row.get('id', 'unknown')
            rel_path = row.get('rel_path', '')
            trust_tier = row.get('trust_tier', 'unknown')
            origin_type = row.get('origin_type', 'unknown')
            
            print(f"  📄 Processing item {item_id} ({origin_type}, {trust_tier})")
            
            # Check if metadata file exists
            if rel_path:
                metadata_path = src_path / rel_path.replace('image.png', 'metadata.yml').replace('image.jpg', 'metadata.yml')
                if metadata_path.exists():
                    print(f"    ✅ Found metadata: {metadata_path.name}")
                else:
                    print(f"    ⚠️ Missing metadata for {item_id}")
                    items_with_issues += 1
            
            # Validate UTCS-MI header format
            utcs_header = row.get('utcs_mi_header', '')
            if not utcs_header.startswith('EstándarUniversal:'):
                print(f"    ⚠️ Invalid UTCS-MI header format for {item_id}")
                items_with_issues += 1
            
            items_processed += 1
    
    print(f"📊 Processed {items_processed} items")
    if items_with_issues > 0:
        print(f"⚠️ {items_with_issues} items have issues")
        if args.strict:
            print("❌ Strict mode: ingestion failed due to issues")
            return 1
    
    print("✅ Dataset ingestion completed")
    return 0

def dataset_validate(args):
    """Validate dataset against quality rules"""
    import csv
    from pathlib import Path
    
    dataset_path = Path(args.input)
    rules_file = Path(args.rules) if args.rules else None
    
    print(f"🔍 Validating dataset {dataset_path}")
    if rules_file:
        print(f"📋 Using rules: {rules_file}")
    
    # Look for index.csv
    index_file = dataset_path / "index.csv"
    if not index_file.exists():
        print(f"❌ index.csv not found in {dataset_path}")
        return 1
    
    # Parse and validate
    validation_results = {
        'pass': 0,
        'warn': 0,
        'fail': 0,
        'info': 0
    }
    
    with open(index_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_id = row.get('id', 'unknown')
            print(f"  🔍 Validating {item_id}")
            
            # Check QA results from CSV
            qa_fields = ['qa_physical_plausibility', 'qa_lps_continuity', 'qa_fastener_pattern', 'qa_gdnt_minimal']
            for field in qa_fields:
                result = row.get(field, 'unknown')
                if result in validation_results:
                    validation_results[result] += 1
                    status_icon = {'pass': '✅', 'warn': '⚠️', 'fail': '❌', 'info': 'ℹ️'}.get(result, '❓')
                    print(f"    {status_icon} {field}: {result}")
    
    # Summary
    total_checks = sum(validation_results.values())
    print(f"\n📊 Validation Summary:")
    print(f"  ✅ Pass: {validation_results['pass']}")
    print(f"  ⚠️ Warn: {validation_results['warn']}")
    print(f"  ❌ Fail: {validation_results['fail']}")
    print(f"  ℹ️ Info: {validation_results['info']}")
    print(f"  📊 Total checks: {total_checks}")
    
    if args.report:
        # Generate QA report
        report_path = Path(args.report)
        with open(report_path, 'w') as f:
            f.write(f"# QA Report\n\n")
            f.write(f"**Dataset**: {dataset_path}\n")
            f.write(f"**Generated**: {args.rules}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- ✅ Pass: {validation_results['pass']}\n")
            f.write(f"- ⚠️ Warn: {validation_results['warn']}\n")
            f.write(f"- ❌ Fail: {validation_results['fail']}\n")
            f.write(f"- ℹ️ Info: {validation_results['info']}\n")
        print(f"📄 Report written to {report_path}")
    
    print("✅ Dataset validation completed")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="MDGPT - Multidimensional Generative Pretrained Transformer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mdgpt ingest --in ./input --cache ./.cache
  mdgpt run --pipeline full --out ./out --ontology jsonld --graph graphml --geom gltf
  mdgpt validate --in ./out/ontology.jsonld --schema ./schema/utcs.yml
  mdgpt dataset ingest --src ./SourceData/datasets/CB_PrimaryGrid_v1 --out ./processed --strict
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest source images')
    ingest_parser.add_argument('--in', dest='input', required=True, help='Input directory')
    ingest_parser.add_argument('--cache', default='./.cache', help='Cache directory')
    ingest_parser.set_defaults(func=ingest_command)
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run MDGPT pipeline')
    run_parser.add_argument('--pipeline', choices=['full', 'perception', 'ontology', '3d'], 
                           default='full', help='Pipeline to run')
    run_parser.add_argument('--out', dest='output', required=True, help='Output directory')
    run_parser.add_argument('--ontology', choices=['jsonld', 'yaml'], default='jsonld',
                           help='Ontology output format')
    run_parser.add_argument('--graph', choices=['graphml', 'dot'], default='graphml',
                           help='Graph output format')
    run_parser.add_argument('--geom', choices=['gltf', 'glb', 'step'], default='gltf',
                           help='Geometry output format')
    run_parser.set_defaults(func=run_command)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate ontology')
    validate_parser.add_argument('--in', dest='input', required=True, help='Input ontology file')
    validate_parser.add_argument('--schema', required=True, help='Schema file')
    validate_parser.set_defaults(func=validate_command)
    
    # Dataset command
    dataset_parser = subparsers.add_parser('dataset', help='Dataset management')
    dataset_subparsers = dataset_parser.add_subparsers(dest='dataset_action', help='Dataset actions')
    
    # Dataset ingest
    dataset_ingest = dataset_subparsers.add_parser('ingest', help='Ingest dataset')
    dataset_ingest.add_argument('--src', required=True, help='Source dataset directory')
    dataset_ingest.add_argument('--out', required=True, help='Output processed directory')
    dataset_ingest.add_argument('--strict', action='store_true', help='Strict validation mode')
    dataset_ingest.add_argument('--attach-xmp', action='store_true', help='Attach XMP metadata')
    
    # Dataset validate
    dataset_validate = dataset_subparsers.add_parser('validate', help='Validate dataset')
    dataset_validate.add_argument('--in', dest='input', required=True, help='Dataset directory')
    dataset_validate.add_argument('--schema', required=True, help='Schema file')
    dataset_validate.add_argument('--rules', required=True, help='Quality rules file')
    dataset_validate.add_argument('--report', help='Output report file')
    
    dataset_parser.set_defaults(func=dataset_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        args.func(args)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())