# 18 · Decisiones — Proyecto «DATUM metadato»



**Versión:** v1.16 — Julio 2026

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



### METADATO-9 — Campo técnico de sistema `TYD_SYSTEM` (universal) — DECIDIDO

Se crea el composite `TYD_SYSTEM` (definido en `datatypes.json` del visualizador, `composites`), que encapsula los tres bloques técnicos de toda tabla: ancla i18n (`row_uuid`), ciclo de vida del registro (`lifecycle_state_code`, FK a `LIFECYCLE_STATE` metadata-first) y auditoría (created_at/by, updated_at/by, is_active, version). Marcado `no_visible_er: true`. **Universalización completa**: las 193 entidades sustituyen sus atributos técnicos sueltos (`row_uuid`, `audit`, `lifecycle_state_code`) por un único atributo `system` de tipo `TYD_SYSTEM`. Se eliminan 372 atributos técnicos sueltos; cero residuales. Resuelve la falta de uniformidad previa (lifecycle solo en 31/193, row_uuid en 148/193). Seed limpiado (283 filas) de esos técnicos, que ahora materializa el bootstrap vía el composite. Representación de la FK a `LIFECYCLE_STATE` dentro del composite: pendiente de definir.



### METADATO-10 — Catálogo de propiedades Delta gobernables (`delta_property`) — DECIDIDO

Se puebla `delta_property` como catálogo de las **20 propiedades Delta gobernables por patrón** (referencia: doc oficial Databricks `delta/table-properties`, jun-2026). Cambios estructurales: (a) se añade `technical_name` (TYD_STRING, mandatory=1) para el nombre `delta.*` oficial; (b) se retira la FK de `value_logical_type_code` (queda atributo libre TYD_CODE); (c) se eliminan `allowed_values_reference_catalog_code` y `technical_default`. Atributos finales: `code` (PK), `technical_name`, `value_logical_type_code`, `system`. Las 20 propiedades: OPTIMIZE_WRITE, AUTO_COMPACT, TARGET_FILE_SIZE, DATA_SKIPPING_COLS, DATA_SKIPPING_STATS_COLS, DELETION_VECTORS, APPEND_ONLY, CHANGE_DATA_FEED, ROW_TRACKING, LOG_RETENTION, DELETED_FILE_RETENTION, SET_TXN_RETENTION, COLUMN_MAPPING, TYPE_WIDENING, ISOLATION_LEVEL, CHECKPOINT_POLICY, PARQUET_COMPRESSION, ICEBERG_COMPAT_V2, UNIFORM_FORMATS, SYMLINK_MANIFEST. Fuera del catálogo (plataforma, no gobernables por patrón): protocolo (minReaderVersion, minWriterVersion), checkpoint stats, parquet.format.version, randomizeFilePrefixes/randomPrefixLength, tuneFileSizesForRewrites, y todo `spark.databricks.*` y `pipelines.*`. Los catálogos de valores de los enumerados quedan para una 2ª pasada. Distinción auditoría: `TYD_SYSTEM` (auditoría de negocio, columna permanente, agnóstica de plataforma) es plano distinto y complementario del commit history / userMetadata / row tracking de Delta.



### METADATO-11 — Patrón `DEFAULT` obligatorio en toda entidad — DECIDIDO

Se crea el patrón `DEFAULT` en el seed de `config_pattern` (antes 0 filas; había 193 FK apuntando a un patrón inexistente), estado ACTIVE. `canonical_entity.config_pattern_code` pasa a **obligatorio** (`mandatory` 0→1): toda entidad definida debe tener patrón de configuración. Las 193 entidades quedan asignadas a `DEFAULT` en seed; cero entidades con patrón huérfano. La matriz `config_pattern_delta_default` (qué propiedad Delta activa/prohíbe cada patrón) y el resto de patrones quedan pendientes.



### METADATO-12 — Catálogos de datos: FK a acelerador, autoridades externas y limpieza — DECIDIDO

En `reference_catalog`: (a) nueva FK `canonical_accelerator_code` → `canonical_accelerator`, **obligatoria** (todo catálogo pertenece a un acelerador; no se puede definir un catálogo sin haber cargado aceleradores). En `reference_value`: (b) se eliminan `valid_from` y `valid_to` (la vigencia la da Delta vía historificación) y `external_code` (la traducción de valor por fuente se modelará como relación valor↔fuente, pendiente de especificar). Nuevo catálogo `STANDARD_AUTHORITY` en `DATUM_Catalogos.json` (estado ACTIVE, 10 valores: ISO, IETF, UN_CEFACT, ITU, IANA, SWIFT, W3C, NIST, OGC, INTERNAL), destino de `reference_catalog.external_authority_code`. `reference_category` se mantiene fija en el sistema (se puebla después).



### METADATO-13 — Saneamiento de `object_delta_override` — DECIDIDO

Se elimina el atributo `layer_code` (que era parte de la PK y apuntaba a un catálogo `layer` sin definir). La PK queda: `object_row_uuid + object_type_code + delta_property_code`. Ajuste práctico; el modelo se refinará más adelante si se requiere.



### METADATO-14 — ACCELERATOR reparentado a COMMON_STRUCTURE — DECIDIDO

El término `ACCELERATOR` pasa de colgar de `COMMON_DATA` a colgar de `COMMON_STRUCTURE` (`parent_term_code`). Motivo: como todo catálogo lleva FK obligatoria a acelerador (METADATO-12), ACCELERATOR debe residir en la estructura común base, junto a DATA_CATALOG, para garantizar el orden de carga (aceleradores antes que catálogos). Hijos de COMMON_STRUCTURE: DATA_CATALOG, ACCELERATOR, DATA_DOMAIN, I18N, ISO_CODE.



### METADATO-15 — Visualizador alineado con el metamodelo saneado — DECIDIDO

La página «Modelo canónico» se actualiza para reflejar los cambios de sesión: modelo/seed/catálogos propagados a `public/`; `TYD_SYSTEM` definido en `datatypes.json`; el ERView oculta el atributo `system` (además de la ubicación física) en el ER conceptual. Es el medio de verificación visual del estado saneado del metamodelo.



### METADATO-16 — Formato-documento canónico universal de definición de entidad — DECIDIDO

Se define el **formato-documento** como la representación exacta y universal de una entidad canónica, aplicable a las 195 tablas y a las que aporten los aceleradores. Se **deriva del modelo** (`DATUM_Modelo_Datos_Metadato.json`) que se ha ido poblando (no se puebla `canonical_attribute` en seed; el modelo ya lleva la definición de cada atributo). Estructura del documento por entidad (dos planos, análogos a PostgreSQL — propiedades DE la tabla arriba + columnas propias abajo):

- **`entity_metadata`** (cabecera): TODOS los campos de `canonical_entity` (salvo `code`, que es el nombre de la entidad), **con sus valores reales del seed** para esa tabla. Incluye `system`. Cada campo: `field`, `value`, `data_type_domain_code`, `mandatory`, `is_visible_er`, y `fk_entity` (FK a entidad) o `catalog_ref {catalog, value, metadata_only:true}` (FK a catálogo).

- **`attributes`**: las columnas propias de la entidad, cada una descrita con el **esquema de `canonical_attribute`** (no con campos improvisados). Todos los atributos, funcionales y técnicos (incl. `system`).

- **`keys`**: la PK SIEMPRE presente. UN/IX si existen.

- **`relations`**: FK a ENTIDAD (las de catálogo van en el atributo como `catalog_ref`), con mapeo de atributos source→target. Incluye las relaciones técnicas universales (ver METADATO-19).

- **`constraints`**: siempre a nivel de ENTIDAD (validaciones de negocio con N atributos).

- **`partitions`**: cabecera + detalle de particionamiento.

El visualizador se ajusta a estos JSON, no al revés. Documento piloto validado: **CATALOGOS DE DATOS** (término DATA_CATALOG: reference_category, reference_catalog, reference_value). Generalización término a término, saneando FK de cada uno en su tanda.



### METADATO-17 — Eliminación de `canonical_attribute_constraint` — DECIDIDO

Se elimina la tabla `canonical_attribute_constraint` (del modelo y del seed). Motivo: las restricciones por atributo ya están definidas a nivel de **TYD** (el tipo trae su regex, longitud, obligatoriedad). Las constraints de negocio son siempre a nivel de ENTIDAD (`canonical_entity_constraint` + `canonical_entity_constraint_attribute`), y una constraint puede usar N atributos. Verificado: sin FK entrantes, eliminación limpia. Total entidades: 195→194.



### METADATO-18 — Esquema de `canonical_attribute`: `is_visible_er` y eliminación de `physical_column_name` — DECIDIDO

(a) Se añade a `canonical_attribute` el flag **`is_visible_er`** (TYD_BOOLEAN, mandatory=1): controla si el atributo se pinta en el ER. La visibilidad ER **se mueve al metamodelo** (dato), dejando de ser lógica hardcodeada en el visualizador. El ERView pasa a leer `is_visible_er` del atributo (función `isHidden` que combina flag + fallback HIDDEN). (b) Se elimina `physical_column_name`: es el propio `code` del atributo; la nomenclatura física se aplicará después (en el peor caso, columna computada generada automáticamente). (c) La ocultación de la FK de catálogo para crear la tabla NO es un flag nuevo: ya está cubierta por `catalog_ref_metadata_only` (FK definida en metadato, oculta como FK física ejecutable, integridad por DQ). Esquema final de `canonical_attribute` (16 campos): canonical_entity_code, code, attribute_order, is_visible_er, data_type_domain_code, materialization_mode_code, referenced_entity_code, is_pii, is_sensitive, security_classification_code, is_nullable, column_default, is_auto_increment, is_generated, generation_expression, regex_pattern_override, system.



### METADATO-19 — Reincorporación de `physical_catalog_code` y relaciones técnicas universales — DECIDIDO

Se reañade **`physical_catalog_code`** (FK a `physical_catalog`, mandatory=1) a `canonical_entity`: aunque redundante con la PK compuesta de `physical_schema` [physical_catalog_code, code], el documento debe llevar todas las columnas explícitas (la visualización solo representa, no resuelve). Toda entidad canónica tiene FK universales aplicables a las 195 tablas: **término** (business_term_code), **patrón Delta** (config_pattern_code) y **ubicación física** (physical_catalog_code + physical_schema_code, FK compuesta de 2 columnas). Estas columnas van en `attributes`/`entity_metadata` marcadas `is_visible_er:false`, y sus relaciones en `relations` marcadas `relation_type:technical`, `is_universal:true`, `is_visible_er:false`. La relación a physical_schema mapea 2 columnas (catálogo + esquema). Seed: 194 entidades con physical_catalog_code=metadato.



### METADATO-20 — Patrón de visualización maestro-detalle (UX auto-generada) — DECIDIDO

Se establece el **patrón de presentación por entidad canónica** = UX auto-generada de las aplicaciones DATUM. Es **solo presentación** del documento JSON, **sin lógica**. Estructura: cabecera (definición/metadatos de la entidad) + bloque i18n + pestañas Atributos / Keys / Relations / Constraints / Partitions + botón Editar (→ wizard con un paso por bloque, pendiente). Dos principios sobre el multiidioma: (a) el i18n **no se gestiona desde esta ficha**, sino desde el multiidioma general de la aplicación (tabla polimórfica `object_text` por `object_row_uuid`+`object_type_code`, tres `text_field_kind`: SHORT=rótulo UI, SUMMARY=descripción, FUNCTIONAL=detalle, en es/en/fr/pt); la ficha lo consume. (b) **Cada texto de la visualización va por multiidioma, y en general por SHORT** — los rótulos de la propia UX (campos, pestañas, cabeceras) se resuelven por i18n tomando SHORT en el idioma activo; no son literales quemados. Pendiente: llevar el mockup a página real Next.js `/dashboard/entidad/[code]` y construir el wizard de edición.



### METADATO-21 — Reorganización del seed en N ficheros por naturaleza — ACORDADO (pendiente de ejecución)

Se acuerda que la carga de datos debe separarse en N ficheros por naturaleza (no en un `DATUM_Carga_Inicial_Metadato.json` monolítico): **catálogos de datos**, **tipos de datos** (TYD), **definiciones según estructura canónica** (formato-documento), **carga inicial** del resto de estructuras según su modelo. Es objetivo posterior al cierre del formato-documento. La definición estructural (documento por acelerador: acelerador→términos→entidades en formato-documento) es plano distinto de la carga de datos.



### METADATO-22 — Formato-documento canónico jerárquico autocontenido en las tablas del término — DECIDIDO

El documento canónico de una entidad **autocontiene la entidad en las tablas del término CANONICAL_ENTITY**, con estructura jerárquica (no plana): `code` (raíz, nombre de la entidad) + `entity{}` (metadatos: todos los campos de canonical_entity con sus valores reales del seed, incluido `system`) + `children{}` con arrays `attributes[]`, `keys[]` (cada key con su `columns[]`), `relations[]` (cada una con `attribute_map[]`), `constraints[]`, `partitions[]`. Solo se incluyen los valores de los que dispone la entidad; arrays vacíos si no aplica. Se deriva del modelo (`DATUM_Modelo_Datos_Metadato.json`), no se inventa nada. Dos planos análogos a PostgreSQL: propiedades DE la tabla (entity) + columnas propias (attributes). Documentos de referencia: `_documento_reference_category.json` (entidad simple) y `_documento_canonical_entity.json` (entidad rica con relaciones — referencia canónica del formato). Distinción de planos: ER funcional (metadata-first, `system` como unidad, FK a catálogo declaradas no ejecutables) vs. estructura física (`system` descompuesto en 8 columnas, FK a catálogo materializadas sin constraint, integridad DQ). El plano físico es el que se compila a DDL.



