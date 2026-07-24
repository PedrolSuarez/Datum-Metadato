# 99 · Control de sincronización — Proyecto «DATUM metadato»



**Versión:** v1.37 — Julio 2026

**Propósito:** estado consolidado del metamodelo DATUM y de los aceleradores/modelos cargables. Los JSON son bootstrap del Control Plane.



## Regla de oro

La fuente de verdad es el **documento en disco**, no este registro. Nada se canoniza sin "registro oficial" del founder. Ficheros completos, nunca parches.



## Estado consolidado (tras METADATO-16..61, v1.37)

- Metamodelo: **291 entidades**, **2608 atributos** (M-42 retención; M-47 population_mode_code + emits_observability_entity; M-48 derived_from_entity). Fuente: `DATUM_Modelo_Datos_Metadato.json`. Trazabilidad del recuento: 178→311 (acelerador **OBSERVABILITY** materializado en 3 bloques —14 núcleo reasignado + 47 funcional DATUM A–I + 72 Unity Catalog—, M-41); 194→190 (simplificación CANONICAL_ENTITY, M-23); 190→187 (saneamiento BUSINESS_TERM, M-28); 187→202 (GEOGRAPHY/ORG/D07, M-30); 202→196 estado consolidado del rediseño D3 (M-31, base registrada 187→196); 196→184 (rediseño definición TRANSFORMATION, M-32); 184→189 (modelo de transformaciones por tipologías, M-33); 189→171 (ORCHESTRATION + fusión de identidad + limpieza integral de D3: captura/contracts/discovery/D-G/runners, M-34); 171→172 (acelerador DATA_QUALITY: +`dq_check_type`, M-35); 172→176 (cierre capa analítica D7 → término ANALYTICS, M-37); 176→178 (agregación nativa del hecho: +`accumulative_fact_filter`/`accumulative_fact_join`, M-38/39); 178→311 (materialización OBSERVABILITY, M-41); **311→303 (poda del gobierno de calidad DQ + acto único de evaluación, M-54)**; 303→295 (cierre D8 SECURITY/GDPR + eliminación D5 + poda discovery_rule + unificación retención, M-55..59); **295→291 (consolidación del versionado: 4 `*_version` dispersos → `object_version` polimórfico, M-61)**. Reparto por acelerador: **METADATA 159 / OBSERVABILITY 132**.

- Catálogos: **134** en `DATUM_Catalogos.json` (+9 OBSERVABILITY M-41; +RETENTION_POLICY M-42; +POPULATION_MODE M-47; M-54: −DQ_GOVERNANCE_KIND, +MATURITY_FRAMEWORK, +DATA_CRITICALITY, +SCORING_METHOD, +ANSWER_SCALE; ASSESSMENT_TYPE fuera de cuarentena; assessment_type/scoring_method/answer_scale saneados metadata-first; +LEVEL_SCALE, nivel dinámico como par autodescriptivo scale+value; M-55: +23 catálogos de D9/D10/D14 generados y cableados metadata-first). **M-61: sin cambio de recuento (134); recategorizados los 134 en 9 categorías funcionales** {KIND 71, MODE 17, STATUS 10, LEVEL 10, ACTION 7, FORMAT 5, DIMENSION 5, TIME 5, ROLE 4}.

- **Campo técnico universal `system` (TYD_SYSTEM)** en todas las entidades: encapsula ancla i18n (`row_uuid`), ciclo de vida (`lifecycle_state_code` → LIFECYCLE_STATE) y auditoría (created_at/by, updated_at/by, is_active, version). No visible en ER; en el plano físico se descompone en 8 columnas.

- **Término BUSINESS_TERM saneado a 3 tablas** (METADATO-28): `business_term` (núcleo), `business_term_synonym`, `business_term_related`. Eliminadas 3 puentes (`source_entity_business_term`→linaje D4; `business_term_canonical_entity`→redundante con `canonical_entity.business_term_code`; `canonical_attribute_business_term`→glosario a nivel entidad). `business_term_related` remodelado como **grafo semántico de negocio** (espejo de `canonical_relation` en D2): FK `business_term_code`(identifying)+`reference_business_term_code`, `code` discriminador (N arcos por par), `cardinality_code`→**CARDINALITY** (catálogo reutilizado). FK dependientes con `fk_composite`+`is_identifying`+RESTRICT; FK a catálogo metadata-first; `is_visible_er` de las FK identificativas corregido. Sin cambios de `.tsx` (el visualizador ya soportaba estos campos). **Catálogos saneados 16→10** (METADATO-28f): eliminados 6 huérfanos de la remodelación de CANONICAL_ENTITY (RELATION_KIND, RELATION_END_ROLE, CONSTRAINT_TYPE, MATERIALIZATION_MODE, EXPRESSION_ROLE, CARDINALITY viejo); CARDINALITY_REL→CARDINALITY.

- **Término CANONICAL_ENTITY reestructurado a 7 tablas** (METADATO-23..26): `canonical_entity`, `canonical_attribute`, `canonical_key`, `canonical_key_attribute`, `canonical_entity_constraint`, `canonical_relation`, `canonical_relation_attribute_map`.

- **Formato-documento canónico jerárquico autocontenido** (METADATO-22): `code` raíz + `entity{}` (metadatos con valores reales del seed) + `children{}` (attributes/keys/relations/constraints/partitions). Referencias: `_documento_reference_category.json` (simple) y `_documento_canonical_entity.json` (rica, canónica). Distinción plano ER funcional vs. plano físico (el físico se compila a DDL).

- **Patrón de entidades dependientes (weak entities)** (METADATO-26): padre→hijos→nietos con PK propagada y FK identificativas compuestas (`fk_composite{target, columns[{source,target}]}` + `is_identifying`; on_delete/on_update=RESTRICT). Patrón universal, sirve para modelo y para la UX en árbol.

- **`canonical_entity`** (11 campos): code(PK), business_term_code, config_pattern_code, physical_catalog_code, physical_schema_code (FK compuesta a physical_schema), is_pii, is_sensitive, security_classification_code, estimated_annual_volume, access_frequency_code, partition_strategy_code, system.

- **`canonical_attribute`** (PK `[canonical_entity_code, code]`): sin `referenced_entity_code` (la referencia va vía canonical_relation) ni `materialization_mode_code`; con `is_visible_er` y `partition_order`.

- **`canonical_relation`** (PK `[canonical_entity_code, code]`): `cardinality_code` (cat CARDINALITY {0:N,1:N,0:1,1:1}), `reference_canonical_entity_code`, on_delete/on_update_action_code, `is_identifying`. Sin `relation_kind_code`.

- **`canonical_entity_constraint`**: validaciones de negocio con `expression` (tipo CHECK) + `error_message_text`. Sin `constraint_type_code`. (Eliminada `canonical_entity_constraint_attribute`.)

- **Ficha de entidad integrada en el árbol** (METADATO-27): `/dashboard/canonico`, al pulsar entidad el panel muestra cabecera + i18n (3 campos con el code, sin ejecutar multiidioma) + pestañas Atributos/Constraints/Keys/FKs. Atributos muestra TODOS los campos (system descompuesto); catálogo en el atributo; FK a entidad solo en pestaña FKs.

- **Configuración Delta**: `delta_property` con 20 propiedades; patrón `DEFAULT` obligatorio. **Catálogos de datos**: `reference_catalog` con FK a acelerador; `STANDARD_AUTHORITY`. Catálogo de cardinalidad **CARDINALITY** (renombrado desde CARDINALITY_REL; {0:N,1:N,0:1,1:1}).

- **Término DATA_TYPE_DOMAIN saneado y cerrado** (METADATO-29): `data_type_domain_simple`→**`data_type_domain`** (nodo central, 12 FK entrantes). Nuevos defaults DDL heredables (is_pii/is_sensitive/is_nullable/is_auto_increment/is_generated _by_default, column_default, generation_expression) + `security_classification_code` metadata-first + formato i18n (`date_format_code`→**DATE_FORMAT**, `decimal_format_code`→**DECIMAL_FORMAT**). `data_type_domain_composite` reducido a `code`+`system` (materialización siempre EMBEDDED; clasificación emerge de sus campos). `data_type_domain_field` con FK renombradas (`data_type_domain_composite_code` identifying, `data_type_domain_code`), sin `cardinality_code`. Eliminada `data_type_domain_dq_rule` (FK colgante a `dq_rule` inexistente) → sustituida por **`data_type_domain_validation`**: validaciones tipadas (`expression` TYD_EXPRESSION: REGEX/SQL_SPARK) con **dueño polimórfico** [owner_object_row_uuid, owner_object_type_code, code] (patrón `expression`) que sirve a SIMPLE y COMPOSITE — un composite declara reglas completas que cruzan varios campos. `regex_pattern` eliminado del dominio (→ validación VALIDITY). `data_type_domain_ui_control` en **CUARENTENA** (revisión D10).

