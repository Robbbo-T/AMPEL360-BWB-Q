# T-TECHNOLOGICAL — Índice Tecnológico (CA → CI)

Este directorio concentra la **T** de OPTIM: arquitectura técnica organizada por **dominios → CAs (Configuration Architectures) → CIs (Configuration Items)**.  
Las **fases UTCS (01–11)** viven **dentro de cada CI** (nombres oficiales, sin prefijo).

---

## Programa integrado (AMEDEO-PELLICCIA)
- Índice: [`./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/)

### Dominios (abrir para navegar CA → CI)
- [`A-ARCHITECTURE`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A-ARCHITECTURE/) ·
  [`A2-AIRPORTS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A2-AIRPORTS/) ·
  [`C-CONTROL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/C-CONTROL/) ·
  [`C2-CRYOGENICS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/C2-CRYOGENICS/) ·
  [`D-DIGITAL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/D-DIGITAL/) ·
  [`E-ENVIRONMENTAL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/E-ENVIRONMENTAL/) ·
  [`E2-ENERGY`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/E2-ENERGY/) ·
  [`E3-ELECTRONICS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/E3-ELECTRONICS/) ·
  [`I-INFRASTRUCTURES`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/I-INFRASTRUCTURES/) ·
  [`I2-INTELLIGENCE`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/I2-INTELLIGENCE/) ·
  [`L-LOGISTICS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/L-LOGISTICS/) ·
  [`L2-LINKS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/L2-LINKS/) ·
  [`M-MECHANICAL`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/M-MECHANICAL/) ·
  [`O-OPERATING_SYSTEMS`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/O-OPERATING_SYSTEMS/) ·
  [`P-PROPULSION`](./AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/P-PROPULSION/)

> Cada **CA** lista sus **CIs**. Dentro de cada **CI** encontrarás las carpetas `01-Requirements` … `11-Sustainment-Recycle`.

---

## Fases UTCS (referencia rápida)
1. 01-Requirements · 2. 02-Design · 3. 03-Building-Prototyping · 4. 04-Executables-Packages ·  
5. 05-Verification-Validation · 6. 06-Integration-Qualification · 7. 07-Certification-Security ·  
8. 08-Production-Scale · 9. 09-Ops-Services · 10. 10-MRO · 11. 11-Sustainment-Recycle

---

## 🔗 Blockchain / CI-Ledger (GLOBAL en T — **fuera de `INTEGRATED`**)

El **ledger de CIs** es **transversal** a todos los programas bajo T y vive en `T-TECHNOLOGICAL/LEDGER/`.

### Tooling
- CLI:    [`./LEDGER/cli/ci-ledger.sh`](./LEDGER/cli/ci-ledger.sh)  
- Watch:  [`./LEDGER/cli/ledger_watch.yaml`](./LEDGER/cli/ledger_watch.yaml)  
- Plan (por PR): [`./LEDGER/cli/ledger-plan.json`](./LEDGER/cli/ledger-plan.json)  
- Schema plan: [`./LEDGER/cli/plan.schema.json`](./LEDGER/cli/plan.schema.json)  
- Helper: [`./LEDGER/cli/make_plan.py`](./LEDGER/cli/make_plan.py)  
- Schema evento CI: [`./LEDGER/schemas/ci-event.schema.json`](./LEDGER/schemas/ci-event.schema.json)  
- Reconciliación: [`./LEDGER/reconciliation/reconcile.py`](./LEDGER/reconciliation/reconcile.py)  
- Políticas: [`./LEDGER/policies/endorsement.yaml`](./LEDGER/policies/endorsement.yaml) · [`./LEDGER/policies/access-control.yaml`](./LEDGER/policies/access-control.yaml)  
- Anclajes Merkle: [`./LEDGER/anchors/`](./LEDGER/anchors/)

### Eventos
`EvidenceLink`, `BaselineFreeze`, `GateDecision`, `ChangeRequest`, `ChangeApproval`,  
`InterfaceUpdate`, `RiskUpdate`, `WaiverGrant`, `ObsoleteMarked`.

### Flujo mínimo
1) Edita un artefacto de un CI (p. ej. `…/CI-…/01-Requirements/requirements.yaml`).  
2) Genera plan (desde **T-TECHNOLOGICAL**):
```bash
python LEDGER/cli/make_plan.py <ruta1> <ruta2> ...
````

3. PR → CI valida **schema + SHA-256 + cobertura**.
4. Tras el merge:

```bash
LEDGER/cli/ci-ledger.sh linkEvidence <CI_ID> <UTCS_PHASE> <artifact-json>
# opcional:
LEDGER/cli/ci-ledger.sh freezeBaseline <CI_ID> <UTCS_PHASE>
```

**Ejemplo `artifact-json`:**

```json
{
  "path": "AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A-ARCHITECTURE/CA-A-001-CENTER-BODY-BOX/CI-CA-A-001-001-CB-PRIMARY-GRID/01-Requirements/requirements.yaml",
  "sha256": "<hash>",
  "size_bytes": 24567,
  "mime": "text/yaml",
  "storage_uri": "s3://ampel360/…/requirements.yaml"
}
```

**Política de anclaje:** Merkle root **diario** (interno) · anclaje **público trimestral** (txid referenciado).
**SLOs Fabric:** ≥100 tx/s (write) · **p99** query < 500 ms · ABAC por rol (ARB/SRB/DSC/CCB).

---

## Convenciones T

* Nombres **canónicos** para CA/CI; carpetas de fase con los **nombres UTCS oficiales**.
* Artefactos **as-code** (YAML/JSON/PDF/XLSX) en la fase correcta.
* Cuando cambies artefactos de un CI, **actualiza `LEDGER/cli/ledger-plan.json`** para trazabilidad criptográfica.

```


