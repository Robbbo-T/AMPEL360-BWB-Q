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

## Evidencias (índices navegables)
- **Analysis** → [`./evidence/analysis/`](./evidence/analysis/)
- **Calculations** → [`./evidence/calculations/`](./evidence/calculations/) *(XLSX)*
- **Compliance** → [`./evidence/compliance/`](./evidence/compliance/)
- **Test** → [`./evidence/test/`](./evidence/test/)
- **Inspection** → [`./evidence/inspection/`](./evidence/inspection/)
- **Archivo histórico (opcional)** → [`./evidence/_archive/`](./evidence/_archive/)

> Mantén **una sola copia** de cada artefacto. Si conservas PDFs, déjalos en `_archive/` y usa `.md` como documento vivo.

---

## Rail de fases (en este CI)
Siguiente → [`../02-Design/`](../02-Design/) · [`../03-Building-Prototyping/`](../03-Building-Prototyping/) · [`../04-Executables-Packages/`](../04-Executables-Packages/) · [`../05-Verification-Validation/`](../05-Verification-Validation/) · [`../06-Integration-Qualification/`](../06-Integration-Qualification/) · [`../07-Certification-Security/`](../07-Certification-Security/) · [`../08-Production-Scale/`](../08-Production-Scale/) · [`../09-Ops-Services/`](../09-Ops-Services/) · [`../10-MRO/`](../10-MRO/) · [`../11-Sustainment-Recycle/`](../11-Sustainment-Recycle/)

---

### 2) `evidence/analysis/README.md`


# Evidence · Analysis (CB-PRIMARY-GRID)

Documentos `.md` navegables (cada uno con metadatos, trazas y enlaces a cálculo/ensayo).

- [`EMC-AN-001.md`](./EMC-AN-001.md) — Lightning Return Path Isolation Analysis
- [`FDT-AN-001.md`](./FDT-AN-001.md) — Fatigue Damage Tolerance (overview)
- [`STR-AN-001.md`](./STR-AN-001.md) — Structural Analysis I
- [`STR-AN-002.md`](./STR-AN-002.md) — Structural Analysis II
- [`STR-AN-003.md`](./STR-AN-003.md) — Structural Analysis III
- [`STR-AN-003_Loads-Analysis.md`](./STR-AN-003_Loads-Analysis.md)
- [`STR-AN-005_Damage-Tolerance.md`](./STR-AN-005_Damage-Tolerance.md)
- [`STR-AN-005b_Crack-Analysis.md`](./STR-AN-005b_Crack-Analysis.md)
- [`THR-AN-003_Thermal-FEM.md`](./THR-AN-003_Thermal-FEM.md)
- [`OPS-AN-001_Fatigue-Analysis.md`](./OPS-AN-001_Fatigue-Analysis.md)
- [`PRF-AN-001_Weight-Analysis.md`](./PRF-AN-001_Weight-Analysis.md)
- [`PRF-AN-002_CG-Analysis.md`](./PRF-AN-002_CG-Analysis.md)
- [`REL-AN-001_MTBF-Analysis.md`](./REL-AN-001_MTBF-Analysis.md)
- [`REL-AN-002_FMEA-Analysis.md`](./REL-AN-002_FMEA-Analysis.md)
- [`REL-AN-003_Statistical-Analysis.md`](./REL-AN-003_Statistical-Analysis.md)
- [`SAF-AN-001_FTA-Analysis.md`](./SAF-AN-001_FTA-Analysis.md)
- [`SAF-AN-002_Safe-Life-Analysis.md`](./SAF-AN-002_Safe-Life-Analysis.md)
- [`SEC-AN-003_Cyber-Analysis.md`](./SEC-AN-003_Cyber-Analysis.md)
- [`TST-AN-002_POD-Analysis.md`](./TST-AN-002_POD-Analysis.md)

> **Plantilla**: usa [`../_template.md`](../_template.md) para crear cada `.md` y enlaza cálculos/ensayos asociados.


---

### 3) `evidence/compliance/README.md`

# Evidence · Compliance (CB-PRIMARY-GRID)