- **Tipología de validación anclada a D6 (calidad)** (METADATO-29): `data_type_domain_validation.dq_dimension_code`→**DQ_DIMENSION** (DAMA-DMBOK: COMPLETENESS/VALIDITY/ACCURACY/CONSISTENCY/UNIQUENESS/TIMELINESS). Catálogo **ISO_CHARACTERISTIC** (ISO/IEC 25012 inherentes). Cerradas las 2 FK colgantes de `dq_dimension_to_iso_characteristic`. Reglas DQ compiladas desde el metamodelo, no modeladas como tabla en D6.

- **Dimensión GEOGRAPHY incorporada** (METADATO-30): término GEO_STRUCTURE (bajo HIERARCHY) con 15 entidades. Jerarquía administrativa weak dependiente (continent→supra_zone→country[pivote]→region→province→locality) con PK propagado y FK compuestas identificativas. `country` mantiene PK simple; FK no dependiente a supra_zone. 3 jerarquías (ADMIN/COMMERCIAL/FISCAL); comercial y tax como puentes N:M polimórficos anclados a geografía (catálogo **GEO_LEVEL**). Eliminada `country_subdivision` (redundante). Las 4 ISO (country/language/currency/unit_of_measure) movidas de ISO_CODE a GEO_STRUCTURE (ISO_CODE vacío). `unit_of_measure` en CUARENTENA.

- **Refactor ORG_STRUCTURE y GOVERNANCE** (METADATO-30): madurez/criticidad QUITADAS de business_unit y business_process (son resultado de evaluación → van a `object_assessment`/`assessment_pattern`). `topology_code` se queda (config) → catálogo **GOVERNANCE_TOPOLOGY**. Catálogos nuevos **BUSINESS_UNIT_KIND**, **MATURITY_LEVEL**. `business_rule`→término DATA_QUALITY. Roles rediseñados: `business_unit_role_assignment`→**`governance_role_assignment`** (polimórfico, término GOVERNANCE, gobierna cualquier objeto) + catálogo **BUSINESS_ROLE_PROFILE**. Principio: gobierno (madurez/calidad/criticidad/roles) asociado polimórficamente a cualquier nivel.

- **frequency_code genérico** (METADATO-30): `SOURCE_FREQUENCY`→**FREQUENCY** (reutilizado por source y process), actualizado en modelo y seed.

- **D07 patrones de workflow → ORG_STRUCTURE** (METADATO-30): `workflow_pattern`/`workflow_pattern_step` movidas; +`scope_level_code`→**WORKFLOW_SCOPE** {ENTITY,TERM,PROCESS}; catálogos **RUNNER_TYPE** (9 valores) y **WORKFLOW_PURPOSE**. ⚠️ **PROVISIONAL — requiere gran vuelta, NO controlado** (ver pendientes).

- **Rediseño integral del dominio D3 → acelerador DATA_SOURCE** (METADATO-31): 4 términos hijos — **SOURCE_SYSTEM** (system→container, weak dependiente profundidad libre, secreto opaco), **SOURCE_TABLE** (source_entity espejo de canonical_entity + attribute/key/relation, tipo por tecnología vía `data_type`), **SOURCE_INGESTION** (capture 1:1 + capture_attribute nieto sin rol + extraction_filter), **DISCOVERY** (plantillas de autodescubrimiento por tecnología: template→object→[view_column | field_mapping], poblado para SQL Server/PostgreSQL/MySQL/Oracle). Eliminadas conectividad, 9 especializaciones por tipo, satélites API, multi_record, constraint, partition_strategy, source_entity_relation. Enriquecimiento discovery (Opción A) en container/entity/attribute. Sin formato fecha/decimal (tipos se replican origen→Delta; solo VARCHAR usa charset/collation). Pendiente: versionado + diff/drift del re-descubrimiento.

- **Término TECHNOLOGY** (bajo COMMON_STRUCTURE, METADATO-31): technology + data_type + data_type_mapping (esta desde DATA_DOMAIN); generic_data_type permanece en DATA_DOMAIN. technology.category_code→**TECHNOLOGY_CATEGORY** (metadata-first). ISO_CODE (vacío) eliminado.

- **Reorganización de términos** (METADATO-31): ORG_STRUCTURE/BUSINESS_PROCESS/DATA_QUALITY/TRANSFORMATION bajo COMMON_DATA. ORG_STRUCTURE solo business_unit; process/term/workflow_* → BUSINESS_PROCESS. **TRANSFORMATION (todo D4) dividido en 3 hijos por capa**: TRANSFORMATION_DEFINITION, TRANSFORMATION_EXECUTION, TRANSFORMATION_SECURITY. FK físicas (physical_catalog/schema/storage) restauradas.



### Término TRANSFORMATION — capa DEFINICIÓN reescrita (METADATO-32)

De 19 tablas a **4** — `transformation` (cabecera: entidad canónica ← tabla origen, rol PRINCIPAL/ENRICHMENT, orden), `transformation_field` (campos + `is_variant` + `source_expression` + agregación), `transformation_filter` (campo·operador·valor + `filter_stage`), `transformation_variant` (unpivot por eje, cuelga de field). Correlación del enriquecimiento = PK canónica (sin tabla extra). El motor compila INSERT (PRINCIPAL) / MERGE (ENRICHMENT) y expande variantes a UNION ALL. Catálogos +**TRANSFORMATION_ROLE**, +**OPERATOR** (13), −**MAPPING_CONDITION_KIND** (huérfano). Estado tras M-32: 184 entidades / 38 catálogos.



### Modelo de transformaciones por tipologías (METADATO-33) — 189 entidades / 51 catálogos

- **Definición**: `transformation` += `business_process_code`, `is_distinct`; nueva `transformation_join` (→**JOIN_TYPE**); agregación GROUP BY/HAVING **derivada** vía `transformation_field.aggregate_function_code` (→**AGGREGATE_FUNCTION**) + `transformation_filter.filter_stage_code` (→**FILTER_STAGE**). Sin `is_group_by` (redundante).

- **Matching / identidad** (término nuevo **LOAD_CANONICAL**): `match_rule_set`→`match_rule`→`match_rule_condition` (reglas AND dentro, OR entre reglas por `combine_mode`; deterministas=filtro duro, probabilísticas=score con puerta `is_required`+pesos; satélites 1:N por EXISTS/ANY con `row_filter`+vigencia; `canonical_expression` para identidad descompuesta). Identidad por entidad en `canonical_entity_bk_lookup_config` (`identity_mode_code`→**IDENTITY_MODE** {BK_HASH,MDM_SURROGATE,RDM_STANDARD}, `on_miss_code`→**ON_MISS**, `surrogate_strategy_code`→**SURROGATE_STRATEGY**). **`xref`** (traza fuente→maestro, FK compuesta a la ruta completa de `source_entity`, `valid_from`/`valid_to`, unifica reference_translation). **`survivorship_rule`** (→**SURVIVORSHIP_STRATEGY**, marca vs. autogenera). **`match_function_impl`** (implementación de cada función como metadato/seed, →**IMPL_KIND**; UDF norm/jw/metaphone se instalan una vez, resto nativas). Catálogos +COMBINE_MODE, +MATCH_FUNCTION, +RULE_NATURE, +IDENTITY_MODE, +ON_MISS, +MATCH_CARDINALITY, +SURVIVORSHIP_STRATEGY, +SURROGATE_STRATEGY, +IMPL_KIND.

- **Vistas**: catálogo **VIEW_KIND** {CANONICAL, MATCHING}; la vista de match compilada se registra como `canonical_view` (kind MATCHING) + `compiled_ddl`. Compiladores genéricos 100% dirigidos por metadato (código de runner guardado en `runner/`).

- **Ejecución**: **eliminadas `transformation_run` y `transformation_run_step`** → reasignadas a **Observabilidad** (`run` no es metadato de transformación). `compiled_ddl` permanece.

