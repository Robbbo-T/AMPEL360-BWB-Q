# CI-CA-A-001-001 — CB-PRIMARY-GRID · 01-Requirements

[◀︎ CI root](../) • [CA](../../) • [A-ARCHITECTURE](../../../) • [Programa](../../../../)

Carpeta de **requisitos** y **evidencias** de la fase **01-Requirements**.

---

## Especificaciones
- [`requirements.yaml`](./requirements.yaml) — requisitos “shall”, unidades, trazabilidad
- [`verification-matrix.csv`](./verification-matrix.csv) — REQ ↔ método ↔ artefacto
- [`phase-data.yaml`](./phase-data.yaml) — metadatos de fase (UTCS, gate, estado)
- [`change-log.yaml`](./change-log.yaml) — cambios controlados de la fase
- [`phase.md`](./phase.md) — resumen ejecutivo de la fase

---

## Evidencias
- **Analysis** → [`./evidence/analysis/`](./evidence/analysis/)
  - `STR-AN-001.pdf`, `STR-AN-002.pdf`, `STR-AN-003.pdf`, `THR-AN-003_Thermal-FEM`, `EMC-AN-001.pdf`, `OPS-AN-001_Fatigue-Analysis`, `PRF-AN-001_Weight-Analysis`, `PRF-AN-002_CG-Analysis`, `REL-AN-00x_*`, `SAF-AN-00x_*`, `SEC-AN-003_Cyber-Analysis`, etc.
- **Calculations** → [`./evidence/calculations/`](./evidence/calculations/)
  - `STR-CALC-001.xlsx`, `FDT-CG-001.xlsx`, …
- **Compliance** → [`./evidence/compliance/`](./evidence/compliance/)
  - `LOAD-341-VC-VD.pdf`, `CRT-AN-001_Compliance-Analysis`, `CRT-AN-002_Special-Conditions`, `MAT-ALW-CRYO-001.pdf`, `MAT-INS-003_QA-Traceability`, …
- **Test** → [`./evidence/test/`](./evidence/test/)
  - `AEL-FLT-001.pdf`, `AEL-GVT-001.pdf`, `PRF-TST-003_Modal-Test`, `STR-TST-004_GVT-Flutter`, `IFX-TST-MOUNT-001.pdf`, `LPS-TST-001.pdf`, `ENV-TST-001_Lightning-Protection`, `ENV-TST-002_Resistance-Test`, `THR-TST-CRYO-001.pdf`, `THR-TST-HFX-001.pdf`, etc.

> Nota: **elimina duplicados** en la carpeta (p. ej., `EMC-AN-001.pdf`, `FDT-AN-001.pdf`, `STR-AN-001.pdf`, `LOAD-341-VC-VD.pdf` aparecen repetidos). Deja **una sola copia** en la subcarpeta correcta y ajusta los enlaces de la matriz de verificación.

---

## Paquete de revisión (SRR)
- **Revisiones** → `./reviews/` (minutas y checklist)
- **SRR** → `./SRR/` (acta, asistentes, decisión, condiciones)

---

## Rail de fases (en este CI)
Siguiente → [`../02-Design/`](../02-Design/) · [`../03-Building-Prototyping/`](../03-Building-Prototyping/) · [`../04-Executables-Packages/`](../04-Executables-Packages/) · [`../05-Verification-Validation/`](../05-Verification-Validation/) · [`../06-Integration-Qualification/`](../06-Integration-Qualification/) · [`../07-Certification-Security/`](../07-Certification-Security/) · [`../08-Production-Scale/`](../08-Production-Scale/) · [`../09-Ops-Services/`](../09-Ops-Services/) · [`../10-MRO/`](../10-MRO/) · [`../11-Sustainment-Recycle/`](../11-Sustainment-Recycle/)