### METADATO-23 — Simplificación del término: relaciones, particiones, constraints — DECIDIDO

Reducción del término CANONICAL_ENTITY para expresar solo lo necesario. **Relaciones:** eliminada `canonical_relation_end` (rol/cardinalidad en dos filas → innecesario) y `relation_kind_code` (redundante); la cardinalidad pasa a campo único `cardinality_code` en `canonical_relation` (FK a nuevo catálogo CARDINALITY_REL {0:N, 1:N, 0:1, 1:1}); se mantiene `is_identifying`; se conserva `canonical_relation_attribute_map` (mapeo source→target, soporta FK compuesta). **Particiones:** eliminadas las 2 tablas (`canonical_entity_partition`, `canonical_entity_partition_attribute`); `partition_strategy_code` (FK cat PARTITION_STRATEGY, default NONE, no visible ER) pasa a `canonical_entity`; `partition_order` (TYD_INT, nullable, null=no participa) pasa a `canonical_attribute`. **Constraints:** `canonical_entity_constraint` representa validaciones de negocio con expresión (tipo CHECK); eliminado `constraint_type_code` (siempre sería CHECK); eliminada `canonical_entity_constraint_attribute` (los atributos participantes ya están en la `expression`; el DQ la parsea). Total entidades: 194→190. Término: 11→7 tablas.



### METADATO-24 — Eliminaciones adicionales en canonical_attribute — DECIDIDO

(a) Eliminado `referenced_entity_code` de `canonical_attribute`: la referencia a otra entidad cuando el atributo es FK se expresa **mediante `canonical_relation`** (+ attribute_map), no como atributo. Se conserva la FK identificativa `canonical_entity_code` (pertenencia). (b) Eliminado `materialization_mode_code` (no contemplado). Confirmado en revisión contra el Excel de definición del término aportado por Pedro (`Modelo_Termino_Canonical_Entity.xlsx`).



### METADATO-25 — Ajuste del término a la definición del Excel (nombres y campos) — DECIDIDO

Ajustes de nombres/campos para cuadrar con `Modelo_Termino_Canonical_Entity.xlsx`: `canonical_key` sin `is_used_for_matching`. `canonical_key_attribute`: +`canonical_entity_code` (PK), −`referenced_attribute_code`, −`partition_transform`. `canonical_relation`: `source_canonical_entity_code`→`canonical_entity_code`, `target_canonical_entity_code`→`reference_canonical_entity_code`. `canonical_relation_attribute_map`: `target_attribute_code`→`reference_attribute_code`, +`canonical_entity_code` (PK), +`orden`. `canonical_attribute.data_type_domain_code` → FK a `data_type_domain_simple`. La FK a `physical_schema` se declara como **una FK compuesta** (physical_catalog_code + physical_schema_code → physical_schema[physical_catalog_code, code]), no dos sueltas.



### METADATO-26 — Patrón de entidades dependientes (weak entities) con FK identificativas compuestas — DECIDIDO

Patrón general universal (modelo y visualización): entidad canónica (padre) → N hijos dependientes → hijos de los hijos, propagando la PK del padre por la jerarquía. **PKs:** canonical_entity `[code]`; canonical_attribute/canonical_key/canonical_entity_constraint/canonical_relation `[canonical_entity_code, code]`; canonical_key_attribute `[canonical_entity_code, canonical_key_code, canonical_attribute_code]`; canonical_relation_attribute_map `[canonical_entity_code, canonical_relation_code, source_attribute_code]`. **FK identificativas compuestas:** hijos directos → FK identifying a canonical_entity; canonical_key_attribute → FK compuestas identifying a canonical_key `[canonical_entity_code, canonical_key_code]` + canonical_attribute `[canonical_entity_code, canonical_attribute_code]`; canonical_relation_attribute_map → FK compuesta a canonical_relation + 2 a canonical_attribute (source identifying, reference no). `on_delete`/`on_update` = RESTRICT. Estructura FK compuesta en el modelo: campo `fk_composite {target, columns[{source,target}]}` + `is_identifying`. Este patrón sirve tanto para el modelo de datos (integridad) como para la UX (árbol padre→hijos→nietos).



### METADATO-27 — Ficha de entidad integrada en el árbol del visualizador — DECIDIDO

La ficha de entidad canónica (patrón METADATO-20) se integra **dentro del árbol** de `/dashboard/canonico` (no en página aparte): al pulsar una entidad, el panel de detalle muestra la ficha completa (reemplaza el detalle anterior). Estructura: cabecera (code + catálogo físico + esquema físico, del seed) + bloque i18n (3 campos SHORT/SUMMARY/FUNCTIONAL, cada uno con el code de la entidad — **sin ejecutar multiidioma**) + pestañas navegables (Atributos por defecto): **Atributos** muestra TODOS los campos (funcionales y técnicos, obligatorio mostrarlos con independencia de is_visible_er), con `system` **descompuesto** en sus 8 columnas físicas (row_uuid, lifecycle_state_code, created_at, created_by, updated_at, updated_by, is_active, version), obligatorio, default, referencia a catálogo (metadata-first, en el propio atributo), visibilidad ER; **Constraints**; **Keys** (PK/UN/IX con detalle de columnas); **FKs** (solo FK a entidad reales, con mapeo, detectando compuestas). Las referencias a catálogo NO son FK y van en Atributos; las FK a entidad van solo en la pestaña FKs. La ficha lee del modelo en disco; es plantilla universal para las 190 entidades.



### METADATO-28 — Saneamiento y modelado semántico del término BUSINESS_TERM — DECIDIDO

Revisión completa del término BUSINESS_TERM sobre el estado real en disco. Bloque de cambios:

**(a) FK identificativas de las dependientes:** las FK que forman PK de las tablas puente se marcan `fk_composite {target, columns[{source,target}]}` (1 columna, PK simple del padre) + `is_identifying:true` + `on_delete`/`on_update`=RESTRICT, conforme al patrón weak-entity de METADATO-26. **(b) FK a catálogo metadata-first:** las FK a `reference_value` del término se uniforman al contrato `reference_catalog`=<CAT> + `catalog_ref_metadata_only:true` (dejan de dibujarse como FK/relación; se representan como catálogo en Atributos, coherente con METADATO-12/16/18). **(c) Corrección de visibilidad ER:** la FK identificativa `business_term_code` de las puentes tenía `is_visible_er=false` (incoherente con sus columnas identificativas hermanas), lo que impedía dibujar la línea de dependencia; se fija `is_visible_er=true`. Defecto de dato, no de código; el visualizador ya soportaba `fk_composite`/`is_identifying`/`reference_catalog` sin tocar `.tsx`. **(d) Eliminación de 3 tablas puente** (hojas, sin FK entrantes → eliminación limpia): `source_entity_business_term` (cruzaba D2↔D3; el vínculo fuente→término es linaje y vive en D4/transformaciones, como declara su propio desc; resto de la `critical_entity` disuelta); `business_term_canonical_entity` (redundante con la columna directa `canonical_entity.business_term_code` 1:N — principio de simplificación); `canonical_attribute_business_term` (glosario se gestiona a nivel entidad, no atributo). Se retiran del alcance los catálogos que solo usaban esas tablas: `TERM_ENTITY_ROLE`, `ATTRIBUTE_MAPPING_KIND`, `SOURCE_COVERAGE_KIND` (nunca poblados). **Total entidades: 190→187.** **(e) `business_term_related` remodelado como grafo semántico de negocio (E-R conceptual entre términos), espejo de `canonical_relation` en el plano D2:** se elimina `relation_type_code` y su catálogo `TERM_RELATION_TYPE` (nunca poblado); el arco se tipa por **cardinalidad** reutilizando el catálogo existente `CARDINALITY_REL` (0:N,1:N,0:1,1:1), ahora compartido por `canonical_relation` (físico) y `business_term_related` (semántico). Arco nombrado por `code` (discriminador técnico, PK; el nombre legible va por i18n — sin descripción embebida), permitiendo N arcos por par (VENTA→CLIENTE, VENTA→RESTAURANTE, VENTA→CANAL). **Nombres de las dos FK a business_term alineados al patrón de `canonical_relation`:** lado identificativo `business_term_code` (propaga identidad) + lado destino `reference_business_term_code`. **Estructura final del término (3 tablas):** `business_term` (núcleo, 8 atributos + system); `business_term_synonym` (PK [business_term_code, synonym]); `business_term_related` (PK [business_term_code, code]; reference_business_term_code FK no-identifying; cardinality_code→CARDINALITY_REL). Verificado: 187 entidades, JSON válido, build OK. Visualización: solo cambian los JSON de datos (`public/datum_modelo_canonico.json`, `public/datum_carga_inicial.json`); ningún `.tsx`. **(f) Saneamiento de catálogos huérfanos por la remodelación de CANONICAL_ENTITY:** eliminados 6 catálogos sin uso (declaración en `DATUM_Catalogos.json` + cabecera `reference_catalog` + valores `reference_value` del seed): `RELATION_KIND`, `RELATION_END_ROLE`, `CONSTRAINT_TYPE`, `MATERIALIZATION_MODE`, `EXPRESSION_ROLE` (todos residuales de METADATO-23/24) y el viejo `CARDINALITY` {ONE,MANY} (su tabla `canonical_relation_end` fue eliminada). Además, **`CARDINALITY_REL` renombrado a `CARDINALITY`** (el sufijo _REL era solo para distinguirlo del viejo): catálogo {0:N,1:N,0:1,1:1} + sus 2 referencias en el modelo (`canonical_relation.cardinality_code`, `business_term_related.cardinality_code`). Catálogos: 16→10. Se conservan por decisión los huérfanos `LIFECYCLE_STATE` (falso positivo: se usa vía composite TYD_SYSTEM), `ASSESSMENT_TYPE` (CUARENTENA) y `MAPPING_CONDITION_KIND` (tabla `mapping_condition` viva). Pendiente: poblar valores seed de `CARDINALITY` (0:N,1:N,0:1,1:1), hoy sin filas en reference_value.



### METADATO-29 — Saneamiento y cierre del término DATA_TYPE_DOMAIN (tipos de datos) + tipología de validación DQ — DECIDIDO

Revisión completa del término de tipos de datos sobre el estado real en disco. Bloque de cambios (total entidades: 187→187; catálogos: 10→14):



**(a) Renombrado `data_type_domain_simple` → `data_type_domain`.** El sufijo `_simple` subestimaba su papel: es el nodo central del término (12 FK entrantes desde canonical_attribute, source_attribute, rule_attribute, mapping_attribute, discovery_rule, etc.). El composite pasa a ser el caso nombrado explícitamente. Rename propagado a: clave de entidad, 12 `fk_target` (incl. self `parent_domain_code`), y la fila de registro en `seed.canonical_entity`.



**(b) Nuevos atributos en `data_type_domain`** (defaults DDL heredables al atributo, semántica de herencia: nullable/default null = "el dominio no fuerza, decide el atributo"): `is_pii_by_default`, `is_sensitive_by_default`, `is_nullable_by_default`, `is_auto_increment_by_default`, `is_generated_by_default` (TYD_BOOLEAN); `column_default`, `generation_expression` (TYD_EXPRESSION). Renombrado `classification_code`→`security_classification_code` con contrato metadata-first (→SECURITY_CLASSIFICATION), idéntico a `canonical_attribute`.



**(c) Internacionalización (i18n de formato):** dos catálogos nuevos referenciados desde `data_type_domain` (metadata-first) para el formato canónico, agnóstico del valor almacenado: `DATE_FORMAT` {YMD, DMY, MDY} (`date_format_code`) y `DECIMAL_FORMAT` {DOT_COMMA, COMMA_DOT, COMMA_SPACE, DOT_NONE} (`decimal_format_code`). El formato es propiedad de presentación/parseo, no del valor.



**(d) `data_type_domain_composite` reducido a `code` + `system`.** Eliminado `materialization_code` (la materialización de un composite es SIEMPRE EMBEDDED → constante, no se modela; catálogo MATERIALIZATION no creado) y `classification_code` (redundante: la clasificación emerge de los campos, cada uno referencia un dominio que ya la declara). El composite se define íntegramente por sus campos.



**(e) `data_type_domain_field`: renombres de claridad + eliminación de `cardinality_code`.** `composite_code`→`data_type_domain_composite_code` (FK identificativa, RESTRICT); `referenced_simple_code`→`data_type_domain_code`. Eliminado `cardinality_code` (dado EMBEDDED, un campo de composite no es array). Cada campo referencia UN dominio, sin anidamiento.



**(f) Sustitución de `data_type_domain_dq_rule` por `data_type_domain_validation`.** La tabla puente `data_type_domain_dq_rule` tenía una FK colgante a `dq_rule` (entidad inexistente; cross-dominio D6 nunca materializado). Se elimina y se sustituye por `data_type_domain_validation`: N reglas de validación tipadas por dominio, cada una con `expression` (COMPOSITE TYD_EXPRESSION kind+content: REGEX de formato o SQL_SPARK de check tipo `importe>=0`) + `error_message_text`. Coherente con el patrón heredado "reglas DQ derivadas del metamodelo, no modeladas como tabla en D6": la regla DQ se COMPILA desde aquí. Eliminado en consecuencia `regex_pattern` de `data_type_domain` (el formato pasa a ser una validación de dimensión VALIDITY).