- **Reverts**: rechazados `master_type`/MASTER_TYPE e `identity_owner_entity_code` (circular en business_term; la identidad es per-entidad vía `identity_mode`); `reference_translation` fusionado en `xref`.

- **Transversal D3 (parcial)**: `xref.source_entity_code` como FK compuesta a la ruta completa de `source_entity`; resto de FK a source_entity anotadas para una pasada D3 (no ejecutada).



## Código de runner (plataforma, NO metadato) guardado en el Project

`runner/compile_transformation.py` (compilador de carga), `runner/compile_match_view.py` (compilador de match), `runner/datum_match_udfs.py` (UDF norm/jw/metaphone), `runner/compile_dq_checks.py` (generador de DQ rules por entidad canónica desde el metamodelo, M-35), `runner/observability_emitter.py` (emisor genérico de telemetría run/run_step + dominio, dirigido por runner_capability.emits, M-50/51), `runner/compile_uc_views.py` (UC_VIEW→CREATE VIEW, M-51), `runner/compile_obs_cost_anomaly.py` (proceso de derivación ejemplo, M-51), `runner/README_runner.md`, `runner/README_match_runner.md`, `runner/README_observability_emitter.md`. Regla de oro: cambiar comportamiento = cambiar metadato, no tocar este código.



### Ejecución + saneamiento integral D3 (METADATO-34) — 171 entidades / 66 catálogos

- **Término ORCHESTRATION** (hijo de TRANSFORMATION): ejecución = **Compilación** (al cambiar metadato → `compiled_ddl` con hash de invalidación) + **Orquestación** (el runner ejecuta lo VIGENTE, no compila). Movidas `workflow_pattern`/`_step` (+is_gate, +schedule_override) y `compiled_ddl`; nueva **`runner_capability`** (contrato por RUNNER_TYPE, espejo de match_function_impl). `business_process` += trigger/schedule. Eliminadas `transformation_pipeline`/`_step`/`pipeline_dependency` (resuelto el pendiente M-33). Catálogos QUERY_STATUS/DDL_KIND/WRITE_SEMANTICS/TRIGGER_KIND; sembrados RUNNER_TYPE/WORKFLOW_SCOPE/WORKFLOW_PURPOSE. Vista canónica = AST (concatenación de nodos); serializador universal dirigido por metadato.

- **Fusión de identidad en `canonical_entity`**: += identity_mode/surrogate_strategy/on_miss + ubicación física de la xref (FK compuesta a physical_schema; `<entidad>_xref` en staging.<negocio>). Eliminadas `canonical_entity_bk_lookup_config`, `canonical_entity_bk_alias`, `canonical_entity_business_process`. BK_HASH también lleva xref; satélites INHERITED; match_rule_set = detección (solo MDM).

