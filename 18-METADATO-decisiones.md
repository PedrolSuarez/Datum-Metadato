# 18 · Decisiones — Proyecto «DATUM metadato»

**Versión:** v1.1 — Julio 2026
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

### METADATO-9 — Saneamiento de estado y `display_order` — DECIDIDO
Depuración de estado del modelo y seed: (a) `_meta.total_entities` heredado declaraba 195 vs. entidades reales; el modelo queda en **193 entidades** tras eliminar `metamodel_domain` (fila huérfana en cuarentena) del modelo y del seed, y retirar el atributo `reference_category.metamodel_domain_code`. (b) Nuevo atributo `display_order` (TYD_INT, mandatory=0) en `canonical_accelerator` y `business_term`, para ordenación estable del árbol. Seed de aceleradores: METADATA=10, OBSERVABILITY=20, FINANCE=30, HR=40, LEGAL=50, MARKETING=60.

### METADATO-10 — Unificación de estado en catálogo LIFECYCLE_STATE — DECIDIDO
Se unifica el estado del ciclo de vida en un único catálogo `LIFECYCLE_STATE` (5 valores: DRAFT, IN_DEFINITION, ACTIVE, DEPRECATED, RETIRED), metadata-first (`catalog_ref_metadata_only=true`). Se elimina el catálogo antiguo `RECORD_STATUS`; los ~30 atributos `status_code` se renombran a `lifecycle_state_code` y apuntan a `LIFECYCLE_STATE`. Seed inicial: todas las filas en ACTIVE. Catálogos de valores vigentes: SOURCE_FREQUENCY, LIFECYCLE_STATE, ASSESSMENT_TYPE, MAPPING_CONDITION_KIND, CARDINALITY. Pendiente (sesión aparte): `lifecycle_state_code` debería ser obligatorio y universal (hoy falta en `storage_layer` y es opcional en `storage_location`); se estudia incorporarlo por construcción vía `TYD_AUDIT`.

### METADATO-11 — Reestructuración de términos: COMMON_STRUCTURE, COMMON_DATA, HIERARCHY — DECIDIDO
Se reorganiza la jerarquía de términos del acelerador METADATA con tres términos padre nuevos y reasignación de entidades por `business_term_code` (con `domain`/`subdomain` vaciados):
- **COMMON_STRUCTURE** (order 15): hijos DATA_CATALOG (D01), DATA_DOMAIN, I18N, ISO_CODE (nuevo).
- **COMMON_DATA** (order 16): hijos ACCELERATOR (canonical_accelerator), BUSINESS_TERM, CANONICAL_ENTITY.
- **HIERARCHY** (order 17): hijos GEO_STRUCTURE (nuevo, sin entidades), ORG_STRUCTURE (reparentado, 5 entidades), TEMPORAL_STRUCTURE (nuevo, sin entidades).
Hijos ordenados alfabéticamente vía `display_order` (10/20/30). Bootstrap intacto (las FK entrantes van por `code`). Términos raíz vigentes y su orden: DATABRICKS 10, COMMON_STRUCTURE 15, COMMON_DATA 16, HIERARCHY 17, BUSINESS_PROCESS 20, DATA_QUALITY 60, DATA_SOURCE 70, GOVERNANCE 80, TRANSFORMATION 110.

### METADATO-12 — Visualizador: code en árbol, bolas de estado, tema claro/oscuro — DECIDIDO
Mejoras de la página «Modelo canónico» (`/dashboard/canonico`): (a) el árbol muestra el `code` puro de la entidad (no la traducción i18n); el panel de detalle sigue traducido. (b) Bolas de estado por `lifecycle_state_code` en todos los niveles (paleta 5: 🟢ACTIVE ⚪DRAFT 🟡IN_DEFINITION 🟠DEPRECATED 🔴RETIRED). (c) Jerarquía tipográfica e iconos Tabler (acelerador→término padre→término hoja→entidad). (d) Toggle de tema claro/oscuro local a la página (invierte variables `--dp-*`). Solo visualización; no toca modelo ni seed.

### METADATO-13 — ER por término de negocio (visualizador) — DECIDIDO
La página «Modelo canónico» incorpora, al seleccionar un término **con entidades directas**, un diagrama ER en el panel derecho con las entidades de ese término (`business_term_code`). Lienzo con arrastre por caja (asa en cabecera + fondo, listeners globales), zoom con rueda, pan por el fondo, y **fit-zoom** inicial que encuadra todas las cajas. Posiciones persistentes en `localStorage` combinadas con posiciones frescas (toda caja nueva recibe coordenadas). Pivote sobre la **entidad principal**: se lee de `business_term_canonical_entity.is_primary`; si el seed no lo define (hoy vacío), fallback a la entidad más referenciada por sus hermanas, marcada con ★ y al centro. Pendiente (sesión aparte): poblar `business_term_canonical_entity` con la entidad principal (`is_primary`) de cada término.

