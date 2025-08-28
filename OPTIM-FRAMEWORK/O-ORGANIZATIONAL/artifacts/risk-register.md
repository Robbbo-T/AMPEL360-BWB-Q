# Risk Register

---

### Resumen (Summary)

| Métrica          | Valor |
| ---------------- | ----: |
| Open Risks       |     3 |
| Monitoring Risks |     2 |
| Closed Risks     |     0 |
| Red (Inherent)   |     1 |
| Amber (Inherent) |     4 |
| Green (Inherent) |     0 |

---

### Registro de Riesgos (Risks)

> EMV calculado con mapa Prob(1..5) → {0.05, 0.15, 0.30, 0.55, 0.85}

| Risk_ID   | Título                                    | Categoría   | Dominio          | UTCS_Fases                                           | Gates      | Owner                  | Status     | Prob | Impact | Inherent_Score | RAG   | ImpactCost_kEUR | EMV_kEUR | Resid_Prob | Resid_Impact | Resid_Score | Resid_RAG | KRI                                         | Due_Date   |
|-----------|-------------------------------------------|-------------|------------------|-----------------------------------------------------|------------|------------------------|------------|------|--------|----------------|-------|-----------------|----------|------------|--------------|-------------|-----------|----------------------------------------------|------------|
| THERM-001 | Gradientes térmicos en mounts LH₂         | Cryogenics  | C2-CRYOGENICS    | 02-Design,06-Integration-Qualification              | PDR,QR    | Chief Systems Engineer | Open       | 4    | 4      | 16             | Red   | 2000            | **1100** | 3          | 3            | 9           | Amber     | ΔT criogénico supera límites en transitorios | 2026-01-31 |
| STR-002   | Fabricabilidad AFP (doble curvatura)      | Architecture| A-ARCHITECTURE   | 02-Design,03-Building-Prototyping                   | PDR,CDR   | Chief Architect (DT)   | Open       | 3    | 4      | 12             | Amber | 1500            | **450**  | 2          | 3            | 6           | Green     | Defectos de colocación/porosidad             | 2025-12-15 |
| CERT-003  | Validación caminos de carga no convencionales | Compliance | A-ARCHITECTURE   | 05-Verification-Validation,07-Certification-Security | CDR,CR,ASR| Certification Lead     | Monitoring | 2    | 5      | 10             | Amber | 3000            | **450**  | 2          | 4            | 8           | Amber     | Evidencia adicional requerida por autoridad   | 2026-06-30 |
| OPS-004   | Evacuación 90 s (multi-bubble)            | Safety      | O-OPERATING_SYSTEMS     | 05-Verification-Validation,07-Certification-Security | CDR,CR,ASR| Program Manager        | Open       | 3    | 4      | 12             | Amber | 1200            | **360**  | 2          | 3            | 6           | Green     | Embudos en nuevas geometrías de pasillo      | 2026-03-31 |
| INFRA-005 | Cadena H₂ licuefacción/suministro         | SupplyChain | I-INFRASTRUCTURES| 08-Production-Scale,09-Ops-Services                 | ORR        | Program Board          | Monitoring | 3    | 3      | 9              | Amber | 2500            | **750**  | 2          | 2            | 4           | Green     | Dependencia de plantas/regulación            | 2026-09-30 |

---

### Acciones de Mitigación (Mitigations)

| Risk\_ID  | Action\_ID | Acción                                     | Owner                  | Due\_Date  | Status      | Effectiveness (0–1) | Residual\_P | Residual\_I | Notas                      |
| --------- | ---------- | ------------------------------------------ | ---------------------- | ---------- | ----------- | ------------------: | ----------: | ----------: | -------------------------- |
| THERM-001 | ACT-1001   | Barrera G-10 + MLI; ensayo 20k ciclos      | Chief Systems Engineer | 2026-01-15 | In progress |                 0.6 |           3 |           3 | Reduce ΔT transitorio      |
| STR-002   | ACT-1002   | Cupones AFP doble curvatura + tuning layup | Chief Architect (DT)   | 2025-11-15 | Planned     |                 0.5 |           2 |           3 | Reducir defectos/porosidad |

---

### Indicadores Clave de Riesgo (KRIs)

| KRI\_ID | Nombre               | Definición                                                | Owner                | Unidad | Frecuencia |
| ------- | -------------------- | --------------------------------------------------------- | -------------------- | ------ | ---------- |
| KRI-001 | TRL burndown         | Δ entre TRL objetivo y actual por dominio                 | Program Manager      | level  | monthly    |
| KRI-002 | Cert readiness index | % evidencias aceptadas vs requeridas por gate             | Certification Lead   | %      | per gate   |
| KRI-003 | CVaR tail cost       | Coste esperado en cola (α=0.95) del portafolio de riesgos | CRO                  | kEUR   | weekly     |
| KRI-004 | Defect escape rate   | Defectos que superan V\&V por 1000 artefactos             | QA Lead              | ppm    | weekly     |
| KRI-005 | Feasible set size    |                                                           | Chief Architect (DT) | count  | per run    |

---

### Heatmap (conteos por **Impact** × **Prob**; excluye solo *Closed*)

| Impact \ Prob |  1 |  2 |  3 |  4 |  5 |
| ------------: | -: | -: | -: | -: | -: |
|             1 |  0 |  0 |  0 |  0 |  0 |
|             2 |  0 |  0 |  0 |  0 |  0 |
|             3 |  0 |  0 |  1 |  2 |  0 |
|             4 |  0 |  0 |  0 |  1 |  0 |
|             5 |  0 |  1 |  0 |  0 |  0 |

---

### CVaR (α = 0.95) — Portafolio de Riesgos

*(Monte Carlo 10k+ tiradas; mapping Prob: 1→0.05, 2→0.15, 3→0.30, 4→0.55, 5→0.85)*

| Alpha | Trials | VaR\_kEUR | CVaR\_kEUR | Mean\_kEUR | Std\_kEUR | Max\_kEUR |
| ----: | -----: | --------: | ---------: | ---------: | --------: | --------: |
|  0.95 | 200000 |  **6700** | **7746.6** |     3109.7 |   2057.45 |     10200 |

**Entradas usadas (riesgos incluidos en la simulación):**

| Risk\_ID  | Título                            | Prob (p) | ImpactCost\_kEUR |
| --------- | --------------------------------- | -------: | ---------------: |
| THERM-001 | Gradientes térmicos en mounts LH₂ |     0.55 |             2000 |
| STR-002   | Fabricabilidad AFP                |     0.30 |             1500 |
| CERT-003  | Validación caminos de carga       |     0.15 |             3000 |
| OPS-004   | Evacuación 90 s                   |     0.30 |             1200 |
| INFRA-005 | Cadena H₂ licuefacción            |     0.30 |             2500 |

---

