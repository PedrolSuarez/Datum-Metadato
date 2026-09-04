# 18 · Decisiones — Proyecto «DATUM metadato»



**Versión:** v1.82 — Septiembre 2026

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

**(B) Reubicación.** Las 72 `uc_*` pasan de catálogo físico `system` a **`observability`.`uc`** (esquema nuevo), con `retention_policy_code=AUDIT_7Y` e `is_append_only=1`. El catálogo físico `system` que M-41 había creado para las UC se **retira** (huérfano tras la reubicación): la fuente NO se modela como physical_catalog sino vía `source_system`=`databricks_system` (carga M-42/43); physical_catalog queda solo para el almacenamiento propio de DATUM.

**(C) Carga de ingesta** (fichero propio `DATUM_Carga_Observability_UC.json`, patrón PLANTILLA — cada acelerador añade su bloque de carga): `technology` databricks (LAKEHOUSE) + `source_system` `databricks_system` (kind DATABASE) + 8 `source_container` (los esquemas UC) + 72 `source_entity` + 72 `source_entity_capture` + 72 `transformation` PRINCIPAL + 2 `business_process` (uc_audit_ingest, SCHEDULE diario 03:00; uc_discovery, semanal). **Captura: INCREMENTAL por watermark (OPERATOR GT sobre event_time/start_time/usage_start_time/…) para los 25 logs de evento; FULL/SNAPSHOT fechado para las 47 `information_schema`** (estado-actual, sin marca temporal → se historiza por snapshot). Flujo `system.*` → LANDING (source.fuente_database, DELTA) → STAGING (gate DQ) → `observability.uc` (persistente, inmutable). `source_attribute` y la designación de la columna watermark (`source_entity_capture_attribute` role=WATERMARK) se pueblan por **DISCOVERY** (business_process uc_discovery), cuya corrida se **auto-observa** en `source_discovery_run`/`source_attribute_profile` — recursión limpia: la observabilidad observa su propia ingesta. `watermark_columns[]` documenta la columna prevista por tabla.

**Autogestión ("desde ahí gestionar todo").** Una vez la tabla es canónica de DATUM hereda DQ, linaje, retención/lifecycle (LIFECYCLE_OPS: `archive_execution`/`recertification_execution`/`lifecycle_phase_transition`), i18n y analítica; cada corrida de ingesta se observa en `run`/`run_step`, su calidad en `dq_run_result`. La observabilidad se vuelve autoalimentada.

**Verificado:** carga íntegra (0 FK colgantes: transformation→uc_* canónico, capture/transformation→source_entity, source_entity→container; valores de catálogo válidos; landing físico válido); 72/72 uc_* reubicadas con retención AUDIT_7Y. Modelo **311 / 2714 / 93**.

**PENDIENTES abiertos (M-42):** poblar `source_attribute` vía discovery (o hand-seed si se prescinde de discovery); designar `capture_attribute` WATERMARK tras discovery; `transformation_field` 1:1 si la copia no es SELECT * puro; recordatorio operativo de la ventana de 365d de la fuente (la ingesta debe correr con holgura); política de purga/lifecycle de la copia AUDIT_7Y.

### METADATO-43 — Orquestación de la ingesta UC lista para ejecutar (discovery-first) — DECIDIDO

Completa el bootstrap **ejecutable** de M-42: faltaba la orquestación (el `business_process` apuntaba a un `workflow_pattern` vacío). Solo datos de carga (control-plane) en `DATUM_Carga_Observability_UC.json`; **sin cambios de modelo ni catálogos (311/2714/93).**

- **`workflow_pattern` (2):** `uc_discovery_pattern` (INGEST→TRANSFORM: lee el catálogo Databricks y mapea a `source_*`) y `uc_audit_ingest_pattern` (CAPTURE→DQ_GATE(gate)→WRITE: `system.*`→LANDING→STAGING/DQ→`observability.uc`). purpose=INGESTION_VALIDATION, automated.
- **`workflow_pattern_step` (5):** DISCOVER_INGEST/DISCOVER_MAP; CAPTURE/DQ_GATE(`is_gate`)/WRITE, con `runner_type` RUNNER_INGEST/RUNNER_DQ/RUNNER_TRANSFORM (todos con `runner_capability`, M-34), scope ENTITY.
- **`business_process` enganchados:** uc_discovery→uc_discovery_pattern; uc_audit_ingest→uc_audit_ingest_pattern.

**Discovery-first:** la 1ª corrida es `uc_discovery`, que auto-puebla `source_attribute` + tipos nativos + la columna watermark (`source_entity_capture_attribute` role=WATERMARK) y se auto-observa en `source_discovery_run`/`source_attribute_profile`; después `uc_audit_ingest` ingiere. No hace falta sembrar a mano las 838 columnas ni los `data_type`.

**Ejecutable:** el control-plane queda completo; el runner de plataforma (apuntado a un Databricks real) arranca sin metadato faltante. (No hay runtime Databricks en esta sesión: se prepara el bootstrap, no se lanza el job.)

**Verificado:** 2 patrones + 5 steps; runners con capability; business_process→pattern resueltos (0 colgantes).

**PENDIENTE:** 1ª corrida de discovery real para materializar `source_attribute`; ajustar watermark/particionado tras el profiling.

### METADATO-44 — Política de retención de toda la observabilidad (extiende M-42) — DECIDIDO

Extiende la retención de M-42 (hasta ahora solo las 72 UC) a **las 133 entidades del acelerador OBSERVABILITY**. Solo datos de seed (`canonical_entity.retention_policy_code` + `is_append_only`); **sin cambios de modelo ni catálogos (311/2714/93).** Esquema por naturaleza:

- **AUDIT_7Y (92)** — rastro de auditoría regulatoria: ACCESS_AUDIT (accesos), PRIVACY_DPO (GDPR/DPO), GOLDEN_RECORD (linaje MDM) y las 72 UC.
- **AUDIT_5Y (20)** — evidencia de gobierno/calidad/ciclo de vida: DQ_OBSERVATION, LIFECYCLE_OPS, GOVERNANCE_MATURITY.
- **OPERATIONAL_1Y (21)** — observabilidad operativa: EXECUTION, DISCOVERY_OBSERVATION, METAMODEL_SNAPSHOT, FINOPS, INCIDENT_ALERT.

**`is_append_only`:** 122 append-only (logs/eventos inmutables) y **11 con estado mutable** (registros con ciclo de vida que se actualiza): `access_review_finding`, `alert`, `committee_session`, `consent_record`, `data_subject`, `data_subject_request`, `dq_incident`, `dq_quarantine_record`, `incident`, `reactivation_request`, `support_ticket`.

**Verificado:** 133/133 con `retention_policy_code` válido (→RETENTION_POLICY); recuentos intactos (311/2714/93).

### METADATO-45 — Reestructuración de la vista por acelerador de OBSERVABILITY: 2 términos raíz DATUM / UNITY_CATALOG — DECIDIDO

Ajuste de visualización (propuesta de Pedro). Se **retira el término raíz redundante `OBSERVABILITY`** (ese nivel ya lo aporta el acelerador y no tenía entidades propias) y se crea el término raíz **`DATUM`** (observabilidad nativa), **hermano de `UNITY_CATALOG`**. Los 11 términos funcionales (EXECUTION…GOLDEN_RECORD) pasan a colgar de `DATUM`; `UNITY_CATALOG` pasa a raíz. Solo `business_term` (`parent_term_code`); **sin cambios de modelo, entidades ni catálogos (311/2714/93; OBSERVABILITY sigue con 133 entidades y 21 términos).**

Resultado: el acelerador OBSERVABILITY muestra **2 ramas** — `DATUM` (61 entidades: ejecución, discovery, DQ, snapshot, auditoría, GDPR, incidentes, FinOps, lifecycle, madurez, MDM) y `UNITY_CATALOG` (72 tablas Databricks). Dicotomía clara nativa-DATUM / externo-UC.

**Verificado:** 0 entidades colgaban del término `OBSERVABILITY` retirado; árbol renderiza `DATUM` + `UNITY_CATALOG` con sus hijos; recuentos intactos.

### METADATO-46 — Partición de UC_INFORMATION_SCHEMA en 7 sub-términos especializados — DECIDIDO

Ajuste de visualización (propuesta de Pedro). Las 47 tablas de `system.information_schema` (hasta ahora planas bajo `UC_INFORMATION_SCHEMA`) se agrupan en **7 sub-términos especializados**; `UC_INFORMATION_SCHEMA` pasa a **intermedio** (0 entidades directas). Solo `business_term` + etiqueta de entidad (`business_term`/`subdomain`); **sin cambios de modelo, atributos ni catálogos (311/2714/93; OBSERVABILITY 133 entidades, 28 términos).**

- **IS_OBJECTS (11)** — objetos del catálogo: metastores, catalogs, schemata, tables, views, columns, volumes, routines, routine_columns, parameters, information_schema_catalog_name.
- **IS_CONSTRAINTS (6)** — restricciones: table_constraints, key_column_usage, referential_constraints, constraint_column_usage, constraint_table_usage, check_constraints.
- **IS_PRIVILEGES (11)** — grants (`*_privileges`).
- **IS_TAGS (5)** — etiquetas (`*_tags`).
- **IS_SECURITY (2)** — column_masks, row_filters.
- **IS_EXTERNAL (4)** — conectividad: connections, credentials, external_locations, storage_credentials.
- **IS_SHARING (8)** — Delta Sharing: shares, providers, recipients, recipient_tokens, recipient_allowed_ip_ranges, catalog_provider_share_usage, schema_share_usage, table_share_usage.

**Verificado:** 47/47 clasificadas; `UC_INFORMATION_SCHEMA` sin entidades directas; recuentos intactos.

### METADATO-47 — Contrato de población de la observabilidad (cómo se alimenta cada tabla) — DECIDIDO

La observabilidad **nativa de DATUM se EMITE** (telemetría de write-time), no se ingiere como UC. Se modela el contrato metadata-first ("cambiar comportamiento = cambiar metadato"). **Modelo 2714→2716 atributos; catálogos 93→94.**

- **Catálogo `POPULATION_MODE`** {RUNNER_TELEMETRY, GATE_UDF, DERIVED_SCHEDULED, SOURCE_INGEST, APP_TRANSACTION} (CONFIRMADO).
- **`canonical_entity` += `population_mode_code`** (→POPULATION_MODE, nullable, metadata-first): etiqueta cómo se alimenta cada tabla.
- **`runner_capability` += `emits_observability_entity`** (FK→canonical_entity, nullable): qué observabilidad emite cada runner.

**Clasificación de las 133:** **RUNNER_TELEMETRY (27)** — el runner emite al ejecutar: run/run_step/run_term/run_entity, los 5 discovery-obs, dq_run_result/dq_run_failed_records, los 3 golden_record, y los logs de lifecycle/gobierno. **GATE_UDF (1)** — `dq_column_incident` (UDF del gate PRE_WRITE). **DERIVED_SCHEDULED (13)** — proceso programado o transformación desde otra tabla: dq_incident, incident, alert, cost_aggregate/anomaly, budget_breach, metamodel_snapshot_run, platform_health_snapshot, datum_internal_kpi_value, access_event(_aggregate), anomaly_detection. **SOURCE_INGEST (72)** — las UC (ingesta M-42/43). **APP_TRANSACTION (20)** — DPO/consentimiento, tickets, gateway (data_subject, consent_*, dsr_*, data_breach, support_ticket, api_call, ui_navigation, export_event…).

**`emits_observability_entity`:** RUNNER_DQ/_TERM/_PROCESS→dq_run_result; RUNNER_LOAD_CANONICAL→golden_record_fusion; RUNNER_INGEST→source_discovery_run; RUNNER_KPI/_HIERARCHY/_PROCESS→datum_internal_kpi_value. (run/run_step son telemetría universal del harness, no de un runner_type concreto.)

**Verificado:** 133/133 con `population_mode_code` válido; `emits` resuelven a entidades existentes; recuentos 311/2716/94.

**PENDIENTES abiertos (M-47):** definir los `business_process`/`transformation` concretos de los DERIVED_SCHEDULED y las transformaciones `uc_*`→funcional (p.ej. `access_event`←`uc_access_audit`, `resource_consumption`←`uc_billing_usage`); resolver el **solape** `access_event`/`uc_access_audit` (¿vista sobre la UC o copia derivada?); mapear el emit de los runners a nivel N:M si un runner emite varias (hoy 1:1, el principal).

### METADATO-48 — Dedup de observabilidad redundante con UC: vistas sobre uc_* (menos tablas) — DECIDIDO

El acceso al dato pasa **solo por Databricks/UC** (decisión de Pedro): las tablas funcionales que duplican UC dejan de ser copias mantenidas y pasan a **VISTAS sobre las `uc_*`** (sin tabla física, sin ETL, sin retención propia). **`POPULATION_MODE` += `UC_VIEW`; `canonical_entity` += `derived_from_entity`** (FK→canonical_entity). **Modelo 2716→2717 atributos** (catálogos 94; POPULATION_MODE gana un valor).

- **Vistas (UC_VIEW):** `access_event` ← `uc_access_audit` (sigue siendo el **hub**; sus 3 dependientes `api_call`/`export_event`/`policy_evaluation_log` apuntan a la vista, sin reparentar); `access_event_aggregate` ← `uc_access_audit`; `resource_consumption` ← `uc_billing_usage`; `cost_aggregate` ← `uc_billing_usage`. Retención limpiada (heredan de la `uc_*` de origen).
- **Procesos que leen UC** (DERIVED_SCHEDULED, sin copia cruda propia): `cost_anomaly`, `budget_breach` ← `uc_billing_usage` (necesitan lógica de umbral/tendencia, no son una vista).

Resultado: **−4 tablas físicas y sus procesos**, sin romper FKs ni perder cobertura. Las entidades siguen en el modelo (definen la forma de la vista); su materialización física es VIEW sobre la `uc_*`.

**Verificado:** `access_event` intacta como entidad (FKs entrantes OK); `derived_from_entity` resuelve a `uc_*` existentes; 311/2717/94.

**PENDIENTE:** compilar las `canonical_view` reales (SELECT/agregación sobre `uc_*`).

### METADATO-49 — Inventario y definición de los procesos/UDFs de la observabilidad — DECIDIDO

Se computa desde el contrato de población (M-47/48) la lista concreta de procesos/UDFs a gestionar — **no son 61, son pocos** — y se definen los esqueletos de orquestación. Solo datos de carga; **sin cambios de modelo (311/2717/94).**

**Inventario (133 tablas):** RUNNER_TELEMETRY 27 (harness, nada nuevo) · GATE_UDF 1 (`dq_column_incident`, la UDF del gate M-36) · **DERIVED_SCHEDULED 9 (procesos a definir)** · UC_VIEW 4 (vistas M-48, falta compilar SELECT) · SOURCE_INGEST 72 (ingesta UC, hecha M-42/43) · APP_TRANSACTION 20 (las escribe la app/externos, no es pipeline DATUM). **Total a construir: 1 UDF + 9 procesos + 4 vistas.**

**Los 9 procesos definidos** (fichero `DATUM_Carga_Observability_Procesos.json`: 9 `business_process` + 9 `workflow_pattern` + 9 `workflow_pattern_step`): `obs_dq_incident` (RUNNER_DQ, evento ← dq_run_result), `obs_incident` (RUNNER_KPI, horaria ← run_step ERROR + dq_incident), `obs_alert` (RUNNER_KPI, horaria), `obs_cost_anomaly` / `obs_budget_breach` (RUNNER_KPI, diaria ← uc_billing_usage), `obs_metamodel_snapshot_run` (RUNNER_KPI, quincenal ← metamodelo, M-40), `obs_platform_health_snapshot` / `obs_datum_internal_kpi_value` (RUNNER_KPI, diaria), `obs_anomaly_detection` (RUNNER_KPI, diaria ← access_event). Cada uno con su pattern + step (runner con `runner_capability`); 0 FK colgantes.

**Documento de referencia:** `DATUM_Observabilidad_Procesos_UDFs.md` (mapa completo A-UDF / B-procesos / C-vistas / D-telemetría de runner / E-app).

**PENDIENTE:** la **lógica de cómputo** por proceso (umbrales de anomalía/presupuesto, agregaciones) y el **SELECT de las 4 vistas** (passthrough/agregación sobre uc_*) — es el detalle de cada uno, sobre el esqueleto ya definido. La instrumentación de emisión del harness (telemetría) es transversal, una vez.

### METADATO-50 — Mecanismo de emisión de la telemetría de runner (emisor genérico, plataforma) — DECIDIDO

Aclaración de implementación de la observabilidad **RUNNER_TELEMETRY** (M-47): cómo se pueblan `run`/`run_step`/`run_term`/`run_entity` + la telemetría de dominio. **Sin cambios de modelo (311/2717/94)**; solo doctrina + componente de plataforma.

- **Ni INSERT por runner ni UDF.** Un INSERT por runner duplica código; una UDF es para transformación por-fila (el gate `dq_column_incident`), no para logging de ciclo de vida.
- **Emisor genérico en el harness**, invocado en hooks de ciclo de vida (`on_run_start`→INSERT `run`; `on_step_start`→INSERT `run_step`; `on_step_end`→MERGE `run_step` + `run_term`/`run_entity`; `on_run_end`→MERGE `run`). Todos los runners lo heredan; ninguno escribe su propio INSERT.
- **Dirigido por metadato:** `run`/`run_step` = telemetría universal del harness; la de dominio la resuelve `runner_capability.emits_observability_entity`. Añadir runner/observabilidad = 1 fila, no código.
- **Semántica:** INSERT al abrir + MERGE al cerrar (append inmutable; coherente con RUNNER_TELEMETRY + is_append_only); autocontenido (M-35: nunca rompe el circuito).
- **Home:** `runner/observability_emitter` — código de plataforma (como compile_transformation.py), escrito una vez. README `README_observability_emitter.md`.

### METADATO-51 — Vertical de ejemplo end-to-end: emisor + vista UC + proceso de derivación — DECIDIDO

Se implementa una **vertical completa** como plantilla de las 3 mecánicas de población de la observabilidad. Código de **plataforma** en `runner/` (NO metadato). Sin cambios de modelo (311/2717/94).

- **`runner/observability_emitter.py`** — emisor genérico de **RUNNER_TELEMETRY**: hooks `on_run_start`/`on_step_start`/`on_step_end`/`on_run_end` (INSERT al abrir + MERGE al cerrar) para `run`/`run_step`, y `emit_domain` que resuelve la telemetría de dominio por `runner_capability.emits_observability_entity`. Nombres físicos (`observability.process.run`) y columnas leídos del metadato; ningún runner escribe su propio INSERT. Dry-run verificado (traza de una corrida = 5 sentencias).
- **`runner/compile_uc_views.py`** — compila las 4 **UC_VIEW** a `CREATE OR REPLACE VIEW` sobre su `derived_from_entity`: `access_event` con mapeo real de columnas sobre `uc_access_audit` (canal constante DATABRICKS, M-48), `access_event_aggregate`/`cost_aggregate` con GROUP BY, `resource_consumption` passthrough.
- **`runner/compile_obs_cost_anomaly.py`** — proceso **DERIVED_SCHEDULED** `obs_cost_anomaly`: anomalía de coste por **línea base móvil (media + kσ, 30d)** sobre `uc_billing_usage` → `cost_anomaly`, con severidad por magnitud. Ejemplo-plantilla de la lógica de cómputo.

Con esto las 3 mecánicas quedan ejemplificadas y compilables end-to-end; replicar el resto = clonar el patrón + su mapeo/lógica. **Verificado:** los 3 scripts ejecutan y emiten SQL válido.

**PENDIENTE:** replicar mapeo/lógica en las demás vistas y los 8 procesos restantes; el gate UDF (M-36) como compilador propio.

### METADATO-52 — Columnas UC pre-sembradas + mapeo 1:1 (carga UC por el compilador estándar) — DECIDIDO

Decisión de Pedro: (1) no depender de la 1ª corrida de discovery para las columnas de las tablas UC — sembrarlas ya marcadas; (2) aunque la copia sea 1:1, generar las transformaciones necesarias para que la carga UC use **la misma ruta que el resto** (compilador de transformaciones estándar), no un SELECT * especial. Amplía `DATUM_Carga_Observability_UC.json`; **sin cambios de modelo (311/2717/94).**

- **`source_attribute` (838):** las columnas de las 72 tablas UC sembradas y marcadas con su **tipo nativo** (`native_data_type_code`), `is_nullable`, `is_primary_key`, `attribute_order`, `is_selected`. **Ya no hace falta discovery para arrancar**; `uc_discovery` queda solo para **detección de DRIFT** en re-descubrimientos (supersede el discovery-first de M-43 para las columnas).
- **`data_type` (12):** tipos nativos Databricks (STRING, TIMESTAMP, LONG, INTEGER, DOUBLE, DECIMAL, FLOAT, BOOLEAN, DATE, STRUCT, ARRAY, MAP) bajo `technology=databricks`.
- **`transformation_field` (838):** mapeo **1:1** (`source_expression` = columna de origen) por cada atributo canónico → la carga pasa por `compile_transformation.py` como cualquier transformación, uniforme con el resto (INSERT PRINCIPAL).

**Verificado:** 0 FK colgantes (source_attribute→source_entity, native_data_type→data_type, transformation_field→transformation + canonical_attribute existente); 72/72 tablas con sus columnas; 838 mapeos correctos.