- [`LOAD-341-VC-VD.md`](./LOAD-341-VC-VD.md)
- [`CRT-AN-001_Compliance-Analysis.md`](./CRT-AN-001_Compliance-Analysis.md)
- [`CRT-AN-002_Special-Conditions.md`](./CRT-AN-002_Special-Conditions.md)
- [`CRT-DEM-003_Concurrent-Validation.md`](./CRT-DEM-003_Concurrent-Validation.md)
- [`MAT-ALW-CRYO-001.md`](./MAT-ALW-CRYO-001.md)
- [`MAT-INS-003_QA-Traceability.md`](./MAT-INS-003_QA-Traceability.md)
- [`ENV-AN-003_Current-Analysis.md`](./ENV-AN-003_Current-Analysis.md)


---

### 4) `evidence/test/README.md`

# Evidence · Test (CB-PRIMARY-GRID)

- [`AEL-FLT-001.md`](./AEL-FLT-001.md) — Flight flutter test (plan/result)
- [`AEL-GVT-001.md`](./AEL-GVT-001.md) — Ground Vibration Test
- [`PRF-TST-003_Modal-Test.md`](./PRF-TST-003_Modal-Test.md)
- [`STR-TST-004_GVT-Flutter.md`](./STR-TST-004_GVT-Flutter.md)
- [`IFX-TST-MOUNT-001.md`](./IFX-TST-MOUNT-001.md)
- [`LPS-TST-001.md`](./LPS-TST-001.md)
- [`EMC-TST-001.md`](./EMC-TST-001.md)
- [`ENV-TST-001_Lightning-Protection.md`](./ENV-TST-001_Lightning-Protection.md)
- [`ENV-TST-002_Resistance-Test.md`](./ENV-TST-002_Resistance-Test.md)
- [`ENV-TST-004_Salt-Spray.md`](./ENV-TST-004_Salt-Spray.md)
- [`THR-TST-CRYO-001.md`](./THR-TST-CRYO-001.md)
- [`THR-TST-HFX-001.md`](./THR-TST-HFX-001.md)
- [`MFG-TST-003_Metrology-Test.md`](./MFG-TST-003_Metrology-Test.md)
- [`MNT-TST-003_Repair-Test.md`](./MNT-TST-003_Repair-Test.md)
- [`OPS-TST-003_Climate-Test.md`](./OPS-TST-003_Climate-Test.md)


---

### 5) `evidence/inspection/README.md`

# Evidence · Inspection (CB-PRIMARY-GRID)

- [`MFG-INS-002_Access-Inspection.md`](./MFG-INS-002_Access-Inspection.md)
- [`MNT-INS-002_Borescope-Access.md`](./MNT-INS-002_Borescope-Access.md)
- [`IFC-AN-004_Tolerance-Analysis.md`](./IFC-AN-004_Tolerance-Analysis.md)
- [`IFC-DWG-003_Interface-Drawing.md`](./IFC-DWG-003_Interface-Drawing.md)
- [`IFC-TST-001_Heat-Flux.md`](./IFC-TST-001_Heat-Flux.md)
- [`IFC-TST-002_Load-Test.md`](./IFC-TST-002_Load-Test.md)


---

### 6) `evidence/_template.md` (plantilla para cada informe)


# <DOC_ID>: <Título corto>
## CI-CA-A-001-001 — CB-PRIMARY-GRID

EstándarUniversal:Documento-<Tipo>-<Regulación>-00.00-<NombreCamelCase>-<Secuencia>-<Versión>-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionHumana-AIR-AmedeoPelliccia-<hash>-<UTCSDesde>→<UTCSHasta>

---

### Document Control
| Field | Value |
|---|---|
| **Document ID** | <DOC_ID> |
| **Type** | Analysis/Test/Compliance/Inspection |
| **UTCS Phase** | 01-Requirements |
| **CI** | CI-CA-A-001-001-CB-PRIMARY-GRID |
| **Standards** | <normas> |
| **Version** | v1.0 |
| **Date** | YYYY-MM-DD |
| **Author/Reviewer/Approver** | … |

---

## 1. Summary
Breve resumen del objetivo y resultado.

## 2. Method / Setup
Método, herramientas, condiciones.

## 3. Results
Resultados clave, tablas/gráficas (si procede).

## 4. Compliance Mapping
- REQ-… ↔ Evidencia (este doc)
- Norma → párrafo

## 5. Links
- Cálculos → `../calculations/STR-CALC-001.xlsx`
- Historial (PDF, opcional) → `../_archive/<DOC_ID>.pdf`
