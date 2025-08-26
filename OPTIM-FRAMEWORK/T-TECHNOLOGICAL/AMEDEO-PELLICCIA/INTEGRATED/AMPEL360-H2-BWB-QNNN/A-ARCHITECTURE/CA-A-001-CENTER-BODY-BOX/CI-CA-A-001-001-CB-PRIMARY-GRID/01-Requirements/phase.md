# 01-Requirements - CI-CA-A-001-001-CB-PRIMARY-GRID (v1.3 FROZEN)

EstándarUniversal:Documento-Diseno-ARP4754A-00.00-AMPEL360-REQ-CB-PG-001-0001-v1.3-OPTIM-as-DT-GeneracionHumana-AIR-AmedeoPelliccia-7f3c9a2b-Diseno→Operacion

## Component Architecture: CA-A-001-CENTER-BODY-BOX
## Configuration Item: CI-CA-A-001-001-CB-PRIMARY-GRID
## UTCS Phase: 01-Requirements
**Document ID:** AMPEL360-REQ-CB-PG-001-v1.3  
**Classification:** UNCLASSIFIED // For Official Use Only  
**Effective Date:** 2025-08-26  
**Revision Date:** 2025-08-29  
**Status:** FROZEN - AUDIT READY  
**Owner:** Amedeo Pelliccia

### Revision History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-08-26 | Initial Release | AMPEL360 Team |
| 1.1 | 2025-08-27 | Addressed RFAs from Validation Report | AMPEL360 Team |
| 1.2 | 2025-08-28 | Audit-ready compliance updates | AMPEL360 Team |
| 1.3 | 2025-08-29 | Final RFA resolution - FROZEN | AMPEL360 Team |

### Units Policy
```yaml
units_policy:
  base: SI
  pressure: kPa            # show psi in parentheses
  temperature: °C
  force: kN (lbf in parentheses)
  length: mm
  conversion_note: "Legacy values in psi/lbf provided in parentheses for traceability."
```

### Requirements Index
```yaml
requirements_index:
  REQ-STR-001: "Primary grid shall sustain limit load 2.5g and ultimate 3.75g without failure"
  REQ-STR-002: "Primary grid shall withstand proof pressure 89 kPa (12.9 psi), ultimate 118.6 kPa (17.2 psi)"
  REQ-STR-003: "Primary grid shall meet CS-25.341 discrete gust (VB/VC/VD) per Ude; alleviation factors documented"
  REQ-STR-004: "Primary grid shall have no flutter/LCO up to 1.15·VD and modal margin ≥15% to critical pair — CS-25.629"
  REQ-STR-005: "Primary grid shall meet two-bay crack capacity ≥ limit load; discrete source 1/3 bay — CS-25.571"
  REQ-STR-005a: "Composite shall demonstrate BVID residual strength ≥ limit load post 35 J impact, including cryo-conditioning"
  REQ-STR-005b: "Metallic paths shall meet fail-safe/durability with two-bay crack or equivalent redundancy"
  REQ-THR-001: "Primary grid shall withstand cryogenic thermal gradient without cracks >2mm after 20,000 cycles"
  REQ-IFC-001: "LH2 interface shall maintain: heat flux ≤ 5 W/m²; Tmax_grid_mount ≤ −50°C; k_isolator < 0.5 W/m·K"
  REQ-IFC-002: "H2 mounts shall support capacity per point (X/Y/Z) with factors 1.0 (limit) / 1.5 (ultimate)"
  REQ-MAT-001: "Materials and processes shall be approved with A-/B-basis; properties at −253°C qualified"
  REQ-ENV-EMC-001: "Primary grid shall provide LPS on composite surfaces per DO-160 §22 Cat A3/E3"
  REQ-ENV-EMC-002: "Primary grid shall implement z-bond network with joint resistance ≤ 2.5 mΩ (panels), ≤ 10 mΩ (access covers)"
  REQ-ENV-EMC-003: "Primary grid shall define controlled lightning return path isolated from LH2 volumes"
```

