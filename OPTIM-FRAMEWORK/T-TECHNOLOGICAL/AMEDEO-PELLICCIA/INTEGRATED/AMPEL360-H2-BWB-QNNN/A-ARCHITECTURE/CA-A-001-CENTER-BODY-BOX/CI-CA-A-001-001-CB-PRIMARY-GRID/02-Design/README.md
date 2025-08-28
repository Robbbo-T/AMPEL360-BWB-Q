# 02-Design — CI-CA-A-001-001 · CB-PRIMARY-GRID

[◀︎ 01-Requirements](../01-Requirements/) • [CI root](..) • [CA-A-001](../..) • [A-ARCHITECTURE](../../..) • [Programa](../../../..)

Fase de **diseño** del grid primario del center-body: definición estructural (keel, longerons, frames, refuerzos LG), red LPS, soportes de sistemas e interfaces con RIBS/SKIN/LH₂.

---

## Meta
- **Componente / CI:** CI-CA-A-001-001 — CB-PRIMARY-GRID  
- **Arquitectura / CA:** CA-A-001 — CENTER-BODY-BOX  
- **UTCS Phase:** **02-Design** (gates objetivo: **PDR → CDR**)  
- **Normas base:** ARP4754A/ARP4761 · CS-25 · DO-160G · SAE ARP5412/5416/5414 · ISO 11114-4  
- **Propietarios:** Chief Architect (DT) · Chief Systems Engineer · Certification Lead

---

## Rail de fases (CI)
01 → [01-Requirements](../01-Requirements/) **|** **02 → (aquí)** **|** 03 → [03-Building-Prototyping](../03-Building-Prototyping/) **|** 04 → [04-Executables-Packages](../04-Executables-Packages/) **|** 05 → [05-Verification-Validation](../05-Verification-Validation/) **|** 06 → [06-Integration-Qualification](../06-Integration-Qualification/) **|** 07 → [07-Certification-Security](../07-Certification-Security/) **|** 08 → [08-Production-Scale](../08-Production-Scale/) **|** 09 → [09-Ops-Services](../09-Ops-Services/) **|** 10 → [10-MRO](../10-MRO/) **|** 11 → [11-Sustainment-Recycle](../11-Sustainment-Recycle/)

---

## Objetivos de la fase
- Desarrollar la **arquitectura de producto** (PSB/BoS) y la **definición técnica** del CI.  
- Establecer **entregables** y **criterios de finalización** (PDR/CDR).  
- Consolidar **interfaces** (ICDs) y **restricciones** de diseño (estructura/cryo/LPS).  
- Preparar **evidencias** para V&V (05) y cualificación (06).

---

## Entregables (navegables)
- [x] **Product Structure Breakdown (PSB)** → [`PRODUCT-STRUCTURE.md`](./PRODUCT-STRUCTURE.md)  
- [x] **psb.yaml (machine-readable)** → [`psb.yaml`](./psb.yaml)  
- [x] **BOM semilla** → [`bom.csv`](./bom.csv)  
- [ ] **Especificaciones técnicas** → [`specs/README.md`](./specs/README.md)  
- [ ] **ICDs** (interfaces) → [`icd/README.md`](./icd/README.md)  
- [ ] **Modelos / pre-cálculos** → [`models/README.md`](./models/README.md)  
- [ ] **Trazabilidad** → `../01-Requirements/verification-matrix.csv` (actualizada con artefactos de diseño)

> Si aún no existen `specs/`, `icd/`, `models/`, puede crearlos ahora para mantener la navegación.

---

## Criterios de entrada (desde 01-Requirements, SRR)
- Requisitos **congelados** y trazados (`requirements.yaml`, **PASS** de SRR).  
- Matriz V&V inicial publicada (`verification-matrix.csv`).  
- Riesgos críticos registrados (THERM-001, STR-002, CERT-003, OPS-004).