- **Captura (SOURCE_INGESTION)**: eliminado remanente `source_entity_capture_config`; `source_entity_capture` enriquecida por modo (FULL/INCREMENTAL/CDC/**STREAMING**) + `capture_role_code` en el hijo. Catálogos FULL_RELOAD_STRATEGY, CDC_DELETE_HANDLING, LANDING_FORMAT, CAPTURE_ATTRIBUTE_ROLE, STREAM_MESSAGE_FORMAT, STREAM_START_POSITION.

- **Data contracts → término `SOURCE_CONTRACT`** (UNE 0078, hijo de DATA_SOURCE): SLA tipado (operador+valor+unidad) + breach_action + enganche a DQ (dq_dimension); nueva `source_data_contract_entity` (alcance/esquema). Catálogos CONTRACT_STATUS, SLA_TYPE, SLA_UNIT, BREACH_ACTION, SCHEMA_STABILITY.

- **Discovery = un proceso del orquestador** (BU Gobierno/Arquitectura, término DATA_SOURCE): INGEST catálogo vía `discovery_template*` → TRANSFORM a `source_*`. Eliminadas source_discovery_config/detected_type_domain/runner_discover; a **Observabilidad** run/sampling/profile/rule_evaluation/drift-finding; `discovery_rule` como añadido. DQ de fuentes = **estructural** (sin PK/FK/índice/particionar), derivada + `object_assessment`; índices = `source_key` con key_type (PK/UN/UI).

- **Limpieza D3/D+G+runners**: eliminadas `runner_ingest_managed`/`streaming`, `source_entity_canonical_entity_hint`, `source_attribute_quality_hint`, `golden_source` (fuente autoritativa derivada de transformation.PRINCIPAL + xref.is_golden + survivorship).

- Presentación: las entidades reorganizadas salen de la vista por dominio (domain=''); solo aparecen por acelerador.



### Acelerador DATA_QUALITY — circuito ingesta→calidad cerrado (METADATO-35) — 172 entidades / 72 catálogos

- **Reglas DQ = DERIVADAS del metamodelo, no una tabla de reglas.** 11 tipos: FORMAT (TYD: regex/longitud), STRUCTURE, MANDATORY_SIMPLE/COMPOSITE, REFERENTIAL (MDM/RDM/catálogo), UNIQUENESS, TERM_COMPLETENESS, BUSINESS_RULE, ACCURACY_REFERENCE, FRESHNESS (derivada del contrato SLA), SOURCE_STRUCTURAL. Reporte DAMA-DMBOK + ISO/IEC 25012.

- **`dq_check_type`** (nueva entidad, término DATA_QUALITY, hermana de `runner_capability`; 9 atributos): **dos ejes ortogonales** — ① clasificación (`dq_dimension_code`→DQ_DIMENSION→ISO por **join transitivo por valor**, no FK directo: el mapeo ISO se define una vez por dimensión y los 11 tipos lo heredan) y ② remediación (`on_fail_default_code`→DQ_ON_FAIL + `on_fail_derivation_source` + `default_severity_code`→DQ_SEVERITY). + `execution_phase_code`→DQ_PHASE, `scope_level_code`→WORKFLOW_SCOPE. Se encuentran solo en el registro del incidente. 11 filas seed.

- **Piezas bajo término DATA_QUALITY** (seed `canonical_entity.business_term_code=DATA_QUALITY`, `domain=''`): `dq_check_type`, `dq_dimension_to_iso_characteristic` (puente DAMA↔ISO, solo traduce; 10 filas), `dq_quarantine_policy`, `business_rule`. Materializados **DQ_DIMENSION** (6) e **ISO_CHARACTERISTIC** (7) en reference_value.

- **Remediación autocontenida**: `on_fail` {AUTO_REMEDIATE, REJECT, QUARANTINE, FLAG} derivado del metamodelo (normalización TYD, column_default/generation_expression, survivorship_rule, canonical_entity.on_miss_code, source_data_contract_sla.breach_action_code, business_rule); severidad {INFO, WARNING, ERROR}. **DATUM nunca da error de ejecución** — registra y avisa; estados de runner COMPLETED / COMPLETED_WITH_WARNINGS / COMPLETED_WITH_ERRORS / ERROR; fallo de infraestructura → Observabilidad.

- **Fases + flujo**: catálogo **DQ_PHASE** {PRE_INGEST (RUNNER_INGEST), PRE_WRITE (RUNNER_TRANSFORM, fila), POST_WRITE (RUNNER_DQ, conjunto)}; motor bifásico y agnóstico de canal (misma puerta compilada ligada a la entidad). Capa **STAGING** añadida a `storage_layer` (METADATA, OBSERVABILITY, LANDING, OPERATIONAL, **STAGING**, COMMON, BUSINESS, NEGOCIO). Flujo: fuente→LANDING/OPERATIONAL→**STAGING (temporal, corre calidad)**→COMMON (solo dato validado y veraz). Reglas compiladas al cambiar metadato (M-34); runner ejecuta lo VIGENTE.

- **Catálogos +6** (66→72): DQ_ON_FAIL, DQ_SEVERITY, DQ_PHASE, RULE_KIND, MATURITY_DIMENSION, EXPIRATION_ACTION. Saneadas FK de `business_rule` (severity_code→DQ_SEVERITY, maturity_dimension_code→MATURITY_DIMENSION); añadidas 3 cabeceras `reference_catalog` faltantes (WORKFLOW_SCOPE, RUNNER_TYPE, WORKFLOW_PURPOSE).

- **Generador `runner/compile_dq_checks.py`** (plataforma, no metadato): autogenera todas las DQ rules por entidad canónica desde el metamodelo → **`datum_dq_rules.json`** (1855 checks: 1374 PRE_WRITE / 481 POST_WRITE; agregados por entidad / término (25) / proceso).

- **Visor**: pestaña **«DQ rules»** en `/dashboard/canonico` (3 alcances: entidad / término / proceso) + cajas de catálogo compactas con tooltip de valores en el ER.

- **Reubicación D6→D7/D8**: `dimension` (dimensión analítica, vista sobre MDM/RDM, hermana de `accumulative_fact_dimension`) → **D7**; las 6 definiciones de gobierno de calidad (`data_quality_requirement`, `dq_evaluation_specification`, `dq_assurance_procedure`, `dq_audit_plan`, `dq_certification_criteria`, `dq_implementation_plan`) → **D8** (junto al motor de evaluación genérico). Son DEFINICIONES; la ejecución → Observabilidad (OBS_DQ_*). **D6 queda vacío.**



### Semántica de ejecución del gate PRE_WRITE (METADATO-36) — sin cambios de modelo (172/1121/72)

- El gate **FORMAT + MANDATORY** corre en **PRE_WRITE (RUNNER_TRANSFORM), en STAGING**, como **UDF compilada por columna** desde el metadato (VIGENTE, M-34).

- **Circuito (simple):** (1) ¿`source` null? → obligatoriedad (`canonical_attribute.is_nullable`): default con precedencia atributo→tipo (`column_default`) → **WARNING** y **no se revalida**; sin default → **ERROR/REJECT**. (2) si no null → **`TRY_CAST`**: falla → **FORMAT** (null por cast, sin default); ok → validación **VALIDITY** (regex): `regex_pattern_override` de columna en modo **OVERRIDE** (sustituye al del tipo), o si no la del tipo (`data_type_domain_validation`); WARNING/ERROR por severidad de la regla.

- **Null "de origen" (→default) vs. "por cast fallido" (→FORMAT, sin default)** — el runner distingue cuál.

- **No hay SQL por columna**: validaciones SQL solo a nivel tipo; el SQL de columna/fila, si hiciera falta, es BUSINESS_RULE vía `canonical_entity_constraint` (otro check, fuera del gate).

- **Compuesto**: por campo (cada TYD simple) + validación cruzada del compuesto + MANDATORY_COMPOSITE.

- **Salida UDF/incidente**: valor_origen, valor_destino, reglas con veredicto {PASS,WARNING,ERROR} + acción {CAST,DEFAULT_APPLIED,REJECTED} → Observabilidad (dos ejes de M-35). Autocontenido: nunca error de ejecución.



### Capa analítica D7 cerrada → término ANALYTICS (METADATO-37) — 176 entidades / 80 catálogos
- **Término `ANALYTICS`** (raíz, acelerador METADATA, espejo de DATA_SOURCE) con 4 hijos **FACT / DIMENSION / KPI / DATA_PRODUCT**. Las 7 entidades analíticas pasan de `business_term_code="METADATA"` (placeholder) a su término hoja + `domain=''` (invariante término⟺`domain=''`). **D7 queda vacío como dominio.**
- **Dimensión modelada en firme** (sustituye `analysis_hierarchy_text`): `dimension_attribute` (ejes) + `dimension_level` (jerarquía de drill, self-ref), patrón weak M-26.
- **Medidas modeladas**: `accumulative_fact_measure` (espejo de `transformation_field`, `aggregate_function_code`) + `kpi.fact_measure_code` (FK compuesta) para el KPI BASIC; el DERIVED por `kpi_dependency` + AST.
- **`data_product_dimension`** sustituye `common_dimension_set_text` (juego de dimensiones comunes N:M).
- **8 FK de catálogo D7 → metadata-first** (deuda del modelo 77→69). **8 catálogos nuevos**: TIME_GRAIN, MATERIALIZATION_MODE, KPI_TYPE, SUBJECT_KIND, PUBLICATION_STATUS (CONFIRMADO); UNIT, CERTIFICATION_TIER, PERSPECTIVE (PROPUESTO).
- **Seed `object_type`** (nueva lista): CANONICAL_ENTITY, ACCUMULATIVE_FACT, DIMENSION, KPI, DATA_PRODUCT, DQ_CHECK (enganche `runner_capability`/`compiled_ddl`, M-34/M-35). Censo global de `object_type` = pendiente.

### Capa analítica D7 — dimensiones inferibles, snapshot y auto-observación (METADATO-38..40) — 178 / 1161 / 83
- **Dimensiones inferibles** (M-38): `dimension` += `dimension_kind_code` (DIMENSION_KIND {CLASSIC,SNOWFLAKE}) + `derivation_mode_code` (DERIVATION_MODE {INFERRED,EXPLICIT}); `dimension_level` += `source_entity_code`; `accumulative_fact_dimension` += `dimension_level_code`; `object_type` += REFERENCE_CATALOG/BUSINESS_TERM; `TIME_GRAIN`={HORA,DÍA,MES,AÑO}. Clásica sobre catálogo (estrella) / copo sobre jerarquías, inferidas sin duplicar.
- **Agregación nativa del hecho** (M-38/39): `accumulative_fact_measure` + `accumulative_fact_filter` + `accumulative_fact_join` (espejo de transformation_*, reutiliza AGGREGATE_FUNCTION/OPERATOR/FILTER_STAGE/JOIN_TYPE + AST). No reutiliza la transformación entre-modelos.
- **Snapshot periódico** (M-39): `accumulative_fact` += `fact_kind_code` (FACT_KIND {TRANSACTIONAL, PERIODIC_SNAPSHOT, ACCUMULATING_SNAPSHOT}). PERIODIC_SNAPSHOT inserta filas fechadas → serie temporal/evolución; cadencia por `schedule_cron` del business_process; run→Observabilidad.
- **Auto-observación sembrada** (M-40): siembra de la analítica del propio metamodelo (subject_kind=METAMODEL): 5 dimension + 4 accumulative_fact (PERIODIC_SNAPSHOT) + 9 measure + 8 fact_dimension + 8 kpi + 4 kpi_dependency. Runner → `datum_analitica_snapshot.json`. Páginas demo `/dashboard/analitica` (árbol acelerador→hecho→KPI + detalle) y `/dashboard/cdm` (cuadros de mando).

### Acelerador OBSERVABILITY materializado (METADATO-41) — 311 / 2712 / 92
- **REGISTRADO (0) → ACTIVO (133 entidades)** en 21 términos (raíz + 20 hijos), `domain=''`. Ubicación física: `observability` (process/quality/audit) para lo funcional; nuevo catálogo físico **`system`** + 8 esquemas para Unity Catalog.
- **Bloque 1 — núcleo reasignado (14):** términos EXECUTION (run/run_step, M-33), DISCOVERY_OBSERVATION (5, M-34), DQ_OBSERVATION (6, incl. gate PRE_WRITE `dq_column_incident` de M-36), METAMODEL_SNAPSHOT (1, M-39/40). **+9 catálogos** (EXECUTION_LEVEL, RUN_STATUS, TRIGGER_TYPE, DQ_VERDICT, DQ_ACTION, DQ_INCIDENT_STATUS, DQ_GOVERNANCE_KIND, DRIFT_TYPE, DRIFT_STATUS). i18n de entidad es/en/fr/pt de las 14.
- **Bloque 2 — funcional DATUM A–I (47):** ACCESS_AUDIT (9), PRIVACY_DPO (8, GDPR), INCIDENT_ALERT (7), FINOPS (4), LIFECYCLE_OPS (6), GOVERNANCE_MATURITY (7), GOLDEN_RECORD (3, MDM) + deltas run_term/run_entity + dq_run_failed_records. Elevados de `observability.json` con tipos crudos mapeados a TYD reales, `audit`→`system`, PK único por uuid.
- **Bloque 3 — Unity Catalog (72):** UNITY_CATALOG + 8 hojas (access/billing/compute/lakeflow/query/**information_schema (47)**/data_quality_monitoring/data_classification). Nativas: nombres saneados `uc_*`, PK natural compuesta, catálogo físico `system`.
- **Pendiente:** i18n atributos/entidades bloques 2–3; catalogización de enums STRING; revisión/poda de UC_INFORMATION_SCHEMA; PK compuesta vs. única en A–I; canonical_key/relation reales.

