# FEM Analysis Procedure — AMPEL360 H₂-BWB-Q

**UTCS Phase:** 02-Design, 05-Verification-Validation  
**Owner:** Structural Analysis Lead

## Purpose
Standardized procedure for finite element method analysis of BWB structures.

## Prerequisites
- Validated CAD geometry
- Material properties database
- Boundary condition specifications
- Load case definitions

## Analysis Steps

### 1. Geometry Preparation
- Import CAD model
- Clean up geometry defects
- Extract mid-surfaces for shell elements
- Define symmetry conditions

### 2. Mesh Generation
- Select element types (shell, solid, beam)
- Define mesh density criteria
- Generate initial mesh
- Perform mesh quality checks
- Refine as needed

### 3. Material Assignment
- Apply material properties from MMPDS/CMH-17
- Define ply orientations for composites
- Set failure criteria
- Validate material models

### 4. Boundary Conditions
- Apply structural constraints
- Define load application points
- Set up contact conditions
- Implement symmetry constraints

### 5. Solution Execution
- Select analysis type (linear/nonlinear)
- Set convergence criteria
- Monitor solution progress
- Check for convergence issues

### 6. Post-Processing
- Extract stress/strain results
- Calculate margins of safety
- Generate deformation plots
- Export loads for other analyses

## Quality Checks
- Mesh quality metrics
- Force/moment equilibrium
- Convergence verification
- Results sanity checks

## Deliverables
- Analysis report
- Stress/strain plots
- Margin of safety summary
- Model archive package