**(g) Tipología de validación anclada al gobierno de calidad de D6 (no ad-hoc).** `data_type_domain_validation.dq_dimension_code` (metadata-first) tipa cada validación contra la dimensión de calidad canónica **DAMA-DMBOK**, materializada como catálogo nuevo `DQ_DIMENSION` {COMPLETENESS, VALIDITY, ACCURACY, CONSISTENCY, UNIQUENESS, TIMELINESS}. Se materializa además el catálogo `ISO_CHARACTERISTIC` (ISO/IEC 25012 inherentes) {ACCURACY, COMPLETENESS, CONSISTENCY, CREDIBILITY, CURRENTNESS, PRECISION, CONSISTENCY_SEMANTIC}. Con ello se cierran de paso las dos FK colgantes preexistentes de `dq_dimension_to_iso_characteristic` (dimension_code→DQ_DIMENSION, iso_characteristic_code→ISO_CHARACTERISTIC), ambas metadata-first. No se modela tabla de reglas en D6 (lectura (a) confirmada por Pedro): D6 aporta la tipología; la validación del dominio la referencia.



**(h) `data_type_domain_validation` con dueño polimórfico (SIMPLE y COMPOSITE).** Para que un composite pueda declarar reglas de validación COMPLETAS que cruzan varios de sus campos (ej. `fecha_fin>fecha_inicio`; `si country='ES' → zip ^[0-9]{5}$`), la tabla adopta el patrón de dueño polimórfico ya establecido en `expression`/`dimension`: PK `[owner_object_row_uuid, owner_object_type_code, code]`, con `owner_object_type_code`→`object_type` discriminando DATA_DOMAIN / DATA_DOMAIN_COMPOSITE. Una sola tabla de validaciones sirve a ambas naturalezas, sin duplicar estructura (opción B; descartadas A=tabla gemela y C=fusión simple/composite).



**(i) `data_type_domain_ui_control` en CUARENTENA.** El plano de presentación (contexto×control) y sus catálogos UI_CONTEXT/UI_CONTROL se aplazan a la revisión de D10; la tabla se conserva marcada (type=CUARENTENA), no eliminada, con sus 2 FK a catálogo aún sin sanear (congeladas con ella).



Verificado: 187 entidades, JSON válido, invariante seed↔modelo OK (todo `code` de seed.canonical_entity existe en model.entities — defecto que causó un TypeError de render en sesión intermedia, corregido al eliminar la fila puente del seed y añadir la de validation), FK metadata-first sin roturas, patrón `owner_*` idéntico a `expression`. Visualización (demo): cambian solo los JSON de datos (`public/datum_modelo_canonico.json`, `public/datum_catalogos.json`, `public/datum_carga_inicial.json`) y el volcado ER propio de la demo (`src/data/metamodel.json`); ningún `.tsx`.



**Pendientes que quedan preparados (sesión propia):** validación contextual por país×tipo (identificador nacional) vía condición de aplicabilidad; campos de composite con FK a entidad del metamodelo (TYD_ADDRESS→country, country_subdivision, currency) mediante `fk_target_entity_code` XOR `data_type_domain_code`; poblar `object_type` con DATA_DOMAIN/DATA_DOMAIN_COMPOSITE en seed; poblar el mapeo dimensión↔característica en `dq_dimension_to_iso_characteristic`; revisión de `data_type_domain_ui_control` en D10; posible renombrado de `data_type_domain_validation` (valida simple y composite).



### METADATO-30 — Dimensión GEOGRAPHY, refactor ORG_STRUCTURE/GOVERNANCE y patrones de workflow (D07) — DECIDIDO



Sesión amplia sobre tres bloques: incorporación de la geografía al metamodelo, replanteamiento del gobierno organizativo, y arranque (incompleto) de los patrones de workflow. Total entidades: 187→202; catálogos: 14→25.



**(a) Dimensión GEOGRAPHY incorporada al término GEO_STRUCTURE (bajo HIERARCHY).** Sobre los ficheros de diseño aportados por Pedro (`datum_dimension_GEOGRAPHY.json`, `datum_geografia_demo.json`): grano base único (locality), 3 jerarquías paralelas (ADMINISTRATIVE estándar, COMMERCIAL configurable N:M, FISCAL_TERRITORY por norma), con `country` como nivel pivote de cross-links. Inyectadas 11 entidades nuevas bajo GEO_STRUCTURE: `continent`, `supra_zone`, `region`, `province`, `locality`, `commercial_hierarchy`, `commercial_level`, `commercial_member`, `tax_jurisdiction`, `tax_regime`, `tax_jurisdiction_geo`.



**(b) Jerarquía administrativa como weak entities dependientes (patrón temporal_level, METADATO-26).** PK propagado hacia abajo: continent `[code]` → supra_zone `[continent_code, code]` → country `[code]` (pivote, NO weak) → region `[country_code, code]` → province `[country_code, region_code, code]` → locality `[country_code, region_code, province_code, code]`. Cada FK que forma PK: UNA FK compuesta (`fk_composite.columns[]`) + `is_identifying:true` + RESTRICT + mandatory, NO columnas partidas en varias FK. `country` mantiene PK simple (es pivote referenciado por temporal/cross-links); relación con supra_zone vía FK NO dependiente compuesta (`continent_code`+`supra_zone_code` → supra_zone). Quitada la FK redundante country→continent (el continente se deriva por country→supra_zone→continent).



**(c) Unificación bajo GEO_STRUCTURE + eliminación de `country_subdivision`.** Las 5 entidades que estaban en ISO_CODE (`country`, `language`, `currency`, `unit_of_measure`) movidas a GEO_STRUCTURE por decisión de Pedro (unificar criterios); ISO_CODE queda vacío. `country_subdivision` ELIMINADA (redundante: region/province/locality ya son entidades propias; solo se auto-referenciaba, 0 FK reales entrantes → eliminación limpia). `unit_of_measure` marcada CUARENTENA (no es geografía, sin relaciones claras — revisar si debe existir).



**(d) Comercial y Tax ancladas a la geografía, con puentes polimórficos.** `commercial_member` y `tax_jurisdiction_geo` NO flotan sueltas: son puentes N:M polimórficos (patrón proyecto `*_row_uuid` + `*_type_code`) que anclan a country/region/province/locality. `commercial_member`: FK dependiente compuesta a commercial_level + `member_row_uuid` (polimórfico) + `geo_level_code`→GEO_LEVEL. `tax_jurisdiction_geo`: FK dependiente a tax_jurisdiction + `geo_row_uuid` (polimórfico) + `geo_level_code`→GEO_LEVEL. `commercial_level` con self-parent (`parent_level_code`). Corregido el mal uso previo de `object_type` para geografía (object_type es catálogo interno CANONICAL_ENTITY/KPI/…): se crea catálogo `GEO_LEVEL` {COUNTRY, REGION, PROVINCE, LOCALITY}. Ejemplos validados: COMERCIAL="Ventas EMEA" con zona "Europa del Sur"=ES+IT+PT+GR (N:M, no admin); TAX="ES-País Vasco foral" (jurisdicción no 1:1 admin); cross-link FISCAL_TERRITORY→TIME cierra el pendiente de festivos/periodo fiscal de la dimensión temporal.



**(e) Refactor ORG_STRUCTURE: madurez/criticidad fuera de business_unit (van al motor de evaluación).** Detectado por Pedro: `maturity_level_code`, `maturity_target_code`, `is_critical` NO son atributos de business_unit — son RESULTADO de evaluación. Se QUITAN de `business_unit` y también `is_critical` de `business_process` (coherencia). Se evalúan vía `object_assessment` (polimórfico) + `assessment_pattern`, cuyo `ASSESSMENT_TYPE` ya incluye MATURITY/CRITICALITY. SE QUEDA `topology_code` (config de diseño de gobierno, no evaluación) gestionado con catálogo `GOVERNANCE_TOPOLOGY` {CENTRALIZED, FEDERATED, HYBRID, DELEGATED}. Creados catálogos gestionados `BUSINESS_UNIT_KIND` {C_LEVEL (raíz negocio datos), DIVISION, AREA, DEPARTMENT, TEAM} y `MATURITY_LEVEL` {INITIAL, MANAGED, DEFINED, QUANTITATIVELY_MANAGED, OPTIMIZING} (como level_reference_catalog del assessment_pattern MATURITY). Principio consolidado: la información de gobierno (madurez/calidad/criticidad) vive en el motor de evaluación asociada polimórficamente a CUALQUIER nivel (org/unidad/proceso/término/entidad); business_unit raíz (parent=null, kind=C_LEVEL) define el perímetro del negocio de datos.



**(f) business_rule → término DATA_QUALITY.** Movida de ORG_STRUCTURE a DATA_QUALITY (su desc dice "se evalúan como DQ"; forman la madurez del dato). Relaciones finas se ajustan al trabajar calidad.



**(g) Roles de gobierno como asignación polimórfica en GOVERNANCE.** `business_unit_role_assignment` rediseñada como `governance_role_assignment` y movida al término GOVERNANCE. Los roles NO generan jerarquía (son catálogo de perfiles; la jerarquía la da business_unit.parent). Patrón polimórfico: `object_row_uuid` + `object_type_code` (gobierna CUALQUIER objeto: unidad/dominio/término/entidad/producto) + `role_profile_code`→`BUSINESS_ROLE_PROFILE` {DATA_OWNER (1 por objeto), DATA_STEWARD (N), DATA_CUSTODIAN, DATA_CONSUMER} + `idp_role_ref` (rol del IdP, NO la persona) + vigencia. Integridad por DQ.



**(h) frequency_code → catálogo genérico FREQUENCY (reutilizado).** `business_process.frequency_code` apuntaba a reference_value sin catálogo. Renombrado `SOURCE_FREQUENCY`→`FREQUENCY` (genérico, reutilizable por source y process); actualizadas todas las referencias en modelo Y seed (`reference_catalog` + `reference_value`, 7 filas), y `canonical_entity.access_frequency_code`. Cero residuos.



**(i) D07 (patrones de workflow) → ORG_STRUCTURE.** `workflow_pattern` y `workflow_pattern_step` movidas de METADATA a ORG_STRUCTURE (coherente: business_process ya referencia workflow_pattern). Añadido `scope_level_code`→`WORKFLOW_SCOPE` {ENTITY, TERM, PROCESS} al step (la imagen real de Pedro muestra runners a 3 niveles: entidad 1-5, término 10-11, proceso 90-91). Declarados gestionados `runner_type_code`→`RUNNER_TYPE` {RUNNER_INGEST, RUNNER_TRANSFORM, RUNNER_DQ, RUNNER_LOAD_CANONICAL, RUNNER_KPI, RUNNER_DQ_TERM, RUNNER_KPI_HIERARCHY, RUNNER_DQ_PROCESS, RUNNER_KPI_PROCESS} y `purpose_code`→`WORKFLOW_PURPOSE`.



**(j) [ATENCIÓN] Patrones y steps de workflow: modelado PROVISIONAL, requiere una gran vuelta — NO está controlado.** El modelado actual de `workflow_pattern` / `workflow_pattern_step` NO refleja todavía el concepto real de Pedro y debe replantearse por completo en sesión propia. Puntos abiertos identificados pero NO resueltos: (1) el "patrón" para Pedro es la CONJUNCIÓN de las escalas entidad+término+proceso en un mismo workflow_pattern (no capas separadas; se descartó la idea de "instancia"); (2) un runner NO es atómico: cada runner debe DETALLAR qué steps concretos ejecuta, enganchando con los pasos YA modelados en D3 (sources: runner_ingest_managed/streaming), D4 (transformación: transformation_pipeline_step) y D6 (calidad: dq_evaluation_specification) — el patrón COMPONE, no duplica; (3) sin decidir: si el enganche runner→dominio es por TIPO (genérico, patrón reutilizable) o al paso CONCRETO (específico del proceso) o solo declarando runner_type. Los catálogos WORKFLOW_SCOPE/RUNNER_TYPE/WORKFLOW_PURPOSE y el campo scope_level_code quedan como andamiaje provisional, sujetos a revisión total. **Abrir sesión específica para D07 patrones/steps.**



Verificado en cada paso: JSON válido, invariante seed↔modelo OK (todo `code` de seed.canonical_entity existe en model.entities), FK reales sin colgar (las polimórficas `(polimórfico)`/`(D8)` no cuentan como colgantes), build Next.js OK. Visualización: nueva pestaña Geografía (3 jerarquías: ADMIN poblada + COMMERCIAL/FISCAL estructura + rama "Estructura canónica" de verificación) y pestaña Dominios de tipo; cambios en JSON de datos de la demo. **Sin registro oficial en disco**: outputs con 202 entidades / 25 catálogos; pendiente de canonización por Pedro.



---

---

### METADATO-31 — Rediseño integral del dominio D3 (DATA_SOURCE): SOURCE_TABLES, DISCOVERY, TECHNOLOGY y reorganización de términos — DECIDIDO



**(a) Rediseño del dominio D3 bajo el acelerador DATA_SOURCE, dividido en términos de negocio.** El antiguo D3 (con conectividad, especializaciones por tipo y captura mezcladas) se rediseña bajo el principio "el metamodelo modela *qué*, no *cómo* (el runner)". DATA_SOURCE agrupa 4 términos hijos: **SOURCE_SYSTEM** (`source_system`, `source_container`), **SOURCE_TABLE** (`source_entity`, `source_attribute`, `source_key`, `source_key_attribute`, `source_relation`, `source_relation_attribute_map`), **SOURCE_INGESTION** (`source_entity_capture`, `source_entity_capture_attribute`, `source_entity_extraction_filter`), **DISCOVERY** (`discovery_template`, `discovery_template_object`, `discovery_view_column`, `discovery_field_mapping`).