### Ingesta de auditoría UC→observabilidad + retención (METADATO-42) — 311 / 2714 / 93
- **Refina M-41.** UC (Databricks system tables) retiene 365 días; DATUM persiste copia propia que sobrevive. Dos capas: `system.*` = fuente efímera (modelada como `source_system`=databricks_system); las 72 `uc_*` = copia persistente en **`observability.uc`**, `retention_policy_code=AUDIT_7Y`, `is_append_only`. **El catálogo físico `system` que M-41 creó se retira (huérfano tras la reubicación).**
- **Metamodelo:** `canonical_entity` += `retention_policy_code` (→**RETENTION_POLICY** {SOURCE_DEFAULT/OPERATIONAL_90D/OPERATIONAL_1Y/AUDIT_5Y/AUDIT_7Y/PERMANENT}) + `is_append_only`. +1 catálogo, +2 atributos.
- **Carga** (`DATUM_Carga_Observability_UC.json`): source_system databricks_system + 8 containers + 72 source_entity + 72 capture + 72 transformation PRINCIPAL + 2 business_process. **INCREMENTAL por watermark (25 logs de evento) / FULL-SNAPSHOT (47 information_schema)**. Flujo system.* → LANDING → STAGING (DQ) → observability.uc. source_attribute + watermark por DISCOVERY (auto-observado en source_discovery_run).
- **Pendiente:** poblar source_attribute (discovery); capture_attribute WATERMARK; transformation_field si no es SELECT * puro.
- **M-43 (orquestación ejecutable):** sembrados `workflow_pattern` (uc_discovery_pattern, uc_audit_ingest_pattern) + 5 steps (INGEST/DQ_GATE/WRITE) y enganchados los business_process. Discovery-first: la 1ª corrida (uc_discovery) auto-puebla source_attribute/tipos/watermark. Control-plane completo y ejecutable.
- **M-44 (retención de toda la observabilidad):** las 133 con `retention_policy_code` — AUDIT_7Y (92: accesos/GDPR/MDM/UC), AUDIT_5Y (20: DQ/lifecycle/madurez), OPERATIONAL_1Y (21: ejecución/discovery/finops/incidentes/snapshot); `is_append_only` en 122, 11 con estado mutable.
- **M-45 (vista):** retirado el término raíz redundante `OBSERVABILITY`; 2 términos raíz **`DATUM`** (61) y **`UNITY_CATALOG`** (72). Solo business_term.
- **M-46 (vista):** `UC_INFORMATION_SCHEMA` (47) partido en 7 sub-términos especializados (IS_OBJECTS/CONSTRAINTS/PRIVILEGES/TAGS/SECURITY/EXTERNAL/SHARING). Solo business_term; 21→28 términos.
- **M-47 (contrato de población):** cómo se alimenta cada tabla — catálogo POPULATION_MODE + `population_mode_code` (133) + `runner_capability.emits_observability_entity`. La nativa DATUM se EMITE (RUNNER_TELEMETRY 27 / GATE_UDF 1 / DERIVED_SCHEDULED 13 / APP_TRANSACTION 20); UC = SOURCE_INGEST 72. +2 atributos, +1 catálogo.
- **M-48 (dedup vs UC):** las funcionales que duplican UC pasan a **vistas** (POPULATION_MODE +UC_VIEW; `canonical_entity.derived_from_entity`): access_event/access_event_aggregate←uc_access_audit, resource_consumption/cost_aggregate←uc_billing_usage; cost_anomaly/budget_breach leen uc_billing_usage. −4 tablas físicas, sin romper FKs.
- **M-49 (procesos/UDFs):** inventario computado — a construir = **1 UDF (gate) + 9 procesos programados + 4 vistas**; el resto es telemetría de runner (27) o app (20). Definidos los 9 procesos (business_process+pattern+step) en `DATUM_Carga_Observability_Procesos.json` + doc `DATUM_Observabilidad_Procesos_UDFs.md`. Pendiente: lógica de cómputo y SELECT de vistas.
- **M-50 (emisión de telemetría):** RUNNER_TELEMETRY se puebla con un **emisor genérico** del harness (hooks on_run/step_start/end; INSERT al abrir + MERGE al cerrar), dirigido por `runner_capability.emits`. Ni INSERT por runner ni UDF. Componente de plataforma `runner/observability_emitter` + README.
- **M-51 (vertical ejemplo):** implementadas 3 piezas de plataforma end-to-end — `observability_emitter.py` (run/run_step+dominio), `compile_uc_views.py` (access_event y las 4 UC_VIEW), `compile_obs_cost_anomaly.py` (proceso de derivación). Plantilla para replicar el resto.
- **M-52 (carga UC completa):** sembrados 838 `source_attribute` (columnas UC con tipo nativo) + 12 `data_type` Databricks + 838 `transformation_field` 1:1. La carga UC ya no depende de discovery (solo drift) y usa el compilador de transformaciones estándar.
- **M-53 (capa analítica OBS):** capa analítica del acelerador (subject_kind=OBSERVABILITY): +7 dimensiones, 6 hechos (EXECUTION/QUALITY/ACCESS/COST/INCIDENT/INGESTION) con 18 medidas, 14 KPIs (10 básicos + 4 derivados), 5 data products publicados (platform_health, dq_scorecard, access_audit, finops_chargeback, ingestion_monitor). Solo seed analítico.

## Aceleradores incorporados

| Acelerador | Estado | Notas |

|---|---|---|

| Metadato (METADATA) | ACTIVO | el metamodelo mismo; **178 entidades**; capa analítica de auto-observación sembrada (M-40) |

| Calidad (DATA_QUALITY) | ACTIVO | circuito ingesta→calidad cerrado (M-35); motor de reglas derivadas + generador `compile_dq_checks.py` + visor «DQ rules» |

| Observabilidad (OBSERVABILITY) | ACTIVO | **133 entidades** / 28 términos, **2 raíz: DATUM (61) + UNITY_CATALOG (72)** (M-45); information_schema partido en 7 sub-términos (M-46); ejecución (run/run_step) + discovery-obs + DQ-obs + snapshot + funcional DATUM A–I (auditoría/GDPR/incidentes/FinOps/lifecycle/madurez/MDM) + **72 tablas Unity Catalog** (UNITY_CATALOG). Físico `observability` (process/quality/audit + esquema `uc` persistente). UC ingerido desde Databricks `system.*` (fuente 365d, modelada como `source_system`=databricks_system) → `observability.uc` (retención AUDIT_7Y, append-only), ingesta incremental/snapshot (M-42/43) |

| Financiero (FINANCE) | REGISTRADO (0 entidades) | catálogo físico `business` |

| RRHH (HR) | REGISTRADO (0 entidades) | — |

| Legal (LEGAL) | REGISTRADO (0 entidades) | — |

| Marketing (MARKETING) | REGISTRADO (0 entidades) | — |



## Pendientes abiertos

- **⚠️ EJECUCIÓN — decisión pendiente (M-33)**: ¿ejecución = `workflow_pattern`+`workflow_pattern_step` (nuevo, step→RUNNER_TYPE, ya registrado/CONFIRMADO) o `transformation_pipeline`+`_step`+`pipeline_dependency` (viejo, acoplado a canonical_view/MAPPING, aislado)? Recomendación registrada: quedarse con `workflow_pattern`+runners y **retirar `transformation_pipeline*`**. No tocado a la espera de orden de Pedro. Enlaza con el pendiente D07 de patrones/steps.

- **⚠️ D07 PATRONES/STEPS DE WORKFLOW — GRAN REVISIÓN PENDIENTE (sesión propia, NO controlado)**: el modelado actual de `workflow_pattern`/`workflow_pattern_step` es PROVISIONAL. Abierto: (1) patrón = conjunción de escalas entidad+término+proceso; (2) cada runner detalla sus steps enganchando con D3/D4/D6 — componer, no duplicar; (3) enganche runner→dominio (tipo genérico vs. paso concreto vs. solo runner_type).

- **Transversal D3 — FK a `source_entity` como compuesta a ruta completa**: aplicada en `xref` (M-33); pendiente para source_entity_capture_config, source_entity_canonical_entity_hint, source_entity_version, source_discovery_drift, source_discovery_sampling_result, source_relation.reference_source_entity_code.

- **Matching — pendientes anotados**: política de ambigüedad (multi-candidato → REVIEW) anotada, no modelada explícitamente; modelado del satélite de validez temporal para identificadores reasignables; poblar seed de los catálogos nuevos de match; asistente/UX de reglas de match.

