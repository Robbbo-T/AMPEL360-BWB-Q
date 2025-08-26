# AMPEL360-H2-BWB-Q
Optimized BWB Aircraft Configuration Model. Born in Hydrogen and Quantum Simulation

```yaml
{
  "utcs_mi": {
    "version": "5.0",
    "doc_id": "UTCS-MI/CS25-H2/AMPEL360-QNNN/2025-08-26/v1.0",
    "status": "P2-Approved-Pending-QNNN"
  },
  "architecture": {
    "fuselage": 24,
    "wing": 24,
    "primary_structure": 24,
    "flight_controls": 24,
    "propulsion": 37,
    "energy": 38,
    "avionics": 1,
    "landing_gear": 1,
    "cabin": 1,
    "tail": "N/A-BWB"
  },
  "constraints_paths": {
    "hard_constraints": "constraints/hard_constraints.yaml",
    "candidates": "data/candidates.yaml",
    "feasible_set": "feasible_set.json",
    "selector": "scripts/qaoa_over_F.py"
  },
  "capacity": {
    "QNNN": null,
    "binning_range_pax": [
      150,
      220
    ],
    "objective": "E[cost] + beta * CVaR_alpha(cost)"
  },
  "corridors_seed": [
    "LHR",
    "FRA",
    "DXB",
    "SIN"
  ],
  "risk": {
    "cvar_alpha": 0.8,
    "beta": 0.25
  },
  "notes": "Tail not applicable for BWB; if geometry gates fail for TUW gear/avionics/cabin, select BWB-dedicated modules."
}
```
# Acta de Nacimiento Digital — **AMPEL360 H₂‑BWB QNNN**
**UTCS‑MI v5.0 — Documento de Decisión de Arquitectura**  
ID: UTCS‑MI/CS25‑H2/AMPEL360‑QNNN/2025-08-26/v1.0

---

## 1. Objeto
Formalizar la **decisión de arquitectura** del programa *AMPEL360 H₂‑BWB QNNN*, resultado del pipeline **feasible‑first** (MILP/CP‑SAT + QAOA sobre 𝔽) con objetivo **ecosistema** (E[coste] + β·CVaR_α).

## 2. Ámbito y contexto
- Fase de madurez: **P2 — Introduce BWB**.  
- Dataset base: **43 AMPELs** (métricas normalizadas, TRL por subsistema, geometría).  
- Corredores H₂ iniciales (ejemplo): **LHR–FRA–DXB–SIN**.
- Criterios de certificación: **CS‑25/FAR‑25** con apéndices H₂ (alineación preliminar).

## 3. Decisión de arquitectura (selección de donantes)
- **Fuselaje**: **24 — BWB**
- **Ala**: **24 — BWB** *(opcional 34 si TRL≥6 para superficies avanzadas)*
- **Estructura primaria**: **24 — BWB**
- **Sistemas de control**: **24 — BWB** (alivio de cargas + control CG por quema H₂)
- **Propulsión**: **37 — H₂ turbofan**
- **Energía / Tanques**: **38 — H₂ BWB rear‑mounted**
- **Aviónica**: **01 — TUW** (siempre que pase integración IO/buses)
- **Tren de aterrizaje**: **01 — TUW** (si encaja en bays BWB; si no, set BWB‑dedicado)
- **Cabina**: **01 — TUW** (maquetas y puertas/evac adaptadas a BWB)
- **Empenaje**: **No aplica (BWB)** — superficies integradas

> **Justificación:** volumen criogénico y L/D del BWB (24), con **módulos TUW maduros** donde la geometría lo permite, y cadena Propulsión–Energía **H₂‑H₂** (37–38) para mantener compatibilidad y riesgo controlado.

## 4. Parámetro de capacidad (QNNN)
El número **QNNN** se fija como
\[
\mathrm{QNNN} = \arg\min_N \; \mathbb{E}_s[H_s(N)] + \beta\,\mathrm{CVaR}_\alpha(H_s(N))
\]
donde **H_s** es el coste ecosistema (RD + MFG_INV + CERT_TIME·CAPITAL + INFRA + TRAIN + MAINT·FLEET·LIFE + FUEL·BLOCK_HRS·PRICE) por escenario *s*.
- **Rango de diseño inicial**: 150–220 pax (binning por módulos de cabina BWB y puertas).
- **Estado**: **TBD** → se cerrará tras ejecutar `feasible_pool.py` y el selector sobre 𝔽.

## 5. Restricciones duras aplicadas
- **TRL gates** por subsistema (P2): ala≥6, fuselaje≥6, estr. primaria≥7, propulsión≥6, energía≥6, control≥7, aviónica≥8, tren≥8, cabina≥7.
- **Compatibilidad estructural** (allowed_pairs): *(wing,fuselage) ∈ {(24,24),(34,24),(24,34)}; *(energy,fuselage) ∈ {(38,24),(38,34)}.*
- **Conflictos** (forbidden_pairs): ej. (wing=1, fuselage=24), (wing=5, energy=38).
- **Física/operación** (normalizado): Peso≤0.65; TWR≥0.55; Ruido≤0.65; Evac≤90 s.
- **Política H₂**: *energy_type(propulsión) = energy_type(energía) = 'Hydrogen'*.
- **Cap de diversidad**: ≤4 subsistemas del mismo donante.

## 6. Integración y geometría (criterios mínimos)
- Volumen criogénico **≥ demanda de ruta** y **margen CG** con secuencia de consumo.
- **Gear TUW** solo si **keel_depth** y **gear_bay_span** del BWB lo admiten; si no, gear BWB dedicado.
- **Evacuación 90 s** con puertas y pasillos BWB; si no se cumple, rediseño de layout/cabina.

## 7. Roadmap TRL y certificación (resumen)
- **P2 (este documento)**: BWB estructural + H₂ turbofan + tanques traseros + módulos TUW factibles.  
- **P3**: BLI/DP selectiva, morphing (34) si TRL≥6 y se mantiene cumplimiento OEI/runway y evac.

## 8. Riesgos principales y mitigación
- **Integración tanques‑estructura** → validación de cargas y crashworthiness (ensayos sub‑escala).  
- **Evac BWB** → simulación dinámica y mockups; redistribución de puertas si es preciso.  
- **Suministro H₂** → corredores priorizados, contratos de abastecimiento, buffer de licuefacción.

## 9. Trazabilidad y artefactos
- **Constraints**: `constraints/hard_constraints.yaml`  
- **Donantes**: `data/candidates.yaml`  
- **Feasible set**: `feasible_set.json` (post‑enumeración)  
- **Selector**: `scripts/qaoa_over_F.py` (stub CVaR; sustituible por QAOA one‑hot)

## 10. Aprobación
- **Estado**: *Aprobado para desarrollo detallado (P2)*, a reserva de cierre de **QNNN** tras la corrida completa.

---

**Firmas electrónicas**  
- Chief Architect (DT): AMEDEO PELLICCIA Fecha: 2025-08-26  
- Chief Systems Engineer: _____________________  Fecha: 2025-08-26  
- Certification Lead: _________________________  Fecha: 2025-08-26
