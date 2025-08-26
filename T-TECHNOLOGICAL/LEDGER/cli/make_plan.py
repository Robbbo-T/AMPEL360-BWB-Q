#!/usr/bin/env python3
import sys, json, hashlib, os, re, yaml
from pathlib import Path

WATCH = yaml.safe_load(open("T-TECHNOLOGICAL/LEDGER/cli/ledger_watch.yaml"))
PLAN = {"version":"1.0","plans":[]}

CI_REGEXES = [
  re.compile(r"(CI-CA-[A-Z0-9-]{3,})"),
  re.compile(r"(CI-[A-Z0-9-]{5,})")
]

def sha256_stream(path, chunk=8192, progress_mb=100):
  h=hashlib.sha256(); size=os.path.getsize(path); done=0
  with open(path,"rb") as f:
    while True:
      b=f.read(chunk)
      if not b: break
      h.update(b); done += len(b)
      # print progress every ~100MB
      if progress_mb and done and done%(progress_mb*1024*1024)==0:
        pct = (done/size*100) if size else 100
        print(f"  hash {Path(path).name}: {pct:.1f}%")
  return h.hexdigest(), size

def guess_phase(path:str):
  p = Path(path)
  # Check if path contains a direct phase directory match
  phase_names = {
    "01-Requirements": "01-Requirements", 
    "02-Design": "02-Design", 
    "02-Architecture": "02-Design",  # Support for existing 02-Architecture
    "03-Building-Prototyping": "03-Building-Prototyping",
    "04-Executables-Packages": "04-Executables-Packages",
    "05-Verification-Validation": "05-Verification-Validation",
    "05-Integration": "05-Verification-Validation",  # Support for existing 05-Integration
    "06-Integration-Qualification": "06-Integration-Qualification",
    "07-Certification-Security": "07-Certification-Security",
    "07-Deployment": "07-Certification-Security",  # Support for existing 07-Deployment
    "08-Production-Scale": "08-Production-Scale",
    "09-Ops-Services": "09-Ops-Services",
    "09-Maintenance": "09-Ops-Services",  # Support for existing 09-Maintenance
    "10-MRO": "10-MRO",
    "11-Sustainment-Recycle": "11-Sustainment-Recycle"
  }
  
  # Check each directory part for phase names
  for part in p.parts:
    if part in phase_names:
      return phase_names[part]
  
  # fallback by folder name e.g. UTCS-02-Design
  m=re.search(r"UTCS-(\d{2})-[^/]+", str(p))
  if m:
    code=m.group(1)
    names={
      "01":"01-Requirements","02":"02-Design","03":"03-Building-Prototyping",
      "04":"04-Executables-Packages","05":"05-Verification-Validation",
      "06":"06-Integration-Qualification","07":"07-Certification-Security",
      "08":"08-Production-Scale","09":"09-Ops-Services","10":"10-MRO","11":"11-Sustainment-Recycle"
    }
    return names.get(code)
  return None

def extract_ci_from_path(path:str)->str:
  parts=list(Path(path).parts)
  # Common pattern: .../CA-.../<UTCS-xx-...>/... and CI appears in filenames or a sibling
  # First, scan each part for explicit CI-...
  for part in parts:
    if part.startswith("CI-"): return part
  # Try regex over full string
  s=str(path)
  for rgx in CI_REGEXES:
    m=rgx.search(s)
    if m: return m.group(1)
  # Try to infer from CA folder + default first CI (domain-specific convention)
  for i,part in enumerate(parts):
    if part.startswith("CA-") and i+1 < len(parts) and parts[i+1].startswith("CI-"):
      return parts[i+1]
  raise ValueError(f"Cannot determine CI for {path}")

def main(paths):
  entries=0
  for p in paths:
    if not os.path.isfile(p): continue
    phase=guess_phase(p)
    if not phase: continue
    ci = extract_ci_from_path(p)
    sh, size = sha256_stream(p)
    PLAN["plans"].append({
      "ci_id": ci,
      "utcs_phase": phase,
      "freeze_after_link": (phase=="01-Requirements"),
      "artifact": {
        "path": p, "sha256": sh, "size_bytes": size,
        "mime": "application/octet-stream",
        "storage_uri": f"s3://TO-FILL/{os.path.basename(p)}"
      },
      "refs": {}
    })
    entries += 1
  out="T-TECHNOLOGICAL/LEDGER/cli/ledger-plan.json"
  Path(out).write_text(json.dumps(PLAN, indent=2))
  print(f"Wrote {out} with {entries} entries")

if __name__=="__main__":
  if len(sys.argv)==1:
    print("Usage: make_plan.py <file1> <file2> ... (e.g. from git diff)"); sys.exit(2)
  main(sys.argv[1:])