- **Geografía — pendientes**: poblar COMMERCIAL y FISCAL; poblar localidades/municipios INE; poblar seed de GEO_LEVEL/BUSINESS_UNIT_KIND/GOVERNANCE_TOPOLOGY/MATURITY_LEVEL/BUSINESS_ROLE_PROFILE; assessment_pattern MATURITY; verificar object_type=BUSINESS_UNIT.

- **unit_of_measure en CUARENTENA**: revisar si debe existir como tabla.

- **Limpieza D3 en seed** (remanente de M-31): 16 filas `seed.canonical_entity` nombradas-solo sin entidad en el modelo (source_connection*, source_entity_database/file/api_endpoint/stream_topic/webhook/excel_workbook, source_api_endpoint_parameter/graphql_query/soap_operation, source_archive_container, source_entity_relation, source_entity_partition_strategy, multi_record). Sanear en una vuelta D3.

- **i18n del término BUSINESS_TERM** (business_term_related: nombres de arco por SHORT; synonym) — pendiente de poblar.

- **Generalizar formato-documento y ficha** al resto de términos y a las 171 entidades; poblar canonical_key/canonical_relation reales.

- **Compilador documento→DDL Databricks** + cargador documento→datos (objetivo mayor: Control Plane cycle). Los compiladores de carga/match (M-33) son la primera pieza materializada.

- **Sanear FK a reference_value sin refcat**: por tandas. Hecho para BUSINESS_TERM (M-28), DATA_TYPE_DOMAIN + parte de D6 (M-29), TRANSFORMATION/MATCHING (M-32/33), `business_rule` (severity→DQ_SEVERITY, maturity→MATURITY_DIMENSION) + 3 cabeceras refcat faltantes (M-35). Pendientes: resto de las definiciones de calidad ahora en D8 (on_expiration_action_code→EXPIRATION_ACTION ya tiene catálogo pero falta enganche, priority_code, frequency_code, certification_level_code→CERT_LEVEL) y el resto de términos.

- **DATA_QUALITY — pendientes (M-35)**: solapamiento de `dq_certification_criteria`/`dq_evaluation_specification` con el motor genérico de evaluación de D8 (`assessment_pattern_threshold`/`object_assessment`) — decidir si las 6 definiciones se apoyan en ese motor o se mantienen específicas; **sembrar los 36 TYD + formatos** en el bootstrap (hoy FORMAT deriva del catálogo de tipos en runtime); sembrar `business_process`/`business_rule` para la DQ por proceso (hoy 0 procesos); `MATURITY_DIMENSION`/`EXPIRATION_ACTION`/`RULE_KIND` con valores PROPUESTO (ajustables); **retirar D6 vacío** del `DOMAIN_ORDER` del visor si no va a albergar nada; acelerador **Observabilidad** que reciba OBS_DQ_* (ejecución de planes/auditorías/certificaciones/incidentes DQ).

- **ANALYTICS — pendientes (M-37)**: confirmar valores **PROPUESTO** de UNIT/CERTIFICATION_TIER/PERSPECTIVE; decidir si UNIT es catálogo o entidad `unit_of_measure` (CUARENTENA); **censo completo de `object_type`** (todas las referencias polimórficas del modelo, hoy sembrado solo lo que D7 usa + DQ_CHECK); i18n de la rama ANALYTICS (términos y entidades nuevas, sin traducir); poblar `canonical_key`/`canonical_relation` reales de las 4 nuevas; `src/data/metamodel.json` (ER por-dominio de la demo) desincronizado desde M-35/36 — regenerar si se quiere mantener esa vista.
- **`rule` reutilizable en Definición**: decidir si se reintroduce un catálogo de funciones cuando el volumen de expresiones repetidas lo justifique.

- **Reorganización del seed en N ficheros por naturaleza** (METADATO-21): posterior al formato-documento.

- **Wizard de edición** de la ficha (botón Editar).

- **PROBLEMA DE INTEGRIDAD conocido**: `physical_schema_code`="metadata" en el seed, pero "metadata" no es esquema válido (reales: d0..d14, storage, process…). Ajuste aplazado por Pedro.

- **Alineación modelo vs. Excel** en `estimated_annual_volume` (Excel: obligatorio; modelo: nullable) — pendiente de decisión.

- Aplicar `on_delete/on_update=RESTRICT` como default del catálogo REFERENTIAL_ACTION.

- i18n de reference_category y tablas nuevas (sin traducir).



## Historial de versiones

- **v1.0 (Julio 2026):** creación del proyecto. Gobierno propio (par 99/18-METADATO), JSON como bootstrap.

- **v1.1 (Julio 2026):** METADATO-3..8. Jerarquía por acelerador (D20 raíz), saneamientos, seed de aceleradores/términos, visualizador por acelerador.

- **v1.2 (Julio 2026):** METADATO-9..15. `TYD_SYSTEM`; `delta_property` (20 propiedades); patrón `DEFAULT`; catálogos de datos; `object_delta_override`; ACCELERATOR→COMMON_STRUCTURE; visualizador alineado.

- **v1.3 (Julio 2026):** METADATO-16..21. Formato-documento canónico universal (piloto DATA_CATALOG); eliminación de `canonical_attribute_constraint`; `is_visible_er` + eliminación de `physical_column_name`; reincorporación de `physical_catalog_code` + relaciones técnicas universales; patrón de visualización maestro-detalle; reorganización del seed en N ficheros (acordado, pendiente).

- **v1.4 (Julio 2026):** METADATO-22..27. Formato-documento jerárquico autocontenido; simplificación del término CANONICAL_ENTITY (11→7 tablas, 194→190 entidades): relaciones (2 tablas, cardinalidad como campo, cat CARDINALITY_REL), particiones (a entity+attribute), constraints (solo CHECK); eliminación de `referenced_entity_code`/`materialization_mode_code`; ajuste al Excel de definición del término (nombres, PK/FK); patrón de entidades dependientes con FK identificativas compuestas; ficha de entidad integrada en el árbol del visualizador.

- **v1.5 (Julio 2026):** METADATO-28. Saneamiento del término BUSINESS_TERM (190→187): eliminación de 3 tablas puente; `business_term_related` como grafo semántico de negocio con cardinalidad (catálogo CARDINALITY reutilizado) y FK alineadas al patrón de `canonical_relation`; FK dependientes identificativas; FK a catálogo metadata-first; corrección de `is_visible_er`. Saneamiento de catálogos (16→10): eliminados 6 huérfanos y renombrado CARDINALITY_REL→CARDINALITY. Solo datos, sin cambios de código en el visualizador.

- **v1.6 (Julio 2026):** METADATO-29. Saneamiento y cierre del término DATA_TYPE_DOMAIN: rename `_simple`→`data_type_domain`; defaults DDL heredables + clasificación metadata-first + formato i18n (DATE_FORMAT/DECIMAL_FORMAT); composite reducido a code+system; field con FK renombradas sin cardinality; eliminación de `data_type_domain_dq_rule` (FK colgante) → `data_type_domain_validation` con dueño polimórfico (sirve a simple y composite); `regex_pattern` consolidado en validación; tipología de validación anclada a DAMA/ISO 25012 (catálogos DQ_DIMENSION, ISO_CHARACTERISTIC) cerrando las FK colgantes de `dq_dimension_to_iso_characteristic`; ui_control en cuarentena (D10). Catálogos 10→14. Solo datos, sin cambios de código en el visualizador. 187 entidades.

- **v1.7 (Julio 2026):** METADATO-30..31. Dimensión GEOGRAPHY (término GEO_STRUCTURE) + refactor ORG_STRUCTURE/GOVERNANCE (madurez/roles al motor de evaluación, polimórfico) + arranque provisional D07 patrones de workflow (187→202); rediseño integral del dominio D3 → acelerador DATA_SOURCE (SOURCE_SYSTEM/SOURCE_TABLE/SOURCE_INGESTION/DISCOVERY) + término TECHNOLOGY + reorganización de términos + TRANSFORMATION dividido en 3 capas (base registrada 187→196). Catálogos 14→25→37.

- **v1.8 (Julio 2026):** METADATO-32. Rediseño de la capa de definición de TRANSFORMATION a 4 tablas (transformation/_field/_filter/_variant); unpivot por variantes colgando de field; correlación por PK canónica; catálogos TRANSFORMATION_ROLE/OPERATOR, eliminado MAPPING_CONDITION_KIND. 196→184 entidades; 37→38 catálogos.

