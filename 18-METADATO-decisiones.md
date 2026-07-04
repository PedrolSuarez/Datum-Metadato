# 18 · Decisiones — Proyecto «DATUM metadato»

**Versión:** v1.0 — Julio 2026
**Numeración:** METADATO-n (propia del proyecto, independiente de DATUM-n de Producto).

## Decisiones

### METADATO-1 — Creación del proyecto y gobierno propio — DECIDIDO
El metamodelo y los aceleradores se separan del proyecto DATUM-Producto (saturado) a un proyecto propio, «DATUM metadato». Gobierno propio: par de control `99-METADATO-control.md` + `18-METADATO-decisiones.md`, numeración METADATO-n. Hereda como estado inicial el resultado de DATUM-108 (metamodelo de 194 entidades, D00, 6 catálogos físicos, carga inicial, metadata-first). NO incluye doctrina de negocio/oferta/GTM (se queda en Producto/Dirección).

### METADATO-2 — Los JSON son bootstrap del Control Plane — DECIDIDO
Los ficheros JSON de este proyecto (`DATUM_Catalogos.json`, `DATUM_Carga_Inicial_Metadato.json`, `DATUM_Modelo_Datos_Metadato.json`) no son documentación: son el **artefacto de carga (bootstrap)** que arranca el Control Plane de DATUM. Orden de carga: catálogos → carga inicial (physical_catalog→schema→storage_layer→location→canonical_entity) sobre la estructura del modelo. Cada acelerador añade su bloque de carga siguiendo el mismo patrón.

### METADATO-3 — D20 como raíz de la jerarquía de aceleradores — DECIDIDO
`canonical_accelerator` se reubica de `D0 / D01 · Catálogos de datos` a `D2 / D20 · Términos de Negocio`. D20 pasa a ser la raíz de la jerarquía **acelerador → término de negocio → entidad canónica**, y `canonical_accelerator` es su cabecera. Solo reclasificación (`domain`/`subdomain`); `code`, atributos y FK sin cambios. FK entrante única (`canonical_entity.canonical_accelerator_code`) apunta por `code`, no se rompe. Recuentos: D0 31, D2 31, D20 6.

### METADATO-4 — Saneamiento de `canonical_accelerator` — DECIDIDO
Se elimina el atributo `domain_scope`. `status_code` se alinea al patrón metadata-first de D00: FK `reference_value`, `reference_catalog="RECORD_STATUS"`, `catalog_ref_metadata_only=true`. Atributos finales: `code` (PK), `accelerator_version`, `status_code`, `entity_count`, `row_uuid`, `audit`.

### METADATO-5 — Adscripción entidad→acelerador transitiva vía término — DECIDIDO
`business_term`: (a) `status_code` → metadata-first RECORD_STATUS; (b) nueva FK `canonical_accelerator_code` → `canonical_accelerator`, `mandatory=1` (todo término pertenece a un acelerador); (c) se elimina `owner_business_domain_code` (apuntaba a `business_domain`, tabla inexistente). En `canonical_entity` se elimina la FK directa `canonical_accelerator_code` (y de las 194 filas del seed). La adscripción de una entidad a su acelerador pasa a ser transitiva: `canonical_entity → business_term → canonical_accelerator`.

### METADATO-6 — Catálogo de aceleradores y términos base (seed) — DECIDIDO
Carga inicial ampliada con dos bloques nuevos. **6 aceleradores** (`canonical_accelerator`), version `1.0.0`, estado `ACTIVE`: METADATA (entity_count 194), OBSERVABILITY, FINANCE, HR, LEGAL, MARKETING (0). **12 términos base** (`business_term`) del acelerador METADATA: BUSINESS_TERM, CANONICAL_ENTITY, ORG_STRUCTURE, CATALOG, DATA_DOMAIN, I18N, DELTA_CONFIG, BUSINESS_PROCESS, DATA_SOURCE, DATA_QUALITY, TRANSFORMATION, GOVERNANCE. Orden de carga: acelerador antes que término (FK). Lista de términos abierta, se irá ajustando.

### METADATO-7 — Término padre DATABRICKS y reclasificación de D00/D05 — DECIDIDO
Nuevo término padre `DATABRICKS` (acelerador METADATA). Dos hijos vía `parent_term_code=DATABRICKS`: `CATALOG` (cuelgan physical_catalog, physical_schema, storage_layer, storage_location) y `DELTA_CONFIG` (config_pattern, delta_property, config_pattern_delta_default, object_delta_override). Estas 8 entidades se vinculan a su término por `canonical_entity.business_term_code` y se les **vacía `domain`/`subdomain`**: su clasificación pasa a ser el término, no el dominio. Bootstrap intacto (conservan `code`/PK; las 21 FK entrantes van por `code`). Recuentos vista por dominio: D0 23, D00 0, D05 0; el `.md` (vista por dominio) lista 186 de las 194 entidades (las 8 reclasificadas ya no cuelgan de dominio).

### METADATO-8 — Visualizador por acelerador — DECIDIDO
La página «Modelo canónico» incorpora conmutador **Por acelerador / Por dominio** (arranca en acelerador). Árbol nuevo alimentado del seed: acelerador (📦) → término padre (🗂️) → término hoja (🏷️) → entidad canónica (🧊), con indentación escalonada y guías. La relación término→entidad se lee de `canonical_entity.business_term_code`. La vista por dominio se conserva y se irá sustituyendo por la de acelerador.

---
*Fin de `18-METADATO-decisiones.md` v1.0.*
