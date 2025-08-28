# O-OPERATING_SYSTEMS

Sistemas operativos y runtimes para aeroespacio: **RTOS**, **Digital-Twin runtimes**, **OS kernels**, **HMI runtimes**, **middleware de integración**.

> CA = **Constituent Assembly** por entorno.  
> Base de enlaces:  
> `OPTIM-FRAMEWORK/T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/O-OPERATING_SYSTEMS/`

---

## CA-O-001 — COCKPIT
**Ámbito:** UIs/HMIs de cabina, front-ends NAV/COM, datalink y evidencias (DET).  
**Seguridad:** Sin control FBW/flight-laws; aviónica certificada en sus particiones.

**CIs (OS-centrados)**
- HMI Runtime —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/CI-CA-O-001-001-HMI-RUNTIME/`
- NAV/COMM Gateway —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/CI-CA-O-001-002-NAV-COMM-GATEWAY/`
- Datalink AOC/CPDLC —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/CI-CA-O-001-003-DATALINK-AOC-CPDLC/`
- FBW I/O Gateway (RO/particionado) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/CI-CA-O-001-004-FBW-IO-GATEWAY-RO/`
- EFB Apps Runtime —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/CI-CA-O-001-005-EFB-APPS-RUNTIME/`
- DET Ops Logger —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/CI-CA-O-001-006-DET-OPS-LOGGER/`
- README del CA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-001-COCKPIT/README.md`

---

## CA-O-002 — CABIN
**Ámbito:** IFE/IFC, personalización, control de cabina, privacidad/consentimiento, KPIs de servicio.  
**Seguridad:** Aislamiento duro frente a sistemas de vuelo.

**CIs (OS-centrados)**
- IFE Runtime —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/CI-CA-O-002-001-IFE-RUNTIME/`
- Personalization Profiles —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/CI-CA-O-002-002-PERSONALIZATION-PROFILES/`
- Cabin-Bus Gateway —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/CI-CA-O-002-003-CABIN-BUS-GATEWAY/`
- Privacy & Consent Engine —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/CI-CA-O-002-004-PRIVACY-CONSENT-ENGINE/`
- Content OTA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/CI-CA-O-002-005-CONTENT-OTA/`
- DET Service (Cabin) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/CI-CA-O-002-006-DET-SERVICE/`
- README del CA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-002-CABIN/README.md`

---

## CA-O-003 — CARGO
**Ámbito:** Orquestación ULD/carga, celdas ROS 2, puente SCADA/PLC, visión, evidencias de ejecución.  
**Seguridad:** Interlocks físicos / e-stop por encima del software.