**(b) Tres niveles de contención (system→container→entity) como weak entities.** `source_system` (a dónde me conecto: system_kind, technology, connection_secret_ref opaco — SIN business_unit ni environment, que son de la canónica y del Data Plane respectivamente). `source_container` (jerarquía de contención autorreferente de profundidad libre; BK = `parent_container_code`+`code`, Opción 2; PK propagada de system). `source_entity` (la tabla origen ≈ canonical_entity, decisión B: misma forma, información diferente; cuelga del container hoja). PK propagada en cascada con FK identificativas compuestas (patrón METADATO-26). Eliminadas: 3 tablas de conectividad, 9 de especialización por tipo, 3 satélite de API, `multi_record`, `source_entity_partition_strategy`, `source_entity_relation` (→ `source_relation`). FK de `mapping_condition` repuntada a `source_relation`.



**(c) Captura e ingesta.** `source_entity_capture` (1:1 con entity: capture_mode FULL/INCREMENTAL/CDC, landing, cdc_mechanism). `source_entity_capture_attribute` (nieto de capture, NO de entity; FK a source_attribute; SIN rol — el capture_mode determina el significado). `source_entity_extraction_filter` (filtro declarativo INITIAL/INCREMENTAL). Proyección por atributo (`is_selected`). El "parámetro" no es entidad: se reparte en filtro (qué) / runner (cómo) / secreto (custodia). Sin `source_entity_constraint` (en origen no se validan datos; DQ es post-transformación).



**(d) Tipo de dato por tecnología.** `source_attribute` referencia `data_type` (D0, PK [technology_code, code]) vía `native_data_type_code` + descomposición (native_length/precision/scale); eliminados `logical_type_code` (+catálogo LOGICAL_TYPE) y `data_type_domain_code` (el dominio semántico es gobierno D2/D4, no origen). Fechas/números tipados se replican origen→Delta sin conversión; solo VARCHAR requiere charset/collation (propiedad de database y override por atributo).



**(e) Término DISCOVERY: plantillas de autodescubrimiento por tecnología.** `discovery_template` (weak de `technology`; has_server_catalog marca fase 0 — SQL Server enumera databases desde master.sys.databases; root_container_kind). `discovery_template_object` (qué vista de catálogo leer: metadata_schema + catalog_view_name + object_scope SERVER/DATABASE + target_entity_code que declara contra qué tabla de DATA_SOURCE mapea). Dividido el mapeo en dos tablas por naturaleza: **`discovery_view_column`** (definición objetiva de las columnas de la vista de catálogo) y **`discovery_field_mapping`** (transformación: source_column_name FK a view_column XOR fixed_value → target_field). Seed poblado para SQL Server, PostgreSQL, MySQL, Oracle (4 templates, 37 objetos, 155 columnas de vista, 172 mapeos). Enriquecidos `source_container` DATABASE (charset/collation), `source_entity` (row_count, size_bytes, has_native_partitioning, native_partition_column, stats_collected_at) y `source_attribute` (charset, collation, distinct_count, null_count, min/max_value, max_length_observed) como campos directos (Opción A: la definición es la base para recrear en Delta). Catálogos nuevos: OBJECT_SCOPE, DISCOVERY_OBJECT_KIND, CAPTURE_MODE, LANDING_STRATEGY, CDC_MECHANISM, EXTRACTION_FILTER_MODE, EXPRESSION_DIALECT, CONTAINER_KIND, SOURCE_ENTITY_KIND, SOURCE_SYSTEM_KIND, SCOPE_REASON, TECHNOLOGY_CATEGORY (todos en 3 capas). charset/collation como texto libre. Pendiente sesión siguiente: versionado + diff/drift del re-descubrimiento.



**(f) Término TECHNOLOGY (bajo COMMON_STRUCTURE).** Movidas `technology`, `data_type`, `data_type_mapping` (esta última desde DATA_DOMAIN); `generic_data_type` permanece en DATA_DOMAIN. `technology.category_code` asociado a catálogo TECHNOLOGY_CATEGORY (metadata-first). Eliminado término vacío ISO_CODE.



**(g) Reorganización de términos.** ORG_STRUCTURE, BUSINESS_PROCESS, DATA_QUALITY, TRANSFORMATION movidos bajo COMMON_DATA. ORG_STRUCTURE queda solo con `business_unit`; `business_process`, `business_process_term`, `workflow_pattern`, `workflow_pattern_step` movidos a BUSINESS_PROCESS (workflow_* con domain vaciado, bug de doble vista corregido).



**(h) Término TRANSFORMATION (todo el dominio D4) dividido por capas.** Padre TRANSFORMATION + 3 hijos: **TRANSFORMATION_DEFINITION** (19: rules+versions+parameters, mappings+versions, mapping_input/output/condition, attributes de extensión, pipeline+step+dependency como DAG diseñado, source_attribute_canonical_attribute_map, reference_mapping_set*), **TRANSFORMATION_EXECUTION** (3: transformation_run, transformation_run_step, compiled_ddl), **TRANSFORMATION_SECURITY** (2: masking_config, encryption_config). Separa definición de ejecución.



**(i) Visualización.** Nueva pestaña `/dashboard/plantillas-discovery`: por tecnología muestra template, objetos (schema.vista, scope, target), con toggle Definición-de-vista / Transformación-al-modelo. Solo cambian JSON de datos + la nueva página + nav.config + translations; ficheros del núcleo del visualizador (`canonico`) sin cambios de lógica (solo limpieza de `multi_record`). **Total entidades: 187→196.** Build OK (19 páginas), integridad FK verificada.



---

---

### METADATO-32 — Rediseño de la capa de DEFINICIÓN del término TRANSFORMATION (definición metadata-first de transformaciones) — DECIDIDO



Replanteamiento completo de cómo se **define** una transformación, sobre el estado real en disco, tras invalidar la interpretación previa (mapping a nivel de atributo). **Una transformación = el proceso que carga una entidad canónica desde UNA tabla origen.** Por entidad canónica hay N: una **PRINCIPAL** (la golden source, carga por defecto que inserta) y N **ENRICHMENT** (completan la fila ya cargada, ejecutadas en orden secuencial). El motor compila automáticamente `INSERT` (principal) / `MERGE` (enriquecimiento); el usuario de negocio solo define la **expresión de cada campo** y sus **filtros**.



**(a) Modelo mínimo — 4 tablas** (sustituyen a las 16 de la definición antigua):

- **`transformation`** (cabecera, NÚCLEO): `code` (PK), `canonical_entity_code` (FK→canonical_entity), `source_entity_code` (FK→source_entity, la golden/driving), `role_code` (→**TRANSFORMATION_ROLE** metadata-first), `execution_order`, `system`.

- **`transformation_field`** (weak de transformation): `[transformation_code, canonical_attribute_code]` (PK). `transformation_code` FK identificativa compuesta a `transformation`; `canonical_attribute_code` FK a `canonical_attribute`. `is_variant` (BOOL: campo pivotado), `source_expression` (TYD_EXPRESSION, el valor del campo común; null si variante), `system`.

- **`transformation_filter`** (weak de transformation): `[transformation_code, filter_order]` (PK). `source_attribute_code` (FK→source_attribute), `operator_code` (→**OPERATOR** metadata-first), `filter_value`, `system`. Filtro declarativo campo·operador·valor, AND-eados; rellenable por negocio sin SQL.

- **`transformation_variant`** (weak de **transformation_field**): `[transformation_code, canonical_attribute_code, variant_order]` (PK). FK identificativa compuesta (2 columnas) a `transformation_field`. `value_expression` (valor del campo variante en ese eje: literal o columna), `system`.



**(b) Correlación del enriquecimiento sin estructura extra.** El `MERGE` casa por la **PK de la entidad canónica** (`canonical_key`); los atributos-PK se producen como `transformation_field` normales desde el origen. No hay tabla ni columna de correlación: el motor usa los fields-PK como `ON` y el resto como `UPDATE SET`. Coherente con la identidad por clave natural heredada (`id = sha2(BK…)`).



**(c) Generación de filas 1:N (unpivot) por variantes.** Se definen todos los campos destino; se marca `is_variant` en los que se pivotan. Cada **eje** (`variant_order`) asigna el `value_expression` de cada campo variante. Sin variantes = 1 fila; con N = `UNION ALL`. Cubre con una sola mecánica: redes sociales, direcciones y contactos. Regla DQ: el conjunto de `variant_order` debe ser el mismo en todos los campos variantes (ejes completos).



**(d) Catálogos.** Reutiliza `LIFECYCLE_STATE` (vía TYD_SYSTEM). Nuevos, contrato metadata-first: **TRANSFORMATION_ROLE** {PRINCIPAL, ENRICHMENT} y **OPERATOR** {EQ, NE, GT, GE, LT, LE, IN, NOT_IN, LIKE, NOT_LIKE, BETWEEN, IS_NULL, IS_NOT_NULL}. Eliminado el catálogo huérfano **MAPPING_CONDITION_KIND** (su única tabla `mapping_condition` se elimina).



**(e) Tablas eliminadas (16, capa definición antigua, eliminación limpia — cero FK entrantes verificado):** `transformation_mapping`, `transformation_mapping_version`, `mapping_input`, `mapping_output`, `mapping_condition`, `mapping_attribute`, `mapping_attribute_value`, `mapping_parameter_value`, `transformation_rule`, `transformation_rule_version`, `transformation_rule_parameter`, `rule_attribute`, `rule_attribute_value`, `source_attribute_canonical_attribute_map`, `reference_mapping_set`, `reference_mapping_set_entry`.



**(f) NO tocado en M-32 (su propio momento):** las capas TRANSFORMATION_EXECUTION y TRANSFORMATION_SECURITY, y la orquestación `transformation_pipeline`/`_step`/`pipeline_dependency` (frontera con D07 workflow). La `rule` reutilizable se deja fuera del primer punto.



**Verificado:** JSON válido; modelo **196→184 entidades** (−16 +4); eliminación limpia (0 FK entrantes a las 16); patrón weak-entity idéntico a `province`; catálogos **37→38**; `canonical_accelerator.METADATA.entity_count`=184.



### METADATO-33 — Registro del modelo de transformaciones por tipologías (Definición + Matching/LOAD_CANONICAL) y limpieza de Ejecución — DECIDIDO



Consolidación como **registradas** de las decisiones de diseño cerradas en sesión (hasta ahora solo en mockups y en el visualizador). Tres tipologías: **Definición**, **Matching/identidad (LOAD_CANONICAL)** y **Ejecución**. La ejecución en curso (`run`) se reconoce como **Observabilidad** y sale de este metamodelo. Operado sobre disco con `json.loads`/`json.dumps` (sin regex); ficheros completos.



**(A) Definición (término TRANSFORMATION_DEFINITION)**

- `transformation` += `business_process_code` (FK→business_process, opcional, RESTRICT) y `is_distinct` (TYD_BOOLEAN; DISTINCT sobre el grano — dedup y niveles de estructura jerárquica).

- Nueva **`transformation_join`** (weak de `transformation`; PK `[transformation_code, join_order]`): `joined_source_entity_code` (FK→source_entity), `join_type_code` (→**JOIN_TYPE**), `join_condition` (TYD_EXPRESSION, expresión única).

- **Agregación (GROUP BY / HAVING) derivada, no marcada:** `transformation_field` += `aggregate_function_code` (→**AGGREGATE_FUNCTION**, nullable). Campo con función = agregado; sin función = clave de agrupación; la transformación agrega si algún campo tiene función. `COUNT(*)` = COUNT + `source_expression` vacía. `transformation_filter` += `filter_stage_code` (→**FILTER_STAGE**: WHERE pre-agregación | HAVING post-agregación). Se descartó `is_group_by` por redundante.

- Catálogos nuevos: **JOIN_TYPE** {INNER, LEFT, RIGHT, FULL}, **AGGREGATE_FUNCTION** {SUM, COUNT, COUNT_DISTINCT, AVG, MIN, MAX}, **FILTER_STAGE** {WHERE, HAVING}.



**(B) Matching / identidad (término nuevo LOAD_CANONICAL, hijo de TRANSFORMATION)**

Modelo de reglas de match jerárquico rule_set→rule→condition:

- **`match_rule_set`** (NÚCLEO; PK `[canonical_entity_code, code]`): `combine_mode_code` (→**COMBINE_MODE**), `auto_match_threshold`, `review_threshold` (TYD_DECIMAL), `blocking_expression` (TYD_EXPRESSION). Sigue el patrón `province`: `canonical_entity_code` es PK plana (sin FK directa); no hay doble FK a canonical_entity.

- **`match_rule`** (weak de match_rule_set): `rule_order`, `nature_code` (→**RULE_NATURE**). Condiciones AND dentro de la regla; reglas OR vía `combine_mode` (FIRST_MATCH/BEST_SCORE/ALL).

- **`match_rule_condition`** (weak de match_rule): `match_entity_code` (ancla; entidad canónica raíz o satélite dependiente), `canonical_attribute_code` (FK compuesta a `canonical_attribute` vía [match_entity_code→canonical_entity_code, canonical_attribute_code→code]), `canonical_expression` (para identidad descompuesta en N campos, p.ej. nombre+ap1+ap2), `row_filter` (tipo+vigencia del satélite), `cardinality_code` (→**MATCH_CARDINALITY** {ANY,ALL}), `match_function_code` (→**MATCH_FUNCTION**), `weight` (TYD_DECIMAL), `is_required` (puerta AND vs. puntúa). Satélites 1:N se resuelven por EXISTS/ANY con `row_filter` (tipo + `valid_from`/`valid_to`).

