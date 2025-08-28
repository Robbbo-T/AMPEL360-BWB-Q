# CA: CA-MRO-SYS

## CI: DSA-ALGO-001

## UTCS Phase: 01-Requirements

**Doc ID:** REQ-DSA-001-v1.0
**Classification:** UNCLASSIFIED // FOUO
**Date:** 2025-08-28
**Status:** DRAFT (Audit-Ready)
**Owner:** Systems Engineering Team

---

## 1. Revision History

| Ver | Date       | Changes                                                                                   | Author  |
| --- | ---------- | ----------------------------------------------------------------------------------------- | ------- |
| 1.0 | 2025-08-28 | Initial requirements definition for Disassembly Sequence Algorithm; audit-ready hardening | SE Team |

---

## 2. Definitions & Acronyms

* **BOM**: Bill of Materials.
* **DET**: Digital Evidence Twin (trazabilidad inmutable).
* **Anytime**: el planificador devuelve mejor-hasta-ahora con cota del gap.
* **Optimalidad** (en este CI): mínimo de una función de coste definida (tiempo, cambios de herramienta, re-fixturing, riesgo) con tolerancia y bound explícitos.
* **No-destruct**: política que prohíbe operaciones irreversibles (corte/despegue).
* **COG/COM**: Center of Gravity/Mass.
* **UTCS-MI**: esquema de trazabilidad universal (IDs únicos para REQ→CODE→TEST→EVIDENCE).

---

## 3. Units Policy (Mandatory)

```yaml
units_policy:
  base: SI
  pressure: kPa (bar)
  temperature: °C
  force: kN
  length: mm
  time: s
  angle: degrees
```

---

## 4. Assumptions & Constraints

```yaml
assumptions:
  - A1: BOM y esquema de juntas contienen relaciones de sujeción completas (no faltan fijaciones críticas).
  - A2: Los modelos CAD proporcionan sólidos cerrados o mallas watertight para comprobaciones de colisión.
  - A3: Librería de herramientas expone alcance/volumen de trabajo/torque.
  - A4: Política de seguridad define LOTO (Lockout/Tagout) y límites de H₂/fluido.

constraints:
  - C1: Cómputo sobre HW de referencia: 8 vCPU/32 GB RAM; GPU opcional para colisiones.
  - C2: Persistencia y logs firmados bajo UTCS-MI + DET (WORM).
  - C3: Versionado inmutable de heurísticas/semillas: misma entrada + misma semilla ⇒ mismo plan.
```

---

## 5. Requirements Index (Mandatory)

> **Nota de estilo**: todas las "shall" son **medibles y testeables**; "óptimo" se reemplaza por **"mínimo de J con gap ≤ ε"**.

