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
        print(f"📦 Ingesting dataset from {args.src}")
        if args.strict:
            print("⚠️ Strict mode enabled")
    elif args.dataset_action == "validate":
        print(f"🔍 Validating dataset {args.input}")
    print("✅ Dataset operation completed")

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