### METADATO-14 — Principios de representación del ER conceptual/lógico — DECIDIDO
**Decisión de fondo sobre cómo se modela y representa un ER en DATUM.** El visualizador representa un ER **conceptual/lógico**, no el modelo físico. Reglas:

1. **Las FK no se pintan como columnas.** Una relación se representa como **línea**, no como atributo. Toda FK a otra entidad se dibuja como relación, y desaparece de las columnas de la caja.
2. **Excepción — FK que además es PK (dependiente):** cuando un atributo es a la vez `pk=1` y `fk≠null`, forma parte de la identidad propagada del padre; **sí se muestra como columna PK** y además genera su línea de relación.
3. **Atributos técnicos ocultos:** `row_uuid` y `audit` no se representan en el ER conceptual.
4. **Ubicación física oculta:** toda entidad canónica lleva por construcción una FK a `physical_schema` (que aporta catálogo + esquema para el `CREATE TABLE catalogo.esquema.tabla`), materializada como la pareja `assigned_catalog_code` + `assigned_schema_code`. Esta FK de infraestructura es **universal** y se **oculta** del ER (por nombre), igual que los técnicos, para no saturar el diagrama con relaciones idénticas. No se pinta ni como columna ni como relación.
5. **Dos ejes gobiernan cada relación:**
   - **Dependencia:** *dependiente* (identifying) ⟺ la FK forma parte de la PK (`pk=1 AND fk≠null`); el padre propaga su clave a la PK de la hija; **siempre 1:N**. *No dependiente* (non-identifying) en caso contrario.
   - **Obligatoriedad:** `mandatory=1` → **1:N**; `mandatory=0` → **0:N**.
6. **Notación:** ERD estándar **pata de gallo (crow's-foot)**. Representación visual: dependiente = línea sólida; no dependiente = línea discontinua; etiqueta de cardinalidad (1:N / 0:N) y patita de "muchos" en el lado hijo.
7. **BK vs PK:** se difiere la distinción entre clave de negocio (BK, clave natural funcional) y clave técnica (PK). De momento **todo se trata como PK**; en una relación dependiente, la PK física de la hija = composición de su propia clave + la clave del padre dependiente.
8. **La estructura física no se toca:** ocultar o transformar la representación de un atributo **nunca** elimina la columna del modelo. El modelo físico permanece íntegro; solo cambia su representación visual.

Estos principios rigen el ER de cualquier término; se validan sobre el término **CATALOG** (Catálogos de Databricks) como caso de referencia.

### METADATO-15 — ER: cajas por tipo (propia / externa / catálogo) — DECIDIDO
En el ER por término, tres tipos de caja: (a) **entidad propia** del término → tabla con sus columnas propias (atributos no-FK; y la FK-PK dependiente); cada fila muestra marca PK, marca FK, `code`, `*`/punto si obligatorio y TYD; máximo 10 filas visibles con scroll interno. (b) **Entidad externa real** (FK a entidad de otro término) → caja compacta con **solo su PK**, nombrada con su tabla. (c) **Catálogo** (FK metadata-first con `reference_catalog`) → caja simulada con **solo el nombre del catálogo** (`◇ CATÁLOGO`), borde verde punteado, **una por (tabla origen + catálogo)**. Los valores del catálogo no se muestran (se iterará). Alcance: solo el ER por término; el ER por subdominio se conserva.

### METADATO-16 — Cierre del ER conceptual del término CATALOG — DECIDIDO
Se cierra la representación del término **CATALOG** aplicando METADATO-14/15 sobre la estructura real en disco (sin modificar modelo ni seed):
- **Columnas propias:** physical_catalog [code, physical_name]; physical_schema [physical_catalog_code (PK,FK dep), code, physical_name]; storage_layer [code, bucket_uri_location, sort_order]; storage_location [code, container_path].
- **Relación dependiente (1:N, sólida):** physical_catalog → physical_schema (la PK de physical_schema es compuesta [physical_catalog_code, code]).
- **No dependientes (discontinua):** physical_catalog → storage_layer, → storage_location; storage_location → storage_layer.
- **Catálogo LIFECYCLE_STATE (metadata-first):** 1:N en physical_catalog y physical_schema; 0:N en storage_location (su `lifecycle_state_code` es `mandatory=0`).
- **Ocultos:** `row_uuid`, `audit` (técnicos) y `assigned_catalog_code` + `assigned_schema_code` (ubicación física universal a physical_schema). Con ello desaparece el enjambre de relaciones redundantes catálogo↔esquema.

---
*Fin de `18-METADATO-decisiones.md` v1.1.*
