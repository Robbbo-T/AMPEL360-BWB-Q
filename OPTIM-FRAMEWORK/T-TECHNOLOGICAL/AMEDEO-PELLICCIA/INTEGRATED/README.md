# AMEDEO-PELLICCIA / INTEGRATED — Systems Index

This directory aggregates **integrated technological programs** under the AMEDEO-PELLICCIA taxonomy.  
Each program exposes domain folders (A, A2, C, C2, D, E, E2, E3, I, I2, L, L2, M, O, P), which contain **Configuration Architectures (CAs)** and their **UTCS 01–11** phase artifacts.

---

## Programs

- **AMPEL360-H₂-BWB-QNNN**  
  Integrated hydrogen BWB case study with full CA/CI coverage and UTCS folders.  
  ➜ [`./AMPEL360-H2-BWB-QNNN/`](./AMPEL360-H2-BWB-QNNN/)

> Add new integrated programs as sibling folders at this level (one folder per program).

---

## Directory Contract (per program)

Each program directory MUST contain:

- `README.md` — navigable index of all domains and CAs
- `ampel-config.yaml` — program-level config (paths, validators, CI ledger hooks)
- Domain folders:
```

A-ARCHITECTURE/   A2-AIRPORTS/   C-CONTROL/      C2-CRYOGENICS/
D-DIGITAL/        E-ENVIRONMENTAL/ E2-ENERGY/    E3-ELECTRONICS/
I-INFRASTRUCTURES/ I2-INTELLIGENCE/ L-LOGISTICS/ L2-LINKS/
M-MECHANICAL/     O-OPERATIONS/   P-PROPULSION/

```

Inside each **CA** folder, provide the canonical UTCS layout:

```

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

```

---

## Validation & Traceability (summary)

- **Naming**: CA/CI IDs must follow program conventions and be referenced in UTCS artifacts.  
- **Artifacts-as-code**: Keep requirements, ICDs, analyses, SBOMs, test logs in the relevant UTCS phase.  
- **CI Ledger** (optional but recommended): if enabled, update `T-TECHNOLOGICAL/LEDGER/cli/ledger-plan.json` when UTCS artifacts change to ensure cryptographic traceability.

---

## Navigation

- Parent (AMEDEO-PELLICCIA): [`../`](../)
- Technological root: [`../../`](../../)
- Optimization Framework root: [`../../../`](../../../)
```
