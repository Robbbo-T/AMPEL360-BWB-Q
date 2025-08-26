# 01-Requirements - CI-CA-A-001-001-CB-PRIMARY-GRID (v1.4 DRAFT)

EstándarUniversal:Documento-Diseno-ARP4754A-00.00-AMPEL360-REQ-CB-PG-001-0001-v1.4-OPTIM-as-DT-GeneracionHumana-AIR-AmedeoPelliccia-8a4d5c3f-Diseno→Operacion

## CA: CA-A-001-CENTER-BODY-BOX
## CI: CI-CA-A-001-001-CB-PRIMARY-GRID  
## UTCS Phase: 01-Requirements
**Doc ID:** AMPEL360-REQ-CB-PG-001-v1.4
**Classification:** UNCLASSIFIED // FOUO
**Date:** 2025-08-26
**Status:** DRAFT
**Owner:** Amedeo Pelliccia

### Revision History
| Ver | Date | Changes | Author |
|-----|------|---------|--------|
| 1.0 | 2025-08-20 | Initial Release | AMPEL360 Team |
| 1.1 | 2025-08-22 | Addressed initial review comments | AMPEL360 Team |
| 1.2 | 2025-08-24 | Audit-ready compliance updates | AMPEL360 Team |
| 1.3 | 2025-08-25 | Final RFA resolution | AMPEL360 Team |
| 1.4 | 2025-08-26 | Enhanced traceability and verification matrix | Robbbo-T |

### 3. UNITS POLICY (MANDATORY)
```yaml
units_policy: { base: SI, pressure: kPa (bar), temperature: °C, force: kN, length: mm }
```