### METADATO-53 — Capa analítica del acelerador OBSERVABILITY (subject_kind=OBSERVABILITY) — DECIDIDO

Se siembra la capa analítica D7/ANALYTICS **sobre los datos de observabilidad** (mismo patrón que M-40 para el metamodelo), para consumo por cualquier usuario DATUM. Solo seed analítico; **sin cambios de modelo ni catálogos (311/2717/94).**

- **Dimensiones (+7):** `DIM_CANONICAL_ENTITY`, `DIM_BUSINESS_PROCESS`, `DIM_RUNNER_TYPE`, `DIM_SEVERITY`, `DIM_SOURCE_SYSTEM`, `DIM_PRINCIPAL` (expl.), `DIM_COST_CENTER` (expl.); reutiliza `DIM_SNAPSHOT_DATE`/`DIM_ACCELERATOR`/`DIM_DQ_DIMENSION` de M-40. Inferidas del metadato (catálogo/entidad).
- **6 hechos** PERIODIC_SNAPSHOT · grano DÍA · VIEW (18 medidas, 18 fact_dimension): `FACT_OBS_EXECUTION` (run), `FACT_OBS_QUALITY` (dq_run_result), `FACT_OBS_ACCESS` (access_event), `FACT_OBS_COST` (uc_billing_usage), `FACT_OBS_INCIDENT` (incident), `FACT_OBS_INGESTION` (source_discovery_run).
- **14 KPIs** (10 básicos + 4 derivados con `kpi_dependency`): básicos runs/failed/records/dq_checks/dq_failed/accesses/cost/open_incidents/mttr/drift; derivados `KPI_OBS_SUCCESS_RATE`, `KPI_OBS_DQ_PASS_RATE`, `KPI_OBS_COST_PER_ENTITY`, `KPI_OBS_TRUST_SCORE` (compuesto calidad+incidencia+drift).
- **5 data products publicados** (`data_product`+`_fact`+`_dimension`): `DP_PLATFORM_HEALTH` (CERTIFIED), `DP_DATA_QUALITY_SCORECARD` (CERTIFIED), `DP_ACCESS_AUDIT` (CERTIFIED), `DP_FINOPS_CHARGEBACK` (CURATED), `DP_INGESTION_MONITOR` (CURATED); todos PUBLISHED.

**Verificado:** 0 FK colgantes (fact_dimension→dimension, kpi→fact/measure, kpi_dependency, data_product_fact/dimension); `subject_kind=OBSERVABILITY`; unidades/tiers/perspectivas válidas.

**PENDIENTE:** compilar las vistas de agregación de los 6 hechos y las expresiones de los 4 KPIs derivados (mismo runner analítico de M-40).

### METADATO-54 — Poda del gobierno de calidad (planes DQ) y consolidación del motor de evaluación en un acto único — DECIDIDO

Cierre del bloque D8 de gobierno de calidad + motor de evaluación, sobre disco (`json.loads`/`json.dumps`, ficheros completos). **Modelo 311→303 entidades; 2717→2675 atributos; catálogos 94→95.** Validado estructuralmente (0 FK colgantes, seed↔modelo consistente).

**Principio (confirmado por Pedro):** las reglas DQ ya se **derivan** del metamodelo (`dq_check_type` + `runner/compile_dq_checks.py`, M-35); UNE 0079/0081 e ISO 25012/25040 exigen la **capacidad y la evidencia**, no una forma de tabla. No se regenera información que ya existe.

**(A) Eliminadas (8 entidades, conjunto cerrado, 0 FK externas):**
- Definiciones DQ (D8): `data_quality_requirement`, `dq_implementation_plan`, `dq_assurance_procedure`, `dq_audit_plan`, `dq_certification_criteria`, `dq_evaluation_specification`. Sus campos eran prosa derivable o parámetro absorbible.
- Observabilidad: `dq_governance_execution` (su contenido = run+score+scope+objeto = `object_assessment`) y `maturity_assessment_execution` (acto DAMA-CMMI paralelo y descoordinado del motor genérico).

**(B) Doctrina del gobierno de calidad:** no hay planes de evaluación DQ como entidades. La **certificación** es un `assessment_pattern` de tipo DQ (score derivado de la vista de checks, umbral→nivel vía `assessment_pattern_threshold`); la **auditoría** = cadencia (`business_process.schedule_cron`) + evidencia (`dq_run_result`); el **aseguramiento** = documento/proceso. La medición granular sigue intacta en OBS (`dq_run_result`, `dq_incident`, `dq_column_incident`).

**(C) Acto único de evaluación.** `object_assessment` (+`object_assessment_answer`) reasignado a **OBSERVABILITY** (término `GOVERNANCE_MATURITY`, físico `observability.audit`): hogar único del acto para **todo tipo** (criticidad/madurez/riesgo + certificación DQ). Absorbe `maturity_assessment_execution`. Para DQ el `total_score` sale de agregar `dq_run_result` (no cuestionario); para madurez/criticidad, del cuestionario (`object_assessment_answer`).
- La **definición del motor** SE QUEDA en METADATA: `assessment_pattern`, `assessment_pattern_threshold`, `assessment_question`. `assessment_pattern` +=`framework_code` (→**MATURITY_FRAMEWORK**), +=`dimension_code` (→**MATURITY_DIMENSION**). Estas 3 se sacan del término genérico `METADATA` y se asignan a un término propio **`ASSESSMENT_ENGINE`** (bajo `GOVERNANCE`, acelerador METADATA), para que la definición cuelgue del acelerador con coherencia (el acto vive en OBSERVABILITY/`GOVERNANCE_MATURITY`).
- `object_assessment` +=`target_level_code`, +=`assessor_ref`, +=`evidence_ref` (absorben target_level/assessor_id/evidence_ref del acto DAMA-CMMI).

**(D) Catálogos:** −**DQ_GOVERNANCE_KIND** (huérfano tras eliminar `dq_governance_execution`); +**MATURITY_FRAMEWORK** {DAMA, CMMI}; +**DATA_CRITICALITY** {LOW, MEDIUM, HIGH, CRITICAL} — hueco heredado: catálogo de niveles de resultado para `assessment_pattern` de tipo CRITICALITY (`object_assessment.level_code`/`target_level_code`).

**Verificado:** 303 entidades / 2675 atributos / 95 catálogos; `entity_count` METADATA 178→**170**, OBSERVABILITY **133**; 0 FK colgantes, 0 referencias a DQ_GOVERNANCE_KIND, filas seed de borrados = 0. Registro oficial + propagación al visualizador (public/) + build.



**(F) Saneo del bloque assessment (catálogos metadata-first).** `assessment_type_code`→**ASSESSMENT_TYPE** (sacado de CUARENTENA: es el tipo del patrón del motor genérico), `scoring_method_code`→**SCORING_METHOD** {WEIGHTED_SUM, SIMPLE_AVERAGE, MAX_SCORE} (nuevo), `answer_scale_code`→**ANSWER_SCALE** {BINARY, SCALE_0_5, SCALE_1_5} (nuevo), todos con contrato `reference_catalog`+`catalog_ref_metadata_only`. `framework_code`/`dimension_code`/`MATURITY_FRAMEWORK`/`DATA_CRITICALITY` corregidos a metadata-first + `values`. `level_code`/`target_level_code` permanecen bare a propósito (catálogo de niveles **dinámico** vía `assessment_pattern.level_reference_catalog_code`). Catálogos 95→97.



**(G) Catálogo de nivel dinámico como par autodescriptivo (scale+value).** El nivel de resultado de un assessment usa un catálogo **variable según el tipo**; no puede ser metadata-first con catálogo fijo. Se modela como **par explícito**: nuevo catálogo **`LEVEL_SCALE`** {DATA_CRITICALITY (tipo CRITICALITY), MATURITY_LEVEL (tipo MATURITY); +RISK_LEVEL/COMPLIANCE_LEVEL al crearse} — cada valor es el `code` de un `reference_catalog` de niveles. `assessment_pattern.level_reference_catalog_code`→**`level_scale_code`** (metadata-first→LEVEL_SCALE, deja de ser FK a `reference_catalog`). `assessment_pattern_threshold` y `object_assessment` llevan el **par** `level_scale_code` (chip→LEVEL_SCALE) + `level_code`/`target_level_code` como **valor plano** (`fk_target=null`; ya no se dibuja la relación a `reference_value`). Cada fila es autodescriptiva (escala+valor); integridad (valor ∈ catálogo de la escala) por DQ. Catálogos 97→98; atributos +2.

### METADATO-55 — Reorganización de los dominios residuales D14/D10/D9 a términos de negocio — DECIDIDO

Reubicación de 3 dominios que aún colgaban del genérico `METADATA` a la vista por acelerador, con creación de términos padre/hijo. **Sin cambios de modelo (303 entidades / 2677 atributos / 98 catálogos); solo `business_term` + presentación (`domain=''`).** 22 entidades, 12 términos nuevos (acelerador METADATA). FK intactas (cambia clasificación, no `code`/PK).

- **D14 · Documentación gobernada → `GOVERNANCE` → `DOCUMENTATION`** (término hijo nuevo de GOVERNANCE): `governed_document`, `governed_document_link`, `governed_document_owner`.
- **D10 → término padre nuevo `UX`** con hijos por subdominio: **`UX_SCREENS`** (`ui_module`, `ui_screen`, `ui_screen_breadcrumb_definition`), **`UX_GENERATIVE`** (`presentation_pattern`, `pattern_slot`, `ui_screen_slot_binding`), **`UX_PERMISSIONS`** (`ui_role_permission`, `ui_role_permission_set`), **`UX_BRANDING`** (`client_branding`), **`UX_SUPPORT`** (`support_module_config`, `support_ticket_category`).
- **D9 → término padre nuevo `EXPOSURE`** con hijos: **`EXPOSURE_CORE`** (`data_exposure`, `exposure_consumer`), **`EXPOSURE_MECHANISM`** (`exposure_api_config`, `exposure_push_config`, `exposure_direct_config`), **`EXPOSURE_MARKETPLACE`** (`marketplace_listing`, `marketplace_request`), **`EXPOSURE_COMPLIANCE`** (`exposure_compliance`).

Los dominios D14/D10/D9 quedan vacíos en la vista por dominio (las entidades solo aparecen bajo su acelerador/término). **Verificado:** 22 reubicadas, 12 términos, 0 FK colgantes, `entity_count` METADATA **170** / OBSERVABILITY **133** (sin cambio). Registro oficial + visualizador.



**Carga de catálogos faltantes (parte del ajuste completo).** Las 22 entidades reubicadas tenían **27 atributos `*_code` bare** (FK a `reference_value` sin catálogo). Se **generan y cargan 23 catálogos** (def en `DATUM_Catalogos.json` con `values` + `reference_catalog`/`reference_value` en seed, estado PROPUESTO) y se cablean metadata-first: DOCUMENT_TYPE, STORAGE_KIND, LINK_KIND, OWNERSHIP_ROLE (D14); ADDON_MARKETPLACE, RENDER_MODE, FUNCTIONALITY_KIND, SLOT_KIND, UI_CONTROL, UI_ACTION, THEME, SUPPORT_TIER (D10); RECIPIENT_KIND, EXPOSURE_CHANNEL, APPROVAL_STATUS, API_STYLE, PUSH_ENDPOINT, OUTPUT_FORMAT, SHARE_PLATFORM, ACCESS_LEVEL, LISTING_MODE, TRANSFER_JURISDICTION, SECTORAL_TEMPLATE (D9). **3 excepciones (no son catálogo):** `consumer_principal_code`/`requester_principal_code` → referencia a principal del IdM (`fk_target=null`); `exposure_compliance.legal_basis_code` → FK a la entidad `legal_basis`. Catálogos 98→121. Valores en PROPUESTO, ajustables.

### METADATO-56 — Modelo de seguridad de acceso: término SECURITY (RBAC/ABAC/CONSENT), fusión del consentimiento y poda del baseline derivado — DECIDIDO

Reorganización del bloque de accesos de D8 a un término de seguridad propio, con doctrina de 3 capas: **IdM = identidad** (quién, roles/grupos, pertenencia — NO se remodela); **metamodelo = política de autorización sobre el dato** (qué rol accede a qué objeto del modelo canónico, con qué condición y consentimiento); **Unity Catalog = enforcement** (allow/deny real). **El acceso baseline por rol+scope se DERIVA** del grafo estructural (`business_unit`→`business_process`→`business_term`→`canonical_entity`→`data_product`) + la asignación; se compila, no se modela como filas.

**Dos modos operativos** (misma estructura, distinta fuente de verdad): **A** IdM-autoritativo (`governance_role_assignment` = espejo del IdP, `idp_role_ref`); **B** DATUM-gestionado (DATUM es la fuente de las asignaciones). Flag de provenance a nivel de despliegue.

**Término `SECURITY`** (raíz, acelerador METADATA, hermano de GOVERNANCE) con 3 hijos:
- **`RBAC`**: `governance_role` (roles + `scope_kind`), `governance_role_assignment` (perfil↔objeto gobernable, espejo/gestión IdP).
- **`ABAC`**: `access_policy`, `access_policy_target` (refinamiento fila/masking dentro del alcance → compila a UC).
- **`CONSENT`**: flujo de acceso con consentimiento del owner:
  - **`data_access_request`** (NÚCLEO, fusiona `data_access_grant`+`data_access_grant_approval`+`data_sharing_request`): `requester_role_code`, objeto polimórfico, `access_level_code`→ACCESS_LEVEL, **`purpose_code`→`processing_purpose`** (para qué), `justification_text` (por qué), `valid_from`/`valid_to` (por cuánto), `approval_status_code`→APPROVAL_STATUS (**+REVOKED**), `approved_by_role_code` (el owner), `decided_at`, `recert_frequency_code`→FREQUENCY, `next_recert_date`. El owner aprueba/deniega bajo condiciones; recertificación periódica renueva o revoca.
  - **`data_access_request_condition`** (renombre de `data_access_grant_condition`): enganche ABAC (`access_policy`).
  - **`data_access_review`**: config de recertificación; los **eventos** de recert → Observabilidad.

**Podado:** `effective_permission_cache` (baseline derivado del grafo + asignación; runtime, no metadato).

**Pendiente (no tocado):** las entidades de **privacidad/RGPD** de D8 (`legal_basis`, `processing_purpose`, `processing_activity_record`/ROPA, `data_processing_agreement`, `data_sharing_agreement`, `international_data_transfer`) e `incident_type_definition` siguen en D8, a la espera de su término propio (PRIVACY_DPO / incidentes).

**Verificado:** 303→300 entidades (−4 borradas, +1 fusión); 2677→2666 atributos; APPROVAL_STATUS +REVOKED; 0 FK colgantes; conjunto de borrado cerrado (FK de `_condition` repuntada a `data_access_request`); `entity_count` METADATA 170→**167** / OBSERVABILITY 133. Registro oficial + visualizador.

### METADATO-57 — Cierre de D8: privacidad/RGPD (GDPR_DPO), acuerdos de cesión/encargo (DATA_AGREEMENTS) e incidencias — DECIDIDO

Reubicación de las **7 entidades residuales de D8**, **vaciando el dominio** (D8 cerrado). Sin cambios de lógica, solo `business_term` + presentación; una entidad se reduce a catálogo.

- **Término `GDPR_DPO`** (hijo de `GOVERNANCE`, acelerador METADATA, regulatorio RGPD): `legal_basis` (Art.6), `processing_purpose` (fin del tratamiento) — bases legales (E); `processing_activity_record` (ROPA, Art.30) — (I).
- **Término `DATA_AGREEMENTS`** (hijo de `GOVERNANCE`, **provisional**): `data_processing_agreement` (encargo controller-processor), `data_sharing_agreement` (cesión controller-controller), `international_data_transfer` (SCC/BCR) — cesiones y encargos (H). **Pendiente de decidir** si se mantiene independiente o se lleva a `EXPOSURE` (son el instrumento legal de la exposición externa; `exposure_compliance` ya toca base legal/jurisdicción).
- **`incident_type_definition` → catálogo `INCIDENT_TYPE`** {DATA_BREACH, PII_EXPOSURE, DQ_FAILURE, SLA_BREACH, ACCESS_VIOLATION, PIPELINE_FAILURE} (PROPUESTO). La **entidad se elimina** (0 FK entrantes; solo tenía `code`+texto libre de severity/workflow). Los incidentes reales y su severity/workflow se resuelven en **Observabilidad** (`dq_incident` ya tiene `severity_code`/`incident_status_code`). El catálogo queda **sin enganchar aún** (candidato a un `incident_type_code` en los incidentes de observabilidad).

**Verificado:** dominio D8 = 0 entidades (cerrado); 300→299 entidades (−1 incident); 121→122 catálogos; 0 FK colgantes; `entity_count` METADATA 167→**166** / OBSERVABILITY 133. Registro oficial + visualizador.



**Saneo de catálogos del bloque D8 (parte del ajuste completo).** Los atributos `*_code` bare de las entidades reubicadas: **generados** `SCOPE_KIND` {BUSINESS/BUSINESS_UNIT/BUSINESS_PROCESS/OWNER_SET} (`governance_role.scope_kind_code`) y `SAFEGUARD` {SCC/BCR/ADEQUACY} (`international_data_transfer.safeguard_code`); **sembrado** `BUSINESS_ROLE_PROFILE` (estaba referenciado por `governance_role_assignment.role_profile_code` sin seed); **cableado** `data_access_review.frequency_code`→FREQUENCY. **FK a entidad:** `international_data_transfer.destination_country_code`→`country`. **Referencia externa (no catálogo):** `data_processing_agreement`/`data_sharing_agreement.external_organization_code` → `fk_target=null` (master data de organización externa **no modelado aún** — candidato a entidad). Catálogos 122→124. `DATA_AGREEMENTS` recolocado como **hijo de GOVERNANCE** (no raíz).

### METADATO-58 — Eliminación del dominio D5 (linaje/impacto) — DECIDIDO

Eliminadas las 2 entidades de **D5**: `lineage_view_definition` (vista declarativa de linaje, DATUM-26) e `impact_analysis` (vista aguas abajo de impacto). Conjunto cerrado (0 FK entrantes externas; `impact_analysis`→`lineage_view_definition` interna). Dominio D5 vaciado. **Verificado:** 299→297 entidades; 2649 atributos; 0 FK colgantes; `entity_count` METADATA 166→**164** / OBSERVABILITY 133. Registro oficial + visualizador.

### METADATO-59 — Poda de discovery_rule y unificación de la retención (ciclo de vida del dato) — DECIDIDO

**(A) Poda de `discovery_rule` (+`discovery_rule_evaluation`).** Decisión de Pedro: **las estructuras de las fuentes NO se acomodan a los dominios de datos de common data**. `discovery_rule` solo servía para inferir el `data_type_domain` (semántico) de una columna de origen; sin ese mapeo, no tiene función. El descubrimiento se queda con **estructura + drift** (`discovery_template` + `source_discovery_drift`), sin clasificación semántica. Eliminadas ambas (0 FK entrantes externas).

**(B) Retención unificada (ciclo de vida del dato — distinto del versionado).** Había dos mecanismos redundantes: el catálogo plano `RETENTION_POLICY` (en `canonical_entity.retention_policy_code`) y la entidad paramétrica `lifecycle_policy`. Se **unifica en `lifecycle_policy`**: pasa a ser la definición de cada tier (`retention_days`/`archive_after_days`/`purge_after_days`/`requires_approval`), sembrada con los 6 tiers (SOURCE_DEFAULT, OPERATIONAL_90D, OPERATIONAL_1Y, AUDIT_5Y, AUDIT_7Y, PERMANENT); `canonical_entity.retention_policy_code` → **FK a `lifecycle_policy`** (deja de ser catálogo); **catálogo `RETENTION_POLICY` retirado**. `lifecycle_policy` + `lifecycle_phase_approval_rule` → nuevo término **`LIFECYCLE`** (hijo de GOVERNANCE). Retención = cumplimiento (RGPD storage limitation) + coste (archivar/purgar) + operación; un runner de ciclo de vida la ejecuta; la ROPA la *declara*, esto la *ejecuta*.

**Verificado:** 297→295 entidades (−2); 2636 atributos; 124→123 catálogos; 0 FK colgantes; `entity_count` METADATA 164→**163** / OBSERVABILITY 133→**132**. Registro oficial + visualizador.

### METADATO-60 — Saneo integral de catálogos (todo el modelo) — DECIDIDO

Auditoría de **todo** el modelo (no por bloques): **21 atributos `*_code` bare** (FK a `reference_value` sin catálogo) + **9 referencias a catálogo inexistente**. Todos corregidos a metadata-first:
- **17 catálogos generados** (def + seed, PROPUESTO): `GEO_LEVEL`, `CARDINALITY`, `BUSINESS_UNIT_KIND`, `GOVERNANCE_TOPOLOGY`, `DATE_FORMAT`, `DECIMAL_FORMAT`, `CHANGE_KIND`, `DATA_LAYER`, `UI_CONTEXT`, `ENCRYPTION_ALGORITHM`, `EXPRESSION_TYPE`, `NODE_KIND`, `OPERAND_KIND`, `LOGICAL_TYPE`, `LIFECYCLE_PHASE`, `MASKING_METHOD`, `VERSION_STATUS`. (Varios ya estaban referenciados desde M-28/29/30 pero nunca se sembraron: CARDINALITY, BUSINESS_UNIT_KIND, GOVERNANCE_TOPOLOGY, DATE_FORMAT, DECIMAL_FORMAT, GEO_LEVEL.)
- **Reutilizados** los existentes: `APPROVAL_STATUS` (canonical_view, encryption×2, masking, object_approval), `OPERATOR` (expression_node), `UI_CONTROL` (data_type_domain_ui_control), `BUSINESS_ROLE_PROFILE` (lifecycle_phase_approval_rule), `WRITE_SEMANTICS` (canonical_view).
- **FK a entidad** (no catálogo): `object_approval.approver_role_code`→`governance_role`.