- `canonical_entity_bk_lookup_config` (hogar de la config de identidad por entidad; ya albergaba la ubicación física de la xref) += `identity_mode_code` (→**IDENTITY_MODE** {BK_HASH, MDM_SURROGATE, RDM_STANDARD}), `on_miss_code` (→**ON_MISS** {CREATE, REMEDIATE, NONE}), `surrogate_strategy_code` (→**SURROGATE_STRATEGY** {SEQUENCE, UUID}, generación del master_id en MDM). **`identity_mode` es el único eje de identidad** (se rechazó un `master_type` a nivel término por redundante); cubre los 3 casos xref: MDM (surrogate+match), RDM (traducción estándar) y BK_HASH (ventas: id derivado + reversibilidad).

- **`xref`** (NÚCLEO): trazabilidad universal fuente→maestro. PK `[canonical_entity_code, source_entity_code, source_natural_key]`; `source_entity_code` es FK **compuesta a la ruta completa de `source_entity`** (source_system_code, container_parent_code, source_container_code, code); `master_id`, `is_golden`, `matched_by_rule_code`, `valid_from`/`valid_to` (vigencia para identificadores reasignables), `system`. Unifica el antiguo `reference_translation` (RDM) y la xref (MDM): `identity_mode` discrimina — se **fusiona `reference_translation` en `xref`** (no se duplican dos entidades con la misma información). La xref actúa además como "catálogo general" de valores traducidos.

- **`survivorship_rule`** (weak de `canonical_attribute`): `survivorship_strategy_code` (→**SURVIVORSHIP_STRATEGY** {SOURCE_OF_RECORD, MANUAL, MOST_RECENT, MOST_COMPLETE, MOST_FREQUENT}) + `winning_source_entity_code`. Responde "¿marco el maestro o autogenero?": SOURCE_OF_RECORD/MANUAL = marcado; MOST_RECENT/COMPLETE/FREQUENT = auto.

- **`match_function_impl`** (implementación de cada MATCH_FUNCTION como **metadato**, seed): `match_function_code`, `impl_kind_code` (→**IMPL_KIND** {NATIVE, COMPOSED, UDF}), `udf_ref`, `sql_template`. 6 filas seed: EXACT/NATIVE, EXACT_NORMALIZED/COMPOSED, JARO_WINKLER/UDF/`datum.udf.jaro_winkler`, LEVENSHTEIN/COMPOSED, SOUNDEX/NATIVE, METAPHONE/UDF/`datum.udf.metaphone`. Las funciones no nativas (norm, jw, metaphone) se instalan **una vez** como UDF de plataforma; EXACT/SOUNDEX/LEVENSHTEIN son nativas/derivadas.

- Nuevo business_term **`LOAD_CANONICAL`** (detalle de RUNNER_LOAD_CANONICAL).

- Catálogos nuevos: **COMBINE_MODE** {FIRST_MATCH, BEST_SCORE, ALL}, **MATCH_FUNCTION** {EXACT, EXACT_NORMALIZED, JARO_WINKLER, LEVENSHTEIN, SOUNDEX, METAPHONE}, **RULE_NATURE** {DETERMINISTIC, PROBABILISTIC}, **IDENTITY_MODE** {BK_HASH, MDM_SURROGATE, RDM_STANDARD}, **ON_MISS** {CREATE, REMEDIATE, NONE}, **MATCH_CARDINALITY** {ANY, ALL}, **SURVIVORSHIP_STRATEGY** (5), **SURROGATE_STRATEGY** {SEQUENCE, UUID}, **IMPL_KIND** {NATIVE, COMPOSED, UDF}.



**(C) Vistas de materialización**

- Catálogo **VIEW_KIND** {CANONICAL, MATCHING} tipando `canonical_view.view_kind_code`. La vista de match compilada se registra como `canonical_view` (kind MATCHING) + `compiled_ddl` (`CREATE OR REPLACE VIEW …`); la de carga como kind CANONICAL. Compiladores **genéricos, 100% dirigidos por metadato** (no hardcode por caso): leen `match_rule_set`/`match_rule`/`match_rule_condition`/`match_function_impl` (match) y `transformation`/`_field`/`_filter`/`_join`/`_variant` (definición) y emiten el SQL. Cambiar comportamiento = cambiar metadato.



**(D) Ejecución — limpieza**

- **Eliminadas `transformation_run` y `transformation_run_step`** → pertenecen a **Observabilidad**, no al metamodelo de transformación (aisladas: 0 FK entrantes externas). `compiled_ddl` se mantiene (artefacto de materialización genérico).



**(E) Transversal D3 (identidad de origen).** `xref.source_entity_code` como FK compuesta a la ruta completa de `source_entity` (la PK de source_entity es entity + sus padres). Queda anotada la misma pasada para el resto de FK a `source_entity` (source_entity_capture_config, source_entity_canonical_entity_hint, source_entity_version, source_discovery_drift, source_discovery_sampling_result, source_relation.reference_source_entity_code) — no ejecutada aún.



**Reverts / decisiones de simplificación:**

1. Rechazado `master_type` a nivel término y `identity_owner_entity_code`: `business_term` tenía 2 FK a `canonical_entity` (circular) y el catálogo MASTER_TYPE quedaba incompleto → **revertidos ambos**. La identidad es per-entidad vía `identity_mode` (que ya cubre los 3 casos xref). Catálogo MASTER_TYPE eliminado.

2. `reference_translation` **fusionado** en `xref` (misma información; discrimina `identity_mode`).

3. Config de identidad sobre `canonical_entity_bk_lookup_config`, no sobre `canonical_entity` (no ampliar su blast radius).

4. `xref`/`translator` runtime: la tabla física por entidad la ubica `canonical_entity_bk_lookup_config`; el metamodelo registra **reglas + config de identidad**, no las filas.

5. Identidad per-entidad ("la bomba"): los dependientes son INHERITED (FK al principal, sin xref propia); la jerarquía geográfica lleva **una xref RDM por nivel** (no identidad compartida).



**Código de runner guardado en el Project** (plataforma, NO metadato; regla de oro: cambiar comportamiento = cambiar metadato): `runner/compile_transformation.py` (compilador de carga), `runner/compile_match_view.py` (compilador de match), `runner/datum_match_udfs.py` (las 3 UDF a instalar: norm/jw/metaphone), `runner/README_runner.md`, `runner/README_match_runner.md`.



**PENDIENTE DE DECISIÓN DE PEDRO (no ejecutado):** **Ejecución = ¿`workflow_pattern` o `transformation_pipeline`?** Conviven en disco el nuevo `workflow_pattern`+`workflow_pattern_step` (step→RUNNER_TYPE, ya registrado y CONFIRMADO) y el viejo `transformation_pipeline`+`_step`(acoplado a `canonical_view`/MAPPING)+`pipeline_dependency` (aislado). Recomendación: ejecución = `workflow_pattern` + runners; retirar `transformation_pipeline*`. No tocado a la espera de orden.



**Verificado:** JSON válido (3 ficheros); modelo **184→189 entidades** (+7 −2): +transformation_join, +match_rule_set, +match_rule, +match_rule_condition, +xref, +survivorship_rule, +match_function_impl; −transformation_run, −transformation_run_step. Catálogos **38→51** (+13). `total_attributes`=1199. `canonical_accelerator.METADATA.entity_count`=189. Patrón weak-entity/`fk_composite` idéntico a `province`. Compiladores genéricos verificados reproduciendo el caso cliente/country desde metadato. Visualización (demo `/dashboard/canonico`): rama de término "Transformaciones → Definición Trx / Matching" con catálogos apuntados; validación estructural Playwright headless.



### METADATO-34 — Término ORCHESTRATION (motor de ejecución), fusión de identidad en canonical_entity, y limpieza integral de D3 (captura, contratos, discovery, D/G, runners) — DECIDIDO



Sesión larga de cierre del bloque ejecución + saneamiento de D3. Operado sobre disco con `json.loads`/`json.dumps` (sin regex); ficheros completos. **Modelo 189→171 entidades; catálogos 51→66; total_attributes=1112.** Demo actualizada y validada (Playwright headless) en cada paso.



**(A) Término ORCHESTRATION (hijo de TRANSFORMATION) — ejecución = Compilación + Orquestación.** Dos planos separados: **Compilación** (disparada por *cambio de metadato*: un compilador de plataforma escribe el artefacto en `compiled_ddl` con `source_metadata_hash`; el cambio invalida → `PENDING_RECOMPILE` → recompila) y **Orquestación** (el runner **solo ejecuta lo VIGENTE**, nunca compila). Resuelve el pendiente de M-33 (workflow_pattern vs transformation_pipeline): se consolida en `workflow_pattern`.

- Movidas a ORCHESTRATION: `workflow_pattern`, `workflow_pattern_step` (desde BUSINESS_PROCESS), `compiled_ddl` (desde TRANSFORMATION_EXECUTION).

- `workflow_pattern_step` += `is_gate` (puerta: DQ que corta el circuito) + `schedule_override`.

- Nueva **`runner_capability`** (NÚCLEO; PK `runner_type_code`→RUNNER_TYPE): `reads_definition_entity`, `compiled_object_type_code` (→object_type), `compiles_view_kind_code` (→VIEW_KIND), `write_semantics_code` (→WRITE_SEMANTICS), `is_gate_capable`. Contrato por tipo de runner (espejo de `match_function_impl`): hace el runner genérico y dirigido por metadato. 9 filas seed (una por RUNNER_TYPE). Añadir capacidad = 1 fila + su compilador; el motor no cambia.

- `business_process` += `trigger_kind_code` (→**TRIGGER_KIND** {SCHEDULE,EVENT,MANUAL}) + `schedule_cron` — disparador a nivel proceso.

- **Eliminadas** `transformation_pipeline`, `transformation_pipeline_step`, `pipeline_dependency` (orquestación vieja, 0 FK entrantes). Términos formales `TRANSFORMATION_DEFINITION`/`TRANSFORMATION_EXECUTION` quedaron vacíos → retirados del seed.

- Catálogos: **QUERY_STATUS** {VIGENTE,OBSOLETA,PENDING_RECOMPILE} y **DDL_KIND** {CREATE_TABLE,CREATE_VIEW,CREATE_MATERIALIZED_VIEW} (enganchados a `compiled_ddl.query_status_code`/`ddl_kind_code`, antes colgaban), **WRITE_SEMANTICS** {APPEND,INSERT_MERGE,GATE,MASTER_XREF,OVERWRITE,CREATE}, **TRIGGER_KIND**. Sembrados en seed los vacíos **RUNNER_TYPE** (9), **WORKFLOW_SCOPE** (3), **WORKFLOW_PURPOSE** (4).

- **Vista canónica = AST (concatenación de nodos).** `canonical_view` no es SQL en texto: su contenido son las expresiones `expression` → `expression_node` → `expression_operand` (los `COLUMN_SOURCE` dan linaje formal a `source_attribute`). Cada `transformation_field`/`_join`/`_filter` → una expresión; la vista es la concatenación. El "compilador" es un **serializador universal** dirigido por metadato (plantilla por `node_kind`, símbolo de OPERATOR, cláusula de EXPRESSION_TYPE), escrito una vez, igual para toda vista; `compiled_ddl` es render-cache, no fuente. Cambiar comportamiento = cambiar nodos.



**(B) Fusión de la config de identidad en `canonical_entity` (elimina `bk_lookup_config`).** `canonical_entity` += `identity_mode_code` (→IDENTITY_MODE; +**INHERITED** para satélites), `surrogate_strategy_code` (→SURROGATE_STRATEGY), `on_miss_code` (→ON_MISS), `xref_physical_catalog_code` + `xref_physical_schema_code` (**FK compuesta única** a `physical_schema`; capa `staging.<negocio>`; tabla `<entidad>_xref` por convención). Todas nullables (solo las que resuelven identidad).

- **Eliminadas** `canonical_entity_bk_lookup_config` (config plegada), `canonical_entity_bk_alias`, `canonical_entity_business_process` (0 FK entrantes).

- El principal de un término lleva identidad (MDM_SURROGATE dato maestro / RDM_STANDARD referencia / **BK_HASH derivado — también con xref, para desanonimización**); satélites INHERITED. `match_rule_set` = **detección** (solo MDM); la identidad la gobierna `canonical_entity` (los 3 modos). Corregido de paso el error de FK (el `*_catalog_code` **no** es FK propia, es columna de la compuesta a `physical_schema`; pintada).



**(C) Captura (SOURCE_INGESTION) enriquecida + remanente eliminado.** Eliminado el remanente D3 viejo `source_entity_capture_config` (duplicaba `source_entity_capture`). `source_entity_capture` += `schedule_cron`, `schedule_timezone`, `full_reload_strategy_code` (→**FULL_RELOAD_STRATEGY**, FULL), `watermark_operator_code` (→OPERATOR, INCREMENTAL), `cdc_delete_handling_code` (→**CDC_DELETE_HANDLING**) + `cdc_initial_snapshot` (CDC), `landing_format_code` (→**LANDING_FORMAT**) + landing físico (`landing_physical_catalog_code` + `landing_physical_schema_code` compuesta), y bloque **STREAMING**: `stream_message_format_code` (→**STREAM_MESSAGE_FORMAT**), `stream_start_position_code` (→**STREAM_START_POSITION**), `stream_trigger_interval`, `stream_consumer_group`, `stream_schema_registry_subject`. **CAPTURE_MODE += STREAMING**. `source_entity_capture_attribute` += `capture_role_code` (→**CAPTURE_ATTRIBUTE_ROLE** {WATERMARK, CDC_KEY, CDC_SEQUENCE, CDC_OPERATION, LANDING_PARTITION, STREAM_KEY}) — rol explícito (antes el modo daba el significado, insuficiente para CDC). El estado de ejecución (última marca, offsets) → Observabilidad.