### 4. REQUIREMENTS INDEX (MANDATORY)
```yaml
requirements_index:
  # Structural Requirements (STR)
  REQ-STR-001: "Primary grid shall sustain limit load 2.5g and ultimate 3.75g without failure"
  REQ-STR-002: "Primary grid shall withstand proof pressure 89 kPa (12.9 psi), ultimate 118.6 kPa (17.2 psi)"
  REQ-STR-003: "Primary grid shall meet CS-25.341 discrete gust (VB/VC/VD) per Ude; alleviation factors documented"
  REQ-STR-004: "Primary grid shall have no flutter/LCO up to 1.15·VD and modal margin ≥15% to critical pair — CS-25.629"
  REQ-STR-005: "Primary grid shall meet two-bay crack capacity ≥ limit load; discrete source 1/3 bay — CS-25.571"
  REQ-STR-005a: "Composite shall demonstrate BVID residual strength ≥ limit load post 35 J impact, including cryo-conditioning"
  REQ-STR-005b: "Metallic paths shall meet fail-safe/durability with two-bay crack or equivalent redundancy"
  
  # Thermal Requirements (THR)
  REQ-THR-001: "Primary grid shall withstand cryogenic thermal gradient without cracks >2mm after 20,000 cycles"
  REQ-THR-002: "Primary grid shall maintain structural integrity during rapid temperature change from +20°C to -253°C in 30 minutes"
  
  # Interface Requirements (IFC)
  REQ-IFC-001: "LH2 interface shall maintain: heat flux ≤ 5 W/m²; Tmax_grid_mount ≤ −50°C; k_isolator < 0.5 W/m·K"
  REQ-IFC-002: "H2 mounts shall support capacity per point (X/Y/Z) with factors 1.0 (limit) / 1.5 (ultimate)"
  REQ-IFC-003: "Grid shall provide standardized interfaces for system routing (electrical, hydraulic, fuel)"
  
  # Material Requirements (MAT)
  REQ-MAT-001: "Materials and processes shall be approved with A-/B-basis; properties at −253°C qualified"
  REQ-MAT-002: "All materials in H2 contact zones shall meet ISO 11114-4 hydrogen compatibility requirements"
  
  # Environmental Requirements (ENV)
  REQ-ENV-001: "Primary grid shall provide LPS on composite surfaces per DO-160 §22 Cat A3/E3"
  REQ-ENV-002: "Primary grid shall implement z-bond network with joint resistance ≤ 2.5 mΩ (panels), ≤ 10 mΩ (access covers)"
  REQ-ENV-003: "Primary grid shall define controlled lightning return path isolated from LH2 volumes"
  
  # Manufacturing Requirements (MFG)
  REQ-MFG-001: "Primary grid shall be manufacturable using AFP process with autoclave cure"
  REQ-MFG-002: "All joints shall be accessible for assembly and inspection"
  
  # Test Requirements (TST)
  REQ-TST-001: "Primary grid shall demonstrate compliance through component and full-scale testing"
  REQ-TST-002: "NDI methods shall achieve POD of 90% at 95% confidence for critical defects"
  
  # Certification Requirements (CRT)
  REQ-CRT-001: "Primary grid shall comply with CS-25 Amendment 27 structural requirements"
  REQ-CRT-002: "Primary grid shall meet special conditions for BWB configuration and H2 compatibility"
  
  # Operational Requirements (OPS)
  REQ-OPS-001: "Primary grid shall support 20,000 flight cycles without major maintenance"
  REQ-OPS-002: "Primary grid shall enable access for inspection within 30 minutes"
  
  # Performance Requirements (PRF)
  REQ-PRF-001: "Primary grid weight shall not exceed 4,200 kg (+5%/-2% tolerance)"
  REQ-PRF-002: "Primary grid shall maintain CG within 35% MAC ± 2%"
  
  # Maintenance Requirements (MNT)
  REQ-MNT-001: "Primary grid shall support on-condition maintenance with 5,000 FH inspection intervals"
  REQ-MNT-002: "Critical areas shall be accessible for borescope inspection"
  
  # Reliability Requirements (REL)
  REQ-REL-001: "Primary grid shall achieve MTBF > 100,000 flight hours"
  REQ-REL-002: "Primary grid shall have no single point failures affecting safety"
  
  # Safety Requirements (SAF)
  REQ-SAF-001: "Primary grid failure shall not result in catastrophic event (10^-9 per FH)"
  REQ-SAF-002: "Primary grid shall maintain safe-life design for critical elements"
  
  # Security Requirements (SEC)
  REQ-SEC-001: "Primary grid design data shall be ITAR controlled"
  REQ-SEC-002: "Primary grid shall include tamper-evident features at access points"
  
  # End-of-Life Requirements (EOL)
  REQ-EOL-001: "Primary grid shall be 85% recyclable by weight"
  REQ-EOL-002: "Primary grid shall enable safe disposal of H2-exposed materials"
```

### 5. STANDARDS MAPPING (MANDATORY)
```yaml
standards_mapping:
  CS-25.301: [REQ-STR-001, REQ-STR-002]
  CS-25.305: [REQ-STR-001]
  CS-25.307: [REQ-STR-002]
  CS-25.341: [REQ-STR-003]
  CS-25.365: [REQ-STR-002]
  CS-25.571: [REQ-STR-005, REQ-STR-005a, REQ-STR-005b]
  CS-25.603: [REQ-MAT-001, REQ-MAT-002]
  CS-25.605: [REQ-MFG-001, REQ-MFG-002]
  CS-25.613: [REQ-MAT-001]
  CS-25.629: [REQ-STR-004]
  DO-160G: 
    - Section 4: [REQ-ENV-001]
    - Section 5: [REQ-ENV-001]
    - Section 22: [REQ-ENV-001, REQ-ENV-002, REQ-ENV-003]
  ISO-11114-4: [REQ-MAT-002]
  ISO-19880: [REQ-IFC-001, REQ-IFC-002]
  SAE-AIR6464: [REQ-IFC-001, REQ-IFC-002]
  SAE-ARP5412: [REQ-ENV-001]
  SAE-ARP5414: [REQ-ENV-001]
  SAE-ARP5416: [REQ-ENV-002, REQ-ENV-003]
  ARP4754A: [REQ-CRT-001, REQ-CRT-002]
  ARP4761: [REQ-SAF-001, REQ-REL-002]
```

