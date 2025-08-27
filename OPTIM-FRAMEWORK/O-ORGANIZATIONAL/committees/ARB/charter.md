# Architecture Review Board Charter

EstándarUniversal:Documento-Gobernanza-ARP4754A-00.00-ArchitectureReviewBoardCharter-0001-v1.1-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionHumana-CROSS-AmedeoPelliccia-7f3c9a2b-RestoDeVidaUtil

---

## Document Control

| Field | Value |
|---|---|
| **Document ID** | AMPEL360-ARB-CHARTER-v1.1 |
| **Classification** | INTERNAL |
| **Effective Date** | 2025-08-26 |
| **Status** | Active |
| **Owner** | Program Board |
| **Secretariat** | Architecture PMO |
| **Supersedes** | AMPEL360-ARB-CHARTER-v1.0 |
| **Distribution** | ARB, SRB, DSC, CCB, Program Board |

---

## 1. Purpose
Provide authoritative governance for **technical architecture decisions and reviews** across the AMPEL360 program, ensuring compliance with **ARP4754A/ARP4761** and UTCS phases (01–11).

## 2. Scope
The ARB is responsible for:
- Defining and approving **Architecture Baselines** (CA/CI level).
- Approving **interface contracts** (ICDs) and cross-domain integration patterns.
- Selecting **core technologies** (compute, networks, cryogenics integration) and enforcing deprecation paths.
- Managing **architecture waivers/deviations** and **risk acceptances** tied to design choices.
- Ensuring traceability of **requirements → design → verification** and alignment with **UTCS gates** (SRR, PDR, CDR, IRR/QR).

## 3. Authority & Decision Rights
- **Decide** on CA/CI architecture, interface schemas, and baseline freezes (UTCS-02 Design).
- **Recommend** gate outcomes to Program Board; **co-sign** with SRB/DSC where safety/security are impacted.
- **Escalate** unresolved issues to Program Board.
- **Request** resources and independent reviews as needed.

## 4. Membership
- **Chair (voting):** Chief Architect (DT)  
- **Vice Chair (voting):** Chief Systems Engineer  
- **Secretary (non-voting):** Architecture PMO  
- **Voting members:** Domain Leads — A-ARCHITECTURE, C2-CRYOGENICS, E2-ENERGY, P-PROPULSION, D-DIGITAL, E3-ELECTRONICS  
- **Advisors (non-voting):** Certification Lead, SRB rep, DSC rep, Program Manager

**Quorum:** ≥ **2/3** of voting members.  
**Voting:** Simple majority for standard ADRs; **2/3** required for **BaselineFreeze** or **Waiver** with cross-domain impact.  
**Tie-break:** Chair; if conflict of interest, Vice Chair.

**Conflict of Interest:** Members must declare conflicts; conflicted members abstain from discussion and vote.

## 5. Meetings
- **Cadence:** Bi-weekly (standing), ad-hoc for critical gates.  
- **Agenda & Materials:** Circulated ≥ 48 h before meeting.  
- **Minutes:** Issued within 48 h; decisions recorded as **ADR** items and anchored to the CI ledger.

Refs: see `members.yaml` for current roster and `schedule-2025.yaml` for calendar.

## 6. Processes

### 6.1 Intake
1. Submit **ADR proposal** (one-pager + evidence links).
2. Secretariat triages; assigns reviewers; schedules ARB slot.

### 6.2 Review flow (SLA)
- Triage ≤ 2 working days → Review ≤ 10 days → Decision publication ≤ 2 days.

### 6.3 Decision classes
- **ArchitectureBaseline** (BaselineFreeze @ UTCS-02).  
- **InterfaceContract** (ICD update; InterfaceUpdate event).  
- **TechnologySelection** (approved stacks/patterns).  
- **Waiver/Deviation** (time-boxed; includes exit criteria).  
- **RiskAcceptance** (document residuals + mitigation).

### 6.4 Outputs
- **ADR record** (see template below).  
- **Ledger event**: `BaselineFreeze | InterfaceUpdate | ChangeApproval | GateDecision`.  
- **Updates** to constraints (`constraints/hard_constraints.yaml`) when applicable.

#### ADR Template (minimal)
```yaml
adr_id: ADR-YYYY-NNN
title: <short decision title>
category: <ArchitectureBaseline|InterfaceContract|TechnologySelection|Waiver|RiskAcceptance>
utcs:
  phases: ["02-Design","07-Certification-Security"]
  gates: ["PDR","CDR"]
decision: <concise statement>
rationale: <why; alternatives considered>
consequences:
  positive: []
  negative: []
evidence:
  - path: <repo-path-or-uri>
    sha256: <hash>
ledger:
  event_kind: <BaselineFreeze|InterfaceUpdate|ChangeApproval|GateDecision>
  endorsement_policy: "Chief Architect (DT) AND Certification Lead"
signoff:
  approvals:
    - role: Chief Architect (DT)
    - role: Certification Lead
````

## 7. Interfaces with Other Bodies

* **SRB (Safety):** Co-approval for safety-relevant architecture; alignment to ARP4761 artifacts.
* **DSC (Security):** Co-approval for security-relevant architecture; cyber cases and SBOM attestation.
* **CCB (Change Control):** Implements approved changes; maintains CR lifecycle.

## 8. Metrics & KRIs

* **ADR lead time** (median days)
* **% ADRs with complete evidence at submission**
* **Rework rate** (ADRs requiring re-review)
* **Gate schedule adherence** (PDR/CDR on-time)

## 9. Records & Traceability

* **Repository paths:**

  * `O-ORGANIZATIONAL/governance/committees/ARB/`
  * `O-ORGANIZATIONAL/artifacts/decision-log.yaml` (master index)
* **Ledger anchoring:** Daily internal Merkle; quarterly public anchor (txid referenced).

## 10. Amendments

Charter reviewed annually or upon Program Board request. Amendments require **2/3** ARB approval and Program Board ratification.

---

*Charter effective date: 2025-08-26*
*Document ID: AMPEL360-ARB-CHARTER-v1.1*

```