### Standards Mapping
```yaml
standards_mapping:
  CS-25.301/305/307: [REQ-STR-001, REQ-STR-002, load_combinations]
  CS-25.341: [REQ-STR-003]
  CS-25.365: [REQ-STR-002, pressure_policy]
  CS-25.561/562: ["landing loads/reinforcement CA-A-001-004"]
  CS-25.571: [REQ-STR-005, REQ-STR-005a, REQ-STR-005b]
  CS-25.629: [REQ-STR-004]
  DO-160G: ["Sections 4,5,8,19,20,22 for sensors/LPS/EMC"]
  ISO-19880/SAE-AIR6464: [REQ-IFC-001, REQ-IFC-002, h2_safety]
  SAE-ARP5412/5414/5416: [REQ-ENV-EMC-001, LPS_design_verification]
  ARP4754A/ARP4761: ["development plan and structural safety case"]
```

### 1. Structural Requirements

#### 1.1 Primary Load Requirements

```yaml
load_requirements:
  limit_load_factor: 2.5g
  ultimate_load_factor: 3.75g
  negative_limit_load: -1.0g
  gust_load_cases:
    Ude_specification: "Per CS-25.341 + Appendix G with altitude/gradient-dependent Ude (30/100/300 ft); VB/VC/VD per Loads Manual §3.2"
  ground_loads:
    - taxi_bump: "2.0g vertical"
    - braking: "0.5g longitudinal"
  pressure_loads:
    - max_differential: "59.3 kPa (8.6 psi)"
    - proof_pressure: "89 kPa (12.9 psi)"
    - ultimate_pressure: "118.6 kPa (17.2 psi)"
    - policy_note: "Proof/ultimate multipliers per Program PVP-01 aligned to CS-25.365. Current values (proof=1.5×, ultimate=2.0×) are conservative pending weight trade"
  thermal_induced_loads:
    - tank_filling: "ΔT = +20°C to -253°C in 30 minutes"
    - steady_state_cryo: "Grid @ -100°C, Tank @ -253°C"
    - boil_off_condition: "10K/hour temperature rise (measured via Type-K thermocouples @ 500mm intervals)"
    - emergency_venting: "Rapid depressurization scenario"
  load_combinations:
    LC-1: { case: "Limit maneuver + pressurization", factors: {limit: 1.0}}
    LC-2: { case: "Ultimate maneuver + pressurization", factors: {ultimate: 1.5}}
    LC-3: { case: "Discrete gust (CS-25.341) @VC/VD + press", factors: {limit: 1.0}}
    LC-4: { case: "Taxi/braking + local thermal gradient", factors: {limit: 1.0}}
    LC-5: { case: "Emergency venting + thermal shock", factors: {ultimate: 1.5}}
  notes: "Align factors with program Loads Manual; document pressure/fuel relief"
```

#### 1.2 Aeroelastic Requirements

```yaml
aeroelastic_requirements:
  flutter_free: "No flutter/LCO up to 1.15·VD in all configurations — CS-25.629"
  damping_margin: "ζ ≥ 3% at 1.0·VD; ≥ 0% at 1.15·VD"
  ground_vibration_test: "GVT with FEM correlation ±5% in frequencies/ζ"
  control_reversal: "> 1.15 VD"
  divergence_speed: "> 1.2 VD"
```

#### 1.6 Damage Tolerance (CS-25.571)

```yaml
damage_tolerance:
  REQ-STR-005a: "Composite BVID tolerance: demonstrate residual strength ≥ limit load with 35 J impact or program-defined indentation criterion (≤1.0 mm), including cryo-conditioning"
  REQ-STR-005b: "Fail-safe/durability for metallic load paths: two-bay crack assumption or equivalent load-path redundancy; crack growth analysis with NDI intervals justified"
  inspection_detectability: "Define POD/CL for NDI (UT/Shearography/Thermography) with a90/95 thresholds for critical defects"
  coupon_element_component: "CEC pyramid including cryo; residual strength at limit & ultimate factors per load combinations"
```

### 2. Material Specifications

#### 2.1 Primary Structure Materials