### 6. TECHNICAL REQUIREMENTS SECTIONS

#### 6.1 Structural
```yaml
structural:
  load_factors: { limit: 2.5g, ultimate: 3.75g, negative_limit: -1.0g }
  pressure: { proof: "89 kPa", ultimate: "118.6 kPa", max_differential: "59.3 kPa" }
  gust_cases: { Ude_spec: "CS-25.341 Appendix G", velocities: "VB/VC/VD" }
  ground_loads: { taxi_bump: "2.0g vertical", braking: "0.5g longitudinal" }
  flutter: { no_flutter_speed: "1.15·VD", damping_margin: "≥3% at VD" }
  damage_tolerance: { two_bay_crack: "limit load", BVID: "35 J impact" }
```

#### 6.2 Material
```yaml
material:
  primary_composite: { system: "IM7/8552-1", basis: "B", temp_range: "[-253, +50]°C" }
  titanium: { alloy: "Ti-6Al-4V", yield_min: "800 MPa", h2_compatible: "yes" }
  aluminum: { alloy: "Al-Li 2099-T8X", yield_min: "500 MPa", galvanic_protection: "required" }
  interlaminar: { GIc_min: "0.50 kJ/m²", GIIc_min: "1.00 kJ/m²", test_temp: "-150°C" }
```

#### 6.3 Interface
```yaml
interface:
  h2_storage: { mount_points: 12, load_rating_x: "±222 kN", thermal_isolation: "k<0.5 W/m·K" }
  cb_ribs: { type: "bolted/bonded", fastener_pitch: "50mm", rows: 2 }
  cb_skin: { type: "co-bonded", bond_thickness: "0.25mm", surface_prep: "plasma" }
  landing_gear: { load_ultimate: "622 kN per strut", fitting_material: "titanium" }
```

#### 6.4 Environmental
```yaml
environmental:
  temperature: { operational: "[-55, +85]°C", cryo_interface: "[-253, +50]°C" }
  humidity: "0-100% RH"
  altitude: "0-51,000 ft"
  lightning: { protection: "DO-160G Cat A3/E3", bond_resistance: "≤2.5 mΩ" }
  chemicals: { hydraulic: "Skydrol LD-4", fuel: "Jet A-1/LH2", deicing: "Type I/II/IV" }
```

#### 6.5 Manufacturing
```yaml
manufacturing:
  method: "AFP with autoclave cure"
  cure_cycle: { temp: "180°C±5°C", pressure: "7 bar min", time: "180 min" }
  tooling: { material: "Invar 36", tolerance: "±0.5mm/10m", surface: "Ra<3.2μm" }
  ndi: { ultrasonic: "100% coverage", detection: "6mm minimum" }
```

#### 6.6 Certification
```yaml
certification:
  compliance: { primary: "CS-25 Amdt 27", special_conditions: ["SC-BWB-01", "SC-H2-01"] }
  moc: { analysis: "FEM/PRA", test: "component/full-scale", similarity: "BWB demonstrator" }
```

#### 6.7 Operational
```yaml
operational:
  service_life: "20,000 flight cycles"
  inspection_access: "30 minutes to critical areas"
  dispatch_reliability: "99.5%"
```

#### 6.8 Performance
```yaml
performance:
  weight: { target: "4,200 kg", tolerance: "+5%/-2%" }
  cg_location: { longitudinal: "35% MAC±2%", lateral: "±100mm from centerline" }
  stiffness: { min_frequency: "5 Hz first mode", deflection_limit: "span/300" }
```

