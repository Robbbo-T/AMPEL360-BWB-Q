# AMPEL360-H2-BWB-QNNN

Perfect—here’s the same navigable index without any “how long ago” timestamps. Drop this in:

# AMEDEO-PELLICCIA • Integrated Index — AMPEL360-H₂-BWB-QNNN

This index routes to each domain directory and the local config. Keep folder names exactly as-is for relative links to work.

---

## Quick links
- ▶︎ **Program README**: [`./README.md`](./README.md)
- ⚙️ **Config**: [`./ampel-config.yaml`](./ampel-config.yaml)

---

## Domains (navigation)

- **A-ARCHITECTURE** — Airframe configuration, geometry, CA/CI registry, interfaces.  
  ➜ [`./A-ARCHITECTURE/`](./A-ARCHITECTURE/)

- **A2-AIRPORTS** — Ground infrastructure, hydrogen handling, turnaround, safety corridors.  
  ➜ [`./A2-AIRPORTS/`](./A2-AIRPORTS/)

- **C-CONTROL** — Flight control laws, stability/handling, FbW/FbQW integration, autopilot.  
  ➜ [`./C-CONTROL/`](./C-CONTROL/)

- **C2-CRYOGENICS** — LH₂ tanks, insulation, thermal barriers, purge & venting, cold-soak.  
  ➜ [`./C2-CRYOGENICS/`](./C2-CRYOGENICS/)

- **D-DIGITAL** — Avionics software, DT/MBSE assets, data models, toolchains, SBOMs.  
  ➜ [`./D-DIGITAL/`](./D-DIGITAL/)

- **E-ENVIRONMENTAL** — DO-160 profiles, noise, emissions, lightning/EMC evidence.  
  ➜ [`./E-ENVIRONMENTAL/`](./E-ENVIRONMENTAL/)

- **E2-ENERGY** — Electrical power generation & distribution, energy management.  
  ➜ [`./E2-ENERGY/`](./E2-ENERGY/)

- **E3-ELECTRONICS** — LRUs/PCBs, harnessing, connectors, HW assurance, qualification.  
  ➜ [`./E3-ELECTRONICS/`](./E3-ELECTRONICS/)

- **I-INFRASTRUCTURES** — Industrial/test facilities, manufacturing networks, QA flows.  
  ➜ [`./I-INFRASTRUCTURES/`](./I-INFRASTRUCTURES/)

- **I2-INTELLIGENCE** — AI/ML optimization, Q-enhanced solvers, autonomy logic.  
  ➜ [`./I2-INTELLIGENCE/`](./I2-INTELLIGENCE/)

- **L-LOGISTICS** — Supply chain, spares, MRP/ERP integration, sustainment planning.  
  ➜ [`./L-LOGISTICS/`](./L-LOGISTICS/)

- **L2-LINKS** — Comms/data links, networking, security segmentation, timing.  
  ➜ [`./L2-LINKS/`](./L2-LINKS/)

- **M-MECHANICAL** — Structures, mechanisms, landing gear, doors, loads & margins.  
  ➜ [`./M-MECHANICAL/`](./M-MECHANICAL/)

- **O-OPERATIONS** — CONOPS, EIS procedures, training, dispatch reliability.  
  ➜ [`./O-OPERATIONS/`](./O-OPERATIONS/)

- **P-PROPULSION** — Turbomachinery, inlets/nozzles, integration with LH₂ & energy.  
  ➜ [`./P-PROPULSION/`](./P-PROPULSION/)

---

## Suggested per-domain structure (optional)

If you follow UTCS 01–11 inside each domain, use this pattern for subfolders:

UTCS-01-Requirements/
UTCS-02-Design/
UTCS-03-Building-Prototyping/
UTCS-04-Executables-Packages/
UTCS-05-Verification-Validation/
UTCS-06-Integration-Qualification/
UTCS-07-Certification-Security/
UTCS-08-Production-Scale/
UTCS-09-Ops-Services/
UTCS-10-MRO/
UTCS-11-Sustainment-Recycle/

Each `UTCS-*` folder should include a short `README.md` and the relevant artifacts (YAML/JSON, analyses, test logs).

---

## Notes

- Keep `ampel-config.yaml` at this level for tooling to discover domains and UTCS phases.