```yaml
materials:
  primary_composite:
    system: "CFRP epoxy toughened, cryo-rated"
    specification: "IM7/8552-1 or equivalent"
    allowables: 
      basis: B
      source: "CMH-17 / internal testing"
      temperature_range: [-253, +50]
    properties:
      - tensile_strength: "2,750 MPa"
      - compressive_strength: "1,690 MPa"
      - elastic_modulus: "165 GPa"
      - density: "1.57 g/cm³"
    interlaminar_toughness:
      mode_I_GIc_min: "≥ 0.50 kJ/m² @ -150°C (ASTM D5528)"
      mode_II_GIIc_min: "≥ 1.00 kJ/m² @ -150°C (ASTM D7905)"
      mode_mix_definition: "ψ per Reeder (GII/(GI+GII)); test at ψ = 0, 45°, 90°"
    layup: "[45/-45/0/90]s typical"
    
  ti_6al_4v:
    allowables_source: "MMPDS / program cryo test"
    properties_nominal:
      yield_strength_min: "≥ 800 MPa @ RT; cryo curve TBD"
      ultimate_strength_min: "≥ 860 MPa @ RT; cryo curve TBD"
      elongation_min: "≥ 10% @ RT"
    hydrogen_compatibility: "ISO 11114-4 risk assessment; surface treatment to mitigate hydride formation"
    
  al_li_2099_t8x:
    allowables_source: "MMPDS / program cryo test"
    properties_nominal:
      yield_strength_min: "≥ 500 MPa @ RT; cryo curve TBD"
      ultimate_strength_min: "≥ 540 MPa @ RT; cryo curve TBD"
      elongation_min: "≥ 6% @ RT"
    galvanic_protection: "Barrier systems vs CFRP; sealants per MP-001"
    
  processes:
    afp: "Spec-AFP-001; autoclave cure 180°C/7bar/180min"
    ndt: ["UT phased array", "Shearography", "PULSE Thermography"]
```

#### 2.2 Environmental Requirements

```yaml
environmental_conditions:
  temperature:
    operational: "-55°C to +85°C"  # General structure
    ground_survival: "-65°C to +95°C"
    local_cryo_zones:
      h2_tank_interfaces: "-253°C to +50°C"
      gradient_zone_1m: "-253°C to -100°C over 1000mm"
      gradient_zone_2m: "-100°C to +20°C over 2000mm"
  humidity: "0% to 100% RH"
  altitude: "0 to 51,000 ft"
  chemical_resistance:
    - hydraulic_fluid: "Skydrol LD-4"
    - fuel: "Jet A-1 and LH₂"
    - deicing: "Type I, II, IV fluids"
  radiation: "RTCA DO-160G Section 19"
  thermal_cycling:
    - cycles_per_flight: "2 (fill/drain)"
    - lifetime_cycles: "20,000 minimum"
    - rate_of_change: "10°C/minute maximum"
```

### 3. Geometric Constraints

#### 3.1 Grid Geometry

```yaml
grid_configuration:
  cell_dimensions:
    longitudinal_spacing: "800mm ± 10mm"
    lateral_spacing: "750mm ± 10mm"
    diagonal_members: "45° ± 2°"
  grid_depth:
    center_section: "400mm nominal"
    transition_zone: "400mm to 250mm taper"
  manufacturing_constraints:
    minimum_radius: "50mm"
    draft_angle: "2° minimum"
    access_holes: "600mm x 400mm minimum"
```

#### 3.2 Weight Targets

```yaml
weight_allocation:
  primary_grid_structure: "4,200 kg"
  tolerance: "+5% / -2%"
  center_of_gravity:
    longitudinal: "35% MAC ± 2%"
    lateral: "± 100mm from centerline"
```

### 4. Interface Requirements

#### 4.1 Structural Interfaces

**CB Ribs and Bulkheads Interface**
- Interface Type: Bolted/Bonded combination
- Load Transfer: Shear and moment
- Fastener Pattern: Double row, 50mm pitch
- Link: [→ CI-CA-A-001-002-CB-RIBS-BULKHEADS](../CI-CA-A-001-002-CB-RIBS-BULKHEADS/)

**CB Skin Panels Interface**
- Interface Type: Co-bonded/Co-cured
- Bond Line Thickness: 0.25mm nominal
- Surface Preparation: Peel ply + plasma treatment
- Link: [→ CI-CA-A-001-003-CB-SKIN-PANELS](../CI-CA-A-001-003-CB-SKIN-PANELS/)