#### 6.9 Maintenance
```yaml
maintenance:
  inspection_interval: "5,000 FH"
  msg3_category: "on-condition"
  access_provisions: { borescope_ports: "every 2m", removal_time: "4 hours max" }
```

#### 6.10 Reliability
```yaml
reliability:
  mtbf: ">100,000 flight hours"
  failure_criticality: { catastrophic: "10^-9/FH", hazardous: "10^-7/FH" }
  redundancy: "no single point failures"
```

#### 6.11 Safety
```yaml
safety:
  failure_modes: { primary: "safe-life", secondary: "fail-safe" }
  hazard_classification: { structural_failure: "catastrophic", h2_leak_path: "hazardous" }
  fmea_required: "yes"
```

#### 6.12 Security
```yaml
security:
  data_classification: "ITAR controlled"
  physical_security: { tamper_evidence: "required", access_control: "badge+log" }
```

#### 6.13 End-of-Life
```yaml
end_of_life:
  recyclability: "85% by weight"
  hazardous_materials: { identification: "required", disposal: "certified facility" }
  disassembly_time: "<40 hours"
```

### 7. VERIFICATION MATRIX (MANDATORY)
| ID | Method | Medium | Evidence | Criterion | Phase |
|----|--------|--------|----------|-----------|-------|
| REQ-STR-001 | Analysis | FEM | STR-AN-001 | MoS≥0.0(limit), ≥0.5(ult) | Design |
| REQ-STR-002 | Test | Pressure | STR-TST-PP-001 | No damage/failure | Qualification |
| REQ-STR-003 | Analysis | Loads | LOAD-341-001 | Stress within limits | Design |
| REQ-STR-004 | Test/Analysis | GVT+Flutter | AEL-GVT-001 | No flutter to 1.15VD | Qualification |
| REQ-STR-005 | Analysis | F&DT | FDT-AN-001 | Residual≥limit | Design |
| REQ-STR-005a | Test | Impact | BVID-TST-001 | Strength≥limit | Qualification |
| REQ-STR-005b | Analysis | Crack | FDT-CG-001 | Two-bay meets limit | Design |
| REQ-THR-001 | Test | Cryo-cycle | THR-TST-001 | No cracks>2mm | Qualification |
| REQ-THR-002 | Test | Thermal-shock | THR-TST-002 | Integrity maintained | Qualification |
| REQ-IFC-001 | Test | Heat-flux | THR-HFX-001 | q≤5W/m² | Design |
| REQ-IFC-002 | Test | Load | IFC-TST-001 | Meets capacity | Qualification |
| REQ-IFC-003 | Inspection | Drawing | IFC-DWG-001 | Interfaces defined | Design |
| REQ-MAT-001 | Test | Coupon | MAT-ALW-001 | A/B-basis met | Design |
| REQ-MAT-002 | Test | H2-compat | MAT-H2C-001 | ISO-11114-4 pass | Design |
| REQ-ENV-001 | Test | Lightning | LPS-TST-001 | DO-160 compliance | Qualification |
| REQ-ENV-002 | Test | Resistance | EMC-TST-001 | R≤specified | Qualification |
| REQ-ENV-003 | Analysis | Current | EMC-AN-001 | Path isolated | Design |
| REQ-MFG-001 | Demonstration | Prototype | MFG-DEM-001 | Process validated | Design |
| REQ-MFG-002 | Inspection | Mock-up | MFG-ACC-001 | Access confirmed | Design |
| REQ-TST-001 | Test | Multiple | TST-PLN-001 | All tests complete | Qualification |
| REQ-TST-002 | Analysis | POD | NDI-POD-001 | 90/95 achieved | Design |
| REQ-CRT-001 | Analysis | Compliance | CRT-RPT-001 | CS-25 met | Design |
| REQ-CRT-002 | Analysis | SC-review | CRT-SC-001 | SC approved | Design |
| REQ-OPS-001 | Analysis | Fatigue | OPS-FAT-001 | 20k cycles OK | Design |
| REQ-OPS-002 | Demonstration | Mock-up | OPS-ACC-001 | 30 min verified | Design |
| REQ-PRF-001 | Analysis | Weight | PRF-WGT-001 | ≤4,200kg | Design |
| REQ-PRF-002 | Analysis | CG | PRF-CG-001 | Within envelope | Design |
| REQ-MNT-001 | Analysis | MSG-3 | MNT-MSG-001 | 5000FH justified | Design |
| REQ-MNT-002 | Inspection | Mock-up | MNT-BSC-001 | Access verified | Design |
| REQ-REL-001 | Analysis | MTBF | REL-MTB-001 | >100k FH | Design |
| REQ-REL-002 | Analysis | FMEA | REL-FME-001 | No SPF | Design |
| REQ-SAF-001 | Analysis | FTA | SAF-FTA-001 | <10^-9/FH | Design |
| REQ-SAF-002 | Analysis | Safe-life | SAF-SL-001 | Criteria met | Design |
| REQ-SEC-001 | Inspection | Process | SEC-ITA-001 | ITAR compliance | Design |
| REQ-SEC-002 | Demonstration | Feature | SEC-TAM-001 | Tamper evident | Design |
| REQ-EOL-001 | Analysis | Materials | EOL-RCY-001 | 85% recyclable | Design |
| REQ-EOL-002 | Analysis | Disposal | EOL-DSP-001 | Process defined | Design |