- **v1.9 (Julio 2026):** METADATO-33. Modelo de transformaciones por tipologías: Definición (join, agregación GROUP BY/HAVING derivada), Matching/identidad (nuevo término LOAD_CANONICAL: match_rule_set/rule/condition, xref, survivorship_rule, match_function_impl, config de identidad en bk_lookup_config), vistas (VIEW_KIND, compiladores genéricos), y limpieza de Ejecución (run/run_step → Observabilidad). Reverts: MASTER_TYPE/identity_owner e integración de reference_translation en xref. Código de runner guardado en `runner/`. 184→189 entidades; 38→51 catálogos.



---

- **v1.10 (Julio 2026):** METADATO-34. Término ORCHESTRATION (ejecución = compilación + orquestación; runner_capability; workflow_pattern consolidado, retirado transformation_pipeline*); fusión de identidad en canonical_entity (elimina bk_lookup_config/bk_alias/business_process); captura enriquecida por modo + streaming; data contracts → SOURCE_CONTRACT con SLA tipado; discovery consolidado como proceso del orquestador; limpieza D3/D+G+runners. 189→171 entidades; 51→66 catálogos.

- **v1.11 (Julio 2026):** METADATO-35. Acelerador DATA_QUALITY — circuito ingesta→calidad cerrado: reglas DQ derivadas del metamodelo (11 tipos, DAMA+ISO 25012); `dq_check_type` (dos ejes ortogonales clasificación/remediación + fase); puente `dq_dimension_to_iso_characteristic` y DQ_DIMENSION/ISO_CHARACTERISTIC materializados; remediación autocontenida (on_fail/severity derivados; DATUM nunca da error de ejecución); fases DQ_PHASE + capa STAGING + flujo fuente→LANDING/OPERATIONAL→STAGING→COMMON; generador `compile_dq_checks.py` → `datum_dq_rules.json` (1855 checks); visor pestaña «DQ rules» + cajas de catálogo compactas con tooltip; reubicación de dominios (dimension→D7; 6 definiciones de gobierno→D8; D6 vacío). +6 catálogos (66→72); 171→172 entidades; 1112→1121 atributos. Saneadas FK de business_rule + 3 cabeceras refcat.



- **v1.12 (Julio 2026):** METADATO-36. Semántica de ejecución del gate PRE_WRITE (FORMAT + MANDATORY) como UDF compilada por columna: TRY_CAST (null de origen→default WARNING sin revalidar / null por cast fallido→FORMAT sin default), regex de columna en modo OVERRIDE o del tipo, sin SQL por columna (solo a nivel tipo; columna/fila = BUSINESS_RULE vía canonical_entity_constraint), compuesto en dos niveles, salida = incidente {veredicto, acción} a Observabilidad. Sin cambios de modelo (172/1121/72).



- **v1.13 (Julio 2026):** METADATO-37. Cierre de la capa analítica D7 → término ANALYTICS (raíz) + 4 hijos FACT/DIMENSION/KPI/DATA_PRODUCT; jerarquía de dimensión modelada (dimension_attribute/dimension_level); medidas modeladas (accumulative_fact_measure + kpi.fact_measure_code); data_product_dimension (sustituye common_dimension_set_text); 8 FK de catálogo D7 a metadata-first (deuda 77→69); +8 catálogos (72→80); seed object_type (KPI/DQ_CHECK + valores D7). 172→176 entidades; 1121→1142 atributos. D7 vacío como dominio. Sin registro en Project hasta canonización.

- **v1.14 (Julio 2026):** METADATO-38. Dimensiones inferibles estrella/copo (DIMENSION_KIND/DERIVATION_MODE, object_type +REFERENCE_CATALOG/BUSINESS_TERM, dimension_level.source_entity_code, accumulative_fact_dimension.dimension_level_code, TIME_GRAIN a 4) + agregación nativa del hecho (accumulative_fact_filter/_join). 176→178 entidades; +2 catálogos.
- **v1.15 (Julio 2026):** METADATO-39. Hechos snapshot periódico: accumulative_fact.fact_kind_code + FACT_KIND; evolución temporal de KPIs vía inserción de filas fechadas; cadencia por schedule_cron. 178/1161/83.
- **v1.16 (Julio 2026):** METADATO-40. Auto-observación del metamodelo: siembra de la capa analítica (subject_kind=METAMODEL; 5 dim/4 hechos/9 medidas/8 kpi/…), runner de snapshot (datum_analitica_snapshot.json) y páginas demo Analítica (árbol acelerador→hecho→KPI) y CdM. Sin cambios de modelo.

- **v1.17 (Julio 2026):** METADATO-41. Materialización del acelerador **OBSERVABILITY** (REGISTRADO 0 → ACTIVO 133 entidades / 21 términos) en 3 bloques: núcleo reasignado M-33..40 (14, +9 catálogos), funcional DATUM A–I (47), Unity Catalog nativo (72, +catálogo físico `system`). 178→311 entidades; 1161→2712 atributos; 83→92 catálogos.

- **v1.18 (Julio 2026):** METADATO-42. Ingesta de auditoría UC→observabilidad + retención (refina M-41): `canonical_entity` += retention_policy_code/is_append_only + catálogo RETENTION_POLICY; las 72 uc_* reubicadas a `observability.uc` (AUDIT_7Y, append-only); carga de ingesta `DATUM_Carga_Observability_UC.json` (system.* → observability.uc, incremental/snapshot, source_attribute+watermark por discovery). 2712→2714 atributos; 92→93 catálogos.\n\n- **v1.19 (Julio 2026):** METADATO-43. Orquestación de la ingesta UC lista para ejecutar (discovery-first): +2 workflow_pattern +5 steps enganchados a los business_process, en DATUM_Carga_Observability_UC.json. Sin cambios de modelo (311/2714/93). La 1ª corrida de discovery auto-puebla source_attribute/tipos/watermark.

- **v1.20 (Julio 2026):** METADATO-44. Política de retención de las 133 entidades OBSERVABILITY (AUDIT_7Y 92 / AUDIT_5Y 20 / OPERATIONAL_1Y 21; is_append_only 122, 11 mutables). Solo seed; sin cambios de modelo (311/2714/93).

- **v1.21 (Julio 2026):** METADATO-45. Vista por acelerador de OBSERVABILITY: retirado el término raíz redundante OBSERVABILITY; 2 raíz DATUM (61) + UNITY_CATALOG (72). Solo business_term; sin cambios de modelo (311/2714/93).

- **v1.22 (Julio 2026):** METADATO-46. UC_INFORMATION_SCHEMA (47 tablas) partido en 7 sub-términos especializados (IS_OBJECTS 11 / IS_CONSTRAINTS 6 / IS_PRIVILEGES 11 / IS_TAGS 5 / IS_SECURITY 2 / IS_EXTERNAL 4 / IS_SHARING 8). Solo business_term; 21→28 términos OBSERVABILITY; sin cambios de modelo (311/2714/93).

- **v1.23 (Julio 2026):** METADATO-47. Contrato de población de la observabilidad: catálogo POPULATION_MODE + canonical_entity.population_mode_code (clasificadas las 133) + runner_capability.emits_observability_entity. La observabilidad nativa se emite (telemetría), no se ingiere. 2714→2716 atributos; 93→94 catálogos.

- **v1.24 (Julio 2026):** METADATO-48. Dedup de observabilidad vs UC: access_event/access_event_aggregate/resource_consumption/cost_aggregate → vistas sobre uc_* (POPULATION_MODE +UC_VIEW, canonical_entity +derived_from_entity); cost_anomaly/budget_breach leen uc_billing_usage. −4 tablas físicas. 2716→2717 atributos.

- **v1.25 (Julio 2026):** METADATO-49. Inventario de procesos/UDFs de observabilidad (1 UDF gate + 9 procesos + 4 vistas; resto telemetría/app) y definición de los 9 procesos (business_process+pattern+step) en DATUM_Carga_Observability_Procesos.json. Doc de referencia. Sin cambios de modelo (311/2717/94).

- **v1.26 (Julio 2026):** METADATO-50. Mecanismo de emisión de telemetría de runner: emisor genérico del harness (hooks de ciclo de vida, INSERT+MERGE, dirigido por runner_capability.emits), no INSERT por runner ni UDF. Componente de plataforma runner/observability_emitter + README. Sin cambios de modelo (311/2717/94).