**Landing Gear Reinforcements Interface**
- Interface Type: Machined titanium fittings
- Load Cases: 622 kN (140,000 lbf) ultimate per strut
- Backup Structure: Required
- Link: [→ CI-CA-A-001-004-CB-LANDING-GEAR-REINFS](../CI-CA-A-001-004-CB-LANDING-GEAR-REINFS/)

#### 4.2 Systems Interfaces

**Hydrogen Storage System (CA-E2-005)**  
- Mounting points: 12 primary / 24 secondary  
- Load rating per point (limit/ultimate):  
  - X (longitudinal): ±222 kN (50,000 lbf), ±333 kN (75,000 lbf)
  - Y (lateral): ±178 kN (40,000 lbf), ±267 kN (60,000 lbf)  
  - Z (vertical): ±222 kN (50,000 lbf), ±333 kN (75,000 lbf)
- Thermal isolation (REQ-IFC-001): 
  - Heat flux ≤ 5 W/m²
  - k < 0.5 W/m·K
  - T_grid ≤ −50°C  
- Differential expansion: ±15 mm (X), ±10 mm (Y), ±10 mm (Z) with spherical bearings (stiffness range 100-500 N/mm per FEA model)
- **V&V**: Nonlinear analysis (NASTRAN SOL400) + component testing + strain-gauge correlation
- Link: [→ CA-E2-005-HYDROGEN-STORAGE](../../../E2-ENERGY/CA-E2-005-HYDROGEN-STORAGE/)

**Electrical Distribution System**
- Raceway Provisions: 100mm x 50mm channels
- Grounding Points: Every 2m
- EMI Shielding: Integrated copper mesh
- Link: [→ CA-E2-002-DISTRIBUTION](../../../E2-ENERGY/CA-E2-002-DISTRIBUTION/)

**Hydraulic Systems**
- Mounting Provisions: Standard MS33649 bosses
- Pressure Rating: 34.5 MPa (5000 psi) proof
- Leak Detection: Integrated sensors
- Link: [→ CA-M-002-HYDRAULICS](../../../M-MECHANICAL/CA-M-002-HYDRAULICS/)

### 5. Electrical Protection Requirements

```yaml
electrical_protection:
  REQ-ENV-EMC-001: "The primary grid shall provide LPS on outer CB surfaces ensuring no sustained arcing within cryo adjacency; verify per DO-160 §22 Cat A3/E3"
  REQ-ENV-EMC-002: "The primary grid shall implement z-bond network with joint resistance ≤ 2.5 mΩ (panel joints) and ≤ 10 mΩ (access covers-to-structure)"
  REQ-ENV-EMC-003: "The primary grid shall define controlled lightning return path clear of LH2 volumes; demonstrate current sharing and equipotential bonding"
  verification: "Lightning Indirect Effects analysis per SAE ARP5416 for CB area proximate to LH2"
```

### 6. Manufacturing Requirements

#### 6.1 Production Requirements

```yaml
manufacturing:
  production_method: "Automated Fiber Placement (AFP)"
  cure_cycle:
    temperature: "180°C ± 5°C"
    pressure: "7 bar minimum"
    time: "180 minutes at temperature"
  tooling_requirements:
    material: "Invar 36"
    tolerance: "± 0.5mm over 10m"
    surface_finish: "Ra < 3.2 μm"
  assembly_sequence:
    phase_1: "Grid structure layup and cure"
    phase_2: "Metallic interface installation"
    phase_3: "Systems integration"
    phase_4: "Final assembly to wing box"
```

#### 6.2 Quality Requirements

```yaml
quality_control:
  ndi_requirements:
    ultrasonic: "100% coverage, 6mm minimum detection"
    thermography: "Critical areas only"
    visual: "100% accessible surfaces"
  acceptance_criteria:
    porosity: "< 2% by volume"
    delamination: "None > 25mm²"
    fiber_waviness: "< 5°"
  traceability:
    material_batch: "Full tracking required"
    process_parameters: "Digital recording"
    as_built_documentation: "3D scanning ± 1mm"
```