**Verificado (auditoría a cero sobre TODO el modelo):** 0 atributos bare, 0 referencias a catálogo inexistente, 0 FK colgantes. Catálogos 123→134; sin cambios de entidades/atributos (295/2636). Registro oficial + visualizador.

### METADATO-61 — Consolidación del versionado + recategorización de catálogos — DECIDIDO

Dos frentes de limpieza cerrados juntos (respuestas de Pedro: **a sí, b no, c recategorizar TYPE**).

**(a) Versionado consolidado.** El versionado de objetos estaba disperso en 4 tablas SCD2 casi idénticas —`canonical_attribute_version`, `canonical_entity_version`, `source_attribute_version`, `source_entity_version`—, una por tipo de objeto. Se **fusionan en una única tabla polimórfica `object_version`** (patrón ya usado en `object_text`/`object_approval`): identidad `object_row_uuid` + `object_type_code` (→ OBJECT_TYPE) + `version_number`, con los campos SCD2 (valid_from/valid_to, is_current, change_kind_code, version_status_code…). La FK entrante `source_discovery_drift.accepted_into_version_code` (apuntaba a `source_entity_version`) se **repunta a `object_version`**. `object_version` + `object_approval` se agrupan en un término nuevo **VERSIONING** (padre GOVERNANCE, bajo METADATA).

**(b) `VERSION_STATUS` NO se fusiona con `PUBLICATION_STATUS`** (decisión explícita de Pedro): son ciclos distintos (estado de una versión de objeto vs. estado de publicación de un artefacto), se mantienen separados aunque hoy compartan valores.

**(c) Recategorización de catálogos.** Los 134 catálogos tenían `category` heterogénea/heredada. Se reclasifican en **9 categorías funcionales** por la semántica del valor que codifican:

- **KIND (71)** — tipologías/clasificaciones (qué *es* algo): AGGREGATE_FUNCTION, ASSESSMENT_TYPE, CARDINALITY, INCIDENT_TYPE, JOIN_TYPE, KEY_TYPE, OPERATOR, RULE_KIND, SOURCE_SYSTEM_KIND, TRANSFORMATION_ROLE… (TRANSFORMATION_ROLE reclasificado FORMAT→KIND: es una tipología de transformación, no un formato).
- **MODE (17)** — modo/estrategia/método de operar: CAPTURE_MODE, MASKING_METHOD, MATERIALIZATION_MODE, SCORING_METHOD, SURVIVORSHIP_STRATEGY, WRITE_SEMANTICS…
- **STATUS (10)** — estado en un ciclo de vida: APPROVAL_STATUS, LIFECYCLE_STATE, PUBLICATION_STATUS, RUN_STATUS, VERSION_STATUS…
- **LEVEL (10)** — nivel/escalón ordenado: ACCESS_LEVEL, DATA_CRITICALITY, DQ_SEVERITY, LEVEL_SCALE, MATURITY_LEVEL, SECURITY_CLASSIFICATION…
- **ACTION (7)** — acción a ejecutar: BREACH_ACTION, DQ_ACTION, ON_MISS, REFERENTIAL_ACTION…
- **FORMAT (5)** — formato de representación: DATE_FORMAT, DECIMAL_FORMAT, LANDING_FORMAT, OUTPUT_FORMAT, STREAM_MESSAGE_FORMAT.
- **DIMENSION (5)** — eje/dimensión de medida: DQ_DIMENSION, ISO_CHARACTERISTIC, MATURITY_DIMENSION, PERSPECTIVE…
- **TIME (5)** — temporalidad: FREQUENCY, TEMPORAL_HIERARCHY_TYPE, TIME_GRAIN…
- **ROLE (4)** — rol de negocio/autoridad: BUSINESS_ROLE_PROFILE, OWNERSHIP_ROLE, STANDARD_AUTHORITY, CAPTURE_ATTRIBUTE_ROLE.

Propagado al **bootstrap del Control Plane**, no solo al fichero de definición: `categories[]` de `DATUM_Catalogos.json` reescrito con las 9, y en `DATUM_Carga_Inicial_Metadato.json` el seed `reference_category` pasa de 6→9 (KIND/STATUS/LEVEL/MODE/ACTION/FORMAT/DIMENSION/ROLE/TIME) y los 133 `reference_catalog.category_code` remapeados (antes 116 en `TYPE`; ahora KIND 71, MODE 17, STATUS 10, LEVEL 9, ACTION 7, FORMAT 5, DIMENSION 5, TIME 5, ROLE 4 — `MATURITY_LEVEL` es def-only, no sembrado). La categorización es **organizativa** (agrupación en el visualizador/gobierno), no cambia el contrato metadata-first ni los valores.

**Verificado:** entidades 295→291, atributos 2636→2608, METADATA 163→159 / OBSERVABILITY 132 sin cambio; catálogos 134 (recuento sin cambio); 0 FK colgantes en todo el modelo. Registro oficial + visualizador.

### METADATO-62 — Poda de tablas de extensibilidad + término VIEWS — DECIDIDO

**Poda.** `canonical_attribute_attribute` y `canonical_entity_attribute` (D2·H · Extensibilidad, tipo REF) eran tablas para colgar atributos ad-hoc extra sobre un atributo/entidad canónicos. Duplicaban el concepto ya cubierto por `canonical_attribute` y **no tenían ninguna FK entrante ni uso** en el modelo. Eliminadas de modelo y seed.

**Término VIEWS.** Las 5 entidades de vistas canónicas y expresión —`canonical_view`, `expression`, `expression_node`, `expression_operand`, `function_catalog`— vivían en el subdominio genérico `D2·G` con `business_term` = `METADATA` (placeholder), por lo que no colgaban de ningún término real en el árbol del acelerador. Se crea el término **VIEWS** (hijo de `COMMON_DATA`, orden 40, junto a `CANONICAL_ENTITY`) y se les asigna.

**Verificado:** entidades 291→289, atributos 2608→2598; 0 bare, 0 catálogo inexistente, 0 FK colgantes. Registro oficial + visualizador.

### METADATO-63 — Cierre de flecos de términos + coherencia seed↔modelo — DECIDIDO

Cuatro ajustes que dejan el árbol de términos limpio y el seed alineado con el modelo:

1. **`canonical_model_change` → VERSIONING.** Es el changelog del esquema del metamodelo (qué cambió, si es breaking, cuándo se anunció). Misma familia que `object_version`/`object_approval`; se agrupa bajo VERSIONING.

2. **Borradas 16 filas seed de ingesta de fuentes.** `source_entity_partition_strategy`, `source_connection`, `source_connection_credential`, `source_connection_token_state`, `source_entity_database`, `source_entity_file`, `source_entity_api_endpoint`, `source_api_endpoint_parameter`, `source_api_graphql_query`, `source_api_soap_operation`, `source_entity_stream_topic`, `source_entity_webhook`, `source_entity_excel_workbook`, `source_archive_container`, `multi_record`, `source_entity_relation`. Estaban en `seed.canonical_entity` con el placeholder `business_term_code='METADATA'` pero **no materializadas en el modelo** y su contenido ya está incluido en otras tablas de fuentes. Se retiran del seed.

3. **DATA_AGREEMENTS: GOVERNANCE → EXPOSURE.** Las cesiones (`data_sharing_agreement`), encargos (`data_processing_agreement`) y transferencias internacionales (`international_data_transfer`) son exposición de datos a terceros; el término cuelga ahora de EXPOSURE (mantiene `is_regulatory`/RGPD).

4. **Geografía = estructura + dimensión (patrón TIME).** El término `GEO_STRUCTURE` ya existía bajo `HIERARCHY` (junto a `TEMPORAL_STRUCTURE`) y las 11 entidades (`continent`, `supra_zone`, `region`, `province`, `locality`, jerarquía comercial y fiscal) ya lo tenían en el seed. Es la **definición de la estructura geográfica** que luego se usa como dimensión, igual que TIME. Solo se alineó el campo `business_term` del modelo (estaba a None).

**Aclaración sobre "las 17 entidades genéricas":** eran exactamente las **16 de ingesta** (punto 2) **+ `canonical_model_change`** (punto 1). Al ejecutar 1 y 2 desaparece el grupo: **0 entidades con término genérico**.

**Verificado:** entidades 289, atributos 2598; `seed.canonical_entity` (289) coincide 1:1 con el modelo (289); 0 bare, 0 catálogo inexistente, 0 FK colgantes; acelerador METADATA 157 / OBSERVABILITY 132. Registro oficial + visualizador.

### METADATO-64 — Maestro de terceros `external_organization` — DECIDIDO

Cierre del último fleco: la organización externa contraparte de cesiones y encargos estaba referenciada pero no modelada (`external_organization_code` como código suelto con `fk_target=None` y nota "master data no modelado aún").

**Entidad nueva `external_organization`** (master-data, tipo MDM), asignada al término **DATA_AGREEMENTS** (bajo EXPOSURE), patrón `business_unit`:
- `code` (BK, PK), `legal_name` (razón social), `country_code` → FK `country`, `tax_id` (NIF/VAT), `gdpr_role_code` → catálogo `GDPR_PARTY_ROLE` (metadata-first), `dpo_contact`, `system` (TYD_SYSTEM).

**Catálogo nuevo `GDPR_PARTY_ROLE`** (categoría ROLE, CERRADO, autoridad RGPD): CONTROLLER (responsable), PROCESSOR (encargado), JOINT_CONTROLLER (corresponsable), RECIPIENT (cesionario), SUB_PROCESSOR (subencargado). Sembrado completo: def + `reference_catalog` + 5 `reference_value`.

**Conversión a FK reales:** `data_sharing_agreement.external_organization_code` (el cesionario) y `data_processing_agreement.external_organization_code` (el encargado) pasan de código suelto a **FK `external_organization`** (RESTRICT), dando integridad referencial y reutilización del mismo tercero en varios acuerdos.

**Verificado:** entidades 289→290, atributos 2598→2605, catálogos 134→135; seed↔modelo 290=290; 0 bare, 0 catálogo inexistente, 0 FK colgantes; acelerador METADATA 158 / OBSERVABILITY 132. Registro oficial + visualizador.

### METADATO-65 — Cierre de coherencia de catálogos — DECIDIDO

Tras la auditoría integral de coherencia (que salió limpia en integridad, seed↔modelo y árbol de términos), se cierran los cuatro puntos de pulido detectados:

1. **48 catálogos PROPUESTO → CONFIRMADO.** Toda la curaduría de contenido pendiente pasa a definitiva (incluye el recién creado GDPR_PARTY_ROLE). Estado del catálogo unificado: **133 CONFIRMADO, 0 PROPUESTO, 0 ACTIVE**.
2. **`MATURITY_LEVEL` eliminado.** Estaba definido pero ni sembrado ni referenciado: `assessment_pattern_threshold` usa el patrón dinámico `level_scale_code`→LEVEL_SCALE + `level_code` (dinámico, integridad por DQ), que lo sustituye. Catálogo muerto → fuera.
3. **`STANDARD_AUTHORITY` estado `ACTIVE`→`CONFIRMADO`.** Era el único catálogo con ese valor de estado; normalizado al vocabulario del resto.
4. **Unificación `VERSION_STATUS` → `PUBLICATION_STATUS`.** Los dos catálogos tenían valores idénticos {DRAFT, PUBLISHED, DEPRECATED, RETIRED}. Se conserva `PUBLICATION_STATUS` (CONFIRMADO, ordenado, autoridad INTERNAL) y se retira `VERSION_STATUS` (el duplicado creado en M-60). `object_version.version_status_code` repunta a `PUBLICATION_STATUS`; VERSION_STATUS eliminado de def, `reference_catalog` y `reference_value`. (Revierte la decisión b de M-61 a petición del founder.)

**Verificado:** catálogos 135→133; `reference_value` 558→554; def↔seed cuadran (133=133); 0 catálogos sembrados sin valores; 0 bare, 0 catálogo inexistente, 0 FK colgantes; entidades 290 / atributos 2605 sin cambio. Registro oficial + visualizador.

### METADATO-66 — FINANCE materializado en la vista canónica, corrección integral de TYD, capa organizativa, eliminación de `party` (maestros por tipo + registro de dependencias) y acelerador Compras (PROCUREMENT) — DECIDIDO

Sesión amplia sobre los **modelos cargables (aceleradores de negocio)** y su integración en la demo canónica Next.js (`/dashboard/canonico`, `dataplane - demo`). Operado sobre disco con `json.loads`/`json.dumps`; ficheros completos. **El metamodelo núcleo (290 entidades METADATA+OBSERVABILITY) no cambia**; M-66 materializa/registra aceleradores de negocio y su integración.

**(A) FINANCE materializado e integrado.** El acelerador `FINANCE_CORPORATE_v1` pasa de REGISTRADO (0) a **ACTIVO (131 entidades)**: inyectado en `datum_carga_inicial.json` (seed acelerador→business_term→canonical_entity) y `datum_modelo_canonico.json` (detalle). **11 términos padre `FIN_*`** + término `FIN_EXTERNAL_PARTIES`. **316 catálogos** integrados en `datum_catalogos.json`, con relación atributo↔catálogo metadata-first (`reference_catalog` + `catalog_ref_metadata_only` + `usado_en`). Glosario de entidades (artefacto).

**(B) `legal_entity` de primera clase.** Promocionada desde `legal_entity_role_profile` (perfil de rol colgado de `party_role_assignment`) a entidad maestra: PK `[id, legal_entity_code]`; árbol societario unificado al nivel LE; **50 FK** repuntadas; **5 FK rotas preexistentes reparadas**.

**(C) Corrección integral de TYD.** El acelerador usaba 9 tipos gruesos, incl. `TYD_DECIMAL`/`TYD_TIMESTAMP` **inexistentes en el catálogo canónico** de 36 dominios. **1.502 columnas** retipadas: FK→`TYD_UUID`; importes→`TYD_MONETARY_VALUE`; `_pct`→`TYD_DECIMAL_PERCENT`; `_at`→`TYD_TIMESTAMP_UTC`; currency/country/language→dominios ISO; IBAN/BIC/NIF; textos→`TYD_TEXT_DESCRIPTION`. **0 TYD no canónicos**; 18 casos particulares anotados (tipos de cambio, sensibilidades, medidas físicas).

**(D) Capa organizativa FINANCE** (`datum_org.json`): 7 unidades (raíz FINANCE + 7 departamentos), 21 procesos, 27 asignaciones proceso→término (`business_process_term`).

**(E) Eliminación de `party` — arquitectura de identidad.** Se **RECHAZA la tabla `party` monolítica**. Cada tipo de actor es su **propia entidad maestra** (`supplier`, `legal_entity`, futuros `customer`/`employee`); la identidad "es el mismo actor" entre tipos se resolverá por **matching/xref**, no por fila compartida. Retirado `party_id`/`party_role_assignment_id` de los maestros. Las **144 referencias `*_party_id`** restantes se **ANOTAN** (metadata-first, sin tabla): `pending_party_role` + `pending_accelerator` + `party_nature` + `resolved_entity`. Catálogo `PARTY_ROLE`. Registro de dependencias (artefacto). **El viejo modelo PARTY (G33) queda SUPERADO.**

**(F) Acelerador Compras (PROCUREMENT) — NUEVO, ACTIVO (15 entidades).** Hogar del proveedor que faltaba. Términos: **SUPPLIER** (`supplier` maestro + site/bank/contact/qualification), **PURCHASE_REQUISITION**, **PURCHASE_ORDER**, **GOODS_RECEIPT**, **PROCUREMENT_CONTRACT** (contrato marco), **SUPPLIER_EVALUATION**. 17 catálogos, TYD canónicos. Integrado en la vista canónica (3 términos padre `PROC_*`) y org (BU **COMPRAS**, 4 procesos). Three-way match `supplier_invoice`↔`purchase_order`↔`goods_receipt`. **Repunte AP de FINANCE**: `supplier_party_id`→`supplier_id`. Ficheros fuente: `datum_terminos_modelo__PROCUREMENT_v1.json`, `datum_catalogos__PROCUREMENT_v1.json`.