```yaml
# Categories: STR, MAT, IFC, THR, ENV, MFG, TST, CRT, CMP, OPS, PRF, MNT, REL, SAF, SEC, EOL, DSP
requirements_index:

  # Interface Requirements (IFC)
  REQ-IFC-001: "System shall accept BOM data in JSON/XML with hierarchical parts, joints, subassemblies; schema UTCS-BOM-1.0."
  REQ-IFC-002: "System shall interface with CAD (STEP AP242/JT or native API) to retrieve geometry and optional kinematics."
  REQ-IFC-003: "System shall provide APIs for tool & fixture libraries (reach, torque, envelopes, mounting)."
  REQ-IFC-004: "System shall export sequences in JSON (action_id, part_id, tool_id, motion_vector/path, prerequisites, safety_flags) and optional WebGL anim."

  # Computational (CMP)
  REQ-CMP-001: "System shall build assembly/precedence/occlusion graphs ≤5 s for ≤10,000 parts, ≤50,000 joints on HW ref."
  REQ-CMP-002: "System shall implement A* with pluggable heuristics and deterministic seeding."
  REQ-CMP-003: "System shall resolve cycles via minimum feedback edge set heuristic with evidence of chosen cutset."
  REQ-CMP-004: "System shall perform collision checks via swept-volume or Minkowski sum; tolerance ≤0.5 mm."
  REQ-CMP-005: "System shall maintain and version constraint graphs (precedence, occlusion, stability) per state."

  # Performance (PRF)
  REQ-PRF-001: "For 'standard assemblies' (≤3k parts, ≤15k joints), system shall return a sequence with cost J within ε=5% of best-known lower bound or ≤60 s, lo que ocurra antes."
  REQ-PRF-002: "System shall exploit parallelism: plan componentes independientes en hilos separados (≥2× speedup para ≥2 particiones)."
  REQ-PRF-003: "System shall be anytime: devolver mejor-hasta-ahora con (UB−LB)/LB ≤ 20% al timeout configurado."
  REQ-PRF-004: "System shall batch operations reduciendo cambios de herramienta ≥20% respecto a baseline greedy."

  # Operational (OPS)
  REQ-OPS-001: "System shall classify joints: reversible/conditionally reversible/irreversible con reglas configurables."
  REQ-OPS-002: "System shall enforce no-destruct policy: 0 operaciones irreversibles salvo whitelisting explícito."
  REQ-OPS-003: "System shall validate stability after each removal: COM dentro del polígono de soporte con margen ≥10 mm."
  REQ-OPS-004: "System shall track energy/fluids: estados 'energized/isolated/vented' y requisitos LOTO por acción."
  REQ-OPS-005: "System shall emit requirement pack por acción: herramienta, orientación (Rz,Ry,Rx), fixture, clearances."

  # Safety (SAF)
  REQ-SAF-001: "System shall forbid sequences que generen estados inestables (fallo de soporte o pérdida de sujeción crítica)."
  REQ-SAF-002: "System shall ensure COM ∈ soporte durante toda la secuencia (margen ≥10 mm; configurable)."
  REQ-SAF-003: "System shall flag steps que requieran desenergizar/depresurizar antes de ejecutar."
  REQ-SAF-004: "System shall identify y mantener load paths críticos (≥1 camino resistente por componente colgado)."

  # Security (SEC)
  REQ-SEC-001: "All sequence artifacts and logs shall be signed (Ed25519 or PQC profile) y sellados en DET (WORM)."
  REQ-SEC-002: "APIs shall enforce authZ mTLS; SBOM del componente SW disponible (CycloneDX/SPDX)."

  # Reliability (REL)
  REQ-REL-001: "Determinism: misma entrada + misma semilla ⇒ mismo plan, hash-stable."
  REQ-REL-002: "Failover: ante OOM/timeout, degradar a plan simbólico manteniendo invariantes SAF."

  # Maintenance (MNT)
  REQ-MNT-001: "System shall log constraint violations y resoluciones (cutsets, overrides) con UTCS-MI IDs."
  REQ-MNT-002: "System shall visualize secuencia y grafos; reproducir paso a paso y filtrar por acciones/safety flags."
  REQ-MNT-003: "System shall allow user override por acción con re-plan local y verificación SAF."
  REQ-MNT-004: "System shall maintain audit trail completo: inputs, semilla, versión heurísticas, tiempos, bounds."

  # Disposal/EOL (DSP)
  REQ-DSP-001: "System shall categorize componentes: recycle/refurbish/dispose con justificación (material/hazard)."
  REQ-DSP-002: "System shall optimize J con término de recuperación de material ponderable (α configurable)."
  REQ-DSP-003: "System shall identify materiales peligrosos (REACH/CLP) y marcar manejo especial."
```

## Document Control (Mandatory)

**Approvals:** Systems Lead: ****, Chief Systems Eng: ****, Chief Arch (DT): Amedeo Pelliccia
**Control:** Version: 1.0 • Gate: DRAFT • Distro: Engineering Team • Repo: `/requirements/01-phase/DSA-ALGO-001/`