- **v1.27 (Julio 2026):** METADATO-51. Vertical de ejemplo end-to-end (código de plataforma en runner/): observability_emitter.py (telemetría run/run_step+dominio), compile_uc_views.py (access_event + las 4 UC_VIEW), compile_obs_cost_anomaly.py (proceso de derivación). Sin cambios de modelo (311/2717/94).

- **v1.28 (Julio 2026):** METADATO-52. Columnas UC pre-sembradas (838 source_attribute + 12 data_type Databricks) + mapeo 1:1 (838 transformation_field) en DATUM_Carga_Observability_UC.json. La carga UC deja de depender de discovery (solo drift) y usa compile_transformation.py estándar. Sin cambios de modelo (311/2717/94).

- **v1.29 (Julio 2026):** METADATO-53. Capa analítica del acelerador OBSERVABILITY (subject_kind=OBSERVABILITY): +7 dimensiones, 6 hechos PERIODIC_SNAPSHOT, 14 KPIs (10 básicos+4 derivados), 5 data products publicados. Solo seed analítico; sin cambios de modelo (311/2717/94).

- **v1.30 (Julio 2026):** METADATO-54. Poda del gobierno de calidad (planes DQ) y consolidación del motor de evaluación: eliminadas 8 entidades (6 definiciones DQ + `dq_governance_execution` + `maturity_assessment_execution`); reglas DQ derivadas (M-35), certificación = `assessment_pattern` de tipo DQ, auditoría = cadencia + evidencia; **acto único** `object_assessment` (+`_answer`) reasignado a OBSERVABILITY/GOVERNANCE_MATURITY (`observability.audit`), absorbe el acto DAMA-CMMI; `assessment_pattern` +framework_code/+dimension_code; `object_assessment` +target_level_code/+assessor_ref/+evidence_ref. Catálogos −DQ_GOVERNANCE_KIND +MATURITY_FRAMEWORK {DAMA,CMMI} +DATA_CRITICALITY {LOW,MEDIUM,HIGH,CRITICAL}. Definición del motor sacada del genérico METADATA a término propio **ASSESSMENT_ENGINE** (bajo GOVERNANCE). 311→303 entidades; 2717→2675 atributos; 94→98 catálogos; 2717→2677 atributos; entity_count METADATA 178→170.

- **v1.31 (Julio 2026):** METADATO-55. Reorganización de 3 dominios residuales a la vista por acelerador (METADATA), 22 entidades → 12 términos nuevos + **23 catálogos generados y cableados** para las FK bare de esas entidades (98→121), sin cambios de entidades/atributos (303/2677): **D14** (Documentación gobernada) → `GOVERNANCE`→**DOCUMENTATION**; **D10** → término padre **UX** (hijos UX_SCREENS/UX_GENERATIVE/UX_PERMISSIONS/UX_BRANDING/UX_SUPPORT); **D9** → término padre **EXPOSURE** (hijos EXPOSURE_CORE/EXPOSURE_MECHANISM/EXPOSURE_MARKETPLACE/EXPOSURE_COMPLIANCE). Dominios D14/D10/D9 vaciados de la vista por dominio; solo business_term + presentación. FK intactas.

- **v1.32 (Julio 2026):** METADATO-56. Modelo de seguridad de acceso → término **`SECURITY`** (raíz/METADATA, hijos RBAC/ABAC/CONSENT). Doctrina: IdM=identidad, metamodelo=política de autorización sobre el dato, UC=enforcement; acceso baseline por rol+scope se **deriva** del grafo (no se modela). 2 modos (IdM-autoritativo / DATUM-gestionado). Fusión `data_access_grant`+`_approval`+`data_sharing_request` → **`data_access_request`** (consentimiento del owner: propósito→processing_purpose, vigencia, recertificación, +REVOKED); `data_access_grant_condition`→`data_access_request_condition`; poda de `effective_permission_cache`. 303→300 entidades; 2677→2666 atributos; APPROVAL_STATUS +REVOKED; entity_count METADATA 170→167.

- **v1.33 (Julio 2026):** METADATO-57. **Cierre de D8** (dominio vaciado): las 7 entidades residuales reubicadas. Término **`GDPR_DPO`** (hijo de GOVERNANCE, regulatorio RGPD): `legal_basis`, `processing_purpose` (bases legales), `processing_activity_record` (ROPA). Término **`DATA_AGREEMENTS`** (hijo de GOVERNANCE, provisional — pendiente si va a EXPOSURE): `data_processing_agreement`, `data_sharing_agreement`, `international_data_transfer` (cesiones y encargos). `incident_type_definition` → **catálogo `INCIDENT_TYPE`** (entidad eliminada; severity/workflow → observabilidad). 300→299 entidades; 121→124 catálogos (+INCIDENT_TYPE, +SCOPE_KIND, +SAFEGUARD, +seed BUSINESS_ROLE_PROFILE; saneo de bare del bloque); entity_count METADATA 167→166.

- **v1.34 (Julio 2026):** METADATO-58. Eliminado el dominio **D5** completo (`lineage_view_definition`, `impact_analysis` — vistas de linaje/impacto declarativas; 0 FK entrantes). 299→297 entidades; 2649 atributos; entity_count METADATA 166→164.

- **v1.35 (Julio 2026):** METADATO-59. Poda de `discovery_rule` (+`discovery_rule_evaluation`): las fuentes NO se acomodan a dominios de common data; discovery = estructura+drift, sin clasificación semántica. Retención **unificada** (opción a): `lifecycle_policy` pasa a ser la definición paramétrica de los tiers (retención/archivar/purgar/aprobación); `canonical_entity.retention_policy_code`→FK `lifecycle_policy`; catálogo `RETENTION_POLICY` **retirado**; `lifecycle_policy`+`lifecycle_phase_approval_rule` → nuevo término **`LIFECYCLE`** (bajo GOVERNANCE). 297→295 entidades; 124→123 catálogos; entity_count METADATA 164→163 / OBSERVABILITY 133→132.

- **v1.36 (Julio 2026):** METADATO-60. **Saneo integral de catálogos**: auditado TODO el modelo → 21 atributos `*_code` bare + 9 referencias a catálogo inexistente. Generados 17 catálogos faltantes (GEO_LEVEL, CARDINALITY, BUSINESS_UNIT_KIND, GOVERNANCE_TOPOLOGY, DATE_FORMAT, DECIMAL_FORMAT, CHANGE_KIND, DATA_LAYER, UI_CONTEXT, ENCRYPTION_ALGORITHM, EXPRESSION_TYPE, NODE_KIND, OPERAND_KIND, LOGICAL_TYPE, LIFECYCLE_PHASE, MASKING_METHOD, VERSION_STATUS), reutilizados los existentes (APPROVAL_STATUS, OPERATOR, UI_CONTROL, BUSINESS_ROLE_PROFILE, WRITE_SEMANTICS), y `object_approval.approver_role_code`→FK `governance_role`. Todos cableados metadata-first. **Resultado: 0 bare, 0 catálogo inexistente, 0 FK colgantes en todo el modelo.** Catálogos 123→134; sin cambios de entidades/atributos (295/2636).

- **v1.37 (Julio 2026):** METADATO-61 (a+c). **Consolidación del versionado (a):** los 4 SCD2 dispersos (`canonical_attribute_version`, `canonical_entity_version`, `source_attribute_version`, `source_entity_version`) → un único **`object_version`** polimórfico (`object_row_uuid` + `object_type_code` + `version_number`); `source_discovery_drift.accepted_into_version_code` repuntado a `object_version`; `object_version`+`object_approval` → nuevo término **VERSIONING** (bajo GOVERNANCE). `VERSION_STATUS` **no** se fusiona con `PUBLICATION_STATUS` (opción b = no). **Recategorización de catálogos (c):** los 134 catálogos clasificados en **9 categorías funcionales** {KIND 71, MODE 17, STATUS 10, LEVEL 10, ACTION 7, FORMAT 5, DIMENSION 5, TIME 5, ROLE 4}; propagado al bootstrap: `categories[]` reescrito **y** seed `reference_category` 6→9 + 133 `reference_catalog.category_code` remapeados (antes 116 en `TYPE`). Entidades 295→291; atributos 2636→2608; METADATA 163→159, OBSERVABILITY 132 sin cambio. Catálogos 134 (sin cambio de recuento). **0 FK colgantes.** Registro oficial + visualizador.

*Fin de `99-METADATO-control.md` v1.37.*