**(G) Maestros de contrapartes externas** (FINANCE, término `FIN_EXTERNAL_PARTIES`): `bank`, `lender` (prestamista: banco/fondo/Estado/bonista), `auditor`, `regulator` con catálogos `*_KIND`. **8 referencias** repuntadas. `external_partner` resuelto a `supplier`/`bank` (factoring→bank; insurance/maintenance/valuator/collection/advisor/**manufacturer**→supplier); `counterparty` → **puntero polimórfico** `counterparty_type_code` (cat COUNTERPARTY_TYPE) + `counterparty_id`. **UNASSIGNED = 0.**

**(H) Franquiciados (doctrina, no ejecutada).** `FRANCHISEE` es rol del dominio franquicia/retail (`OPS_RETAIL_FASTFOOD`), con FK a `brand` (marketing); ni FINANCE ni marketing como dueño. Se modelará con ese acelerador.

**Estado tras M-66:** aceleradores ACTIVOS en la vista canónica: METADATA, OBSERVABILITY, **FINANCE (131)**, **PROCUREMENT (15)**. Modelo canónico de la demo **433 entidades**; catálogos **466**; org 15 BU / 51 procesos / 112 vínculos. Party eliminado; **6 maestros vivos** (supplier, legal_entity, bank, lender, auditor, regulator); **119 dependencias pendientes** registradas (HR 112, COMMERCIAL 7; UNASSIGNED 0).

**Pendientes:** crear aceleradores **COMMERCIAL** (`customer`) y **HR** (`employee`) y repuntar sus 119 dependencias; 18 casos particulares de TYD; i18n de términos padre (`FIN_*`/`PROC_*`) y procesos; modelar franquiciados; retirar físicamente el viejo modelo PARTY (`datum_terminos_modelo__PARTY_v1.json`). **Registro oficial.**

### METADATO-67 — Consolidación técnica de aceleradores, reestructuración de `legal_entity` (golden record + satélites), criterio de PK maestro/dependiente, cardinalidades, calendario fiscal y repo como fuente única — DECIDIDO

Sesión sobre los **aceleradores de negocio** (FINANCE/PROCUREMENT) y la **arquitectura de fuente de verdad**. Operado sobre disco (`json.loads`/`json.dumps`, ficheros completos), escrito en repo + visor. **El metamodelo núcleo (290 METADATA+OBSERVABILITY) no cambia.**

**(A) Bloque técnico suelto → `system` (TYD_SYSTEM) en aceleradores.** FINANCE/PROCUREMENT llevaban `audit` (TYD_AUDIT) + `status_value_id` genérico sueltos, en vez del `system` universal del metamodelo (M-9). Colapsados a un único `system`: FINANCE −132 `audit`, −123 `status_value_id` (su catálogo `STATUS` estaba **roto** —valores `_,P,E,N,D,I,T`— y se retira; el ciclo de vida vive en `system.lifecycle_state_code`→LIFECYCLE_STATE), +135 `system`; PROCUREMENT −15 `audit`, +15 `system`. **Se conservan** los status de **negocio** (`*_status_value_id`, y los `status_value_id` de PROCUREMENT que apuntan a catálogos reales PO_STATUS/RECEIPT_STATUS…). Limpiadas 246 reglas `dq` + 123 `keys` colgantes. **Divisa NO tocada**: el patrón multidivisa (`*_currency_id` de alcance local/funcional/transaccional/reporte) es legítimo, no redundante.

**(B) Barrido SCD2.** Los campos SCD2 (historización de la fila) se **materializan automáticamente desde las delta properties (D05)**, no se modelan (el metamodelo modela 0). Retirados el placeholder basura `"SCD2 (3)"` (33), `is_active`/`version` sueltos (18, ya dentro de `system`) y `valid_from`/`valid_to` donde acompañaban a SCD2 (8). **Conservada la vigencia de negocio real** (contratos/acuerdos/asignaciones con plazo). Después también se retiran `valid_from`/`valid_to` de `address`/`contact`/`ownership_structure` (no son vigencia de negocio; la historia la da SCD2).

**(C) `legal_entity` reestructurada: golden record magro + satélites por concern.** El maestro dejaba de ser identidad para ser cajón de sastre y duplicaba datos (`primary_tax_id`≟`tax_registration_number`, `business_registration_number`≟`registration_number`, `vat_number` mal ubicado). Core reducido a **15 atributos de identidad pura** (`id`, code, name, short_name, legal_form, `country_of_incorporation`, `lei_code`, kind, incorporation/dissolution_date, parent/ultimate_parent, lifecycle_status, notes, system). Cada concern a su satélite (FK al `id` del maestro): `legal_entity_tax_profile`, `legal_entity_registration`, **`legal_entity_financial_profile`** (nuevo), **`legal_entity_listing`** (nuevo), **`legal_entity_audit_profile`** (nuevo), **`legal_entity_classification`** (nuevo), `legal_entity_address`, `legal_entity_contact`. Quitados del core: `country_of_tax_residence` (redundante con `tax_profile`), `internal_management_responsibility_party_id` (es un rol/asignación, no identidad; irá en org/HR), `consolidation_group_id` (ver E). FINANCE 133→137 entidades.

**(D) Criterio de PK para aceleradores de negocio (regla general).** Distinto del metamodelo, para anonimización de datos dependientes:
- **Maestro** (lo referencian otros por FK): `PK=[id]`, `id=sha2('datum:'||BK)`, `UI` sobre la BK natural. El `id` opaco permite anonimizar.
- **Dependiente hoja** (sin FK entrante): **sin surrogate**; `PK=[<id del padre> + discriminadores]`. Hereda anonimización por el `id` del padre; los discriminadores son códigos de catálogo, no sensibles. (Las 8 hijas de `legal_entity` son hojas verificadas: 0 FK entrantes.)

**(E) Cardinalidades corregidas a la realidad de una entidad legal única.** Una entidad se constituye en **un** país, se inscribe en **un** registro, tiene **una** identidad fiscal de origen. La multiplicidad (IVA/registro extranjero) es **presencia operativa / establecimiento**, no filas de la entidad. Resultado: **1:1** `tax_profile`, `registration`, `financial_profile`; **1:N** `audit_profile` (coauditoría FR), `listing` (dual-listing), `classification` (varios CNAE/NAICS por esquema+código), `address`, `contact`. **Pertenencia a consolidación = M:N** vía `consolidation_scope_member` (retirado `consolidation_group_id` del core, forzaba grupo único). Cargos (CEO/administrador) = asignación de rol, futura capa org/HR.

**(F) Calendario fiscal enganchado a TIME.** La dimensión TIME ya trae una jerarquía **`FISCAL` (`PARALLEL_CONFIG`)** parametrizada por compañía (pendiente anotado en el propio fichero: "valores por compañía → perfil de compañía"). Se materializa: `financial_profile.fiscal_year_start_month`/`day` + `fiscal_period_kind_value_id` (→PERIOD_KIND_DEFAULT) **parametrizan TIME.FISCAL**; `accounting_book.fiscal_year_start` pasa a **override**; el **fin de ejercicio se deriva** (inicio−1 día); los períodos reales (`accounting_period.period_start/end_date`) unen a TIME por fecha. Sustituye a `fiscal_year_end_month/day` (fin) del perfil.

**(G) Catálogo `CLASSIFICATION_SCHEME` completo (12 esquemas).** CNAE, NACE, NAICS, SIC, UK_SIC, ISIC, NAF/APE, ATECO, WZ, ANZSIC, GICS, ICB (cada uno con descripción). `legal_entity_classification` es N por esquema **y** por código (una empresa puede tener varios CNAE). `classification_code` debe validar contra el catálogo de códigos de su esquema (per-scheme, pendiente de poblar).

**(H) Repo `DATUM Metadato` = fuente única de verdad.** Los JSON `datum_*` (minúscula) del repo son la fuente que pinta el **visor canónico**; `dataplane-demo` es copia. Sincronizado el repo al estado limpio: **eliminadas 74 tablas de metamodelo obsoletas** (limpiezas ya hechas que el repo arrastraba) e **incluidos OBSERVABILITY/FINANCE/PROCUREMENT** en `datum_modelo_canonico`/`carga_inicial`/`catalogos`. Los ficheros bootstrap `DATUM_*` (mayúscula: `DATUM_Modelo_Datos_Metadato`, `DATUM_Carga_Inicial_Metadato`, `DATUM_Catalogos`) **RETIRADOS a `_to_delete`**: `datum_*` es la fuente única que **formará** el bootstrap del Control Plane — no se gestiona doble. Copia viva de los aceleradores movida al repo.

**Estado tras M-67:** metamodelo núcleo sin cambio; **FINANCE 137** (legal_entity 15 + 8 satélites, 4 nuevos); PROCUREMENT 15; visor y repo alineados (fuente única). `legal_entity` cerrada como golden record.

**Pendientes:** poblar catálogos de códigos por esquema de clasificación; aceleradores COMMERCIAL/HR y sus dependencias; modelar establecimiento/sucursal (IVA extranjero) cuando toque; asignación de cargos (org/HR); i18n; retirar viejo PARTY. **Registro oficial.**

### METADATO-68 — Autoridades fiscales/registrales → maestro `regulator`; impuestos aplicables (`legal_entity_tax`) desacoplando el sesgo IVA — DECIDIDO

Continuación de M-67 sobre `legal_entity` (aceleradores de negocio; **metamodelo núcleo sin cambio**).

**(A) Autoridades como `regulator`.** Los `*_authority_party_id` estaban mal anotados como dependencia `EMPLOYEE`/`HR` (volcado M-66). Repunteados al maestro **`regulator`** (M-66): `legal_entity_registration.registration_authority_party_id` → **`registration_authority_id`** (FK `regulator`; conserva `registration_authority_name` como texto de apoyo); `legal_entity_tax_profile.tax_authority_party_id` → **`tax_authority_id`** (FK `regulator`). `ownership_structure.owner_party_id` se deja **sin tocar** (decisión del founder: el owner polimórfico —legal_entity/persona/fondo— se resolverá con sus maestros). `validity_until_date` de `registration` confirmado **opcional** (null = registro indefinido; con fecha = caduca/renueva).

**(B) Impuestos aplicables desacoplados del IVA.** `tax_profile` cableaba los impuestos como columnas fijas de IVA (`vat_*`) + tasa suelta de IS y de retenciones — **inválido** para IGIC (Canarias), IPSI (Ceuta/Melilla) y para N impuestos simultáneos. **Nueva entidad `legal_entity_tax`** (1:N, hoja; PK `[legal_entity_id, tax_type_value_id]`; sin surrogate, hereda anonimización del padre): un impuesto por fila con `rate_default_pct`, `scheme_value_id`, `registration_number`, `registration_status_value_id`, alta/baja. `tax_profile` queda como **cabecera de identidad fiscal + obligaciones** (territorio, NIF, autoridad, intra-EU, CbC/DAC6/DAC7/precios de transferencia, e-invoicing); **migrados fuera 8 campos** (vat_number/scheme/status/rate, IS is_subject+rate, retención is_subject+rate). **Catálogos**: +`TAX_TYPE` (14: IVA/IGIC/IPSI/VAT/GST/SALES_TAX/IS/CIT/IRPF_RET/WHT/IRNR/IAE/ITP_AJD/STAMP_DUTY), +`TAX_SCHEME` (8, incl. ZEC/REF canario), +`TAX_REGISTRATION_STATUS` (6); **retirados** `VAT_SCHEME`/`VAT_REGISTRATION_STATUS` (huérfanos tras la migración).

**Estado tras M-68:** FINANCE **137→138** entidades; `tax_profile` 29→21 atributos; catálogos +3 −2. Verificado: `legal_entity_tax` PK compuesta, hoja sin surrogate, row_id deterministas; 0 keys/dq colgantes en `tax_profile`. Repo + visor + Instrucciones escritos.

**Pendientes:** `owner` polimórfico de ownership cuando lleguen maestros persona/fondo; ~53 `*_party_id` (approved_by/prepared_by/reviewed_by/customer…) a la espera de HR (`employee`)/COMMERCIAL (`customer`); poblar `classification_code` por esquema; poblar valores reales de impuestos por entidad. **Registro oficial.**

### METADATO-69 — Acelerador **Recursos Humanos (HR)** materializado; `employee` como maestro de persona interna; satélites y cableado de catálogos metadata-first — DECIDIDO

Acelerador de negocio (**metamodelo núcleo sin cambio**). Materializa HHRR sobre `datum_terminos_modelo__HHRR_v1.json` (esquema v2) y su integración en la vista canónica.

**(A) Materialización y saneo global.** **76 entidades** HR bajo 9 términos padre (EMPLOYEE, POSITION, COMPENSATION_PACKAGE, PAYROLL_RUN, PERFORMANCE_REVIEW, BENEFIT_ENROLLMENT, TIME_OFF_REQUEST, EMPLOYEE_CERTIFICATION, CANDIDATE); **1.166 atributos**. Saneo: TYD canónicos, `system` compuesto (M-9) en lugar de audit+`status_value_id` sueltos, repunte de dependencias party/legal_entity. Rellenadas las entidades *stub* vacías desde estándar HR.

**(B) `employee` = maestro de persona interna** (decisión del founder: **no** `natural_person` compartido). Golden record magro (21 atributos: identidad legal, estado de ciclo de vida, empleador actual, contrato actual, manager, fechas de alta, HRBP/recruiter, centro de trabajo primario). `PK=[id]`, `id=sha2('datum:'||BK)`, `UI=[current_legal_entity_id, employee_code]`.

**(C) Dependencias y cardinalidades.** `work_center` (centro de trabajo) **dependiente de `legal_entity`** (`DEPENDENT_MASTER`, `UI=[legal_entity_id, work_center_code]`); `employee` **dependiente de `legal_entity`** (empleador). Del empleado cuelgan como **hojas débiles** (`PK=[employee_id (+discriminador)]`, sin surrogate, heredan anonimización del padre): `employee_contact`, `employee_address`, `employee_work_authorization` (1:N por país). `employee` **partido en 6 satélites 1:1** por *concern*: `employee_personal_profile`, `employee_payroll_profile`, `employee_employment_terms`, `employee_termination`, `employee_data_privacy` (RGPD). Contrato/contacto/dirección = dependientes del empleado, **sin relación directa con `legal_entity`**.

**(D) Catálogos poblados + cableado metadata-first.** **100 catálogos HR**, todos con valores (85 CONFIRMADO + 15 FROM_VISOR pre-sembrados). De **141** atributos `*_value_id`: **138 cableados** al catálogo (`tyd=TYD_CODE`, `fk_target=reference_value`, `reference_catalog`, `catalog_ref_metadata_only=true`) — reutilizando los existentes y **creando 38 catálogos nuevos** (BACKGROUND_CHECK_*, INTERVIEW_STAGE/SESSION/MODE/RECOMMENDATION, OFFER_STATUS, PIP_*, PERFORMANCE_OBJECTIVE/RATING_SCALE/DIMENSION, BENEFIT_CLAIM/PLAN_TIER, DATA_PROCESSING_LEGAL_BASIS (RGPD art. 6), EMERGENCY_CONTACT_RELATIONSHIP, CANDIDATE_SOURCE/WITHDRAWAL, TIME_OFF/PAYROLL transaction, PROFICIENCY_LEVEL, …). **3 dejados sin cablear a catálogo por ser FK a maestro real**: `preferred_language`→`language`; `competency`/`target_competency`→`competency`. `applicable_jurisdiction_value_id` (×3: benefit_program, time_off_accrual_policy, training_program) **reconvertido a FK a `country`** (`applicable_jurisdiction_country_id`, `TYD_COUNTRY_CODE_ISO`).

**Estado tras M-69:** HR **76 entidades / 1.166 atributos / 100 catálogos**. Verificado: los 104 catálogos referenciados por HR existen; canónico y términos coinciden (138 = 138); **0 FK colgantes**. Repo + visor + Instrucciones escritos.

**Pendientes:** repuntar los ~53 `*_party_id` de FINANCE a `employee`; acelerador **COMMERCIAL** (`customer`) y las 2 FK aún colgantes de HR (`brand`, `sales_commission_plan`); i18n; poblar valores reales de catálogo por cliente. **Registro oficial.**

### METADATO-70 — Repunte de `*_party_id` internos a `employee` y saneo integral de `fk_target` malformados (cierre FINANCE/PROCUREMENT) — DECIDIDO

Aceleradores de negocio (**metamodelo núcleo sin cambio**). Cierra los dos flecos que quedaban de M-66/67/68 tras materializar HR (M-69).

**(A) `*_party_id` internos → maestro `employee`.** Los 110 `*_party_id` de FINANCE/PROCUREMENT/MDM estaban todos con `fk_target=None` ("a la espera de HR"). Clasificados por semántica: **97 actores internos** (aprobadores, preparadores, revisores, responsables, custodios, tesorería, comprador interno, comercial interno, firmante, receptor…) **repunteados a FK `employee`** y **renombrados `*_party_id` → `*_employee_id`** (convención de FK a maestro), con su entrada `keys` FK. Los de mayor volumen: `approved_by` (×14), `prepared_by` (×13), `reviewed_by` (×13), `responsible` (×10). En canónico hay ahora **133 FK a `employee`** (97 nuevos + 36 internos de HR), todas resuelven. **13 contrapartes externas dejadas intactas** (no son empleados; esperan **COMMERCIAL** `customer` / maestros de contraparte): `customer_party_id` (×5), `client`, `lessor`, `beneficiary`, `intermediary`, `disputing`, `disposal_buyer`, `account_holder_secondary`, y `owner_party_id` de `ownership_structure` (owner polimórfico, decisión del founder en M-68).

**(B) Saneo de `fk_target` malformados.** Auditado TODO el modelo: **22 valores / 47 ocurrencias** de `fk_target` que no resolvían a entidad (truncamientos `'al'`/`'cc'`/`'opcional'`, anotaciones `'(D8)'`/`'(polimórfico)'`, y destinos con el nombre del atributo en vez del maestro). Corregido derivando el destino del **nombre del atributo** (no de la cadena rota): **29 apuntados a maestro real existente** — `*_currency_id`→`currency`, `*_country_id`→`country`, `journal_entry_id_linked`→`journal_entry`, `bank_statement_entry_id`→`bank_statement_entry`, `cost_center_id`→`cost_center`, `account_id_linked`→`account`, `responsible_business_unit_id`→`business_unit`, `linked_assumption_id`→`budget_assumption`, `access_grant_ref`→`data_access_request`. **40 pasados a `None`** (bien formado = sin FK único): **22 polimórficas** (`*_object_row_uuid`, cuya dispersión porta su `*_object_type_code` acompañante — verificado) y **18 de maestros aún no modelados** (`location` ×3, `billing_item` ×2, `cash_pooling_arrangement`, `brand`, `sales_commission_plan`, `entity_reference`, `source_reference`).

**Estado tras M-70:** FINANCE/PROCUREMENT **sin FK rotas** (0 `fk_target` malformado en todo el modelo); recuentos de entidades/atributos sin cambio (solo renombrado y repunte de FK). Aplicado a canónico + términos FINANCE + términos PROCUREMENT; escrito a repo + visor + Instrucciones. **FINANCE y PROCUREMENT quedan cerrados.**

**Pendientes:** maestros aún no modelados que dejan FK en `None` (marketing `brand`, `sales_commission_plan`, `location`, `billing_item`, `cash_pooling_arrangement` — se enlazarán cuando lleguen sus aceleradores); acelerador **COMMERCIAL** (`customer`) para las 13 contrapartes externas; owner polimórfico de ownership; i18n. **Registro oficial.**

### METADATO-71 — Acelerador **Comercial (COMMERCIAL_v1)**: maestro `customer`, cierre order-to-cash y pipeline `opportunity` — DECIDIDO

Acelerador de negocio (**metamodelo núcleo sin cambio**). Cierra la contraparte cliente que FINANCE tenía en espera.

**(A) Maestro `customer`** (espejo fiel de `supplier`): golden record + satélites. `PK=[id]=sha2('datum:'||customer_code)`, `UI=[customer_code]`, jerarquía de grupo por `parent_customer_id`. **Satélites**: `customer_contact`, `customer_address` (billing/shipping), `customer_bank_account` (SEPA), `customer_credit_profile` (1:1: límite, rating, riesgo, DSO), `customer_tax_registration` (1:N por país, patrón `legal_entity_tax`).

**(B) Cierre order-to-cash.** Los 8 FK que estaban en `None` esperando cliente → `customer` (renombrados a `customer_id`): `customer_invoice`, `credit_note`, `debit_note`, `customer_payment`, `dunning_case` (`customer_party_id`), `invoice_dispute.disputing_party_id`→`disputing_customer_id`, `project.client_party_id`.

**(C) Pipeline de venta (término COM_SALES).** `opportunity` (deal) + `opportunity_line`. Flujo **lead → opportunity → customer**: la oportunidad referencia `source_lead_id` (→`lead`, MARKETING), `customer_id` (→`customer`), `campaign_id` (atribución); `stage`/`status` (QUALIFICATION…CLOSED_WON/LOST), importe/probabilidad/fechas, `owner_employee_id`.

**Estado tras M-71:** COMMERCIAL **8 entidades / 91 atributos / 7 catálogos** (4 CONFIRMADO + 3 BORRADOR). Nuevos catálogos `CUSTOMER_KIND/SEGMENT/STATUS`, `CREDIT_RATING`, `OPPORTUNITY_STAGE/STATUS/LOSS_REASON`; reutilizados CONTACT/ADDRESS/PAYMENT_METHOD/RISK_LEVEL/TAX_SCHEME. Fichero `datum_terminos_modelo__COMMERCIAL_v1.json` (row_id uuid5). Verificado: 0 FK colgantes, canónico↔términos coherentes. Repo + visor + Instrucciones.

**Fronteras:** `brand`/`product`/`billing_item` NO son de COMMERCIAL (→ MARKETING, M-72). Contrapartes no-cliente (lessor/beneficiary/intermediary/disposal_buyer/account_holder_secondary/owner de ownership) intactas. **Pendientes**: quote/order/contract si se amplía el pipeline; afinar los 3 catálogos BORRADOR. **Registro oficial.**

### METADATO-72 — Acelerador **Marketing (MARKETING v1+v2)**: marca, producto/oferta, precios, campañas, segmentos y demand-gen — DECIDIDO

Acelerador de negocio (**metamodelo núcleo sin cambio**). Absorbe `BRAND_AND_PRODUCT` bajo un único acelerador **MARKETING**; greenfield (ninguna entidad marketing preexistente).

**(v1) Marca + Producto + Precios (18→ ver abajo).** **BRAND**: `brand` (maestro) + `brand_registration` (marca registrada/IP) + `brand_license` (royalties) + `brand_valuation`. **PRODUCT**: `product` (maestro/item vendible) + `product_family` + `product_catalog` + `product_catalog_item` (M:N). **PRICING**: `price_list` + `price`. Cierra los 3 FK colgantes: `position.primary_brand_id`→`brand`; `supplier_invoice_line`/`customer_invoice_line`.`billing_item_id`→`product_id`→`product`.

**(v2) Campañas + Segmentos + Demand-gen** (acelerador → v1.1.0). **CAMPAIGN**: `campaign` + `campaign_channel` + `campaign_metric` + `content_asset`. **MARKET**: `market_segment` + `customer_segment_membership` (M:N cliente↔segmento). **DEMAND**: `lead` (PII) + `campaign_response`. **Handoff MARKETING→COMMERCIAL**: `lead.converted_opportunity_id`→`opportunity` (y `converted_customer_id`→`customer`), cerrando el flujo `lead → opportunity → customer`.

**Catálogos:** importados los **39 reservados** de `BRAND_AND_PRODUCT_v1` al `datum_catalogos.json` bajo `canonical_accelerator=MARKETING` (3 CONFIRMADO con valores del doc —NICE_CLASS/BRAND_KIND/BRAND_STATUS—, resto BORRADOR/PENDIENTE); +14 nuevos v2 (CAMPAIGN_*, MARKETING_CHANNEL, CONTENT_*, SEGMENT_KIND, LEAD_*, OPPORTUNITY_* comparte con COMMERCIAL). Fichero suelto `datum_catalogos__BRAND_AND_PRODUCT_v1.json` **retirado a `_to_delete`** (no doble gestión).

**Estado tras M-72:** MARKETING **18 entidades / 179 atributos / 49 catálogos** (3 CONFIRMADO + 38 BORRADOR + 8 PENDIENTE); acelerador v1.1.0. Fichero `datum_terminos_modelo__MARKETING_v1.json` (row_id uuid5). Verificado: 0 FK colgantes/malformados en todo el modelo. Repo + visor + Instrucciones.

**Pendientes:** afinar los catálogos BORRADOR de marketing; `MARKETING_v3` si se amplía (attribution multi-touch, journeys). **Registro oficial.**

### METADATO-73 — COMMERCIAL_v2: extensión del pipeline (CPQ + order + contrato) y puente order-to-cash a FINANCE — DECIDIDO

Continuación de M-71 (COMMERCIAL; **metamodelo núcleo sin cambio**). Extiende el pipeline de venta más allá de `opportunity`.

**(A) CPQ y pedido (término COM_SALES).** `quote` (maestro, desde `opportunity`: `price_list_id`→lista de precios MARKETING, versión, validez, `status`, totales) + `quote_line` (producto, cantidad, precio, descuento). `sales_order` (desde `quote`: `status`, entrega solicitada, PO del cliente, totales) + `sales_order_line` (producto, cantidad servida).

**(B) Contratos (término COM_CONTRACT).** `customer_contract` (espejo de `procurement_contract`: cliente, tipo, vigencia, auto-renovación, `billing_frequency`, importe comprometido, `owner_employee_id`) + `contract_line` (producto, precio recurrente, frecuencia). Soporta la facturación recurrente.

**(C) Puente order-to-cash a FINANCE.** `customer_invoice` gana FK reales `sales_order_id`→`sales_order` y `customer_contract_id`→`customer_contract` (antes referencias de texto). El `customer_purchase_order_reference` se mantiene como texto (PO externo del cliente). Flujo cerrado: **lead → opportunity → quote → sales_order → customer_invoice → customer_payment**, y en paralelo **customer_contract → customer_invoice** (recurrente).

**Estado tras M-73:** COMMERCIAL **8→14 entidades** (v1.1.0), +6 (`quote`/`quote_line`/`sales_order`/`sales_order_line`/`customer_contract`/`contract_line`); catálogos +5 BORRADOR (`QUOTE_STATUS`, `SALES_ORDER_STATUS`, `CUSTOMER_CONTRACT_KIND`, `CONTRACT_STATUS`, `BILLING_FREQUENCY`). Verificado: 0 FK malformados en todo el modelo, row_id uuid5, canónico↔términos coherentes. Repo + visor + Instrucciones.

**Fuera de alcance (otro acelerador):** entrega/logística (albarán/envíos) → OPS. **Pendientes:** afinar catálogos BORRADOR de COMMERCIAL/MARKETING; i18n. **Registro oficial.**

### METADATO-74 — Saneo de catálogos: reparación de corrupción `_PENDIENTE_`, fusión de duplicado y poblado de universales — DECIDIDO

Higiene transversal de catálogos (sin cambios de entidades del núcleo; toca FINANCE ya registrado solo en catálogos + 2 repuntes de `reference_catalog`).

**(A) Corrupción de carga reparada (2 patrones, 42 catálogos).** En la carga original, el literal `"_PENDIENTE_"` se iteró carácter a carácter y se materializó como valores `{_,P,E,N,D,I,T}`. **28 catálogos** (todos FINANCE FROM_VISOR) tenían ese set como únicos valores → vaciados a **PENDIENTE**. Otros **14** lo tenían **mezclado** con valores reales (`ACCOUNTING_STANDARD`, `TAX_KIND`, `TAX_TREATMENT`, `PRECISION_ROUNDING`, `PRESENTATION_UNIT`, `E_INVOICING_STATUS`, `AGING_BUCKET`, `GRANULARITY`…) → eliminadas las letras, conservando sus valores. Corregido de paso un exceso de la limpieza: restaurados `A`/`B` de `CREDIT_RATING`.

**(B) `PAYMENT_METHOD` poblado.** Estaba corrupto y lo reutilizan supplier/customer: BANK_TRANSFER, DIRECT_DEBIT_SEPA, CARD, CASH, CHECK, WIRE, STANDING_ORDER, OTHER (CONFIRMADO).

**(C) Fusión de duplicado intra-FINANCE.** `APPLIES_TO_ACCOUNTING_STANDARD` (asset_category) y `PRESENTATION_ACCOUNTING_STANDARD` (consolidation_group) eran duplicados vacíos del catálogo rico `ACCOUNTING_STANDARD` (20 valores). Repunteados sus 2 atributos → `ACCOUNTING_STANDARD` (13 refs) y **retirados los 2 catálogos**. Criterio de fusión: **solo dentro del mismo acelerador** (decisión del founder); no se cruzan aceleradores.

**(D) Universales de FINANCE poblados (BORRADOR).** 9 catálogos estándar (métodos de amortización, tipos FX AVERAGE/CLOSING, `REPAYMENT_FREQUENCY`, `ASSET_KIND_DEFAULT`, `DISCLOSURE_PERIOD`, `SUBLEDGER_REFERENCE_KIND`, `SOURCE_DOCUMENT_REFERENCE_KIND`). **16 estructurales** dejados vacíos a propósito (CUSTOM_DIMENSION_1..5, PARENT, NEW/PREVIOUS_STATUS, APPROVER_ROLE, SUBSCRIBER_ROLE, DEFAULT_CURRENCY… → deben ser FK a maestro/otro catálogo, no enum propio; pendientes de doctrina del founder).

**(E) Duplicados no fusionados (por diseño).** Tras el saneo quedan 4 grupos con valores idénticos intra-acelerador que son **coincidencia, no mismo concepto** (`PAYMENT_FREQUENCY`≟`CONSOLIDATION_FREQUENCY`, `DEPRECIATION_FREQUENCY`≟`PERIOD_KIND_DEFAULT`, `ENTRY_SIDE`≟`NORMAL_BALANCE_SIDE`, `ACCRUAL_POLICY_STATUS`≟`BENEFIT_PROGRAM_STATUS`). Se **mantienen separados**: son atributos distintos; fusionarlos acoplaría campos no relacionados y quitaría flexibilidad.

**Estado tras M-74:** catálogos 623→**621** (−2 fusionados); **583 referencias resuelven todas, 0 basura de 1 carácter, 0 FK malformados**. Repo + visor + Instrucciones. **Pendientes:** poblar los 16 estructurales de FINANCE con doctrina del founder; i18n. **Registro oficial.**

### METADATO-75 — Acelerador **Almacén (WAREHOUSE_v1 / WMS)** completo — DECIDIDO

Acelerador de negocio nuevo (**metamodelo núcleo sin cambio**). Gestión de almacenes de punta a punta, greenfield.

**17 entidades en 7 familias.** **WH_STRUCTURE**: `warehouse` (maestro→legal_entity), `warehouse_zone`, `storage_bin` (ubicación). **WH_ITEM**: `warehouse_item` (config producto×almacén: tracking NONE/LOT/SERIAL, min/max/reorder, ABC), `stock_lot` (lote/caducidad), `serial_number`. **WH_STOCK**: `stock_balance` (on_hand/reserved/available por producto×almacén×ubicación×lote), `stock_reservation` (contra `sales_order_line`). **WH_MOVEMENT**: `stock_movement` (ledger de inventario), `stock_adjustment`(+`_line`). **WH_INBOUND**: `putaway_task` (desde `goods_receipt_line`). **WH_OUTBOUND**: `pick_task` (desde `sales_order`), `shipment`(+`_line`) = albarán. **WH_COUNT**: `cycle_count`(+`_line`).

**Enganches (sin duplicar):** entrada→`goods_receipt_line` (PROCUREMENT), salida→`sales_order`/`_line` (COMMERCIAL), artículo→`product` (MARKETING), propietario→`legal_entity`, operarios→`employee`, lotes→`supplier`. **Puente order-to-cash a FINANCE**: `customer_invoice.shipment_id`→`shipment` (antes `delivery_note_reference` de texto). Cadena logística cerrada: recepción→putaway→stock→reserva→picking→shipment→factura.

**Estado tras M-75:** WAREHOUSE **17 entidades / 188 atributos / 19 catálogos** (BORRADOR). Fichero `datum_terminos_modelo__WAREHOUSE_v1.json` (row_id uuid5); reutiliza `UOM`. Verificado: 0 FK malformados, canónico↔términos coherentes. Repo + visor + Instrucciones. **Registro oficial.**

### METADATO-76 — Acelerador **Manufactura (MANUFACTURING_v1)** completo — DECIDIDO

Acelerador de negocio nuevo (**metamodelo núcleo sin cambio**). Fabricación de productos desde materias primas vía fórmula/escandallo; greenfield.

**11 entidades en 4 familias.** **MF_BOM**: `bill_of_materials` (fórmula/escandallo: producto terminado, versión, lote base), `bom_line` (componentes MP/semi + merma), `bom_coproduct` (co-productos/subproductos/mermas). **MF_ROUTING**: `production_line` (recurso), `routing`, `routing_operation` (secuencia, tiempos). **MF_ORDER**: `production_order` (OF), `production_order_component` (planificado vs consumido, con lote), `production_order_output` (terminado+co-productos, lote nuevo, calidad), `production_operation_log`. **MF_COSTING**: `product_standard_cost` (escandallo de coste por componente MATERIAL/LABOR/OVERHEAD — estructura modelada; tasas = doctrina del founder).

**Enganches:** MP entra por `goods_receipt` (PROCUREMENT)→`stock_lot`/`stock_balance` (WAREHOUSE); la OF consume componentes (stock out) según BOM y genera `production_order_output` (stock in, lote nuevo)→disponible para `sales_order`. Producto=`product` (MARKETING), con `PRODUCT_KIND` ampliado a **RAW_MATERIAL/SEMI_FINISHED/FINISHED_GOOD**; `STOCK_MOVEMENT_KIND` +CONSUMPTION/PRODUCTION_RECEIPT; `MOVEMENT_REFERENCE_KIND` +PRODUCTION_ORDER.

**Estado tras M-76:** MANUFACTURING **11 entidades / 121 atributos / 11 catálogos** (BORRADOR). Fichero `datum_terminos_modelo__MANUFACTURING_v1.json` (row_id uuid5). **Flujo end-to-end completo**: compra→almacén→fabricación→almacén→venta→envío→factura. Verificado: 0 FK malformados en todo el modelo. Repo + visor + Instrucciones. **Registro oficial.**

### METADATO-77 — Afinado de catálogos BORRADOR de WAREHOUSE y MANUFACTURING — DECIDIDO

Higiene de catálogos (sin cambios de entidades). Los **30 catálogos** en BORRADOR de los dos aceleradores nuevos → **CONFIRMADO**, con descripción en español por cada valor y enriquecimiento puntual: `STOCK_ADJUSTMENT_REASON` +COUNT_VARIANCE/OBSOLESCENCE, `WAREHOUSE_KIND` +CROSS_DOCK. Verificado: 0 BORRADOR restantes en WAREHOUSE/MANUFACTURING, todas las referencias de catálogo resuelven, JSON íntegro. Repo + visor + Instrucciones. **Registro oficial.**

### METADATO-78 — Cierre del modelo común: 6 aceleradores nuevos (SUPPLY_CHAIN, QUALITY, SERVICE, LEGAL, EAM, PROJECT) — DECIDIDO

Cierre funcional del modelo común de empresa (**metamodelo núcleo sin cambio**). Seis aceleradores de negocio nuevos que completan la cobertura de dominios, construidos en una pasada con el patrón heredado (PK/UI, `system`, row_id uuid5, catálogos metadata-first). **36 entidades / 53 catálogos.**

**SUPPLY_CHAIN (8)** — cadena de suministro: `carrier`, `transport_route`, `freight_order`(+`_stop`, enlaza `shipment`), `transfer_order`(+`_line`) entre almacenes, `demand_forecast`, `replenishment_proposal` (MRP: BUY/MAKE/TRANSFER).

**QUALITY (5)** — QMS: `quality_specification`, `quality_inspection`(+`_line`; entrada←`goods_receipt`, proceso←`production_order`), `non_conformance`, `corrective_action` (CAPA).

**SERVICE (6)** — postventa: `service_case`(+`_activity`), `return_order`(+`_line`, RMA con disposición), `warranty`, `warranty_claim`.

**LEGAL (7)** — llena el slot antes vacío (entity_count 0→7): `contract` (repositorio unificado) + `contract_clause`/`contract_obligation`, `legal_case`(+`_event`), `permit_license`(→`regulator`), `compliance_obligation` (GDPR/ISO/SOX…).

**EAM (5)** — mantenimiento: `equipment`(→`fixed_asset`/`production_line`), `maintenance_plan`, `maintenance_work_order`(+`_task`), `spare_part_usage` (consume stock).

**PROJECT/PSA (5)** — extiende el `project` existente: `project_phase`, `project_task`, `project_milestone`, `timesheet_entry`(→`employee`), `project_resource_assignment`.

**Estado tras M-78:** canónico 576→**612 entidades**; **15 aceleradores** (13 de negocio, todos con contenido). Catálogos 651→**703** (+53 BORRADOR). Ficheros `datum_terminos_modelo__{SUPPLY_CHAIN,QUALITY,SERVICE,LEGAL,EAM,PROJECT}_v1.json` (row_id uuid5). **Modelo común completo end-to-end**: planificar→aprovisionar→recepcionar/inspeccionar→almacenar→fabricar→recontar→vender→reservar→picking→enviar(transporte)→facturar→cobrar→postventa/RMA/garantía; con RRHH, Finanzas, Marketing, Legal, Mantenimiento y Proyectos como transversales. Verificado: **0 FK malformados en todo el modelo**, todos los catálogos referenciados existen, row_ids únicos. Repo + visor + Instrucciones.

**Pendientes:** afinar los 53 catálogos BORRADOR de los 6 aceleradores; poblar los 16 estructurales de FINANCE; i18n. **Registro oficial.**

### METADATO-79 — Saneo y cierre de catálogos FINANCE (estructurales + universales) — DECIDIDO

Higiene final de los catálogos de FINANCE que quedaban sin poblar tras M-74. Tratados según su naturaleza real, no poblados a ciegas.

**(A) Estructurales (16).** **4 enum genuinos poblados**: APPROVER_ROLE, CALCULATION_METHOD_USED, SCENARIO_HORIZON_KIND, EFFECTIVE_TAX_RATE_METHODOLOGY (Pilar 2/GloBE). **5 `CUSTOM_DIMENSION_1..5` → catálogo ABIERTO** (dimensiones analíticas definidas por el cliente; valores por instalación). **5 atributos reconducidos a FK real** (no eran catálogos): `analytical_dimension_value.parent_value_id`→FK `analytical_dimension_value`; `account.default_currency_value_id`→`default_currency_id` FK `currency`; `accounting_period_state_history.new_status`/`previous_status`→catálogo `PERIOD_STATUS`; `dunning_communication.dunning_level_at_communication`→`CURRENT_DUNNING_LEVEL`. **2 sin uso eliminados** (SUBSCRIBER_ROLE, BREACHED_THRESHOLD_KIND). Catálogos retirados: PARENT, DEFAULT_CURRENCY, NEW_STATUS, PREVIOUS_STATUS, DUNNING_LEVEL_AT_COMMUNICATION, SUBSCRIBER_ROLE, BREACHED_THRESHOLD_KIND (7).

**(B) Universales (9).** **5 eran duplicados**: DEFAULT/NEW_DEPRECIATION_METHOD → catálogo existente `DEPRECIATION_METHOD` (3 attrs repunteados); ASSET_KIND_DEFAULT → `ASSET_KIND`; AVERAGE/CLOSING_FX_RATE_KIND (idénticos) unificados en nuevo `FX_RATE_KIND` (2 attrs). Los 5 duplicados eliminados. **7 finalizados a CONFIRMADO** con descripción ES: DEPRECIATION_METHOD, ASSET_KIND, FX_RATE_KIND, REPAYMENT_FREQUENCY, DISCLOSURE_PERIOD, SUBLEDGER_REFERENCE_KIND, SOURCE_DOCUMENT_REFERENCE_KIND.

**Estado tras M-79:** catálogos 703→**692** (−11 retirados: 7 estructurales + 5 duplicados − 1 FX_RATE_KIND nuevo). **0 catálogos BORRADOR en todo el modelo**; **0 FK malformados, 0 refs rotas.** Repo + visor + Instrucciones. Registro oficial.

### METADATO-80 — i18n SHORT (es/en/fr/pt) del modelo de negocio — DECIDIDO

Generación de traducciones **nivel SHORT (rótulo UI)** en 4 idiomas (es/en/fr/pt) para todo el modelo de negocio (13 aceleradores). Fichero `datum_i18n_negocio.json`.

**Cobertura: 9.845 objetos** — 335 entidades canónicas + 5.404 atributos + 4.106 valores de catálogo. Anclaje por `row_id` (uuid5) de la entidad/atributo en los ficheros `terminos`; para valores de catálogo `row_id = uuid5('REFERENCE_VALUE:'+catálogo+':'+code)`.

**Generación por tokens** (es/fr/pt derivados de un diccionario de tokens con reversión romance sustantivo→«de»→modificador y fusión sustantivo+adjetivo pospuesto; en fiel al code). Solo SHORT; SUMMARY y FUNCTIONAL quedan pendientes.

**Revisión a mano de los 335 rótulos de entidad** (es/en/fr/pt): 0 tokens EN sin traducir, 0 «de»+adjetivo, gramática romance corregida; idiomatismos por override (escandallo, plan de cuentas, recibo de nómina, Pilar 2/GloBE, CbC, DAC, dependencia jerárquica…). Atributos y valores de catálogo quedan como generación por tokens (revisar es/fr/pt).

**Alcance:** los 13 aceleradores de negocio. El core (METADATA/OBSERVABILITY) usa otro esquema de `row_id` (fuente markdown) y no está incluido — pendiente.

**Entrega:** repo + visor (`public/datum_i18n_negocio.json`) + Instrucciones. Registro oficial.

### METADATO-81 — i18n del CORE y unificación de todo el modelo en el formato del visor — DECIDIDO

**Hallazgo previo.** El visor (`canonico/page.tsx`) une i18n por `sha256('datum:CANONICAL_ENTITY:'+name)[:16]` y **solo lee `datum_i18n_d2.json`**. El `datum_i18n_negocio.json` de M-80 estaba en claves `uuid5` (otro esquema, sin prefijo `datum:`) y **no lo renderizaba nada** — no había script de conversión. Con M-80 el negocio no se veía en el visor.

**(A) i18n del CORE.** Generado nivel SHORT (es/en/fr/pt) para las **279 entidades del core** (METADATA/OBSERVABILITY, D0–D4) + 2.436 atributos + 529 valores de catálogo, en el formato del visor (`sha256-16`, prefijo `datum:`), fusionado en `datum_i18n_d2.json`. El D2 previo (40 entidades con SHORT/SUMMARY/FUNCTIONAL a mano) queda **intacto**. Rótulos de entidad **revisados a mano** (0 tokens EN sin traducir, 0 desacuerdos de género/número). Lexicón ampliado: Unity Catalog (`information_schema`, `compute`, `lakeflow`…), GDPR (interesado, tratamiento, finalidad, consentimiento), metamodelo (golden record→registro maestro, survivorship, cotejo…).

**(B) Unificación del negocio.** Los 335 rótulos de negocio ya revisados a mano se **re-clavaron** de `uuid5` a `sha256-16` y se fusionaron en `datum_i18n_d2.json` (335 entidades + 5.404 atributos + 3.577 valores; 529 colisiones de catálogos compartidos omitidas). +37 atributos residuales de canónico cubiertos. `datum_i18n_negocio.json` queda **obsoleto**.

**Resultado.** `datum_i18n_d2.json` = **modelo completo**: **612/612 entidades** con i18n resoluble por el visor, 0 atributos sin i18n, claves 100% `sha256-16`. Totales: 628 entidades (612 modelo + legacy D2), 8.046 atributos, 4.109 valores → **12.820 objetos**. Visor (`public/`) + repo (`DATUM_i18n_D2.json`). Registro oficial.

### METADATO-82 — i18n niveles SUMMARY y FUNCTIONAL para todo el modelo — DECIDIDO

Completados los tres niveles de texto (SHORT + **SUMMARY** + **FUNCTIONAL**) en es/en/fr/pt para los **12.820 objetos** de `datum_i18n_d2.json` (628 entidades, 8.046 atributos, 4.109 valores).

**Fuente y método (sin invención).**
- **es** — SUMMARY = el campo `desc` real de disco (entidad/atributo/valor); FUNCTIONAL = `desc` + estructura tomada del propio modelo (nº de atributos, clave natural, FK a entidades, catálogos referenciados; en atributos: tyd, obligatoriedad, FK/catálogo).
- **en/fr/pt** — SUMMARY/FUNCTIONAL por **plantilla estructural** en cada idioma, con los nombres ya traducidos (SHORT) y los hechos del modelo. El `desc` libre (solo español en disco) **no se traduce a máquina**: en no-es el texto es estructural, no prosa inventada.

**Preservado.** Las 40 entidades D2 con SUMMARY/FUNCTIONAL redactados a mano (y todo objeto que ya tenía ambos niveles) quedan **intactos**. 56 objetos de negocio no presentes en canónico (`data_product`, `data_product_subscription`, `party`) reciben nivel mínimo derivado del SHORT.

**Estado.** Cobertura 12.820/12.820 con los 3 niveles en 4 idiomas; SHORT intacto. Marcado GENERADO_MAQUINA (revisar es/fr/pt; en fiel). Tamaño del fichero ≈ 10,3 MB — el visor lo descarga completo; si el peso molesta, se puede separar SHORT (visor) de SUMMARY/FUNCTIONAL (Control Plane) en un segundo fichero. Visor (`public/`) + repo (`DATUM_i18n_D2.json`). Registro oficial.

### METADATO-83 — FUNCTIONAL de entidades con prosa traducida real (en/fr/pt) — DECIDIDO

Mejora del nivel FUNCTIONAL (y SUMMARY) de las **entidades** en inglés, francés y portugués: se sustituye la plantilla estructural por **traducción real de la prosa** del `desc`.

**Alcance.** 515 entidades con `desc` en disco (las 40 ya redactadas a mano quedan intactas; las 85 sin `desc` conservan su FUNCTIONAL estructural). Traducción es→en/fr/pt del `desc` con terminología profesional de gobierno del dato, preservando identificadores técnicos (snake_case, `TYD_*`, catálogos en MAYÚSCULAS, siglas, códigos `M-nn`/`DATUM-nn`, flechas →). SUMMARY.{en,fr,pt} = `desc` traducido; FUNCTIONAL.{en,fr,pt} = `desc` traducido + estructura (atributos/PK/FK/catálogos) del modelo. **es** sin cambios.

**Verificación.** 515/515 traducidas, 0 idiomas vacíos, identificadores técnicos conservados (revisión de posibles pérdidas: solo valores de ejemplo localizados, no identificadores reales). SHORT intacto; 40 entidades ricas sin alterar; 12.820/12.820 objetos con los 3 niveles en 4 idiomas.

**Pendiente (no bloqueante).** El desc libre de **atributos y valores** en en/fr/pt sigue como plantilla estructural (no prosa traducida). Fichero ≈ 10,5 MB. Visor (`public/`) + repo (`DATUM_i18n_D2.json`). Registro oficial.

### METADATO-84 — FUNCTIONAL/SUMMARY de atributos y valores con prosa traducida real (en/fr/pt) — DECIDIDO

Cierre de la internacionalización: se sustituye la plantilla estructural por **traducción real de la prosa** del `desc` también en **atributos** (5.225 con `desc`) y **valores de catálogo** (1.461 con `desc`).

**Método (dedup + traducción profesional).** Los 6.686 objetos con `desc` se deduplicaron a **4.777 textos únicos** (muchos `desc` se repiten: campos de auditoría, claves, etc.), traducidos es→en/fr/pt con terminología de gobierno del dato/contabilidad/GDPR y preservando identificadores técnicos (snake_case, `TYD_*`, catálogos en MAYÚSCULAS, siglas, códigos `M-nn`, valores de enum, fórmulas). Reconstrucción: SUMMARY.{en,fr,pt} = `desc` traducido; FUNCTIONAL.{en,fr,pt} = `desc` traducido + estructura (atributos: tyd/obligatoriedad/FK/catálogo; valores: «code» del catálogo). **es** sin cambios.

**Verificación.** 4.777/4.777 textos traducidos, 0 idiomas vacíos, identificadores preservados. 249 objetos redactados a mano en el D2 original intactos; SHORT intacto; 12.820/12.820 objetos con los 3 niveles en 4 idiomas.

**Estado final i18n.** Modelo COMPLETO trilingüe+es: **SHORT + SUMMARY + FUNCTIONAL** en es/en/fr/pt para los 12.820 objetos, con prosa traducida de verdad en todo lo que tiene `desc` en disco (entidades, atributos y valores). Fichero ≈ 11 MB. Visor (`public/`) + repo (`DATUM_i18n_D2.json`). Registro oficial.

### METADATO-85 — Partición del i18n del visor por nivel (rendimiento) — DECIDIDO

Optimización de carga del visor separando el i18n **por nivel**, no por acelerador. Motivo (patrón real de consumo del visor `canonico/page.tsx`): el **SHORT es transversal** (árbol de todos los aceleradores + buscador global), mientras que **SUMMARY/FUNCTIONAL solo se muestran en la ficha** del objeto seleccionado, de uno en uno.

**Datos.** Fichero completo 11 MB (gzip 1,34). SHORT = 3,0 MB; detalle (SUMMARY+FUNCTIONAL) = 7,0 MB. El coste real es el **parseo** del JSON al cargar, no la transferencia.

**Solución.** Dos ficheros en el visor (`dataplane/public`): `datum_i18n_d2.json` = **solo SHORT** (carga al entrar; árbol y buscador funcionan en todo el modelo); `datum_i18n_detail.json` = **SUMMARY+FUNCTIONAL** (carga **diferida** en segundo plano y fusión en el mismo mapa `i18n` por clave `sha256`; la resolución de etiquetas no cambia). Parseo inicial 11 MB → 3,7 MB.

**Cambio de código.** `src/app/dashboard/canonico/page.tsx` y `src/app/page.tsx`: el `fetch` de `datum_i18n_d2.json` encadena un `fetch` diferido de `datum_i18n_detail.json` que hace merge de `texts` por clave. Descartada la partición **por acelerador** como eje único: el SHORT es global (buscador/árbol), partir por acelerador obligaría a cargar los 15 ficheros o degradaría el buscador.

**Fuente de verdad.** El repo `DATUM_i18n_D2.json` conserva el fichero **completo** (bootstrap del Control Plane); los dos ficheros partidos son artefactos derivados del visor. Registro oficial.

### METADATO-86 — Detalle i18n troceado por acelerador con carga bajo demanda — DECIDIDO

Fase 2 de la partición (sobre M-85): el detalle (SUMMARY+FUNCTIONAL) se **trocea por acelerador** y se carga solo el del acelerador cuya ficha se abre.

**Ficheros.** SHORT (`datum_i18n_d2.json`, 3,9 MB) ahora incluye el campo **`acc`** en cada objeto. Detalle repartido en **18 ficheros** `datum_i18n_detail_<ACC>.json` (15 aceleradores + `MISC` para objetos sin acelerador + `GLOBAL`/`_GLOBAL_` para catálogos transversales). Tamaños: FINANCE 3,1 MB (el mayor), METADATA 1,2 / OBSERVABILITY 1,1 / HR 1,0, el resto ≤ 0,3 MB. El antiguo `datum_i18n_detail.json` queda como stub obsoleto.

**Visor.** `canonico/page.tsx` y `page.tsx`: se revierte el fetch único de detalle; se añade `loadDetail(acc)` (guardado por un `Set` de aceleradores ya cargados, merge por clave `sha256`) disparado al seleccionar objeto — `useEffect` sobre `sel` (lee `acc` del objeto en `i18n`) y sobre `selCat` (lee `canonical_accelerator` del catálogo). Al abrir un acelerador se descarga solo su detalle (≤ 3,1 MB) en vez de los 7,9 MB completos.

**Consistencia verificada.** 12.820 objetos de detalle = SHORT; 0 claves ausentes, 0 desajustes de `acc`, 0 objetos SHORT sin detalle. El mapeo entidad→acelerador usa el mismo seed que el visor (`canonical_entity.business_term_code`→`business_term.canonical_accelerator_code`); valores por `canonical_accelerator` del catálogo. Repo `DATUM_i18n_D2.json` sigue **completo** (fuente de verdad). Registro oficial.

### METADATO-87 — Estándares sectoriales: andamiaje en el metamodelo + acelerador HEALTHCARE + piloto FHIR — DECIDIDO

Mecanismo para **sectorizar** aplicando estándares específicos (FHIR salud, BIAN banca, ACORD seguros). Principio: el modelo canónico sigue siendo la **verdad semántica única**; un estándar es una **capa de correspondencia (crosswalk) + perfil** encima del canónico, no un modelo paralelo. Generaliza el patrón que FINANCE ya usa para normas contables (`accounting_standard` + `account_statement_mapping` + `is_required_by_standard`).

**(A) Andamiaje (core, METADATA · subdominio SECTOR_STANDARDS).** 3 entidades nuevas: `sector_standard` (registro: autoridad, versión, sector, URI, estado), `canonical_standard_entity_map` (crosswalk entidad canónica ↔ recurso del estándar), `canonical_standard_attribute_map` (crosswalk atributo ↔ elemento, con transformación, unidad y enlace a value set/terminología). Catálogos nuevos `MAP_DIRECTION`, `STANDARD_STATUS`; y 6 autoridades añadidas a `STANDARD_AUTHORITY` (HL7, BIAN, ACORD, SNOMED, LOINC, ISO 20022). Reutiliza `SECTORAL_TEMPLATE` (ya tenía FHIR/BIAN/ACORD), `MAPPING_RELATION`, `PRIMARY_INDUSTRY_SECTOR` y `reference_catalog.external_authority_code/external_standard_ref`.

**(B) Acelerador HEALTHCARE (6 entidades, alineadas a FHIR).** `patient`, `practitioner`, `care_organization`, `encounter`, `observation`, `condition`. 10 catálogos: value sets FHIR (ADMINISTRATIVE_GENDER, ENCOUNTER_CLASS/STATUS, OBSERVATION_STATUS, CONDITION_CLINICAL/VERIFICATION_STATUS, ORGANIZATION_TYPE) y abiertos enlazados a terminología externa (OBSERVATION_CODE→LOINC, CONDITION_CODE/PRACTITIONER_SPECIALTY→SNOMED CT). Terminos `HEALTHCARE_v1` (2 términos). Acelerador 16.º; PII/sensibilidad marcadas en `patient`/`observation`/`condition`.

**(C) Piloto FHIR (bidireccional).** `sector_standard` FHIR (HL7, R4) + **7 crosswalks de entidad** (patient→Patient, practitioner→Practitioner, care_organization→Organization, encounter→Encounter, observation→Observation, condition→Condition, y `legal_entity`→Organization reutilizando el canónico) + **31 crosswalks de atributo** (p. ej. `patient.family_name`→`Patient.name.family`, `condition.condition_snomed_code`→`Condition.code` [SNOMED], `observation.observation_loinc_code`→`Observation.code` [LOINC]) con `standard_value_set_uri` y `bound_reference_catalog_code`. Sembrados en `carga_inicial`.

**Conformidad = DQ derivada** (no modelada): sale de `is_required_by_standard` + `cardinality_min/max` + value sets enlazados.

**Sectorización de la empresa:** el tenant selecciona estándar(es) por configuración de instalación (D00: no hay tabla `client`); las partes del modelo (`legal_entity`…) se clasifican con `CLASSIFICATION_SCHEME`/`PRIMARY_INDUSTRY_SECTOR`.

**Estado tras M-87:** entidades **612→621** (+3 andamiaje METADATA, +6 HEALTHCARE); METADATA 163→166; aceleradores 15→16. i18n es/en/fr/pt de todo lo nuevo (117 entidad/atributo + 54 valores), prosa traducida; HEALTHCARE ya es fichero de detalle propio del visor (carga bajo demanda). **0 referencias rotas.** Repo + visor. Registro oficial.

### METADATO-88 — Estándar sectorial BIAN (banca): acelerador BANKING + crosswalks — DECIDIDO

Segundo estándar sectorial sobre el andamiaje de M-87, siguiendo `PLANTILLA_estandar_sectorial.md` (los 10 pasos). La banca retail no está en el canónico → **acelerador de extensión BANKING** + estándar **BIAN** como capa de correspondencia+perfil.

**(A) Acelerador BANKING (6 entidades, alineadas a BIAN).** `banking_product` (Product Directory), `account_arrangement` (Current Account / Arrangement), `banking_transaction` (Account Position Transaction), `card` (Bank Card), `payment_order` (Payment Order / ISO 20022 pain.001), `loan_arrangement` (Consumer Loan). 10 catálogos: BANKING_PRODUCT_KIND, ACCOUNT_TYPE_BANKING, ARRANGEMENT_STATUS, BANKING_TRANSACTION_TYPE/STATUS, PAYMENT_METHOD_BANKING, PAYMENT_ORDER_STATUS, CARD_TYPE/STATUS, LOAN_STATUS — enlazados a BIAN / ISO 20022. Terminos `BANKING_v1` (4 términos: BK_PRODUCT/BK_ACCOUNT/BK_PAYMENT/BK_LENDING); `is_regulatory`=PSD2/SEPA; PII/sensibilidad en cuenta/tarjeta/pago/préstamo. Reutiliza `customer`, `legal_entity`, `currency`.

**(B) Estándar BIAN (bidireccional).** `sector_standard` BIAN (autoridad BIAN, v12.0, sector FINANCIAL_SERVICES) + **8 crosswalks de entidad** (los 6 nuevos + `customer`→Customer y `legal_entity`→Legal Entity por solape) + **27 crosswalks de atributo** con rutas BIAN (p. ej. `account_arrangement.iban`→`CurrentAccount.IBAN`, `payment_order.amount`→`PaymentOrder.PaymentAmount`, `banking_transaction.transaction_type_value_id`→`AccountPositionTransaction.TransactionType` [ISO 20022], `loan_arrangement.outstanding_balance`→`ConsumerLoan.OutstandingBalance`). Sembrados en `carga_inicial`.

**Conformidad = DQ derivada** (is_required_by_standard + cardinalidades + value sets).

**Estado tras M-88:** entidades **621→627** (+6 BANKING); aceleradores 16→17; **2 estándares sectoriales** conviviendo sobre el mismo canónico (FHIR salud M-87, BIAN banca). i18n es/en/fr/pt de todo lo nuevo (83 entidad/atributo + 54 valores), prosa traducida; BANKING ya es fichero de detalle propio del visor (carga bajo demanda). **0 referencias rotas.** Repo + visor. Registro oficial.

### METADATO-89 — Estándar sectorial ACORD (seguros): acelerador INSURANCE + crosswalks — DECIDIDO

Tercer estándar sectorial sobre el andamiaje de M-87, siguiendo `PLANTILLA_estandar_sectorial.md`. Los seguros no están en el canónico → **acelerador de extensión INSURANCE** + estándar **ACORD** como capa de correspondencia+perfil. Completa el trío FHIR (salud) / BIAN (banca) / ACORD (seguros) sobre un canónico único.

**(A) Acelerador INSURANCE (7 entidades, alineadas a ACORD).** `insurance_product`, `insurance_policy` (Policy), `coverage` (Coverage), `insured_risk` (InsuredObject), `premium` (Premium), `claim` (Claim), `claim_payment` (ClaimPayment). 9 catálogos: LINE_OF_BUSINESS, POLICY_STATUS, COVERAGE_TYPE/STATUS, RISK_TYPE, PREMIUM_FREQUENCY, CLAIM_TYPE/STATUS, CLAIM_PAYMENT_STATUS — enlazados a ACORD. Terminos `INSURANCE_v1` (3 términos: INS_PRODUCT/INS_POLICY/INS_CLAIM); `is_regulatory`=Solvencia II/IDD; PII/sensibilidad en póliza/siniestro/prima/pago. Reutiliza `customer`, `legal_entity`, `currency`, `country`.

**(B) Estándar ACORD (bidireccional).** `sector_standard` ACORD (autoridad ACORD, v2023, sector FINANCIAL_SERVICES) + **9 crosswalks de entidad** (los 7 nuevos + `customer`→Party y `legal_entity`→Party por solape) + **26 crosswalks de atributo** con rutas ACORD (p. ej. `insurance_policy.policy_number`→`Policy.PolicyNumber`, `coverage.coverage_type_value_id`→`Coverage.CoverageCd`, `claim.claim_status_value_id`→`Claim.ClaimStatusCd`, `claim_payment.payment_amount`→`ClaimPayment.PaymentAmt`). Sembrados en `carga_inicial`.

**Conformidad = DQ derivada** (is_required_by_standard + cardinalidades + value sets).

**Estado tras M-89:** entidades **627→634** (+7 INSURANCE); aceleradores 17→18; **3 estándares sectoriales** sobre un canónico único (FHIR M-87, BIAN M-88, ACORD M-89). i18n es/en/fr/pt de todo lo nuevo (85 entidad/atributo + 63 valores), prosa traducida; INSURANCE ya es fichero de detalle propio del visor (carga bajo demanda). **0 referencias rotas.** Repo + visor. Registro oficial.

### METADATO-90 — HEALTHCARE a operativa exhaustiva (FHIR) — DECIDIDO

Ampliación del acelerador HEALTHCARE de las 6 entidades piloto (M-87) a **28 entidades**, cubriendo la operativa clínica y administrativa alineada con recursos FHIR. Las 6 previas (patient, practitioner, care_organization, encounter, observation, condition) quedan intactas.

**+22 entidades** en 5 términos nuevos:
- **HC_ADMIN:** location, device, practitioner_role, related_person, episode_of_care, healthcare_service.
- **HC_SCHEDULING:** schedule, slot, appointment.
- **HC_CLINICAL (amplía):** procedure, allergy_intolerance, immunization, care_plan, diagnostic_report, service_request, specimen.
- **HC_MEDICATION:** medication, medication_request, medication_administration.
- **HC_FINANCIAL:** patient_coverage (FHIR Coverage), patient_invoice.
- **HC_DOCUMENT:** document_reference.

**36 catálogos** nuevos (value sets FHIR: appointment-status, medicationrequest-status, specimen-status, allergyintolerance-clinical…; abiertos a ATC/SNOMED/CVX). **+22 crosswalks de entidad** y **+47 de atributo** extendiendo el estándar FHIR (M-87), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (234 entidad/atributo + 157 valores), prosa traducida.

**Estado tras M-90:** entidades **634→656** (+22 HEALTHCARE, total acelerador 28); i18n del visor por acelerador (HEALTHCARE 0,26 MB, carga bajo demanda); consistencia SHORT↔detalle verificada. **0 referencias rotas.** Repo + visor. Registro oficial.

### METADATO-91 — BANKING a operativa exhaustiva (BIAN) — DECIDIDO

Ampliación del acelerador BANKING de las 6 entidades piloto (M-88) a **28 entidades**, cubriendo la operativa de banca retail alineada con BIAN. Las 6 previas (banking_product, account_arrangement, banking_transaction, card, payment_order, loan_arrangement) quedan intactas.

**+22 entidades** en 5 términos nuevos:
- **BK_PARTY:** beneficiary, counterparty, party_bank_relationship.
- **BK_ACCOUNT (amplía):** account_balance_snapshot, account_statement, direct_debit_mandate, standing_order, account_signatory.
- **BK_CARD:** card_authorization, card_transaction, card_dispute.
- **BK_PAYMENT (amplía):** payment_execution, sepa_direct_debit.
- **BK_LENDING (amplía):** loan_repayment_schedule, loan_repayment, collateral, guarantee.
- **BK_RISK:** credit_limit, credit_score.
- **BK_COMPLIANCE:** kyc_case, aml_alert.
- **BK_TREASURY:** fx_deal.

**25 catálogos** nuevos (estados de mandato/tarjeta/disputa/ejecución de pago [ISO 20022 pain.002/008], KYC/AML, FX, garantías…). **+22 crosswalks de entidad** y **+45 de atributo** extendiendo el estándar BIAN (M-88), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (216 entidad/atributo + 104 valores), prosa traducida. `is_regulatory`=PSD2/AML5/Basel.

**Estado tras M-91:** entidades **656→677** (+22 BANKING, total acelerador 28); i18n del visor por acelerador (BANKING 0,24 MB, carga bajo demanda); consistencia SHORT↔detalle verificada. **0 referencias rotas.** Repo + visor. Registro oficial.

### METADATO-92 — INSURANCE a operativa exhaustiva (ACORD) — DECIDIDO

Ampliación del acelerador INSURANCE de las 7 entidades piloto (M-89) a **28 entidades**, cubriendo el ciclo de vida asegurador alineado con ACORD. Las 7 previas (insurance_product, insurance_policy, coverage, insured_risk, premium, claim, claim_payment) quedan intactas.

**+21 entidades** en 5 términos nuevos:
- **INS_COMMERCIAL:** insurance_quote, insurance_application, policy_endorsement, policy_renewal, policy_cancellation.
- **INS_DISTRIBUTION:** producer, commission, policy_party, beneficiary_designation.
- **INS_CLAIM (amplía):** claim_activity, claim_reserve, claim_adjuster_assignment, subrogation, loss_event.
- **INS_UNDERWRITING:** underwriting_case, risk_assessment, rating_factor.
- **INS_REINSURANCE:** reinsurance_treaty, reinsurance_cession.
- **INS_BILLING:** billing_account, premium_installment.

**23 catálogos** nuevos (estados de cotización/solicitud/suplemento/siniestro/reaseguro/facturación, decisión de suscripción, motivos, tipos de mediador/reaseguro…). **+21 crosswalks de entidad** y **+39 de atributo** extendiendo ACORD (M-89), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (189 entidad/atributo + 104 valores). `is_regulatory`=Solvencia II/IDD.

**Estado tras M-92:** entidades **677→698** (+21 INSURANCE, total acelerador 28). **Los tres estándares (FHIR/BIAN/ACORD) con acelerador de extensión a 28 entidades.** 0 referencias rotas. Repo + visor. Registro oficial.

> Nota de alcance: "28 entidades" es el **núcleo operativo** de cada dominio, no el modelo completo del estándar (BIAN/ACORD/FHIR son mucho más amplios). Ampliaciones futuras por áreas de negocio priorizadas.

### METADATO-93 — BANKING · Área A «Retail a fondo» (BIAN) — DECIDIDO

Primera ampliación por áreas priorizadas del acelerador BANKING sobre su núcleo operativo de 28 entidades (M-91). El área **A (Retail a fondo)** profundiza depósitos, pagos, tarjetas y préstamos retail alineados con los Service Domains BIAN correspondientes. Las 28 previas quedan intactas.

**+20 entidades** (BANKING **28→48**):
- **BK_DEPOSIT (nuevo):** term_deposit, interest_accrual, account_fee, statement_line.
- **BK_PAYMENT (amplía):** payment_initiation, clearing_settlement, correspondent_bank, payment_batch, swift_message.
- **BK_CARD (amplía):** card_issuance, card_installment_plan, loyalty_program, merchant, acquiring_transaction.
- **BK_LENDING (amplía):** mortgage, loan_drawdown, arrears_case, collection_action, loan_restructuring, loan_provision.

**18 catálogos** nuevos (tipos/estados de depósito a plazo, devengo de intereses, comisiones, compensación/liquidación [ISO 20022], mensajería SWIFT MT, emisión de tarjeta, planes de aplazamiento, fidelización, adquirencia, hipoteca/disposición, impago/mora, acciones de cobro, reestructuración, provisiones IFRS 9…). **+20 crosswalks de entidad** y **+45 de atributo** extendiendo el estándar BIAN (M-88/M-91), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (196 entidad/atributo + 80 valores). `is_regulatory`=PSD2/SEPA/IFRS 9/Basel.

**Estado tras M-93:** entidades **698→718** (+20 BANKING, total acelerador **48**); i18n del visor por acelerador (carga bajo demanda); consistencia SHORT↔detalle verificada. **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: el área A es la primera de una ampliación por áreas de BANKING. Quedan pendientes B (canales y servicing), C (banca corporativa / trade finance) y D (mercados / securities).

### METADATO-94 — BANKING · Área B «Canales y servicing» (BIAN) — DECIDIDO

Segunda ampliación por áreas priorizadas del acelerador BANKING sobre el área A (M-93). El área **B (Canales y servicing)** cubre la atención al cliente, la gestión de casos y reclamaciones, los canales (físicos y digitales) y la venta/relación, alineada con el área de negocio BIAN *Sales & Service*. Las 48 entidades previas quedan intactas.

**+20 entidades** (BANKING **48→68**) en 3 términos nuevos:
- **BK_SERVICING (nuevo):** servicing_case, servicing_order, complaint, complaint_resolution, customer_interaction, interaction_note, customer_communication.
- **BK_CHANNEL (nuevo):** channel, servicing_session, branch, atm, atm_operation, online_banking_enrollment, device_registration, channel_activity.
- **BK_SALES (nuevo):** sales_lead, sales_opportunity, product_application, customer_relationship, customer_appointment.

**35 catálogos** nuevos (tipos/estados de expediente y orden de servicing, categoría/canal/estado de reclamación y resolución, tipo/sentido de interacción y comunicación, tipo/estado de canal, método de autenticación, estado de sesión, tipo/estado de oficina y cajero, operación de cajero, alta digital, dispositivo y confianza, actividad de canal, origen/estado de lead, etapa de oportunidad, estado de solicitud, segmento/estado de relación, tipo/estado de cita). **+20 crosswalks de entidad** y **+37 de atributo** extendiendo el estándar BIAN (M-88), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (193 entidad/atributo + 173 valores). `is_regulatory`=FCA DISP/MiFID II/IDD (reclamaciones y venta asesorada).

Dos IDs colisionaban con otros aceleradores (`lead`→MARKETING, `appointment`→HEALTHCARE); renombrados a **sales_lead** y **customer_appointment** para no sobrescribir.

**Estado tras M-94:** entidades **718→738** (+20 BANKING, total acelerador **68**); i18n del visor por acelerador (carga bajo demanda); consistencia SHORT↔detalle verificada (14.898 objetos, 0 ausentes). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: área B de la ampliación por áreas de BANKING. Quedan pendientes C (banca corporativa / trade finance) y D (mercados / securities).

### METADATO-95 — BANKING · Área C «Banca corporativa / trade finance» (BIAN) — DECIDIDO

Tercera ampliación por áreas priorizadas del acelerador BANKING. El área **C (Banca corporativa / trade finance)** cubre la financiación corporativa, el comercio exterior, la gestión de tesorería corporativa y los mercados de tesorería, alineada con las áreas de negocio BIAN correspondientes. Las 68 entidades previas quedan intactas.

**+20 entidades** (BANKING **68→88**) en 4 términos nuevos:
- **BK_CORPORATE_LENDING:** credit_facility, syndicated_loan, loan_syndication_share, loan_covenant, credit_agreement, facility_utilization.
- **BK_TRADE_FINANCE:** letter_of_credit, documentary_collection, bank_guarantee, trade_finance_document, bill_of_exchange, factoring_agreement, factored_invoice, supply_chain_finance_program.
- **BK_CASH_MANAGEMENT:** cash_pool, pool_participant_account, sweep_instruction, liquidity_position.
- **BK_CORPORATE_TREASURY:** fx_forward_contract, money_market_deal.

**26 catálogos** nuevos (tipos/estados de línea, rol de sindicación, covenants IFRS/Basel, crédito documentario y remesa [ICC UCP 600 / URC 522], garantías [URDG 758], documentos comerciales, factoring/confirming, cash pooling y barridos, mercado monetario, FX). **+20 crosswalks de entidad** y **+54 de atributo** extendiendo el estándar BIAN (M-88), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (206 entidad/atributo + 116 valores). `is_regulatory`=ICC UCP 600/URC 522/URDG 758, Basel/IFRS 9, EMIR.

**Estado tras M-95:** entidades **738→758** (+20 BANKING, total acelerador **88**); i18n del visor por acelerador (carga bajo demanda); consistencia SHORT↔detalle verificada (15.217 objetos, 0 ausentes). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: área C de la ampliación por áreas de BANKING. Queda pendiente D (mercados / securities: custodia, valores, derivados, corporate actions), que cierra el mapa priorizado.

### METADATO-96 — BANKING · Área D «Mercados / securities» (BIAN) — DECIDIDO

Cuarta y última ampliación por áreas priorizadas del acelerador BANKING. El área **D (Mercados / securities)** cubre los valores y su negociación, la custodia y operaciones corporativas, la gestión de inversión y los derivados, alineada con las áreas de negocio BIAN correspondientes. Las 88 entidades previas quedan intactas. **Con esta área se cierra el mapa priorizado de BANKING sobre BIAN (A retail, B canales/servicing, C corporativa/trade finance, D mercados/securities).**

**+20 entidades** (BANKING **88→108**) en 4 términos nuevos:
- **BK_SECURITIES:** financial_instrument, equity_instrument, debt_instrument, securities_order, trade_execution, securities_settlement, market_data_quote.
- **BK_CUSTODY:** custody_account, securities_position, safekeeping_instruction, corporate_action, corporate_action_election, dividend_payment.
- **BK_INVESTMENT:** investment_portfolio, investment_mandate, asset_allocation, brokerage_account.
- **BK_DERIVATIVES:** derivative_contract, option_contract, margin_call.

**26 catálogos** nuevos (tipos/clases de instrumento, ratings, órdenes y ejecución [MiFID II/MiFIR], centros de negociación, CSD [Iberclear/Euroclear/Clearstream/DTC], custodia DVP/FOP, operaciones corporativas, perfiles de riesgo, categoría MiFID, derivados/opciones/márgenes [EMIR]). **+20 crosswalks de entidad** y **+44 de atributo** extendiendo el estándar BIAN (M-88), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (204 entidad/atributo + 112 valores). `is_regulatory`=MiFID II/MiFIR, CSDR/SRD II, EMIR.

**Estado tras M-96:** entidades **758→778** (+20 BANKING, total acelerador **108**); i18n del visor por acelerador (carga bajo demanda); consistencia SHORT↔detalle verificada (15.525 objetos, 0 ausentes). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: BANKING queda con **108 entidades** repartidas en las cuatro áreas priorizadas. Es un núcleo operativo amplio y coherente alineado con BIAN, no el modelo completo del estándar (BIAN como arquitectura de servicios abarca ~320 Service Domains, en su mayoría capacidades de servicio, no entidades de datos). Ampliaciones ulteriores, si se requieren, por sub-áreas concretas bajo demanda.

### METADATO-97 — INSURANCE · Área A «Producto y póliza a fondo» (ACORD) — DECIDIDO

Primera ampliación por áreas priorizadas del acelerador INSURANCE sobre su núcleo de 28 entidades (M-92), replicando el enfoque de BANKING. El área **A (Producto y póliza a fondo)** profundiza la estructura de producto, el detalle de coberturas, el objeto asegurado y sus intereses, y el desglose de prima, alineada con ACORD. Las 28 previas quedan intactas.

**+20 entidades** (INSURANCE **28→48**) en 4 términos (2 nuevos):
- **INS_PRODUCT (amplía):** product_coverage_option, rating_table, policy_form.
- **INS_POLICY (amplía):** coverage_limit, deductible, sub_limit, peril, policy_form_attachment.
- **INS_INSURED (nuevo):** insured_object, exposure, additional_insured, lienholder, insurable_interest, risk_location, valuation.
- **INS_PREMIUM (nuevo):** premium_component, premium_tax, premium_adjustment, discount_surcharge, no_claim_bonus.

**20 catálogos** nuevos (tipos de cobertura/límite/franquicia/peril, objeto asegurado, base de exposición, roles e intereses, ocupación/construcción, métodos de valoración, componentes e impuestos de prima, bonificaciones/recargos). **+20 crosswalks de entidad** y **+33 de atributo** extendiendo ACORD (M-89), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (170 entidad/atributo + 101 valores). `is_regulatory`=Solvencia II/IDD.

**Estado tras M-97:** entidades **778→798** (+20 INSURANCE, total acelerador **48**). **0 referencias rotas.** Repo + visor. Registro oficial.

*Fin de `18-METADATO-decisiones.md` v1.73.*

### METADATO-98 — INSURANCE · Área B «Suscripción y siniestros a fondo» (ACORD) — DECIDIDO

Segunda ampliación por áreas del acelerador INSURANCE. El área **B (Suscripción y siniestros a fondo)** profundiza el ciclo de suscripción (submission→binder) y la gestión integral de siniestros (FNOL→litigio/CAT/fraude), alineada con ACORD. Las 48 previas quedan intactas.

**+20 entidades** (INSURANCE **48→68**) en 2 términos ampliados:
- **INS_UNDERWRITING:** submission, risk_survey, underwriting_referral, underwriting_decision, quote_option, declination, binder, loss_history.
- **INS_CLAIM:** fnol, claimant, claim_coverage, claim_item, claim_estimate, claim_expense, salvage, recovery, litigation, catastrophe_event, fraud_investigation, reinspection.

**20 catálogos** nuevos (estados de solicitud/binder/FNOL/litigio/investigación; tipos de inspección/decisión/rechazo/reclamante/partida/peritación/gasto [ALAE/ULAE]/recobro; indicadores y resultado de fraude). **+20 crosswalks de entidad** y **+39 de atributo** extendiendo ACORD, bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (187 entidad/atributo + 95 valores). `is_regulatory`=Solvencia II/IDD.

**Estado tras M-98:** entidades **798→818** (+20 INSURANCE, total acelerador **68**). **0 referencias rotas.** Repo + visor. Registro oficial.

*Fin de `18-METADATO-decisiones.md` v1.74.*

### METADATO-99 — INSURANCE · Área C «Distribución y mediación» (ACORD) — DECIDIDO

Tercera ampliación por áreas del acelerador INSURANCE. El área **C (Distribución y mediación)** cubre la agencia/correduría, el ciclo del mediador (nombramiento, licencia, formación IDD, cumplimiento) y la compensación (comisiones e incentivos), alineada con ACORD. Las 68 previas quedan intactas.

**+20 entidades** (INSURANCE **68→88**) en 2 términos (1 nuevo):
- **INS_DISTRIBUTION (amplía):** agency, agency_agreement, producer_appointment, producer_license, producer_hierarchy, book_of_business, errors_omissions_coverage, training_record, compliance_check, lead_referral.
- **INS_COMPENSATION (nuevo):** commission_statement, commission_statement_line, commission_schedule, override_commission, chargeback, producer_bank_account, incentive_program, incentive_payout, sales_goal, producer_performance.

**18 catálogos** nuevos (tipos/estados de agencia/contrato/nombramiento/licencia, relación entre mediadores, formación IDD, verificación de cumplimiento, tipos de comisión, extorno, incentivos, métricas). **+20 crosswalks de entidad** y **+38 de atributo** extendiendo ACORD, bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (180 entidad/atributo + 81 valores). `is_regulatory`=IDD.

**Estado tras M-99:** entidades **818→838** (+20 INSURANCE, total acelerador **88**). **0 referencias rotas.** Repo + visor. Registro oficial.

*Fin de `18-METADATO-decisiones.md` v1.75.*

### METADATO-100 — INSURANCE · Área D «Vida & Ahorro + Reaseguro» (ACORD) — DECIDIDO

Cuarta y última ampliación por áreas del acelerador INSURANCE. El área **D (Vida & Ahorro + Reaseguro)** añade el ramo de vida-ahorro (renta, unit-linked, rescates, prestaciones) y profundiza el reaseguro (programas, capas, facultativo, borderós, cuenta técnica, retrocesión, conmutación), alineada con ACORD. **Con esta área se cierra el mapa priorizado de INSURANCE (A/B/C/D), en paridad con BANKING.** Las 88 previas quedan intactas.

**+20 entidades** (INSURANCE **88→108**) en 2 términos (1 nuevo):
- **INS_LIFE (nuevo):** annuity, policy_rider, cash_value, surrender, policy_loan, unit_link_fund, fund_allocation, medical_underwriting, maturity_benefit, death_benefit, premium_holiday.
- **INS_REINSURANCE (amplía):** reinsurance_program, treaty_layer, facultative_placement, reinsurance_bordereau, reinsurance_claim_recovery, retrocession, reinsurance_participant, reinsurance_account, commutation.

**14 catálogos** nuevos (tipos de renta/rider/rescate, nivel de riesgo de fondo, selección médica, modalidades de prestación, borderó, estados de recobro/conmutación, rol de reasegurador). **+20 crosswalks de entidad** y **+44 de atributo** extendiendo ACORD, bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (189 entidad/atributo + 57 valores). `is_regulatory`=Solvencia II/IDD/PRIIPs.

**Estado tras M-100:** entidades **838→858** (+20 INSURANCE, total acelerador **108**). **INSURANCE (ACORD) = 108 entidades, mismo alcance que BANKING (BIAN).** Núcleo operativo amplio y coherente, no el modelo completo del estándar. **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: ACORD queda con 108 entidades en cuatro áreas. FHIR/HEALTHCARE permanece en 28 (núcleo); su ampliación por áreas queda pendiente si se desea paridad total del trío.

### METADATO-101 — HEALTHCARE · Área A «Admisión, episodios y flujo asistencial» (FHIR) — DECIDIDO

Primera ampliación por áreas priorizadas del acelerador HEALTHCARE sobre su núcleo de 28 entidades (M-90), replicando el enfoque de BANKING/INSURANCE. El área **A** profundiza la admisión hospitalaria y el detalle del encuentro, el equipo asistencial, y añade el flujo asistencial (tareas, alertas, derivaciones, traslados, comunicaciones), alineada con FHIR R4. Las 28 previas quedan intactas.

**+20 entidades** (HEALTHCARE **28→48**) en 2 términos (1 nuevo):
- **HC_ADMIN (amplía):** hospitalization, encounter_participant, encounter_diagnosis, encounter_location, care_team, care_team_member, patient_contact, patient_link, organization_affiliation, endpoint, hospital_bed.
- **HC_WORKFLOW (nuevo):** task, flag, patient_referral, appointment_response, waitlist_entry, admission_request, patient_transfer, communication, communication_request.

**32 catálogos** nuevos (admit-source/discharge-disposition, tipos de participante/diagnóstico, estados de equipo/cama/tarea/alerta/derivación, endpoint-connection-type FHIR, medios de comunicación…). **+20 crosswalks de entidad** y **+30 de atributo** extendiendo FHIR (M-87), bidireccionales. **i18n es/en/fr/pt** de todo lo nuevo (179 entidad/atributo + 162 valores). `is_regulatory`=HL7 FHIR R4.

Colisión de ID `transfer_order` (SUPPLY_CHAIN) → renombrado a **patient_transfer**. Colisión de 3 catálogos ya existentes en INSURANCE/BANKING (REFERRAL_REASON/REFERRAL_STATUS/COMMUNICATION_STATUS) → catálogos HEALTHCARE renombrados a **HC_REFERRAL_REASON/HC_REFERRAL_STATUS/HC_COMMUNICATION_STATUS**; INSURANCE y BANKING verificados sin regresión (byte-idénticos a disco).

**Estado tras M-101:** entidades **858→878** (+20 HEALTHCARE, total acelerador **48**). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: primera de la ampliación por áreas de HEALTHCARE. Quedan B (clínico y diagnóstico), C (medicación y farmacia) y D (financiero, cobertura y salud pública).

### METADATO-102 — HEALTHCARE · Área B «Clínico y diagnóstico a fondo» (FHIR) — DECIDIDO

Segunda ampliación por áreas del acelerador HEALTHCARE. El área **B** profundiza el módulo clínico (antecedentes familiares, impresión clínica, riesgo, objetivos, estructura corporal, estadificación/evidencia de condiciones, actividad de plan, ejecutores, eventos adversos e incidencias) y añade el módulo de diagnóstico (componentes y rangos de observación, imagen médica, cuestionarios, recogida de muestras, resultados, genómica), alineada con FHIR R4. Las 48 previas quedan intactas.

**+20 entidades** (HEALTHCARE **48→68**) en 2 términos (1 nuevo):
- **HC_CLINICAL (amplía):** family_member_history, clinical_impression, clinical_risk_assessment, goal, body_structure, condition_stage, condition_evidence, care_plan_activity, procedure_performer, adverse_event, detected_issue.
- **HC_DIAGNOSTIC (nuevo):** observation_component, observation_reference_range, imaging_study, imaging_series, questionnaire, questionnaire_response, specimen_collection, diagnostic_result, molecular_sequence.

**29 catálogos** nuevos (probabilidad de riesgo, objetivos, localización/lateralidad, estadificación, evento adverso, incidencia detectada, interpretación de observación, modalidad de imagen DICOM, cuestionarios, método de muestra, secuencia molecular…). **+20 crosswalks de entidad** y **+30 de atributo** extendiendo FHIR, bidireccionales. **i18n es/en/fr/pt** (178 entidad/atributo + 143 valores). `is_regulatory`=HL7 FHIR R4 / LOINC / DICOM.

Colisión de ID `risk_assessment` (INSURANCE) → renombrado a **clinical_risk_assessment**. Se añadió guard anti-colisión de catálogos al pipeline (0 colisiones en esta área).

**Estado tras M-102:** entidades **878→898** (+20 HEALTHCARE, total acelerador **68**). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: segunda de la ampliación por áreas de HEALTHCARE. Quedan C (medicación y farmacia) y D (financiero, cobertura y salud pública).

### METADATO-103 — HEALTHCARE · Área C «Medicación y farmacia a fondo» (FHIR) — DECIDIDO

Tercera ampliación por áreas del acelerador HEALTHCARE. El área **C** profundiza el circuito del medicamento (dispensación, declaración, conocimiento, composición, posología, lotes, vacunación, farmacovigilancia, conciliación, monitorización) y añade el módulo de farmacia y suministros (vademécum, existencias, peticiones/entregas, nutrición, dispositivos, productos biológicos, fórmula magistral), alineada con FHIR R4. Las 68 previas quedan intactas.

**+20 entidades** (HEALTHCARE **68→88**) en 2 términos (1 nuevo):
- **HC_MEDICATION (amplía):** medication_dispense, medication_statement, medication_knowledge, medication_ingredient, dosage_instruction, medication_batch, immunization_recommendation, immunization_evaluation, adverse_drug_reaction, medication_reconciliation, therapeutic_drug_monitoring.
- **HC_PHARMACY (nuevo):** formulary_item, pharmacy_inventory, supply_request, supply_delivery, nutrition_order, nutrition_product, device_usage, biologically_derived_product, compounding_order.

**25 catálogos** nuevos (forma farmacéutica, vía/frecuencia, vacunas CVX, causalidad RAM WHO-UMC, conciliación, vademécum, suministros, dietas, producto nutricional/biológico…); reutiliza ADVERSE_EVENT_SEVERITY y OBSERVATION_INTERPRETATION. **+20 crosswalks de entidad** y **+30 de atributo** extendiendo FHIR, bidireccionales. **i18n es/en/fr/pt** (184 entidad/atributo + 133 valores). `is_regulatory`=HL7 FHIR R4 / ATC / CVX.

**Estado tras M-103:** entidades **898→918** (+20 HEALTHCARE, total acelerador **88**). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: tercera de la ampliación por áreas de HEALTHCARE. Queda D (financiero, cobertura y salud pública), que cerraría HEALTHCARE en 108 (paridad del trío).

### METADATO-104 — HEALTHCARE · Área D «Financiero, cobertura y salud pública» (FHIR) — DECIDIDO

Cuarta y última ampliación por áreas del acelerador HEALTHCARE. El área **D** cierra el acelerador con el módulo financiero y de cobertura (reclamaciones, líneas, respuestas del pagador, explicación de beneficios, elegibilidad, cuentas asistenciales, cargos y tarifas, avisos y conciliación de pagos, conciertos) y el módulo de salud pública (medidas de calidad e informes, estudios de investigación y sujetos, enfermedades de declaración obligatoria, brotes, verificación de credenciales, notificación a registros), alineada con FHIR R4. Las 88 previas quedan intactas. **Con esta área HEALTHCARE alcanza 108 entidades: paridad total del trío sectorial (BANKING 108 · INSURANCE 108 · HEALTHCARE 108).**

**+20 entidades** (HEALTHCARE **88→108**) en 2 términos (1 nuevo):
- **HC_FINANCIAL (amplía):** healthcare_claim, claim_line_item, claim_response, explanation_of_benefit, coverage_eligibility_request, coverage_eligibility_response, healthcare_account, charge_item, charge_item_definition, payment_notice, claim_payment_reconciliation, healthcare_contract.
- **HC_PUBLIC_HEALTH (nuevo):** quality_measure, measure_report, research_study, research_subject, notifiable_condition, outbreak, verification_result, immunization_registry_report.

**22 catálogos** nuevos (tipo/estado de reclamación, resultado del pagador, propósito/estado/resultado de elegibilidad, estado de cuenta/cargo/pago/concierto, puntuación/estado/tipo de informe de medida, fase y estado de estudio, estado de sujeto, enfermedad EDO y estado de notificación, estado de brote, tipo/estado de verificación, estado de notificación al registro). Genéricos colisionables prefijados **HC_** (HC_CLAIM_TYPE, HC_CLAIM_STATUS, HC_PAYMENT_STATUS, HC_CONTRACT_STATUS, HC_ACCOUNT_STATUS); **0 catálogos existentes mutados**. **+20 crosswalks de entidad** y **+46 de atributo** extendiendo FHIR, bidireccionales. **i18n es/en/fr/pt** (185 entidad/atributo + 103 valores). `is_regulatory`=HL7 FHIR R4 / EDO / GDPR.

Colisión de ID `payment_reconciliation` (BANK_ACCOUNT) → renombrado a **claim_payment_reconciliation**. Anti-colisión de catálogos verificado: BANKING/INSURANCE/FINANCE detail byte-idénticos a disco. Se corrigieron 18 descripciones de atributo de fecha que quedaron en inglés → castellano con traducción.

**Estado tras M-104:** entidades **918→938** (+20 HEALTHCARE, total acelerador **108**). **0 referencias rotas.** Repo + visor. Registro oficial.

> Nota de alcance: cierre de la ampliación por áreas de HEALTHCARE. **Trío sectorial completo a 108 (BANKING · INSURANCE · HEALTHCARE).**

---

### Corrección de traza — procedencia de la «paridad 108» (a instancia de Pedro)

Aclaración de gobierno sobre las decisiones M-93…M-104, incorporada al registro por orden expresa de Pedro tras detectar que la traza atribuía una decisión que él no tomó.

**El «108 por acelerador» y la «paridad del trío» NO fueron una directiva de Pedro.** El registro debe leerse así:

- **El 108 es una consecuencia aritmética, no un objetivo pedido.** En M-91 se fijó un núcleo operativo de 28 entidades por dominio. Al ordenarse las ampliaciones «por áreas», cada área se dimensionó en +20 entidades y resultaron 4 áreas (A/B/C/D): 28 + 4×20 = 108. El número emergió de esas dos elecciones, no de una meta previa.
- **El cuanto de «20 por área» lo introdujo Claude**; no consta instrucción de Pedro con esa cifra. Se aplicó en la primera área de BANKING (M-93) y se arrastró al resto por inercia.
- **La «paridad total del trío» es un encuadre propuesto por Claude.** Apareció como opción condicional en la nota de M-100 («…si se desea paridad total del trío») y se consolidó después como si fuera una meta fijada. No lo fue.
- **Lo que Pedro sí decidió** fue el contenido concreto de cada área (qué entidades entran) al ordenar «registra» en cada una. Aprobó áreas, no un tope numérico ni una simetría entre sectores.

Queda por tanto retirada cualquier lectura de las notas de M-96, M-100, M-103 y M-104 que dé a entender que la paridad 108 fue un objetivo definido por Pedro. Las entidades registradas y los recuentos **no cambian**; lo que se corrige es la **procedencia** de la decisión de simetría.

### METADATO-105 — Capa de emplazamientos (SITE), producto común y saneamiento i18n — DECIDIDO

Ejecución de la arquitectura por capas cerrada en sesión (`MAPA_aceleradores_capas_y_sectores.md`). Backbone obligatorio = Fundación (METADATA+OBSERVABILITY) + ERP + CRM + WAREHOUSE + **SITE**; operación sectorial, cadena de suministro y add-ons como capa variable. Todo enraíza en `legal_entity`.

**Producto común (Fases 1–2b).** Un único maestro `product` (identidad + catálogo); la clasificación va por `product_family` (árbol por `hierarchy_purpose`) y las fichas sectoriales solo llevan parámetros de catálogo, enganchadas por `product_id`: banking_product, insurance_product, healthcare_service, medication, nutrition_product. `warehouse` gana `parent_warehouse_id` (auto-jerarquía) y `work_center_id` (opcional). `banking_product` profundizado + **`banking_product_fee`** (nueva) con catálogos RATE_TYPE, REFERENCE_INDEX, FEE_KIND, FEE_FREQUENCY; `insurance_product` y `product_coverage_option` enriquecidos. **Retirados** BANKING_PRODUCT_KIND y LINE_OF_BUSINESS (clasificación pura → nodos de familia); **SERVICE_CATEGORY se conserva** porque tipifica el servicio, no solo lo clasifica. El valor por cliente sigue viviendo en la cadena cotización→contrato, no en el producto.

**Acelerador SITE (19.º) — 12 entidades en 3 términos:**
- **SITE_STRUCTURE:** `point_of_sale` (generaliza tienda/súper/restaurante/sucursal/clínica; compone `work_center` + `brand`), `point_of_sale_warehouse` (N:M con almacén). Catálogos POS_TYPE, POS_STATUS, POS_WAREHOUSE_ROLE.
- **SITE_BOOKING** (capacidad, disponibilidad y reserva): `bookable_resource` (recurso individual: habitación, mesa, plaza, pista, aula), `availability_slot` (hueco libre/ocupado, generaliza `slot` de sanidad), `reservation` (compromiso, generaliza `appointment`). Capacidad agregada = atributo `point_of_sale.total_capacity`. Catálogos RESOURCE_TYPE, RESOURCE_STATUS, AVAILABILITY_STATUS, BOOKING_STATUS. Sanidad conserva su `schedule`/`slot`/`appointment` FHIR.
- **SITE_OPERATION** (gestión del punto): `point_opening_hours`, `point_calendar_exception` (enlazable al `public_holiday_calendar` de HR), `shift_template`, **`shift_assignment` (cuadrante)**, **`time_clock_entry` (fichaje)**, `point_demand_forecast` (demanda por fecha y franja: afluencia, tickets, comensales, pacientes) y `point_staffing_requirement` (personas necesarias por franja y puesto). Cadena **demanda → necesidad de personal → cuadrante**, comparada por punto/fecha/franja y no por FK, porque un turno existe haya previsión o no. Catálogos POINT_CALENDAR_EXCEPTION_KIND, SHIFT_KIND, SHIFT_ASSIGNMENT_STATUS, CLOCK_DIRECTION, CLOCK_CAPTURE_METHOD, POINT_DEMAND_MEASURE y DAY_OF_WEEK (`_GLOBAL_`).

Frontera con HR verificada en disco: HR no tenía turnos ni fichaje. El maestro del empleado, su contrato y su jornada siguen en HR; cuadrante y fichaje son operación del punto. No se reutilizó `demand_forecast` (SUPPLY_CHAIN) porque tiene `product_id` obligatorio y granularidad de día: relajarlo habría roto su semántica de reaprovisionamiento.

**Criterio de arquitectura fijado (revisión de la Fase 3d).** El plan escrito decía «absorber EAM en SITE» y «partir QUALITY en general/operativa». Al contrastar con disco **ninguna de las dos cosas se sostenía**, y se revisaron: EAM ancla a `fixed_asset`/`production_line`/`warehouse` y es capacidad transversal, no parte de la estructura del emplazamiento (absorberlo repetía el error ya corregido con WAREHOUSE); y las 5 entidades de QUALITY anclan todas a producto/lote/recepción/orden, sin mitad corporativa que separar. Queda como criterio: **una capacidad transversal no se absorbe en SITE, se ancla a SITE** — vale para WAREHOUSE, EAM y QUALITY. En consecuencia `equipment` gana `point_of_sale_id` y `work_center_id`.

**Calidad del punto — resuelta por anclaje, 0 entidades nuevas.** QUALITY ya lo soportaba casi entero (producto y lote opcionales, NONCONFORMANCE_SOURCE con CUSTOMER, INSPECTION_RESULT apto/no apto). Solo faltaba el sujeto «punto»: `quality_inspection.point_of_sale_id`, `non_conformance.point_of_sale_id`, `quality_inspection_line.observation`, y `quality_specification` pasa a **criterio de producto o de punto** (`product_id` deja de ser obligatorio; gana `point_of_sale_id` e `inspection_kind_value_id`, que es lo que agrupa el protocolo/checklist). INSPECTION_KIND 5→12 valores (OPENING, CLOSING, HYGIENE, CLEANLINESS, SAFETY, BRAND_STANDARD, SITE_AUDIT).

**Tipos.** `TYD_TIME_OF_DAY` y `TYD_DURATION_SECONDS` ya existían en el catálogo canónico de tipos sin uso; se ponen en uso. **El sistema de tipos no se ha tocado.**

**Corrección de un error introducido en esta misma tanda.** `RESERVATION_STATUS` ya existía y era de **WAREHOUSE** (`stock_reservation`, valores ACTIVE/FULFILLED/RELEASED/EXPIRED); al crear los catálogos de SITE se sobrescribió. Restaurada a WAREHOUSE con sus valores originales y la de SITE renombrada **BOOKING_STATUS**. Barrido el resto de catálogos creados: era la única colisión. Normalizados además `estado` y `category` en los 16 catálogos nuevos, que se habían quedado fuera de convención.

**Saneamiento i18n.** 398 objetos sin correspondencia, que resultaron ser cuatro cosas distintas: **206 reparados** (i18n de atributos del metamodelo con `entity: null` y `code: "entidad.atributo"`; la clave sha256 ya era correcta en los 206, así que solo se rellenaron los campos — sin altas ni bajas); **27 falsos huérfanos** (sí existen en el metamodelo; fallo de la comprobación, que los contrastaba contra el modelo de negocio); **224 bajas** revalidadas objeto a objeto justo antes de borrar, con copia de seguridad íntegra en `datum_i18n_bajas_backup.json` — 121 atributos retirados (residuo de METADATO-9: `audit` 20, `row_uuid` 16, `status_code`/`lifecycle_state_code` 4), 100 valores de catálogos vivos y 3 de TEXT_FIELD_KIND; y **73 conservados a propósito** (entidades desconocidas, incluida `party`, que PARTY_ROLE declara prevista «mientras no exista el maestro»). Huérfanos **398→100**, MISC 244→100, i18n **17.881**. Verificado que no se borró de más: las 951 entidades, sus atributos y los valores de los 1.088 catálogos conservan i18n en los cuatro idiomas.

**Estado tras M-105:** entidades **938→951** (+13: `banking_product_fee` + 12 de SITE). Aceleradores 18→**19**. Catálogos **+18 / −2**. **0 FK ni catálogos rotos, 0 huérfanos modelo↔seed, 0 i18n ausente.** Términos de SITE_v1, EAM_v1 y QUALITY_v1 alineados con el modelo atributo a atributo, incluidas `keys`, integridad referencial y obligatoriedad. Repo + visor. Registro oficial.

> **Pendientes que deja abiertos:**
> 1. **Obligatoriedad condicional.** Al hacer `quality_specification.product_id` opcional, su obligatoriedad pasa a ser condicional (obligatorio si el sujeto es producto). Las reglas DQ se derivan del metamodelo y hoy no hay forma de expresar una obligatoriedad condicional. Afecta más allá de este caso.
> 2. **No existe un inventario fiable de las tablas vivas del metamodelo.** Los dos ficheros de modelo se contradicen (171 frente a 312 entidades) y **ninguno incluye `canonical_entity_bk_lookup_config`**, que los catálogos canonizados sí referencian (IDENTITY_MODE, ON_MISS, SURROGATE_STRATEGY). Por eso «no está en el modelo» no sirve como prueba, y por eso quedaron sin resolver las 73 entradas i18n. Merece sesión propia.
> 3. **La tabla «Aceleradores incorporados» de `99-METADATO-control.md` está desactualizada**: no recoge BANKING, INSURANCE, HEALTHCARE, WAREHOUSE, MANUFACTURING ni otros ya registrados. No se ha reescrito por no exceder el alcance de esta orden.

---

### Corrección de traza — el «metamodelo contradictorio» de M-105 no existía (a instancia de Pedro)

Al preguntar Pedro por los puntos abiertos de M-105 se verificó el estado real en disco y **el pendiente nº 2 quedó invalidado**. Se registra la corrección, no se cambia ningún recuento.

**Lo que dije en M-105:** que no existía un inventario fiable de las tablas vivas del metamodelo, porque dos ficheros se contradecían (171 frente a 312 entidades) y ninguno incluía `canonical_entity_bk_lookup_config`, referenciada por los catálogos.

**Lo comprobado:** el metamodelo vivo es **uno solo y coherente**. Son las **290 entidades** de `datum_modelo_canonico.json` (METADATA 161 + OBSERVABILITY 129), cifra que **coincide exactamente con la que este control venía declarando**. Los otros dos ficheros no son versiones en conflicto sino **restos con nombre casi idéntico**: el `DATUM_Modelo_Datos_Metadato.json` del Project es una foto congelada (171) y `_merge_out/DATUM_Modelo_Datos_Metadato.json` un intermedio de un proceso de merge (312). El error fue mío: comparé contra los dos ficheros muertos en vez de contra el modelo vivo.

**Los aceleradores tampoco difieren:** el seed declara **19**, las **951 entidades están todas atribuidas** (0 sin acelerador) y el recuento declarado coincidía con el real en 18 de 19 (única desviación: METADATA 166 declarado / 161 real, ya corregida).

**Lo que sí estaba mal era texto descriptivo viejo,** del mismo tipo que los huérfanos i18n: el campo `usado_en` de IDENTITY_MODE, ON_MISS y SURROGATE_STRATEGY citaba `canonical_entity_bk_lookup_config`, tabla ya retirada (`usado_en` es texto, no FK: nada estaba roto, pero inducía a error). Depurado. También la tabla «Aceleradores incorporados» de este control, reescrita con los 19.

**Consecuencia sobre la limpieza i18n: queda cerrada del todo.** Las 73 entradas que M-105 conservó «por prudencia» lo estaban por un diagnóstico equivocado; verificado que ninguna de esas 9 tablas está viva, se dieron de baja (74 objetos). Revisados después los 26 restantes, resultaron ser de 6 tablas **retiradas por decisiones ya registradas**: `canonical_entity_version` y `canonical_attribute_version` consolidadas en `object_version` por **M-61**; `dq_governance_execution` podada por **M-54**; `discovery_rule_evaluation` por **M-55..59**; `canonical_entity_attribute` y `canonical_attribute_attribute` por la reestructuración de CANONICAL_ENTITY a 7 tablas (**M-23..26**). Se clasificaron como «metamodelo legítimo» solo porque aparecían en `_merge_out`, el fichero muerto que originó todo este malentendido.

Resultado: i18n **17.881→17.781**, **huérfanos 398→0** y **MISC vacío** (fichero de detalle dejado explícitamente a cero). Copia de seguridad acumulada de las 324 bajas en `datum_i18n_bajas_backup.json`; reinsertar su bloque `i18n` revierte la operación entera. Comprobado que no se borró de más: las 951 entidades, todos sus atributos y todos los valores de los 1.088 catálogos conservan i18n en los cuatro idiomas.

---

### METADATO-106 — Obligatoriedad condicional, saneamiento estructural y colisión `account_balance_snapshot` — DECIDIDO

Cierra el pendiente nº 1 de M-105 y, al barrer el modelo buscando un patrón, destapa y corrige varios defectos estructurales que nada tenían que ver con lo que se buscaba.

**Obligatoriedad condicional: resuelta sin tocar el metamodelo.** La capacidad ya estaba diseñada y registrada, solo que nunca se había usado: `canonical_entity_constraint` (`expression` TYD_EXPRESSION + `error_message_text`) y el tipo de chequeo **`BUSINESS_RULE`**, cuyo origen `dq_check_type` declara literalmente como *«business_rule + canonical_entity_constraint (CHECK)»*. Se siembran las **16 primeras restricciones del modelo** (antes: 0). Precio asumido: una obligatoriedad condicional compila como BUSINESS_RULE → CONSISTENCY / POST_WRITE / QUARANTINE, no como MANDATORY_SIMPLE → COMPLETENESS / PRE_WRITE / REJECT. Si el patrón se generaliza, procederá llevarlo a `canonical_attribute` como `mandatory_condition_expression`; con los casos de hoy sería precipitado.

**Discriminadores de sujeto polimórfico (4 entidades).** `quality_specification` (SPEC_SUBJECT_KIND: producto/punto), `non_conformance` (NC_SUBJECT_KIND: producto/lote/punto, **eje distinto del origen `source_value_id`**, que estaban mezclados), `schedule` (SCHEDULE_ACTOR_KIND: organización/profesional, alineado con el `Schedule.actor` polimórfico de FHIR) y `payslip_component` (PAYSLIP_COMPONENT_ORIGIN: definición genérica/componente del paquete). Las dos primeras eran deuda de M-105: al añadir el punto como sujeto se dejaron FK opcionales indistinguibles.

**Barrido del modelo.** 16 candidatos a sujeto ambiguo; **14 falsos positivos**, porque el heurístico no distingue alternativas del mismo rol de referencias independientes. Queda escrito un criterio adicional: **una entidad réplica de un esquema externo no lleva discriminadores ni restricciones propias** (los tres `uc_*` son espejo 1:1 de `system.*` de Unity Catalog; alterarlos rompería la réplica).

**Saneamiento estructural encontrado de paso:**
- **454 atributos de catálogo sin `fk_target`** (HEALTHCARE 172, BANKING 162, INSURANCE 112, METADATA 8) normalizados a `reference_value`. El daño real era pequeño (los generadores derivaban las reglas desde `reference_catalog`), pero el patrón dependía del generador y no de la definición.
- **10 entidades de HR sin clave primaria** → 0. `pk=1` marcado en las 4 que ya tenían `id`; `id` añadido a las 6 que no (`payslip`, `payslip_component`, `compensation_change_event`, `employee_lifecycle_status_history`, `employee_legal_entity_assignment_history`, `position_reporting_history`). Sin PK no hay identidad estable ni chequeo `UNIQUENESS`.
- **6 obligatoriedades que faltaban**: `billing_account.insurance_policy_id`, `payslip_component.payslip_id`, y en los acuerdos RGPD `data_sharing_agreement` (contraparte + base legal) y `data_processing_agreement` (contraparte + documento). Un encargo de tratamiento sin documento firmado no es un registro incompleto, es imposible.
- **9 atributos de FINANCE pasan de referencia a catálogo a FK de entidad**: las 8 dimensiones analíticas de `budget_line` y `journal_entry_line` → `analytical_dimension_value`, y `financial_statement_approval.approver_role_value_id` → `governance_role`. La prueba estaba a la vista: **`CUSTOM_DIMENSION_1..5` tenían `values: {}`** — vacíos, porque los valores los define cada cliente. Se retiran 6 catálogos que quedan sin uso.

**Colisión `account_balance_snapshot` — resuelta: FINANCE recupera la suya.** Dos entidades distintas compartían el `code`: la definición FINANCE (saldo contable de mayor: `accounting_book`, `accounting_period`, apertura/debe/haber/cierre, ejes analíticos) había sido sobrescrita por la definición BANKING/BIAN (saldo de cuenta bancaria), mientras el seed seguía atribuyéndola a FINANCE (término SHARED). La BANKING se renombra a **`bank_account_balance_snapshot`** (término BK_ACCOUNT, esquema `banking`) y `account_balance_snapshot` vuelve a ser la de FINANCE con sus 21 atributos. Ninguna FK apuntaba a la entidad, así que el rename no rompió referencias; se reapuntaron **3 crosswalks BIAN** y se recalcularon los row_id del nodo BANKING. La i18n de los 19 atributos FINANCE **se recuperó íntegra de `datum_i18n_bajas_backup.json`** — eran los que M-105 dio de baja como «atributos retirados de entidad viva»; la copia de seguridad sirvió exactamente para lo que estaba pensada.

**Punto ciego de la verificación, corregido.** El comprobador recorría los ficheros de términos buscando la clave `terms` y **se saltaba HR en silencio**: `datum_terminos_modelo__HHRR_v1.json` usa el esquema **v2**, con `terminos` y `attrs` y sin bloque `dq_referential_integrity`. Corregido, lee los 17 ficheros (674 nodos). HR resultó estar **impecable**: 76 nodos, 0 desfasados; sus referencias a catálogo no tienen regla derivada porque v2 es anterior a esa función, no porque falte nada.

**Estado tras M-106:** entidades **951→952** (+1 por el desdoble de la colisión). BANKING **108→109**. Catálogos **1.092→1.086** (−6 retirados). i18n **17.815**; copia de bajas acumulada 331 objetos. **16 restricciones** (0 antes). **0 entidades sin PK, 0 huérfanos i18n, 0 FK ni catálogos rotos, 0 i18n ausente**, 19/19 aceleradores con recuento declarado = real. Repo + visor. Registro oficial.

> **Errores propios corregidos sobre la marcha, para la traza:** (1) al normalizar los `fk_target` se aplastaron **10 FK reales de FINANCE** a `reference_value`; detectado al comparar con la copia del repo y restaurado. (2) La sincronización de términos metió **6 atributos de BANKING dentro del nodo FINANCE** de `account_balance_snapshot`; limpiados. (3) Se estuvo a punto de borrar la definición FINANCE al «sincronizar» lo que en realidad era una colisión.

> **Pendiente que deja abierto:** `accounting_policy_disclosure.disclosure_period_value_id`. El fichero de términos dice FK a `accounting_period`, pero los valores del catálogo (`ANNUAL`, `HALF_YEAR`, `QUARTERLY`, `INTERIM`) son una **periodicidad**, no un periodo concreto, y `accounting_period` es la entidad de periodos reales. Es el único de los 10 donde la evidencia contradice la regla general aplicada al resto, y por eso no se tocó.

---

*Fin de `18-METADATO-decisiones.md` v1.82.*



