# Política de Vida Útil — O-ORGANIZATIONAL (BWB H₂)

**Ruta sugerida:** `OPTIM-FRAMEWORK/O-ORGANIZATIONAL/policies/Service-Life-Policy-BWB-H2.md`  
**Ámbito:** toda la flota BWB-H₂.  
**Objetivo:** alcanzar **45 años** de servicio con evidencia técnica y económica escalonada.

## 1. Definiciones
- **LOV**: Life Of Vehicle vigente (años). Inicial 30 a; extensiones a 35/40/45 a.  
- **Gate-M/X1/X2**: hitos de extensión (mid-life y sucesivos).  
- **MoE**: Measures of Effectiveness; **KPI**: indicadores de control.

## 2. Principios
1) Seguridad ≥ objetivos ARP4754A/4761.  
2) Economía positiva (NPV>0) por extensión.  
3) Evidencia medible (UTCS, V&V, SHM, NDT).  
4) Sustitución planificada de LRUs criogénicos/eléctricos/aviónicos.

## 3. Gobierno y RACI
| Rol | Responsabilidad |
|---|---|
| **Program Board** | Aprueba LOV, gates y presupuesto |
| **Chief Architect (DT)** | Coherencia de arquitectura y UTCS |
| **CSE** | Integridad técnica y V&V |
| **Leads ARC/CRY/ENR/PRO/ELE/INF/CTL** | Evidencias por segmento |
| **Finance Lead** | NPV/ROI/ riesgo financiero |
| **Safety Lead** | FHA/PSSA/SSA y DAL |

## 4. KPIs (mínimos por gate)
- **Safety:** Cierre de hazards Cat/Haz → **100%** mitigados.  
- **Técnicos:** SHM estable 24 mes previos; LPS bonding ≤2.5 mΩ; leak-rate H₂ ≤ umbral.  
- **Masa/CG:** Δmasa ≤ +3% vs baseline; CG en ventana ±50 mm.  
- **Disponibilidad:** ≥ 98% en 12 meses previos.  
- **NPV:** > 0 al horizonte del gate.  
- **Cert-readiness index:** ≥ 0.8.

## 5. Política de LOV y Gates
| Gate | Ventana (años EIS) | LOV objetivo | Paquetes mínimos |
|---|---|---|---|
| **Gate-M** | 12–15 | **35 a** | Refurb CRY (MLI/aislamientos), SHM baseline, upgrade DIG/ELE, LPS refresh |
| **Gate-X1** | 24–28 | **40 a** | **Re-tanques LH₂** + BoP, HV re-cableado, refuerzos locales ARC |
| **Gate-X2** | 33–36 | **45 a** | Segundo ciclo CRY, sensores H₂, adhesivos sandwich, ciber/CNS |

**Regla Go/No-Go:** si cualquier KPI clave < umbral → No-Go o extensión parcial (rutas/uso).

## 6. Criterios económicos
**NPV:** \(\sum_{t=0}^{T} \frac{CF_t}{(1+r)^t}\) − CAPEX gate − OPEX extra.  
Umbral: **NPV>0** y **Payback ≤ 8 años** para X1/X2.

## 7. Riesgos y tolerancias
- Embrittlement H₂, shock térmico, obsolescencia electrónica, infra H₂.  
- Tolerancias de decisión: una (1) desviación menor permitida por gate si NPV y safety ≥ umbral.

## 8. Artefactos requeridos (dossier de gate)
- **Plan técnico** (por segmento): objetivos, evidencias, desviaciones.  
- **V&V extract**: matriz UTCS con evidencias cerradas.  
- **Safety pack:** FHA/PSSA/SSA actualizados.  
- **Finance pack:** NPV, escenarios, sensibilidad.  
- **Operación/MRO:** planificación heavy + capacidad.  
- **Acta de decisión:** Go/No-Go y LOV resultante.

## 9. Reporting
- **Mensual:** KPIs clave y alertas SHM.  
- **Trimestral:** avance hacia próximo gate.  
- **Anual:** revisión de LOV y riesgos.

## 10. Revisión
- Vigencia: 12 meses. Próxima revisión: **P2→P3 Gate Review**.

---
*Documento generado por AMPEL360 H₂-BWB-Q Framework*  
*Estándar Universal: ARP4754A-00.00-OPTIM-O-VIDAUTIL-0001-v1.0*  
*ID: 7f3c9a2b-Diseno→Operacion*