## Criterios de salida
**PDR (Design Review Preliminar)**  
- PSB/psb.yaml y **BOM** completos a nivel de ensamblajes.  
- Interfaces identificadas y borradores **ICD** emitidos.  
- Evidencias preliminares (cálculos/analíticas) enlazadas en V&V.  
- Riesgos con mitigación planificada (acciones en curso).

**CDR (Design Review Crítica)**  
- Especificaciones técnicas **validadas** y **ICDs** firmados.  
- Convergencia de modelos (FEM/GVT) ±5% en modos 1–10 (si aplica).  
- Matriz V&V actualizada con artefactos 02→05 listos.  
- **Checklist de configuración** al día y paquete para 04-Executables.

---

## Interfaces (extracto) y ubicación de ICDs
- **IF-A-STRUCT-JOINTS** — PG ↔ RIBS/SKIN  
- **IF-A-LPS-BONDING** — PG ↔ LPS  
- **IF-C2-H2-MOUNTS** — PG ↔ Cryogenic mounts  
- **IF-P-PROP-INTEGRATION** — PG ↔ Propulsion attach

> Coloque los ICDs en `./icd/` y referéncielos desde `PRODUCT-STRUCTURE.md`.

---

## Restricciones y supuestos
- Compatibilidades y reglas globales: `OPTIM-FRAMEWORK/constraints/hard_constraints.yaml`.  
- Supuestos de materiales y uniones (MMPDS/CMH-17) y continuidad LPS (ARP5412/5416).

---

## Trazabilidad & V&V
- **REQ ↔ Evidencia:** `../01-Requirements/verification-matrix.csv` (actualice con artefactos de esta fase).  
- **Vinculación a riesgos:** THERM-001 · STR-002 · CERT-003 · OPS-004 (véase registro en O-ORGANIZATIONAL).

---

## Ledger (anclaje de evidencias de 02-Design)
Plan global de T: `T-TECHNOLOGICAL/LEDGER/cli/ledger-plan.json`  
Ejemplo (añadir al plan del PR):
```json
{
  "ci_id": "CI-CA-A-001-001",
  "utcs_phase": "02-Design",
  "artifact": {
    "path": "…/CI-CA-A-001-001-CB-PRIMARY-GRID/02-Design/PRODUCT-STRUCTURE.md",
    "sha256": "<hash>",
    "size_bytes": 0,
    "mime": "text/markdown",
    "storage_uri": "s3://…/PRODUCT-STRUCTURE.md"
  }
}
```

---

## Dependencias

* **Previas:** 01-Requirements (SRR **PASS**).
* **Recursos:** dominio A/C2/E2 disponibles para co-diseño de interfaces.
* **Stakeholders:** ARB (arquitectura) · SRB (safety) · DSC (security) para co-revisión de ICDs.

---

## Riesgos y mitigación (resumen)

* **THERM-001** — ΔT criogénicos → barreras G-10/MLI + ensayo 20k ciclos.
* **STR-002** — Fabricabilidad AFP → cupones curvas dobles + tuning layup.
* **CERT-003** — Rutas de carga poco convencionales → building-block + early authority.
* **OPS-004** — Egress 90 s → simulación + mock-ups.

---

## Registros y control

* **Change-log:** `../01-Requirements/change-log.yaml` (añada entrada si cambia rutas/artefactos).
* **Validación de fase:** usar `VALIDATION-SYSTEM.md` para checklist de PDR/CDR.

---

### Accesos directos de diseño

* **PSB / BoS** → [`PRODUCT-STRUCTURE.md`](./PRODUCT-STRUCTURE.md)
* **psb.yaml** → [`psb.yaml`](./psb.yaml)
* **BOM** → [`bom.csv`](./bom.csv)
* **ICDs** → [`./icd/README.md`](./icd/README.md)
* **Specs** → [`./specs/README.md`](./specs/README.md)
* **Models** → [`./models/README.md`](./models/README.md)