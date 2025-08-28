# Dataset Card — CB_PrimaryGrid_v1

**Ámbito**: Estructura primaria (Center Body), vistas isométricas y ortográficas del primary grid framework para AMPEL360 BWB.

## Registro de ejemplo (TSV para `index.csv`)
```tsv
EstándarUniversal:DatosDeOrigen-Desarrollo-ARP4754A-00.00-ImagenDeOrigen-0003-v1.0-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionHybrida-AIR-Amedeo Pelliccia-3a4b5c6d-01-Requirements→07-Certification-Security	cbpg_v1_000003	items/000003/image.png	SyntheticLM	T3	stable-diffusion-xl	1.0	detailed technical drawing of aircraft primary grid structure, center body frame, aluminum construction, isometric view, engineering blueprint style	42	ddim	invisible	0.92	0.08				pass	pass	pass	info	2025-08-28T07:35:00Z
````

<p align="center">
  <img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/1e42708e-21c9-4a17-8c7d-7c9a08ac6439" />
</p>

<p align="center">
  <img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/9d3fbef6-9919-468c-a5f6-f34ec1abce86" />
</p>

## Composición del Dataset

* **Total**: 2,000 imágenes de alta resolución (2048x2048 px mínimo)
* **Distribución por trust tier**:

  * T0 (SyntheticParametric): 600 imágenes con ground truth completo
  * T1 (RenderCAD): 400 imágenes fotorrealistas desde CAD
  * T2 (RealPhoto/TechnicalDrawing): 600 imágenes reales documentadas
  * T3 (SyntheticLM): 400 imágenes hiperrealistas generadas por LM
* **Ground Truth**: 1,200 imágenes con ontología JSON-LD, grafo GraphML, y geometría GLB

## Tipos de Origen

* **SyntheticParametric**: Renders desde modelos CAD paramétricos con GT exacto
* **RenderCAD**: Fotorrealista desde Solidworks/Catia/NX con materiales/lighting
* **RealPhoto**: Fotografías de taller/laboratorio con iluminación controlada
* **TechnicalDrawing**: Planos vectoriales PDF/DWG con simbología normalizada
* **SyntheticLM**: Generado por StableDiffusionXL/DALLE-3 con prompts documentados

## Contenido Técnico

### Componentes Cubiertos

* Hat stringers (profiles 40/60/80 mm)
* Z-stringers y L-angles de refuerzo
* Frames primarios y secundarios
* Access panels y cutouts
* LPS bonding straps y buses eléctricos
* Fastener patterns (rivets, bolts, special fasteners)
* Service routing (cables, hidráulica, neumática)

### Vistas Incluidas

* Isométricas (30°, 45°, 60°)
* Ortográficas (front, side, top, sections)
* Detail views (joints, fasteners)
* Exploded views (secuencias de ensamblaje)

## Metadatos y Proveniencia

* **Licencias**: AQUA-Internal-Use; real photos con consent documentado
* **Derechos**: AQUA Technologies S.L. / colaboradores con IP clearance
* **Localización**: s3://aqua-datasets/cbpg\_v1/
* **Backup**: Réplicas geográficas con checksum validation

## Riesgos y Mitigaciones

1. **Alucinaciones geométricas** (SyntheticLM) → reglas físicas + revisión humana
2. **Sesgo visual** → balance T0/T1/T2 + métricas de diversidad
3. **OCR quality** irregular → filtros de calidad y re-etiquetado
4. **Material misclassification** → validadores y catálogos materiales

## Compliance y Standards

* **ARP4754A** (proceso) • **DO-178C** (rol “informativo/auxiliar” para T3)
* **S1000D** (salidas AGEN-QAI) • **UTCS-MI v5.0** (13 campos, trazabilidad)

## Uso Permitido

* **Training/Dev**: ✅ MDGPT, validación algorítmica, investigación (anonimizada)
* **Certificación**: ✅ T0/T1/T2 (con review) • ❌ T3/T4 como evidencia directa

## Quality Metrics

* **OCR Readability**: μ 0.85 (σ 0.12)
* **Blur Metric**: < 0.1 T0/T1, < 0.2 T2/T3
* **Plausibilidad física**: ≥ 99% tras QA
* **Consistencia geométrica**: ≥ 98.5%

## Versioning y Updates

* **Current**: 1.0.0
* **Next**: 1.1.0 (multi-view consistency)
* **Future**: 2.0.0 (wing + control surfaces)

---

**Maintained by**: AQUA MDGPT Team
**Contact**: [mdgpt-dataset@aqua-technologies.es](mailto:mdgpt-dataset@aqua-technologies.es)
**Last Updated**: 2025-08-28T07:40:00Z
**Review Cycle**: Quarterly (Q1, Q2, Q3, Q4)

````



