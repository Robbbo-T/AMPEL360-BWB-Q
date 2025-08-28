# MDGPT — Source Data
**Gestión de datos de origen (incl. hiperrealistas generados por modelos) para 2D→Ontología→3D**

EstándarUniversal:Documento-Especificacion-ARP4754A-00.00-SourceDataSpecification-0001-v1.0-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionHumana-AIR-AmedeoPelliccia-9ab47cde-01-Requirements→07-Certification-Security

---

## 0) Propósito
Establecer **estructura, metadatos, proveniencia, licencias y validación** de los datos de entrada. Distinguir **SyntheticLM** (hiperrealista) del resto y asegurar que su uso sea **trazable y seguro** para decisiones de ingeniería.

## 1) Estructura de carpetas

```
MDGPT/
└─ SourceData/
   ├─ README.md
   ├─ datasets/
   │  └─ CB_PrimaryGrid_v1/
   │     ├─ dataset.card.md
   │     ├─ index.csv
   │     └─ items/
   │        ├─ 000001/
   │        │  ├─ image.png
   │        │  ├─ metadata.yml
   │        │  ├─ overlay.svg          # anotaciones
   │        │  ├─ ontology.jsonld      # (si GT)
   │        │  ├─ graph.graphml        # (si GT)
   │        │  └─ geom.glb             # (si GT)
   │        └─ 000002/ ...
   └─ processed/
      └─ CB_PrimaryGrid_v1/ ...        # salida de ingesta/validación
```

## 2) Esquema de metadatos por ítem (`metadata.yml`)
```yaml
utcs_mi_header: "EstándarUniversal:Datos-Desarrollo-ARP4754A-00.00-ImagenDeOrigen-0001-v1.0-AmpelTrescientosSesentaHidrogenoAlaCombinadaQuantum-GeneracionHumana-AIR-AmedeoPelliccia-1f2e3d4c-01-Requirements→07-Certification-Security"

id: "cbpg_v1_000001"
origin_type: "SyntheticLM"  # [RealPhoto, TechnicalDrawing, RenderCAD, SyntheticParametric, SyntheticLM, ScanPDF]
trust_tier: "T3"            # T0..T4

provenance:
  source: "internal_gen"
  license: "AQUA-Internal-Use"
  rights_holder: "AQUA Technologies S.L."
  uri: "s3://aqua/source/cbpg_v1/000001.png"

synthetic:
  model_name: "StableDiffusionXL"
  model_version: "1.0.0"
  prompt: "Isometric view of BWB center body primary grid with hat stringers, frames, access cutouts, LPS bonding..."
  negative_prompt: "text artifacts, double holes, non-euclidean joints"
  seed: 421337
  sampler: "DPM++ 2M"
  safety_filter: true
  watermark: "invisible"  # if embedded
  generator_hash: "sha256:ab12...fe"

quality:
  ocr_readability: 0.82
  blur_metric: 0.07
  lighting_ok: true

gt_links:
  ontology_jsonld: "../000001/ontology.jsonld"
  graph_graphml: "../000001/graph.graphml"
  geom_glb: "../000001/geom.glb"

qa_checks:
  physical_plausibility: pass
  lps_continuity: warn   # requiere revisión humana
  fastener_pattern: pass
  gdnt_minimal: pass

notes: "Generated for CB Primary Grid training set; requires reviewer sign-off for LPS."
timestamp: "2025-08-28T07:40:00Z"
```

## 3) Dataset Card (dataset.card.md) — plantilla
```markdown
# Dataset Card — CB_PrimaryGrid_v1

**Ámbito**: Estructura primaria (Center Body), vistas isométricas y ortográficas.  
**Composición**:
- 2,000 imágenes (T0=600, T1=400, T2=600, T3=400).
- 1,200 con ground truth ontológico/geométrico (JSON-LD/GLB/GraphML).

**Origen**:
- `SyntheticParametric` (renders CAD con GT).
- `RenderCAD` (fotorrealista).
- `RealPhoto` (taller).
- `SyntheticLM` (hiperrealista con prompts documentados).

**Licencias**: AQUA-Internal-Use; material real con consentimiento y limpieza de IP.  
**Riesgos**:
- Alucinaciones geométricas en `SyntheticLM`: mitigadas por reglas físicas y revisión humana.
- Dominio visual sesgado: balanceado con T0/T2.

**Uso permitido**:
- Entrenamiento/validación MDGPT.
- No usar `SyntheticLM` como evidencia de certificación (solo ilustración).
```

## 4) Reglas de calidad (schema/quality_rules.yml — extracto)
```yaml
rules:
  - id: "LPS-001"
    description: "Toda correa de bonding debe conectarse a un bus LPS en el grafo."
    applies_to: ["SyntheticLM","RealPhoto","RenderCAD","SyntheticParametric"]
    check: "graph_has_edge_type('grounds_to') or flag('lps_continuity','warn')"

  - id: "FAST-002"
    description: "Patrones de fijación deben corresponder a especificación NAS/MS válida."
    check: "validate_fastener_pattern(metadata, image)"

  - id: "GDNT-003"
    description: "Mínimo esquema GD&T (flatness/perpendicularity) si hay callouts de mecanizado."
    check: "has_gdnt_minimum(metadata)"
```

## 5) Ingesta/validación
```bash
mdgpt dataset ingest --src ./SourceData/datasets/CB_PrimaryGrid_v1 \
  --out ./SourceData/processed/CB_PrimaryGrid_v1 --attach-xmp

mdgpt dataset validate --in ./SourceData/processed/CB_PrimaryGrid_v1 \
  --schema ./schema/utcs.yml --rules ./schema/quality_rules.yml \
  --report ./SourceData/processed/CB_PrimaryGrid_v1/QA_REPORT.md
```

`--attach-xmp` inserta en XMP/EXIF: origin_type, trust_tier, model_name, prompt, seed, utcs_mi_header, y qa_checks.

## 6) Consideraciones de compliance

- **DO-178C**: los artefactos SyntheticLM pueden apoyar diseño/entrenamiento, pero no son evidencia directa de cumplimiento; registrar su rol como "informativo/auxiliar".
- **Trazabilidad**: firmar index.csv y dataset.card.md en QAUDIT y encadenar con DT-TRACE (hashes por ítem).
- **Propiedad intelectual**: limpiar logotipos/marcas y metadatos sensibles; registrar licencias por ítem.

## 7) Roadmap de datos

- **v1.1**: auto-weighting por trust_tier en entrenamiento.
- **v1.2**: generador sintético paramétrico "paired" (imagen ↔ GT exacto).
- **v1.3**: chequeos de consistencia multi-vista (ortos/iso).
- **v1.4**: detección automática de "artefactos imposibles" (non-manifold, tornillos sin tuerca).

---

### Bonus: campos a **embeder** en PNG/JPEG (XMP)
- `mdgpt:origin_type`, `mdgpt:trust_tier`, `mdgpt:model_name`, `mdgpt:model_version`, `mdgpt:prompt`, `mdgpt:seed`, `mdgpt:utcs_mi_header`, `mdgpt:hash_sha256`, `mdgpt:qa_status`.

---