**(D) Data contracts → término nuevo `SOURCE_CONTRACT` (hijo de DATA_SOURCE, UNE 0078).** Movidas `source_data_contract`, `source_data_contract_sla` (de remanente D3/K). SLA de prosa a **metadato accionable**: `target_value` tipado (`target_operator_code`→OPERATOR + `target_value` TYD_DECIMAL + `target_unit_code`→**SLA_UNIT**), `breach_action_code` (→**BREACH_ACTION**), `dq_dimension_code` (→DQ_DIMENSION; **enganche a D6**: la brecha se deriva como comprobación DQ). **SLA_TYPE** ampliado (FRESHNESS, AVAILABILITY, COMPLETENESS, LATENCY, ERROR_RATE, VOLUME, DELIVERY_PUNCTUALITY). Nueva **`source_data_contract_entity`** (alcance: qué `source_entity` cubre + `schema_stability_code`→**SCHEMA_STABILITY**, `expected_min_rows`/`expected_max_rows`, `delivery_schedule_cron`). `contract_status_code` enganchado a **CONTRACT_STATUS**.



**(E) Discovery consolidado — discovery = un proceso del orquestador, no un subsistema.** Concepto: hay un **business_process "discovery"** (BU Gobierno del dato/Arquitectura) sobre el término DATA_SOURCE que corre el `workflow_pattern` clásico: **INGEST** (leer el catálogo de la fuente vía `discovery_template*`) → **TRANSFORM** (mapear a las `source_*` vía `discovery_field_mapping`). Reutiliza el orquestador + la compilación de vistas; cero subsistema.

- **Núcleo (se queda):** `discovery_template` + `_object` + `_view_column` + `_field_mapping`.

- **Eliminadas:** `source_discovery_config` (→ disparador del proceso + `is_in_scope`), `source_attribute_detected_type_domain` (contradice: los tipos de fuente son **nativos por tecnología**, sin relación con `data_type_domain`; el dominio semántico se asigna después, en canónico/transformación), `runner_discover` (→ orquestador).

- **A Observabilidad:** `source_discovery_run`, `source_discovery_sampling_result`, `source_attribute_profile`, `discovery_rule_evaluation`, y el hallazgo de `source_discovery_drift` (el drift aceptado → `source_entity_version`).

- **Añadido opcional (más adelante):** `discovery_rule`.

- **DQ de fuentes = ESTRUCTURAL, no de datos** (decisión de Pedro, muy clara): "tabla sin PK/FK/índice/particionar". Se **deriva** de las `source_*` + `object_assessment` sobre `source_entity`. Los índices son `source_key` con `key_type` (PK/UN/UI) — **no** hace falta `source_index`.



**(F) Limpieza D3/D + D3/G + runners.** Eliminadas: `runner_ingest_managed`, `runner_ingest_streaming` (→ orquestador; streaming ya vive en `source_entity_capture`), `source_entity_canonical_entity_hint` (propuesta de discovery; el confirmado es una fila de `transformation`), `source_attribute_quality_hint` (DQ de datos en origen, descartado; la calidad *declarada* vive en el contrato SLA), `golden_source` (la fuente autoritativa se deriva de `transformation.role=PRINCIPAL` + `xref.is_golden` + `survivorship_rule`; la ratificación por Comité vía `object_approval`).



**Presentación:** todas las entidades reorganizadas/nuevas salen de la vista **por dominio** (`domain=''`) y entran solo en la de **acelerador** (términos ORCHESTRATION, SOURCE_CONTRACT, etc.). Demo sincronizada y escrita en el portátil en cada vuelta.



**Verificado:** JSON válido (3 ficheros); **189→171 entidades**; catálogos **51→66**; `total_attributes`=1112; `canonical_accelerator.METADATA.entity_count`=171; integridad limpia (0 FK reales colgantes; los polimórficos no cuentan); invariante seed↔modelo OK. Demo: árbol carga sin errores, DATA_SOURCE/SOURCE_CONTRACT/ORCHESTRATION visibles.



**PENDIENTES abiertos:** versionado D3/H (`source_entity_version` + `source_attribute_version`) — aplazado; llevar las plantillas de render a los catálogos (NODE_KIND/OPERATOR/EXPRESSION_TYPE); expresión de nodo (texto libre parseado a AST vs. referencia directa a nodos — recomendación híbrido); dar término propio a `canonical_view`/`expression` (hoy sin término, siguen en la vista por dominio); sembrar `object_type` (DQ_CHECK/KPI) para `runner_capability`/`compiled_ddl`; landing (compresión/write_mode); `discovery_rule` como añadido de enriquecimiento; matización de Pedro sobre discovery (pendiente de que la cuente).



### METADATO-35 — Acelerador DATA_QUALITY: motor de reglas DQ derivadas del metamodelo (dos ejes clasificación/remediación), fases de ejecución + capa STAGING, generador + visor, y reubicación de dominios (dimension→D7, definiciones de gobierno→D8) — DECIDIDO



Sesión de cierre del circuito **ingesta→calidad**. Operado sobre disco con `json.loads`/`json.dumps` (sin regex); ficheros completos. **Modelo 171→172 entidades (+`dq_check_type`); total_attributes 1112→1121; catálogos 66→72.** Demo regenerada y escrita en el portátil en cada paso; `page.tsx` validado con esbuild.



**(A) Tipología de reglas DQ que gestiona el motor — DERIVADAS del metamodelo, no una tabla de reglas.** Los tipos: **FORMAT** (dominio TYD del atributo: regex/longitud del catálogo de tipos), **STRUCTURE**, **MANDATORY_SIMPLE** / **MANDATORY_COMPOSITE** (obligatoriedad), **REFERENTIAL** (integridad FK en sus 3 sabores: MDM / RDM / catálogo metadata-first), **UNIQUENESS** (PK/único), **TERM_COMPLETENESS** (completitud por término de negocio), **BUSINESS_RULE**, **ACCURACY_REFERENCE** (exactitud vs. referencia), **FRESHNESS** (puntualidad de carga, 100% derivada del contrato SLA — no es comprobación de contenido fila a fila), **SOURCE_STRUCTURAL** (fuente sin PK/FK/índice/particionar). Se reportan en **DAMA-DMBOK + ISO/IEC 25012**.



**(B) Entidad `dq_check_type` (término DATA_QUALITY, hermana de `runner_capability`) — DOS EJES ORTOGONALES.** 9 atributos: `code`(PK), `dq_dimension_code`(→DQ_DIMENSION), `scope_level_code`(→WORKFLOW_SCOPE), `check_derivation_source`, `on_fail_default_code`(→DQ_ON_FAIL, nullable), `on_fail_derivation_source` (nullable), `default_severity_code`(→DQ_SEVERITY), `execution_phase_code`(→DQ_PHASE), `system`. **Eje ① Clasificación** (para reportar/certificar): `dq_dimension`→ISO vía crosswalk — **join transitivo por el VALOR de la dimensión, no FK directo** (metadata-first, diamante): ambos apuntan a DQ_DIMENSION, el mapeo ISO se define una vez por dimensión y los 11 tipos lo heredan. **Eje ② Remediación** (lo que mueve el circuito): `on_fail` + `severity`, ambos derivables del metamodelo. Son independientes: cambiar el mapeo ISO no toca la remediación y viceversa; **solo se encuentran en el registro del incidente** (cuarentena/Observabilidad), que lleva las dos caras (acción + etiqueta ISO). 11 filas seed.



**(C) Piezas DQ reagrupadas bajo el término DATA_QUALITY (seed `canonical_entity.business_term_code=DATA_QUALITY`, `domain=''`):** `dq_check_type`, `dq_dimension_to_iso_characteristic` (el **puente** DAMA↔ISO: solo traduce dimensión→característica ISO, 10 filas), `dq_quarantine_policy`, `business_rule`. Materializados en `reference_value` los catálogos **DQ_DIMENSION** (6 valores) e **ISO_CHARACTERISTIC** (7), que estaban declarados sin filas.



**(D) Remediación autocontenida — el resultado ante fallo se DERIVA, no se teclea.** `on_fail` ∈ **{AUTO_REMEDIATE, REJECT, QUARANTINE, FLAG}** resuelto leyendo campos que el metamodelo ya declara: normalización del dominio TYD (FORMAT), `column_default`/`generation_expression` (obligatoriedad), `survivorship_rule`/identidad MDM (unicidad/exactitud), `canonical_entity.on_miss_code` (referencial), `source_data_contract_sla.breach_action_code` (frescura), `business_rule` (regla de negocio). Severidad ∈ **{INFO, WARNING, ERROR}**. **Principio DATUM: nunca da error de ejecución — es autocontenido: registra y avisa.** Estados de runner: **COMPLETED / COMPLETED_WITH_WARNINGS / COMPLETED_WITH_ERRORS / ERROR**; los fallos de infraestructura (no existe Databricks/cluster…) → Observabilidad + aviso, sin romper el circuito.



**(E) Fases de ejecución + flujo de datos único.** Catálogo **DQ_PHASE** {**PRE_INGEST** (RUNNER_INGEST), **PRE_WRITE** (RUNNER_TRANSFORM, por fila), **POST_WRITE** (RUNNER_DQ, por conjunto)}. Motor bifásico y **agnóstico de canal** (UI/fichero/API invocan la misma puerta compilada, ligada a la entidad), con trazabilidad en Observabilidad. **Capa STAGING** añadida a `storage_layer` (orden: METADATA, OBSERVABILITY, LANDING, OPERATIONAL, **STAGING**, COMMON, BUSINESS, NEGOCIO). **Flujo:** fuente → LANDING/OPERATIONAL (ingesta) → **STAGING (capa temporal, donde corre la calidad)** → COMMON (solo dato validado y veraz). Las reglas **ya están compiladas o se compilan en cuanto el metadato cambia** (modelo de compilación M-34: `compiled_ddl` + `source_metadata_hash` → PENDING_RECOMPILE → recompila); el runner **solo ejecuta lo VIGENTE**.



**(F) Catálogos (66→72) y saneamiento FK.** Nuevos: **DQ_ON_FAIL** {AUTO_REMEDIATE, REJECT, QUARANTINE, FLAG}, **DQ_SEVERITY** {INFO, WARNING, ERROR}, **DQ_PHASE**, **RULE_KIND**, **MATURITY_DIMENSION**, **EXPIRATION_ACTION**. Saneadas las FK de `business_rule`: `severity_code`→**DQ_SEVERITY**, `maturity_dimension_code`→**MATURITY_DIMENSION**. Añadidas 3 cabeceras `reference_catalog` que faltaban (valores presentes sin header): **WORKFLOW_SCOPE**, **RUNNER_TYPE**, **WORKFLOW_PURPOSE**.



**(G) Generador `runner/compile_dq_checks.py` (plataforma, NO metadato).** Autogenera TODAS las DQ rules por entidad canónica leyendo el metamodelo: dominio TYD del atributo → regex/longitud del catálogo de tipos (FORMAT); PK → UNIQUENESS; `mandatory` → MANDATORY_SIMPLE; `reference_catalog` → REFERENTIAL (catálogo); `fk_target`/`fk_composite` a entidad → REFERENTIAL (entidad, etiquetada por `identity_mode`). Produce **`datum_dq_rules.json`** con **1855 checks** (**1374 PRE_WRITE / 481 POST_WRITE**) y agregados por **entidad / término (25) / proceso**. Regla de oro: cambiar comportamiento = cambiar metadato, no este código.



**(H) Visualización.** Nueva pestaña **«DQ rules»** en `/dashboard/canonico` (3 alcances: por entidad canónica, por término de negocio, por proceso de negocio), con franja del flujo de datos + recuento por fase y filtros por tipo/fase/búsqueda. Además, en el ER: **cajas de catálogo compactadas** (ancho al contenido, no fijo) + **tooltip con los valores del catálogo** (`<title>` SVG, lee `datum_catalogos.json` vía prop `cats`). Cambio de código → requiere RECONSTRUIR; los cambios de datos (JSON) solo Ctrl+Shift+R.



**(I) Reubicación de dominios (D6 → D7/D8).** `dimension` (dimensión **analítica** — vista sobre MDM/RDM, `dim_marca = CREATE VIEW sobre mdm.marca`; hermana de `accumulative_fact_dimension`, que ya la referencia) → **D7**. Las **6 definiciones de gobierno de calidad** → **D8** (dominio de gobierno, junto al motor de evaluación genérico `assessment_pattern`/`assessment_pattern_threshold`/`object_assessment`): `data_quality_requirement`, `dq_evaluation_specification`, `dq_assurance_procedure`, `dq_audit_plan`, `dq_certification_criteria`, `dq_implementation_plan`. Todas son **DEFINICIONES** (planes/criterios); la **EJECUCIÓN** va a Observabilidad (OBS_DQ_*). **D6 queda vacío (0 entidades).** El tag `domain` solo agrupa la vista por dominio; no toca nombres ni FKs (las FK internas de las 6 viajan juntas; integridad intacta).



**Verificado:** JSON válido (3 ficheros); **171→172 entidades** (+`dq_check_type`, única entidad nueva; 0 entidades perdidas); **total_attributes 1112→1121** (+9, los de `dq_check_type`); catálogos **66→72**; integridad FK intacta; invariante seed↔modelo OK. `dq_dimension_to_iso_characteristic` y `dq_quarantine_policy` pasan de D6 a `domain=''` por agrupación bajo DATA_QUALITY. Demo (`datum_modelo_canonico.json`, `datum_catalogos.json`, `datum_carga_inicial.json`, `datum_dq_rules.json`, `page.tsx`) sincronizada y escrita en el portátil.



