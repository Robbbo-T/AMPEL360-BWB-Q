#!/usr/bin/env python3
"""
AMPEL360 Configuration Index Validator
Validates configuration index YAML against schema and checks artifact paths
"""

import sys
import json
import yaml
import hashlib
import pathlib
from jsonschema import validate, ValidationError

BASE = pathlib.Path(__file__).resolve().parents[1]  # repo root
IDX = BASE / "OPTIM-FRAMEWORK/O-ORGANIZATIONAL/artifacts/configuration-index.yaml"
SCHEMA = BASE / "tools/configuration-index.schema.json"

def sha256(p: pathlib.Path) -> str:
    """Calculate SHA256 hash of a file"""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def resolve(base_dir: pathlib.Path, rel: str) -> pathlib.Path:
    """Resolve relative path from base directory"""
    return (base_dir / rel).resolve()

def main():
    """Main validation function"""
    try:
        # Load and validate configuration index
        if not IDX.exists():
            print(f"ERROR: Configuration index not found at {IDX}", file=sys.stderr)
            return 2
            
        data = yaml.safe_load(IDX.read_text(encoding="utf-8"))
        
        # Load and apply schema validation
        if not SCHEMA.exists():
            print(f"ERROR: Schema not found at {SCHEMA}", file=sys.stderr)
            return 2
            
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        
        try:
            validate(instance=data, schema=schema)
            print("✅ Schema validation passed")
        except ValidationError as e:
            print(f"❌ Schema validation failed: {e.message}", file=sys.stderr)
            return 1

        # Determine base directory for path resolution
        idx_dir = IDX.parent if data.get("meta", {}).get("path_base") == "this_file_dir" else BASE
        touched = False
        missing_files = []
        stamped_files = []

        def stamp(node):
            """Stamp SHA256 for artifact files"""
            nonlocal touched
            p = resolve(idx_dir, node["file"])
            if not p.exists():
                missing_files.append(node["file"])
                return False
            if "sha256" in node and (node["sha256"] is None or node["sha256"] == ""):
                node["sha256"] = sha256(p)
                stamped_files.append(node["file"])
                touched = True
            return True

        # Validate and stamp artifact paths
        cfg = data.get("configurations", {})
        for sect_name, sect in cfg.items():
            if isinstance(sect, list):
                for item in sect:
                    if "file" in item:
                        stamp(item)

        # Report results
        if missing_files:
            print("❌ Missing artifacts:", file=sys.stderr)
            for f in missing_files:
                print(f"   - {f}", file=sys.stderr)
            return 2

        if stamped_files:
            print(f"📄 Stamped SHA256 for {len(stamped_files)} files:")
            for f in stamped_files:
                print(f"   - {f}")

        # Write back updated configuration if files were stamped
        if touched:
            IDX.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
            print("✅ Configuration index updated with SHA256 stamps")

        print("✅ All validations passed")
        return 0

    except Exception as e:
        print(f"💥 Unexpected error: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())