### 7. Certification Requirements

#### 7.1 Compliance Matrix

```yaml
certification_compliance:
  cs25_subpart_c:
    CS25.301: "Loads"
    CS25.303: "Factor of safety"
    CS25.305: "Strength and deformation"
    CS25.307: "Proof of structure"
    CS25.571: "Damage tolerance"
    CS25.603: "Materials"
    CS25.605: "Fabrication methods"
    CS25.613: "Material properties"
  
  special_conditions:
    SC-BWB-01: "Non-cylindrical pressure vessel"
    SC-H2-01: "Hydrogen compatibility"
    SC-COMP-01: "Composite primary structure"
```

#### 7.2 Means of Compliance

```yaml
compliance_methods:
  analysis:
    - "Finite Element Analysis (Global/Local)"
    - "Progressive Damage Analysis"
    - "Probabilistic Risk Assessment"
  testing:
    - "Component test articles (3 minimum)"
    - "Subcomponent tests (fatigue, damage tolerance)"
    - "Full-scale static test article"
    - "Full-scale fatigue test article"
  similarity:
    - "Reference to BWB demonstrator data"
    - "Correlation with existing composite structures"
```

### 8. Verification and Validation Plan

#### 8.1 Analysis Requirements

```yaml
analysis_plan:
  phase_1_preliminary:
    - "Global FEM (shell elements)"
    - "Load path analysis"
    - "Trade studies"
  phase_2_detailed:
    - "Detailed FEM (solid elements at joints)"
    - "Progressive failure analysis"
    - "Thermal stress analysis"
  phase_3_validation:
    - "Test correlation"
    - "Model updating"
    - "Certification analysis"
```

#### 8.2 Test Requirements

```yaml
test_plan:
  development_tests:
    - "Material characterization"
    - "Joint specimens"
    - "Repair concepts"
  qualification_tests:
    - "Design limit load"
    - "Design ultimate load"
    - "Fatigue spectrum"
    - "Damage tolerance scenarios"
  acceptance_tests:
    - "Proof load test"
    - "Functional tests"
    - "NDI validation"
```

### 9. Phase Gate 01 Completion Criteria

| Requirement | Status | Owner | Link |
|-------------|--------|-------|------|
| All requirements baselined | COMPLETE | Chief Systems Engineer | [→ CSE Office](../../../../../../../O-ORGANIZATIONAL/governance/organizational-structure/cse-office.yaml) |
| Preliminary FEM complete | COMPLETE | Structures Lead | |
| Material selection validated | COMPLETE | Materials Lead | |
| Certification plan approved | COMPLETE | Certification Lead | [→ Cert Lead](../../../../../../../O-ORGANIZATIONAL/governance/organizational-structure/cert-lead.yaml) |
| Means of compliance defined | COMPLETE | Certification Lead | |
| Cost estimate validated | COMPLETE | Program Manager | |
| Schedule baselined | COMPLETE | Program Manager | |
| Risk register updated | COMPLETE | Risk Manager | [→ Risk Register](../../../../../../../O-ORGANIZATIONAL/artifacts/risk-register.xlsx) |

### 10. Thermal Analysis Requirements

#### 10.1 Thermal Analysis Requirements

```yaml
thermal_analysis:
  required_cases:
    - pre_cooling: "Ambient to LH₂ temperature"
    - steady_operation: "Cruise with full tanks"
    - transient_fill: "Rapid fueling scenario"
    - emergency_dump: "Rapid fuel jettison"
    - ground_hold: "Extended ground operation"
  analysis_methods:
    - coupled_thermal_structural: "ANSYS/NASTRAN"
    - transient_thermal: "Time-dependent analysis"
    - thermal_fatigue: "Coffin-Manson approach"
  acceptance_criteria:
    - max_thermal_stress: "< 0.8 * yield"
    - max_displacement: "< 25mm at interfaces"
    - thermal_fatigue_life: "> 2x service goal"
```

#### 10.2 Thermal Protection Requirements