**PENDIENTES abiertos:** **solapamiento** de `dq_certification_criteria` (umbrales BRONZE/…/PLATINUM) y `dq_evaluation_specification` con el motor genérico de evaluación de D8 (`assessment_pattern_threshold`/`object_assessment`) — decidir si las 6 DQ se apoyan en ese motor o se mantienen específicas; **sembrar los 36 TYD + formatos** en el bootstrap (hoy el FORMAT deriva del catálogo de tipos en runtime); sembrar `business_process`/`business_rule` para la DQ por proceso (hoy 0 procesos); `MATURITY_DIMENSION`/`EXPIRATION_ACTION`/`RULE_KIND` con valores **PROPUESTO** (ajustables); **retirar D6 vacío** del `DOMAIN_ORDER` si no va a albergar nada; acelerador **Observabilidad** (registros de trazabilidad OBS_DQ_* que reciben la ejecución de planes/auditorías/certificaciones).



### METADATO-36 — Semántica de ejecución del gate PRE_WRITE (FORMAT + MANDATORY): UDF compilada por columna — DECIDIDO



Especifica **cómo ejecuta** el runner las comprobaciones FORMAT y MANDATORY_SIMPLE/COMPOSITE que M-35 tipificó. Es semántica de ejecución (contrato del compilador/runner): **no cambia entidades ni catálogos** (modelo intacto 172/1121/72). El gate corre en **PRE_WRITE (RUNNER_TRANSFORM), en STAGING**, como UDF compilada por columna desde el metadato (VIGENTE, M-34) — nunca interpretación en caliente.



**Circuito por columna (tipo simple):**

1. **¿`source` es null?** → rama **obligatoriedad** (`canonical_attribute.is_nullable`). Si no admite null: se aplica default con precedencia **atributo → tipo** (`canonical_attribute.column_default` → `data_type_domain.column_default`); default aplicado → **WARNING**, y **NO se revalida** (se considera de confianza por venir del metadato). Sin default → **ERROR/REJECT**.

2. **Si no es null** → **`TRY_CAST`**(`source` AS TYD destino):

   - **falla** (produce null por cast) → es fallo de **FORMAT**, no de obligatoriedad: valor inválido, **no** se le aplica default (un null "de cast fallido" nunca se remedia con default; solo el null "de origen" lo hace). Severidad la de la regla (ERROR por defecto).

   - **ok** → sobre el valor casteado corre la validación **FORMAT/VALIDITY** (regex): si el atributo declara `regex_pattern_override` → **OVERRIDE** (sustituye por completo al regex del tipo); si no, la validación VALIDITY del tipo (`data_type_domain_validation`, dueño = TYD). Resultado **WARNING o ERROR** según la severidad declarada de la regla.



**Distinción de null (clave):** "de origen" (source venía null → obligatoriedad/default) vs. "por cast fallido" (dato mal formado → FORMAT, sin default). El runner marca cuál es.



**No hay SQL por columna:** las validaciones SQL viven **solo a nivel tipo** (`data_type_domain_validation`, dueño simple o compuesto). Si en el futuro hiciera falta SQL de columna/fila, sería tipo **BUSINESS_RULE** vía `canonical_entity_constraint` (CHECK) — otro check, **fuera** de este gate.



**Tipo compuesto:** el mismo circuito en dos niveles — **por campo** (cada `data_type_domain_field` es un TYD simple: cast + format + obligatoriedad de campo) **más** la **validación cruzada** del compuesto (`data_type_domain_validation` con dueño el compuesto) y la **obligatoriedad del conjunto** (MANDATORY_COMPOSITE).



**Salida de la UDF (por columna):** `valor_origen`, `valor_destino`, y la lista de reglas aplicadas con **veredicto** {PASS, WARNING, ERROR} y **acción** {CAST, DEFAULT_APPLIED, REJECTED}. Es el **registro de incidente** que va a Observabilidad, portando los dos ejes de M-35 (clasificación dimensión→ISO + remediación on_fail/severity).



**Autocontenido (M-35):** el resultado de fila es COMPLETED / COMPLETED_WITH_WARNINGS / COMPLETED_WITH_ERRORS; **nunca error de ejecución**.



**PENDIENTE derivado:** catálogos del incidente (veredicto {PASS, WARNING, ERROR} y acción {CAST, DEFAULT_APPLIED, NORMALIZED, REJECTED}) — se definirán con el **acelerador de Observabilidad**, no aquí.



### METADATO-37 — Cierre de la capa analítica D7: término ANALYTICS (hechos, dimensiones, KPIs, data products) — DECIDIDO

Se cierra la **capa analítica D7**, hasta ahora 7 entidades sin término de negocio (`business_term_code="METADATA"`, placeholder). Se le da término propio, se modelan en firme los huecos (jerarquía de dimensión y medidas), se sanean las FK de catálogo a metadata-first y se siembra `object_type`. Operado sobre disco con `json.loads`/`json.dumps` (sin regex); ficheros completos. **Modelo 172→176 entidades; atributos 1121→1142; catálogos 72→80.**

**(A) Término ANALYTICS + 4 hijos.** Nuevo término raíz **`ANALYTICS`** (acelerador METADATA, `parent_term_code=null`, espejo de DATA_SOURCE) con 4 hijos: **`FACT`**, **`DIMENSION`**, **`KPI`**, **`DATA_PRODUCT`**. Las 7 entidades existentes pasan a `domain=''` + su término hoja (invariante del metamodelo: término ⟺ `domain=''`; aparecen solo en la vista por acelerador). **D7 queda vacío como dominio.** Adscripción: FACT ← `accumulative_fact`, `accumulative_fact_dimension`, `accumulative_fact_measure`; DIMENSION ← `dimension`, `dimension_attribute`, `dimension_level`; KPI ← `kpi`, `kpi_dependency`; DATA_PRODUCT ← `data_product`, `data_product_fact`, `data_product_dimension`.

**(B) Jerarquía de dimensión modelada (sustituye texto libre).** Eliminado `dimension.analysis_hierarchy_text`. Dos hijas weak (patrón M-26, `fk_composite`+`is_identifying`+RESTRICT): **`dimension_attribute`** (ejes expuestos; PK `[dimension_code, code]`; `source_attribute_code` = atributo del MDM/RDM origen, `is_key` = grano base, `attribute_order`) y **`dimension_level`** (jerarquía de drill; PK `[dimension_code, code]`; `dimension_attribute_code` FK compuesta al eje, `parent_level_code` self-FK compuesta para el drill-up, `level_order`).

**(C) Medidas modeladas.** Nueva **`accumulative_fact_measure`** (weak de `accumulative_fact`, espejo de `transformation_field`; PK `[accumulative_fact_code, code]`): `aggregate_function_code`→**AGGREGATE_FUNCTION** (metadata-first), `source_expression` (TYD_EXPRESSION; vacío = COUNT(*)), `measure_order`. `kpi` += `fact_measure_code` (FK compuesta a `accumulative_fact_measure` vía `[accumulative_fact_code, fact_measure_code]`): el KPI **BASIC** expone una medida concreta del hecho; el **DERIVED** sigue por `kpi_dependency` + `calculation_view` (AST). Sin agregación redundante en el KPI.

**(D) `common_dimension_set_text` modelado.** Eliminado `data_product.common_dimension_set_text`; nueva **`data_product_dimension`** (weak de `data_product`, N:M a `dimension`; PK `[data_product_code, dimension_code]`): el juego de dimensiones comunes que el producto expone para cruzar sus hechos de forma consistente.

**(E) Saneamiento weak-entity + metadata-first.** Patrón M-26 aplicado a las 3 hijas N:M/cadena (`accumulative_fact_dimension`, `kpi_dependency`, `data_product_fact`) y a las 4 nuevas (dueño `is_identifying`, referencia como FK compuesta no identificativa). Las **8 FK a `reference_value`** de D7 pasan a metadata-first (`reference_catalog`+`catalog_ref_metadata_only`): deuda del modelo **77→69** (las 69 restantes son D8/D9/D10, pendiente registrado "por tandas").

**(F) Catálogos (8 nuevos, 72→80).** CONFIRMADO: **TIME_GRAIN** {HOUR,DAY,WEEK,MONTH,QUARTER,YEAR}, **MATERIALIZATION_MODE** {TABLE,MATERIALIZED_VIEW,VIEW}, **KPI_TYPE** {BASIC,DERIVED}, **SUBJECT_KIND** {BUSINESS,DATA_QUALITY,METAMODEL,OBSERVABILITY}, **PUBLICATION_STATUS** {DRAFT,PUBLISHED,DEPRECATED,RETIRED}. **PROPUESTO** (valores ajustables): **UNIT** {COUNT,CURRENCY,PERCENTAGE,RATIO,DURATION} — podría diferirse a la entidad `unit_of_measure` (CUARENTENA); **CERTIFICATION_TIER** {RAW,CURATED,CERTIFIED}; **PERSPECTIVE** {CORE,COMPLEMENTARY,REFERENCE}.

**(G) Seed `object_type` (hook M-34/M-35).** Nueva lista `object_type` en el bootstrap con los valores que D7 referencia + el enganche pendiente: CANONICAL_ENTITY, ACCUMULATIVE_FACT, DIMENSION, KPI, DATA_PRODUCT, **DQ_CHECK** (para `runner_capability`/`compiled_ddl`). El **censo completo** de `object_type` sobre todas las referencias polimórficas del modelo queda como pendiente aparte.

**Verificado:** JSON válido (3 ficheros); **0 errores en ámbito D7** (FK a entidad, FK compuestas, invariante término⟺`domain=''`, invariante seed↔modelo, PK de las hijas); recuentos alineados en `_meta`, `canonical_accelerator.METADATA.entity_count` y catálogos: **176 / 1142 / 80**. Árbol acelerador reconstruido: rama ANALYTICS completa (11 entidades, 0 huérfanas). Demo sincronizada (`public/datum_modelo_canonico.json`, `datum_carga_inicial.json`, `datum_catalogos.json`) y escrita en el portátil; `src/data/metamodel.json` (ER por-dominio, ya desincronizado desde M-35/36) no se toca — no es la ruta de la vista por acelerador.

**PENDIENTES abiertos:** valores **PROPUESTO** de UNIT/CERTIFICATION_TIER/PERSPECTIVE a confirmar; decidir si UNIT es catálogo o entidad `unit_of_measure`; **censo completo de `object_type`** (todas las referencias polimórficas); i18n de la rama ANALYTICS (términos y entidades nuevas, sin traducir); poblar `canonical_key`/`canonical_relation` reales de las 4 nuevas; regenerar `src/data/metamodel.json` (ER por-dominio) si se quiere mantener esa vista.

### METADATO-38 — Dimensiones inferibles (estrella/copo) y nivel de dimensión en el hecho — DECIDIDO
Sobre el modelo de dimensiones y hechos de D7 (M-37), para soportar dimensión clásica (estrella) sobre catálogo simple y dimensión copo de nieve sobre jerarquías ya definidas, **inferidas del metadato sin duplicar**. Modelo 176→176 entidades; atributos 1142→1146; catálogos 80→82.
- **`object_type`** += REFERENCE_CATALOG (dimensión clásica sobre catálogo) y BUSINESS_TERM (dimensión sobre una jerarquía completa).
- **`dimension`** += `dimension_kind_code`→**DIMENSION_KIND** {CLASSIC, SNOWFLAKE} y `derivation_mode_code`→**DERIVATION_MODE** {INFERRED, EXPLICIT}. Cuando el origen es un catálogo o una jerarquía conocida, los ejes/niveles se **infieren** (no se pueblan `dimension_attribute`/`_level`); solo se declaran a mano en dimensiones a medida.
- **`dimension_level`** += `source_entity_code` (opcional): el nivel apunta a la entidad de la jerarquía que representa (puntero al metadato → inferencia sin copiar).
- **`accumulative_fact_dimension`** += `dimension_level_code` (FK compuesta a `dimension_level`): el nivel al que se fija cada dimensión jerárquica en el hecho. El grano temporal sigue privilegiado en `accumulative_fact.time_grain_code`.
- **`TIME_GRAIN`** reducido a {HORA (opc), DÍA, MES, AÑO} (quitados WEEK/QUARTER). Catálogos nuevos DIMENSION_KIND, DERIVATION_MODE.
- **Carga de vistas**: clásica = SELECT plano sobre `reference_value`+i18n; copo = join derivado de la cadena de FK identificativas / self-parent de la jerarquía (el compilador la recorre, no se reintroducen niveles).
Verificado: 0 errores de ámbito; render en la demo.

### METADATO-39 — Hechos snapshot periódico: `fact_kind` (evolución temporal de KPIs) — DECIDIDO
Un KPI/hecho no es una foto: la tabla de hechos es una serie temporal y llenarla periódicamente ES su evolución.
- **`accumulative_fact`** += `fact_kind_code`→**FACT_KIND** {TRANSACTIONAL, PERIODIC_SNAPSHOT, ACCUMULATING_SNAPSHOT} (Kimball). PERIODIC_SNAPSHOT = el runner **inserta filas fechadas** por corrida (no re-agrega); el `snapshot_date` es una dimensión temporal.
- **La cadencia** (quincenal/mensual) va por `schedule_cron` del `business_process` (`trigger_kind_code=SCHEDULE`, ya existente en M-34) que dispara el `workflow_pattern` con `RUNNER_KPI`/`RUNNER_DQ`; el log de cada corrida → Observabilidad, el dato fechado → el hecho.
- **Cálculo del hecho/KPI = agregación con filtros y joins**, análoga a la transformación pero **nativa D7** (Opción 2, no se reutiliza la transformación entre-modelos): `accumulative_fact_measure` (campos+`aggregate_function`) + **`accumulative_fact_filter`** + **`accumulative_fact_join`** (espejo de transformation_*, con objeto unido polimórfico), reutilizando catálogos AGGREGATE_FUNCTION/OPERATOR/FILTER_STAGE/JOIN_TYPE y el AST (M-34). [Nota: `accumulative_fact_filter`/`_join` se incorporaron en el mismo tramo M-38/39.]
Modelo 178 entidades / 1161 atributos / 83 catálogos.

