# 99 · Control de sincronización — Proyecto «DATUM metadato»

**Versión:** v1.5 — Julio 2026
**Propósito:** estado consolidado del metamodelo DATUM y de los aceleradores/modelos cargables. Los JSON son bootstrap del Control Plane.

## Regla de oro
La fuente de verdad es el **documento en disco**, no este registro. Nada se canoniza sin "registro oficial" del founder. Ficheros completos, nunca parches.

## Estado consolidado (tras METADATO-16..28, v1.5)
- Metamodelo: **187 entidades**. Fuente: `DATUM_Modelo_Datos_Metadato.json`. (194→190 por la simplificación del término CANONICAL_ENTITY — METADATO-23; 190→187 por el saneamiento del término BUSINESS_TERM — METADATO-28.)
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

## Aceleradores incorporados
| Acelerador | Estado | Notas |
|---|---|---|
| Metadato (METADATA) | ACTIVO | el metamodelo mismo; 187 entidades |
| Observabilidad (OBSERVABILITY) | REGISTRADO (0 entidades) | catálogo físico `observability` |
| Financiero (FINANCE) | REGISTRADO (0 entidades) | catálogo físico `business` |
| RRHH (HR) | REGISTRADO (0 entidades) | — |
| Legal (LEGAL) | REGISTRADO (0 entidades) | — |
| Marketing (MARKETING) | REGISTRADO (0 entidades) | — |

## Pendientes abiertos
- **i18n del término BUSINESS_TERM** (business_term_related: nombres de arco por SHORT; synonym) — pendiente de poblar.
- **Generalizar formato-documento y ficha** al resto de términos y a las 187 entidades (término a término); poblar canonical_key/canonical_relation reales para que la ficha muestre UN/IX y relaciones nombradas.
- **Compilador documento→DDL Databricks** + cargador documento→datos (objetivo mayor: Control Plane cycle).
- **Sanear FK a reference_value sin refcat**: por tandas, acopladas a cada término/acelerador (contrato: fk_target=reference_value + reference_catalog=<CAT> + catalog_ref_metadata_only=true).
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

---
*Fin de `99-METADATO-control.md` v1.5.*
