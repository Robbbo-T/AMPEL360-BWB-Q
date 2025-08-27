# T-TECHNOLOGICAL — Índice Tecnológico (CA → CI)

Este directorio concentra la **T** de OPTIM: la arquitectura técnica del programa organizada por **dominios → CAs (Configuration Architectures) → CIs (Configuration Items)**.  
Las **fases UTCS (01–11)** viven **dentro de cada CI** (nombres oficiales, sin prefijo).

---

## Programa integrado (AMEDEO-PELLICCIA)
- Índice del programa: [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/)

### Dominios (abrir para ver CA → CI)
- [`A-ARCHITECTURE`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A-ARCHITECTURE/)
- [`A2-AIRPORTS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A2-AIRPORTS/)
- [`C-CONTROL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/C-CONTROL/)
- [`C2-CRYOGENICS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/C2-CRYOGENICS/)
- [`D-DIGITAL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/D-DIGITAL/)
- [`E-ENVIRONMENTAL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/E-ENVIRONMENTAL/)
- [`E2-ENERGY`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/E2-ENERGY/)
- [`E3-ELECTRONICS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/E3-ELECTRONICS/)
- [`I-INFRASTRUCTURES`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/I-INFRASTRUCTURES/)
- [`I2-INTELLIGENCE`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/I2-INTELLIGENCE/)
- [`L-LOGISTICS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/L-LOGISTICS/)
- [`L2-LINKS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/L2-LINKS/)
- [`M-MECHANICAL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/M-MECHANICAL/)
- [`O-OPERATIONS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/O-OPERATIONS/)
- [`P-PROPULSION`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/P-PROPULSION/)

> Cada **CA** lista sus **CIs**. Dentro de cada **CI** encontrarás las carpetas de fase `01-Requirements` … `11-Sustainment-Recycle`.

---

## Fases UTCS oficiales (referencia rápida)
1. 01-Requirements  
2. 02-Design  
3. 03-Building-Prototyping  
4. 04-Executables-Packages  
5. 05-Verification-Validation  
6. 06-Integration-Qualification  
7. 07-Certification-Security  
8. 08-Production-Scale  
9. 09-Ops-Services  
10. 10-MRO  
11. 11-Sustainment-Recycle

---

## Ledger (anclaje de evidencias de CIs en T)
Herramientas disponibles dentro del programa integrado:
- CLI:    [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/ci-ledger.sh`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/ci-ledger.sh)
- Watch:  [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/ledger_watch.yaml`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/ledger_watch.yaml)
- Plan:   [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/ledger-plan.json`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/ledger-plan.json)
- Schema: [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/plan.schema.json`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/plan.schema.json)
- Helper: [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/make_plan.py`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/LEDGER/cli/make_plan.py)

**Flujo mínimo**: edita artefacto del CI → genera plan → PR valida → merge ancla evidencia.

---

## Convenciones T
- Nomenclatura **canónica** para CA/CI; carpetas de fase con los **nombres UTCS oficiales**.  
- Artefactos **as-code** en su fase correspondiente.  
- Cuando cambies artefactos de un CI, actualiza el **plan del ledger** para mantener trazabilidad criptográfica dentro de **T-TECHNOLOGICAL**.