### METADATO-40 — Acelerador de auto-observación del metamodelo: siembra de la capa analítica (subject_kind=METAMODEL) + páginas Analítica y CdM — DECIDIDO
Se **puebla** la capa D7 sobre el propio metamodelo (dogfooding): el metamodelo se mide con su propia analítica.
- **Siembra (bootstrap)**: `seed.dimension` (5: DIM_ACCELERATOR clásica, DIM_TERM copo, DIM_ENTITY_TYPE, DIM_DQ_DIMENSION, DIM_SNAPSHOT_DATE), `seed.accumulative_fact` (4: FACT_MM_ENTITY/ATTRIBUTE/CATALOG/QUALITY, todos PERIODIC_SNAPSHOT, grano DÍA), `seed.accumulative_fact_measure` (9), `seed.accumulative_fact_dimension` (8), `seed.kpi` (8: básicos + derivados, subject_kind=METAMODEL), `seed.kpi_dependency` (4). Los hechos se adscriben al acelerador METADATA vía su `business_term` (CANONICAL_ENTITY/DATA_CATALOG/DATA_QUALITY).
- **Runner de snapshot**: script de plataforma que evalúa el metamodelo y emite `public/datum_analitica_snapshot.json` (la corrida de hoy: 178/1161/83, 338 excepciones DQ, 60.1% FK metadata-first, 61.8% término real) + `datum_analitica_history.json` (serie). Cambiar comportamiento = cambiar metadato.
- **Visualizador (2 páginas nuevas, data-driven)**: `/dashboard/analitica` — árbol **acelerador → hecho (grupo) → KPI**, con detalle de hecho y de KPI en el mainlayout (UX auto-generada, METADATO-20). `/dashboard/cdm` — cuadros de mando por acelerador (tiles + calidad DAMA + serie temporal del snapshot). Leen la siembra + el snapshot; ningún dato quemado.
- Modelo sin cambios estructurales (178/1161/83); solo datos de siembra + páginas de la demo.

### METADATO-41 — Materialización del acelerador OBSERVABILITY (ejecución + funcional DATUM A–I + Unity Catalog), en 3 bloques — DECIDIDO

Se **materializa** el acelerador `OBSERVABILITY` (hasta ahora `REGISTRADO` con 0 entidades) a **133 entidades canónicas** en **21 términos** (raíz + 20 hijos), con `domain=''` (aparecen solo por acelerador). Operado sobre disco con `json.loads`/`json.dumps` (sin regex); ficheros completos. Fuente de diseño reconciliada con el mock `src/data/observability.json` de la demo (material de trabajo, no fuente). **Modelo 178→311 entidades; 1161→2712 atributos; catálogos 83→92** (+9). Ubicación física: catálogo `observability` (esquemas process/quality/audit) para lo funcional; nuevo catálogo físico `system` (8 esquemas Databricks) para Unity Catalog. Estructura raíz+hijos por naturaleza (espejo de ANALYTICS/DATA_SOURCE). Validación estructural 133/133 (0 errores: FK, invariante término⟺`domain=''`, PK, ubicación física, TYD reales); árbol por acelerador en `/dashboard/canonico` verificado.

**(A) Bloque 1 — núcleo reasignado por M-33..M-40 (14 entidades, +9 catálogos).** Materializa lo que sesiones previas reasignaron a Observabilidad pero no se había modelado:
- **Término `EXECUTION`** (→process): `run`, `run_step` (ejecución de transformaciones, M-33; raíz self-ref + jerarquía run/step).
- **Término `DISCOVERY_OBSERVATION`** (→process): `source_discovery_run`, `source_discovery_sampling_result`, `source_attribute_profile`, `discovery_rule_evaluation`, `source_discovery_drift` (M-34; el drift ACEPTADO → `source_entity_version`).
- **Término `DQ_OBSERVATION`** (→quality): `dq_run_result`, `dq_column_incident` (gate PRE_WRITE de M-36, veredicto/acción), `dq_incident`, `dq_remediation_action`, `dq_quarantine_record`, `dq_governance_execution` (ejecución de planes/auditorías/certificaciones de D8, M-35).
- **Término `METAMODEL_SNAPSHOT`** (→audit): `metamodel_snapshot_run` (histórico de la corrida del snapshot; el dato agregado sigue en FACT_MM_* de METADATA, M-39/40).
- **Catálogos nuevos (9, CONFIRMADO):** EXECUTION_LEVEL {WORKFLOW,STEP,RUNNER,TASK}, RUN_STATUS {RUNNING,COMPLETED,COMPLETED_WITH_WARNINGS,COMPLETED_WITH_ERRORS,ERROR}, TRIGGER_TYPE {SCHEDULED,MANUAL,EVENT,REPROCESS}, DQ_VERDICT {PASS,WARNING,ERROR}, DQ_ACTION {CAST,DEFAULT_APPLIED,NORMALIZED,REJECTED} (los dos pendientes de M-36), DQ_INCIDENT_STATUS, DQ_GOVERNANCE_KIND, DRIFT_TYPE, DRIFT_STATUS. i18n de entidad es/en/fr/pt de las 14 (row_uuid = sha256('datum:CANONICAL_ENTITY:'+code)[:16]).

**(B) Bloque 2 — funcional DATUM completo A–I (+47 entidades).** Elevadas de `observability.json` (fielmente, saneadas contra el metamodelo): **`ACCESS_AUDIT`** (9, →audit), **`PRIVACY_DPO`** (8, →audit, GDPR/RGPD), **`INCIDENT_ALERT`** (7, →process), **`FINOPS`** (4, →process), **`LIFECYCLE_OPS`** (6, →process), **`GOVERNANCE_MATURITY`** (7, →audit), **`GOLDEN_RECORD`** (3, →quality, MDM), más deltas del grupo A (`run_term`, `run_entity` — weak de run) y de B (`dq_run_failed_records`). Mapeo de tipos crudos a TYD reales (STRING→TYD_STRING, TIMESTAMP→TYD_TIMESTAMP, INTEGER→TYD_INT, `*_uuid`→TYD_UUID…); el campo `audit` de la demo sustituido por el universal `system` (TYD_SYSTEM). Saneamiento del sobre-marcado de PK de la demo → **PK único** por el `*_uuid` de identidad. Sin catálogos nuevos (la demo deja estados/enums como STRING).

**(C) Bloque 3 — Unity Catalog nativo (+72 entidades).** Las 72 system tables de Databricks modeladas como **entidades canónicas nativas** (decisión de Pedro sobre 'fuente externa'), bajo término intermedio **`UNITY_CATALOG`** con 8 hojas: UC_ACCESS (7), UC_BILLING (2), UC_COMPUTE (7), UC_LAKEFLOW (6), UC_QUERY (1), **UC_INFORMATION_SCHEMA (47)**, UC_DATA_QUALITY_MONITORING (1), UC_DATA_CLASSIFICATION (1). Nombres saneados `system.access.audit`→`uc_access_audit` (el FQN Databricks en la descripción); **clave natural compuesta preservada** (no hay uuid); tipos Spark mapeados (STRUCT/ARRAY/MAP/BINARY→TYD_STRING, DOUBLE/FLOAT→TYD_DECIMAL); FKs internos de UC resueltos entre sí. Nuevo catálogo físico `system` (storage_layer=OBSERVABILITY) + 8 esquemas. Ubicación física real Databricks `system.*`, no `observability`.

**Decisiones / saneamientos:** raíz+hijos por naturaleza; PK único por uuid en A–I (limpieza) vs. PK natural compuesta en UC; FK a `source_entity`/`source_attribute` como simples (coherente con la deuda 'Transversal D3' pendiente, no compuestas); `audit`→`system`; los 3 ficheros del visor (`public/datum_modelo_canonico.json`, `datum_carga_inicial.json`, `datum_catalogos.json`) son copias exactas de los `DATUM_*` fuente (los lowercase sueltos en la carpeta fuente estaban obsoletos, a borrar).

**Verificado:** JSON válido (3 ficheros); **311 entidades / 2712 atributos / 92 catálogos**; `canonical_accelerator.OBSERVABILITY.entity_count`=133; 0 FK reales colgantes en los 133; invariante seed↔modelo OK; árbol por acelerador renderiza 12 ramas de primer nivel + `UNITY_CATALOG`→8 hojas.

**PENDIENTES abiertos (M-41):** i18n a nivel **atributo** de las 133 y de **entidad** de las 119 de los bloques 2–3 (solo las 14 del bloque 1 traducidas); **catalogización** de los estados/severidades/tipos que quedaron como STRING (INCIDENT_SEVERITY, CONSENT_STATUS, DSR_STATUS, LIFECYCLE_PHASE…); **revisión/poda de `UC_INFORMATION_SCHEMA` (47 vistas de catálogo Databricks)** — muy homogéneas, valorar dejarlas como referencia; decidir **PK compuesta vs. única** en A–I; poblar `canonical_key`/`canonical_relation` reales; FK compuestas a `source_entity` en discovery-obs (pasada D3 pendiente); `object_type` += EXECUTION_RUN/DQ_OBSERVATION/UC si se necesita para hooks polimórficos.

### METADATO-42 — Ingesta de auditoría UC→observabilidad: persistencia más allá de 365 días + retención (refina M-41) — DECIDIDO

Refina M-41. Las system tables de Databricks (Unity Catalog) retienen solo **365 días**; para auditoría, DATUM persiste una copia propia que sobrevive a esa ventana. Se separan las dos capas que M-41 fundía: `system.*` = **fuente efímera** (read-only, 365d); las 72 `uc_*` = **copia persistente propiedad de DATUM** en `observability`, retención AUDIT_7Y, append-only/inmutable. **Modelo 311 entidades / 2712→2714 atributos / 92→93 catálogos.**

**(A) Metamodelo (retención).** `canonical_entity` += `retention_policy_code` (→**RETENTION_POLICY**, nullable, metadata-first) + `is_append_only` (TYD_BOOLEAN). Catálogo nuevo **RETENTION_POLICY** {SOURCE_DEFAULT, OPERATIONAL_90D, OPERATIONAL_1Y, AUDIT_5Y, AUDIT_7Y, PERMANENT} (CONFIRMADO). Retención = propiedad universal de cualquier tabla canónica.

**(B) Reubicación.** Las 72 `uc_*` pasan de catálogo físico `system` a **`observability`.`uc`** (esquema nuevo), con `retention_policy_code=AUDIT_7Y` e `is_append_only=1`. El catálogo físico `system` queda como ubicación de la **fuente**, no del dato persistente.

**(C) Carga de ingesta** (fichero propio `DATUM_Carga_Observability_UC.json`, patrón PLANTILLA — cada acelerador añade su bloque de carga): `technology` databricks (LAKEHOUSE) + `source_system` `databricks_system` (kind DATABASE) + 8 `source_container` (los esquemas UC) + 72 `source_entity` + 72 `source_entity_capture` + 72 `transformation` PRINCIPAL + 2 `business_process` (uc_audit_ingest, SCHEDULE diario 03:00; uc_discovery, semanal). **Captura: INCREMENTAL por watermark (OPERATOR GT sobre event_time/start_time/usage_start_time/…) para los 25 logs de evento; FULL/SNAPSHOT fechado para las 47 `information_schema`** (estado-actual, sin marca temporal → se historiza por snapshot). Flujo `system.*` → LANDING (source.fuente_database, DELTA) → STAGING (gate DQ) → `observability.uc` (persistente, inmutable). `source_attribute` y la designación de la columna watermark (`source_entity_capture_attribute` role=WATERMARK) se pueblan por **DISCOVERY** (business_process uc_discovery), cuya corrida se **auto-observa** en `source_discovery_run`/`source_attribute_profile` — recursión limpia: la observabilidad observa su propia ingesta. `watermark_columns[]` documenta la columna prevista por tabla.

**Autogestión ("desde ahí gestionar todo").** Una vez la tabla es canónica de DATUM hereda DQ, linaje, retención/lifecycle (LIFECYCLE_OPS: `archive_execution`/`recertification_execution`/`lifecycle_phase_transition`), i18n y analítica; cada corrida de ingesta se observa en `run`/`run_step`, su calidad en `dq_run_result`. La observabilidad se vuelve autoalimentada.

**Verificado:** carga íntegra (0 FK colgantes: transformation→uc_* canónico, capture/transformation→source_entity, source_entity→container; valores de catálogo válidos; landing físico válido); 72/72 uc_* reubicadas con retención AUDIT_7Y. Modelo **311 / 2714 / 93**.

**PENDIENTES abiertos (M-42):** poblar `source_attribute` vía discovery (o hand-seed si se prescinde de discovery); designar `capture_attribute` WATERMARK tras discovery; `transformation_field` 1:1 si la copia no es SELECT * puro; recordatorio operativo de la ventana de 365d de la fuente (la ingesta debe correr con holgura); política de purga/lifecycle de la copia AUDIT_7Y.

*Fin de `18-METADATO-decisiones.md` v1.18.*

