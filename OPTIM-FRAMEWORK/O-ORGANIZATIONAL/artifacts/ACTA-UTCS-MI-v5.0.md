# ACTA-UTCS-MI v5.0 — Decisión de Arquitectura (Architecture Decision Record)

EstándarUniversal:Documento-Decisión-ARP4754A-00.00-ArchitectureDecisionRecord-0001-v1.0-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionHumana-AIR-AmedeoPelliccia-7f3c9a2b-02-Design→07-Certification-Security

**Document ID:** UTCS-MI/CS25-H2/AMPEL360-QNNN/ACTA-0001/v1.0  
**Classification:** INTERNAL  
**Programa:** Ampel Trescientos Sesenta Hidrógeno Ala Combinada Quantum (Generación Humana, Dominio AIR)  
**Effective Date:** 2025-08-28  
**Status:** **P2 — Approved (Introduce BWB)**

---

## 0) Resumen ejecutivo

Se **consolida** la configuración base para el demostrador **H₂‑BWB** con cadena **Propulsión–Energía 100% H₂** y **Quantum‑Onboard (Q‑Compute)** para optimización de misión/energía.  
La decisión queda **anclada** en el **ledger de CIs** (Fabric) y se fija como **Baseline de Arquitectura P2** para el cierre de **PDR/CDR**.

**Hitos incluidos en este ACTA**
- ✅ Congelación de Requisitos (UTCS‑01) a nivel de WBS/segmentos críticos (A, E2, P, C2, D).  
- ✅ Selección de donantes y compatibilidades (BWB+H₂).  
- ✅ Criterios de integración y geometría mínimos.  
- ✅ Plan V&V y calendario de gates UTCS (SRR → PDR → CDR → IRR/QR).  
- ✅ Referencias de **ledger** (baseline, evidencia, políticas de endoso).  

---

## 1) Alcance y contexto

- **Normativa de referencia:** CS‑25/FAR‑25 + apéndices/AMC H₂ (en preparación); ARP4754A/ARP4761; DO‑160G.  
- **Fase UTCS‑MI:** P2 (Introduce BWB).  
- **ConOps:** Corredores H₂ LHR–FRA–DXB–SIN (fase inicial).  
- **Objetivo de capacidad (QNNN):** ventana 150–220 pax (optimización por **E[coste] + β·CVaRᵅ**).  
- **Tecnologías clave:** BWB volumétrico, H₂ turbofan + **H₂ electric hybrid (HVDC)** para taxi/peak‑shave, **Quantum‑Onboard** para optimización misión/energía, y **C2‑Cryogenics** integrada.

---

## 2) Decisión de arquitectura (Baseline P2)

| Subsistema              | Donante / AMPEL | Selección | Comentario clave |
|-------------------------|------------------|-----------|------------------|
| Fuselaje / Body         | 24 — **BWB**     | ✔         | Volumen LH₂ + L/D; grid primario CB. |
| Ala                     | 24 — **BWB** (opción 34 — Morphing si TRL≥6) | ✔ | Transición outboard y control de cargas. |
| Estructura primaria     | 24 — **BWB**     | ✔         | Centro‑body grid + bulkheads + skin. |
| Flight Controls         | 24 — **BWB**     | ✔         | Control CG por consumo H₂ + alivio de cargas. |
| Propulsión              | **37 — H₂ turbofan** | ✔     | Compatibilidad con H₂; **CA‑P‑005 Electric Drive** para híbrido. |
| Energía (tanques/EM)    | **38 — H₂ BWB rear‑mounted** | ✔ | LH₂ trasero con MLI/vacío; boil‑off control. |
| Aviónica                | 01 — TUW (maduros) | ✔       | Integración IMA/AFDX; compatibilidad Q‑links. |
| Tren de aterrizaje      | 01 — TUW (o dedicado BWB si bays no admiten) | ✔ | Condicionado a **keel depth**/**bay span**. |
| Cabina                  | 01 — TUW (adaptada BWB) | ✔   | Egress 90 s; layout multi‑bubble. |
| Empenaje                | N/A — **BWB**    | ✔         | Superficies integradas; no cola clásica. |

> **Política H₂:** *energy_type(propulsión) = energy_type(energía) = "Hydrogen"*.

---

## 3) Supuestos, restricciones y compatibilidades

**TRL gates P2 (mínimos):**  
ala≥6, body≥6, estructura≥7, propulsión≥6, energía≥6, controles≥7, aviónica≥8, tren≥8, cabina≥7.

**Compatibilidades permitidas (extracto):**
- (wing, fuselage) ∈ {(24,24), (34,24), (24,34)}  
- (energy, fuselage) ∈ {(38,24), (38,34)}  

**Conflictos (no permitidos):**  
- (wing=1, fuselage=24), (wing=5, energy=38), o cualquier par que rompa integración térmica/estructural.

**Física/operación (normalizado, extracto):**  
Peso ≤ 0.65; TWR ≥ 0.55; Ruido ≤ 0.65; **Evac ≤ 90 s**.

---

## 4) Criterios de integración y geometría (mínimos)

- Volumen criogénico **≥ demanda de ruta** y margen **CG** a lo largo del consumo LH₂.  
- Tren **TUW** solo si **keel_depth**/**gear_bay_span** lo permiten; si no, gear BWB dedicado.  
- Rutas de **LPS** y **H₂** con barreras térmicas (C2‑Cryogenics) y **MLI** en penetraciones.  
- **Egress** 90 s con **multi‑bubble** y redistribución de puertas si fuese necesario.  

