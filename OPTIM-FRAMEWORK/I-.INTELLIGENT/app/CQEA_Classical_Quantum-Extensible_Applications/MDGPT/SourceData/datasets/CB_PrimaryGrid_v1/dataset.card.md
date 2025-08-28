# Dataset Card — CB_PrimaryGrid_v1

**Ámbito**: Estructura primaria (Center Body), vistas isométricas y ortográficas del primary grid framework para AMPEL360 BWB.

```**prompt**
EstándarUniversal:Datos-Desarrollo-ARP4754A-00.00-ImagenDeOrigen-0003-v1.0-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionSintetica-AIR-AmedeoPelliccia-3a4b5c6d-01-Requirements→07-Certification-Security	cbpg_v1_000003	items/000003/image.png	SyntheticLM	T3	stable-diffusion-xl	1.0	detailed technical drawing of aircraft primary grid structure, center body frame, aluminum construction, isometric view, engineering blueprint style	42	ddim	invisible	0.92	0.08				pass	pass	pass	info	2025-08-28T07:35:00Z
```

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/1e42708e-21c9-4a17-8c7d-7c9a08ac6439" />

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/9d3fbef6-9919-468c-a5f6-f34ec1abce86" />


## Composición del Dataset
- **Total**: 2,000 imágenes de alta resolución (2048x2048 px mínimo)
- **Distribución por trust tier**:
  - T0 (SyntheticParametric): 600 imágenes con ground truth completo
  - T1 (RenderCAD): 400 imágenes fotorrealistas desde CAD
  - T2 (RealPhoto/TechnicalDrawing): 600 imágenes reales documentadas
  - T3 (SyntheticLM): 400 imágenes hiperrealistas generadas por LM
- **Ground Truth**: 1,200 imágenes con ontología JSON-LD, grafo GraphML, y geometría GLB

## Tipos de Origen
- **SyntheticParametric**: Renders desde modelos CAD paramétricos con GT exacto
- **RenderCAD**: Fotorrealista desde Solidworks/Catia/NX con materiales/lighting
- **RealPhoto**: Fotografías de taller/laboratorio con iluminación controlada
- **TechnicalDrawing**: Planos vectoriales PDF/DWG con simbología normalizada
- **SyntheticLM**: Generado por StableDiffusionXL/DALLE-3 con prompts documentados

## Contenido Técnico
### Componentes Cubiertos:
- Hat stringers (profiles diversos: 40mm, 60mm, 80mm width)
- Z-stringers y L-angles de refuerzo
- Frames primarios y secundarios
- Access panels y cutouts
- LPS bonding straps y buses eléctricos
- Fastener patterns (rivets, bolts, special fasteners)
- Service routing (cables, hydraulics, pneumatics)

### Vistas Incluidas:
- Isométricas (30°, 45°, 60° viewing angles)
- Ortográficas (front, side, top, section views)
- Detail views (close-ups de joints, fasteners)
- Exploded views (assembly sequences)

## Metadatos y Proveniencia
- **Licencias**: AQUA-Internal-Use para desarrollo; real photos con consent documentado
- **Derechos**: AQUA Technologies S.L. / colaboradores con IP clearance
- **Localización**: s3://aqua-datasets/cbpg_v1/ (bucket interno)
- **Backup**: Múltiples replicas geográficas con checksum validation

## Riesgos y Mitigaciones
### Riesgos Identificados:
1. **Alucinaciones geométricas** en SyntheticLM: geometrías imposibles, non-manifold surfaces
2. **Sesgo visual**: predominancia de certain viewing angles o lighting conditions
3. **OCR quality**: callouts ilegibles o inconsistentes en synthetic data
4. **Material misclassification**: materials que no existen o incompatibles

### Mitigaciones Implementadas:
- Validation rules físicas y de engineering standards
- Balanced dataset con T0/T1/T2 majority para training stability
- Human-in-the-loop QA para all T3 images antes de inclusion
- Cross-validation con real engineering drawings y specifications

## Compliance y Standards
- **ARP4754A**: All metadata conforme a aircraft development standards
- **DO-178C**: SyntheticLM tagged como "informative/auxiliary" no evidence directa
- **S1000D**: Compatible con AGEN-QAI para auto-generation de tech docs
- **UTCS-MI v5.0**: Full traceability y phase alignment

## Uso Permitido
### Training/Development:
- ✅ ML model training para MDGPT pipeline
- ✅ Algorithm validation y performance testing  
- ✅ Research publications (anonimized)
- ✅ Internal tooling y automation

### Certificación/Evidence:
- ✅ T0/T1/T2 como supporting evidence (con review)
- ❌ T3/T4 NO para certification evidence directa
- ⚠️ T3 solo como ilustrative/explanatory material

## Quality Metrics
- **OCR Readability**: μ=0.85, σ=0.12 (across all types)
- **Blur Metric**: <0.1 para T0/T1, <0.2 para T2/T3
- **Physical Plausibility**: 100% pass rate después de QA
- **Geometric Consistency**: 98.5% pass rate (1.5% flagged para review)

## Versioning y Updates
- **Current Version**: 1.0.0 (baseline dataset)
- **Next Release**: 1.1.0 - añadir multi-view consistency validation
- **Future**: 2.0.0 - expand a wing structure y control surfaces

---

**Maintained by**: AQUA MDGPT Team  
**Contact**: mdgpt-dataset@aqua-technologies.es  
**Last Updated**: 2025-08-28T07:40:00Z  
**Review Cycle**: Quarterly (Q1, Q2, Q3, Q4)