```yaml
thermal_protection:
  insulation_system:
    - type: "Multi-layer insulation (MLI) + aerogel"
    - thickness: "50mm minimum at tank interfaces"
    - thermal_performance: "R-value > 40"
  thermal_barriers:
    - locations: "All H₂ system penetrations"
    - material: "Polyimide/glass composite"
    - temperature_capability: "-270°C to +150°C"
```

### 11. Verification Matrix

| ID | Method | Medium | Evidence/Doc | Criterion |
|-------------|-------------|-------------------|--------------------------------|--------------------------|
| REQ-STR-001 | Analysis | FEM NL + handcalc | STR-AN-001, STR-CALC-001 | MoS ≥ 0.0 (limit), ≥0.5 (ult) |
| REQ-STR-002 | Test | Pressure test | STR-TST-PP-001 (P-Δ curve) | No damage at proof, no failure at ultimate |
| REQ-STR-003 | Analysis | Loads+FEM | LOAD-341-VC/VD, STR-AN-002 | Meet stress/deflection limits |
| REQ-STR-004 | Test/Analysis | GVT + Flutter | AEL-GVT-001, AEL-FLT-001 | No flutter up to 1.15·VD |
| REQ-STR-005 | Analysis/Test | F&DT Analysis + Subcomponent | FDT-AN-001, FDT-SBCT-001 | Residual ≥ Limit; stable growth; NDI justified |
| REQ-STR-005a | Test | Impact + Residual Strength | BVID-TST-001 | Residual strength ≥ limit after 35J |
| REQ-STR-005b | Analysis | Crack Growth Analysis | FDT-CG-001 | Two-bay crack meets limit load |
| REQ-THR-001 | Test | Cryo cycling rig | THR-TST-CRYO-001 | No cracks >2 mm |
| REQ-IFC-001 | Test | Guarded-hot plate | THR-TST-HFX-001 | q ≤ 5 W/m² |
| REQ-IFC-002 | Test/Analysis | Bench + NL-FEA | IFX-TST-MOUNT-001, STR-AN-003 | Fx/Fy/Fz per rating |
| REQ-MAT-001 | Test | Coupons | MAT-ALW-CRYO-001 | A/B-basis approved |
| REQ-ENV-EMC-001 | Test | Lightning Strike | LPS-TST-001 | DO-160 §22 compliance |
| REQ-ENV-EMC-002 | Test | Bonding Resistance | EMC-TST-001 | Resistance within limits |
| REQ-ENV-EMC-003 | Analysis | Current Distribution | EMC-AN-001 | Path isolation verified |

---

**RFA Resolution Status - FINAL:**

| RFA ID | Status | Resolution |
|--------|--------|------------|
| RFA-CBPG-001 | CLOSED | Added REQ-STR-005a/b and V&V entries |
| RFA-CBPG-002 | CLOSED | Replaced KIC with G_Ic/G_IIc |
| RFA-CBPG-003 | CLOSED | Referenced Loads Manual for gust |
| RFA-CBPG-004 | CLOSED | Added pressure policy note |
| RFA-CBPG-005 | CLOSED | Split Ti and Al-Li allowables |
| RFA-CBPG-006 | CLOSED | Added LPS/EMC requirements |

**Validation Status:** APPROVED - FROZEN v1.3

**Approval Signatures:**

- **Structures Lead**: _________________  
  Date: 2025-08-29

- **Materials Lead**: _________________  
  Date: 2025-08-29

- **Chief Systems Engineer**: _________________  
  Date: 2025-08-29

- **Chief Architect (DT)**: Amedeo Pelliccia  
  Date: 2025-08-29

- **Certification Lead**: _________________  
  Date: 2025-08-29

**Document Control:**
- Version: 1.3 (FROZEN - Audit Ready)
- Phase Gate 01: APPROVED
- Distribution: Program Board, Technical Teams, Certification Authorities, Audit Team
- Repository: [T-TECHNOLOGICAL/.../CI-CA-A-001-001-CB-PRIMARY-GRID/01-Requirements/](../../../../../../../T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A-ARCHITECTURE/CA-A-001-CENTER-BODY-BOX/CI-CA-A-001-001-CB-PRIMARY-GRID/)

---
*AMPEL360 H₂-BWB-Q Framework - Requirements v1.3 FROZEN*