---

## 5) Quantum‑Onboard y enlaces (D‑Digital / E3‑Electronics)

- **D‑005 Quantum Compute (QPU Rack + Cryocoolers + Q‑timing):** alojamiento y EMC/EMI.  
- **E3‑005 Quantum Links (QKD/Photonics):** sincronización y seguridad de datos de misión.  
- **Ciberdefensa (D‑006):** IDS, cifrado, logging y hardening del dominio Q.  

---

## 6) Plan V&V (extracto audit‑ready)

| Requisito / Área     | Método           | Evidencia                      | Criterio                  |
|----------------------|------------------|--------------------------------|---------------------------|
| Estructural (2.5g/3.75g, presiones) | FEM NL + Ensayo | STR‑AN‑001/002; STR‑TST‑PP‑001 | MoS≥0 (limit), ≥0.5 (ult) |
| Aeroelastic (CS‑25.629) | GVT + Flutter  | AEL‑GVT‑001; AEL‑FLT‑001       | Sin flutter hasta 1.15·VD |
| Cryo‑thermal         | Ensayo + Térmico | THR‑TST‑CRYO‑001               | Sin grietas >2 mm (20k ciclos) |
| Interfaces LH₂       | Banco + NL‑FEA   | IFX‑TST‑MOUNT‑001; STR‑AN‑003  | Fx/Fy/Fz por rating       |
| Egress 90 s          | Sim + Mock‑up    | CAB‑EGR‑SIM‑001; CAB‑MOCK‑001  | ≤ 90 s, tasa cumplimiento |

> La matriz completa V&V está en `T‑TECHNOLOGICAL/…/ampel-config.yaml` y en `…/05-Verification-Validation/verification-matrix.csv`.

---

## 7) Riesgos críticos y mitigación (top‑5)

1. **THERM‑001 (criogénico):** Gradientes térmicos → **FEA acoplado + MLI + barreras + ensayo 20k ciclos**.  
2. **STR‑002 (fabricación AFP):** Doble curvatura grid → **tooling temprano + cupones + demostrador sub‑escala**.  
3. **CERT‑003 (caminos de carga nuevos):** Validación extensa → **building‑block + early authority engagement**.  
4. **OPS‑004 (egress BWB):** Geometría/puertas → **simulación dinámica + mockups + redistribución**.  
5. **INFRA‑005 (cadena H₂):** Licuefacción/suministro → **corredores priorizados + contratos + buffer planta**.

---

## 8) Calendario y Gates UTCS (P2 → P3)

- **SRR (cerrado):** Requisitos congelados UTCS‑01 (ledger).  
- **PDR (T+3):** Modelos FEM/CFD/ICDs completos y validados.  
- **CDR (T+7):** Diseño detallado + planes ensayo/certificación.  
- **IRR/QR (T+10/T+12):** Integración y calificación (cadenas H₂ y cryo).  
- **Entrada P3:** BLI/DP y morphing (34) si TRL ≥ 6, sin comprometer OEI/runway/egress.

> **Nota:** Fechas absolutas se mantienen en `O‑ORGANIZATIONAL/gates/` y en el **ledger**.