### 8. RISK REGISTER
```yaml
risk_register:
  structural:
    - id: RISK-STR-001, risk: "Composite cryo-cycling degradation", prob: M, impact: H, mitigation: "Extended test program with margin"
    - id: RISK-STR-002, risk: "Flutter boundary uncertainty", prob: L, impact: H, mitigation: "Conservative design + early GVT"
  thermal:
    - id: RISK-THR-001, risk: "Thermal gradient cracking", prob: M, impact: M, mitigation: "Compliant interfaces + gradual transitions"
  manufacturing:
    - id: RISK-MFG-001, risk: "AFP defects in thick sections", prob: M, impact: M, mitigation: "Process development + enhanced NDI"
  interface:
    - id: RISK-IFC-001, risk: "H2 system integration complexity", prob: H, impact: M, mitigation: "Early mockup + digital twin validation"
```

### 9. PHASE GATE CRITERIA
| Requirement | Status | Owner |
|---|---|---|
| All reqs defined | COMPLETE | Chief Systems Engineer |
| V&V methods defined | COMPLETE | V&V Lead |
| Risk assessment done | COMPLETE | Risk Manager |
| Standards mapped | COMPLETE | Certification Lead |
| Interfaces identified | COMPLETE | Interface Manager |
| Verification matrix complete | COMPLETE | V&V Lead |

### 10. DOCUMENT CONTROL (MANDATORY)
**Approvals:** Structures Lead:____, Materials Lead:____, Chief Systems Eng:____, Chief Arch (DT): Amedeo Pelliccia  
**Control:** Version: 1.4, Gate: DRAFT, Distro: Program Board/Technical Teams, Repo: /T-TECHNOLOGICAL/.../CI-CA-A-001-001-CB-PRIMARY-GRID/

---
## Companion File: `phase-data.yaml`
```yaml
utcs_phase: "01"
component_id: "CI-CA-A-001-001-CB-PRIMARY-GRID"
status: "DRAFT"
date: "2025-08-26"
owner: "Amedeo Pelliccia"
doc_id: "AMPEL360-REQ-CB-PG-001-v1.4"
links:
  - evidence/STR-AN-001_FEM-Analysis
  - evidence/STR-TST-PP-001_Pressure-Test
  - evidence/MAT-ALW-001_Material-Allowables
  - evidence/LPS-TST-001_Lightning-Protection
  - evidence/FDT-AN-001_Damage-Tolerance
```