**CIs (OS-centrados)**
- ROS 2 Cell Runtime —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/CI-CA-O-003-001-ROS2-CELL-RUNTIME/`
- OPC UA Bridge (SCADA/PLC) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/CI-CA-O-003-002-OPC-UA-BRIDGE/`
- Safety Interlocks Kernel —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/CI-CA-O-003-003-SAFETY-INTERLOCKS-KERNEL/`
- Vision Pipeline Runtime —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/CI-CA-O-003-004-VISION-PIPELINE-RUNTIME/`
- ULD Planner Adapter —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/CI-CA-O-003-005-ULD-PLANNER-ADAPTER/`
- DET Run Packer —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/CI-CA-O-003-006-DET-RUN-PACKER/`
- README del CA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-003-CARGO/README.md`

---

## CA-O-004 — EMERGENCY
**Ámbito:** Readiness/monitorización, drills/checklists, pasarelas RO a iluminación/EMERG, evidencias.  
**Seguridad:** Asesoría/evidencia; no modifica lógicas certificadas.

**CIs (OS-centrados)**
- Readiness Monitor —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-004-EMERGENCY/CI-CA-O-004-001-READINESS-MONITOR/`
- Drill & Checklist Runtime —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-004-EMERGENCY/CI-CA-O-004-002-DRILL-CHECKLIST-RUNTIME/`
- Emergency Lighting GW (RO) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-004-EMERGENCY/CI-CA-O-004-003-EMERG-LIGHTING-GW-RO/`
- Dispenser Status Service —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-004-EMERGENCY/CI-CA-O-004-004-DISPENSER-STATUS-SERVICE/`
- DET Event Packs —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-004-EMERGENCY/CI-CA-O-004-005-DET-EVENT-PACKS/`
- README del CA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-004-EMERGENCY/README.md`

---

## CA-O-005 — MULTI-DOMAIN-OPS
**Ámbito:** Orquestación aire/tierra, integraciones AOC/ATM/UTM, optimización de flota, cross-link.  
**Seguridad:** Fuera de caminos DAL-A; gateways particionados.

**CIs (OS-centrados)**
- AOC/ATM Gateway —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/CI-CA-O-005-001-AOC-ATM-GATEWAY/`
- SWIM/UTM Connector —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/CI-CA-O-005-002-SWIM-UTM-CONNECTOR/`
- Fleet Optimization Orchestrator (QAL offboard) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/CI-CA-O-005-003-FLEET-OPT-ORCHESTRATOR/`
- Crosslink Network Manager —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/CI-CA-O-005-004-CROSSLINK-NETWORK-MGR/`
- Policy Engine (Energy-as-Policy / RBAC) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/CI-CA-O-005-005-POLICY-ENGINE/`
- DET Fleet Repository —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/CI-CA-O-005-006-DET-FLEET-REPO/`
- README del CA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-005-MULTI-DOMAIN-OPS/README.md`

---

## CA-O-006 — AQUA-OS
**Ámbito:** **Mixed Operating System (MOS)** y tejido de integración (**AQUA-OS BRIDGE v22.0**) unificando diseño→fabricación→operación.  
**Seguridad:** El vuelo crítico permanece **clásico y particionado (DAL-A)**.

**CIs (núcleo AQUA-OS)**
- AQUA-BRIDGE-OS (control plane) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-001-AQUA-BRIDGE-OS/`
- TSN/TSP Sync —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-002-TSN-TSP-SYNC/`
- Data/Model Fabric (Twin APIs, UTCS-MI) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-003-DATA-MODEL-FABRIC/`
- Security & Provenance (DET/FAT/PQC/SBOM) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-004-SECURITY-PROVENANCE/`
- Adapters Suite —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-005-ADAPTERS-SUITE/`
- QAL (Non-RT Optimization) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-006-QAL-NONRT/`

**CIs (bridges de ciclo de vida)**
- **CAD/CAM/CAE/PLM Bridge** —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-007-CAD-CAM-CAE-PLM-BRIDGE/`
- **SCADA/ROS/NC Bridge (producción)** —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-008-SCADA-ROS-NC-BRIDGE/`
- **CaaS — Certification as a Service** —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-009-CAAS-CERTIFICATION-AS-SERVICE/`
- **MRO Bridge** —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-010-MRO-BRIDGE/`
- **EOL Bridge (End-of-Life/Disposal)** —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-011-EOL-BRIDGE/`
- **Procurement/ERP Bridge** —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-012-PROCUREMENT-ERP-BRIDGE/`
- **Legacy Systems Bridge** (ARINC 429/AFDX/Proprietary) —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/CI-CA-O-006-013-LEGACY-SYSTEMS-BRIDGE/`

- README del CA —  
  `OPTIM-FRAMEWORK/.../O-OPERATING_SYSTEMS/CA-O-006-AQUA-OS/README.md`

---

### Notas
- Puedes crear los directorios de cada CI exactamente con los nombres mostrados para que los enlaces funcionen tal cual.  
- ¿Quieres que genere **plantillas README** para cada CI (Scope • Interfaces • Seguridad • DET • KPIs)? Las dejo listas para commit.

- **Computación Circular Multi-Física (CCMF)** - The computational paradigm for continuous optimization
- **GAIA AIR-RTOS** - Real-time operating system kernel with DAL-A certification framework