---

## 9) Trazabilidad criptográfica (ledger de CIs)

**Baseline de arquitectura P2 — evento de ledger**  
- **Tipo:** `BaselineFreeze` (UTCS‑02/Design)  
- **CI raíz:** `AMPEL360‑H2‑BWB‑QNNN/ampel-config.yaml`  
- **SHA‑256:** `⟦ RELLENAR_SHA256 ⟧`  
- **Event ID:** `⟦ cievt‑YYYYMMDD‑NNNNNN ⟧`  
- **Política de endoso:** `Chief Architect (DT)` **y** `Certification Lead` (2/2).  
- **Merkle root (día):** `anchors/anchor‑YYYY‑MM‑DD.json` (**public anchor:** `⟦ txid ⟧`).

> Evidencias asociadas (extracto): requirements, FEM, ICDs, cryo‑tests, safety/security cases.

---

## 10) Cambios y gobernanza

- **CR‑Series:** `CR‑2xxx` (impacto estructura/cryo), `CR‑3xxx` (propulsión/energía), `CR‑4xxx` (Q‑onboard).  
- **Aprobación:** **CCB ≥ 3/5**; actualización de baseline vía `ChangeApproval` en ledger.  
- **Comités:** ARB (arquitectura), SRB (safety), DSC (security), Program Board.

---

## 11) Declaración de cumplimiento (checklist)

- [x] UTCS‑01 **Requirements** congelado (WBS críticos A, E2, P, C2, D).  
- [x] Selección de donantes y compatibilidades (BWB/H₂).  
- [x] V&V plan (audit‑ready) y riesgos críticos con mitigación.  
- [x] Ledger: baseline + evidencias **ancladas**.  
- [ ] **PDR** preparado (modelos correlacionados ±5% GVT/FEM).  
- [ ] **CDR** preparado (diseño detallado + ensayos planificados).  

---

## 12) Firmas electrónicas

- **Chief Architect (DT):** Amedeo Pelliccia — `⟦ firma ⟧` — Fecha: 2025‑08‑28  
- **Chief Systems Engineer:** `⟦ nombre ⟧` — `⟦ firma ⟧` — Fecha: `⟦ ⟧`  
- **Certification Lead:** `⟦ nombre ⟧` — `⟦ firma ⟧` — Fecha: `⟦ ⟧`  
- **Safety Board (SRB):** `⟦ nombre ⟧` — `⟦ firma ⟧` — Fecha: `⟦ ⟧`  
- **Security Board (DSC):** `⟦ nombre ⟧` — `⟦ firma ⟧` — Fecha: `⟦ ⟧`

---

## 13) Control documental

- **Periodo de Validez (UTCS):** **02‑Design → 07‑Certification‑Security**  
- **Versionado:** v1.0 (ACTA P2). Próxima revisión en **PDR**.  
- **Distribución:** Program Board, ARB, SRB, DSC, CCB, Equipos Técnicos, Autoridades.  
- **Repositorio:** `O‑ORGANIZATIONAL/artifacts/ACTA‑UTCS‑MI‑v5.0.md`  
- **Vínculos clave:**  
  - `T‑TECHNOLOGICAL/AMEDEO‑PELLICCIA/INTEGRATED/AMPEL360‑H2‑BWB‑QNNN/ampel-config.yaml`  
  - `…/A‑ARCHITECTURE/CA‑A‑001‑CENTER‑BODY‑BOX/`  
  - `…/E2‑ENERGY/CA‑E2‑005‑HYDROGEN‑STORAGE/`  
  - `…/C2‑CRYOGENICS/`  
  - `T‑TECHNOLOGICAL/LEDGER/anchors/anchor‑YYYY‑MM‑DD.json`

---

### Anexos (índice)

1. **Matriz V&V** completa (`…/05-Verification-Validation/verification-matrix.csv`).  
2. **Plan de Ensayos Cryo‑Thermal** (`C2‑001/thermal‑validation.yaml`).  
3. **Compatibilities & Forbidden Pairs** (`constraints/hard_constraints.yaml`).  
4. **Políticas de endoso** (`T‑TECHNOLOGICAL/LEDGER/policies/endorsement.yaml`).  
5. **Actas de gates** (SRR cerrado; PDR/CDR planificados).
