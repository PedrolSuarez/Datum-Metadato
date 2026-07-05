# 99 · Control de sincronización — Proyecto «DATUM metadato»

**Versión:** v1.2 — Julio 2026
**Propósito:** estado consolidado del metamodelo DATUM y de los aceleradores/modelos cargables. Los JSON son bootstrap del Control Plane.

## Regla de oro
La fuente de verdad es el **documento en disco**, no este registro. Nada se canoniza sin "registro oficial" del founder. Ficheros completos, nunca parches.

## Estado inicial (heredado de DATUM-Producto, decisión DATUM-108)
- Metamodelo: **194 entidades** (D0–D14). Fuente: `DATUM_Modelo_Datos_Metadato.json` (+ `.md`).
- Submodelo de ubicación física **D00** operativo (storage_layer, storage_location, physical_catalog, physical_schema).
- **6 catálogos físicos**: databricks(managed→storage), metadato(→d0..d14), observability(process/quality/audit), source(fuente_database), commondata(rdm/mdm/dpo), business(fact/dataproduct/dataset/dimension).
- Catálogos de valores en `DATUM_Catalogos.json` (incl. RECORD_STATUS).
- Carga inicial (bootstrap) en `DATUM_Carga_Inicial_Metadato.json`: storage_layer 7, storage_location 12, physical_catalog 6, physical_schema 24, canonical_entity 194.
- i18n: `DATUM_i18n_D2.json` cubre **solo D2 (236 objetos)**; D00, subdominios nuevos y catálogos físicos SIN traducir.
- En cuarentena: `reference_category`, `metamodel_domain` (pendiente decidir colapso).

## Aceleradores incorporados
| Acelerador | Estado | Ficheros | Notas |
|---|---|---|---|
| Metadato (METADATA) | ACTIVO | modelo + catálogos + carga inicial | el metamodelo mismo; 193 entidades |
| Observabilidad (OBSERVABILITY) | REGISTRADO (0 entidades) | seed acelerador | catálogo físico `observability` previsto |
| Financiero (FINANCE) | REGISTRADO (0 entidades) | seed acelerador | catálogo físico `business` |
| RRHH (HR) | REGISTRADO (0 entidades) | seed acelerador | — |
| Legal (LEGAL) | REGISTRADO (0 entidades) | seed acelerador | — |
| Marketing (MARKETING) | REGISTRADO (0 entidades) | seed acelerador | — |

## Estado tras METADATO-3..8 (v1.1)
- Jerarquía **acelerador → término → entidad canónica** operativa. Raíz en D20; `canonical_accelerator` reubicado a D2/D20.
- Modelo: 194 entidades. 8 entidades (D00 físico + D05 config) reclasificadas a términos (DATABRICKS→CATALOG/DELTA_CONFIG), con `domain`/`subdomain` vacíos. Vista por dominio: D0 23, D00 0, D05 0.
- `business_term`: FK obligatoria a acelerador; sin `owner_business_domain_code`; `status_code` metadata-first. `canonical_entity` sin FK directa a acelerador (adscripción transitiva vía término).
- Seed ampliado: 6 aceleradores (v1.0.0, ACTIVE) + 13 términos (12 base + DATABRICKS) del acelerador METADATA.
- Visualizador: conmutador Por acelerador / Por dominio.

## Estado tras METADATO-9..16 (v1.2)
- **Modelo: 193 entidades** (eliminada `metamodel_domain`, huérfana; retirado `reference_category.metamodel_domain_code`). `_meta.total_entities` a sanear (declara 195).
- **Estado unificado en `LIFECYCLE_STATE`** (metadata-first, 5 valores DRAFT/IN_DEFINITION/ACTIVE/DEPRECATED/RETIRED); eliminado `RECORD_STATUS`; `status_code`→`lifecycle_state_code` (31 atributos). Seed en ACTIVE.
- **Catálogos de valores vigentes**: SOURCE_FREQUENCY, LIFECYCLE_STATE, ASSESSMENT_TYPE, MAPPING_CONDITION_KIND, CARDINALITY.
- `display_order` en `canonical_accelerator` y `business_term` (orden estable del árbol).
- **Jerarquía de términos (METADATA)** — raíces y orden: DATABRICKS 10 (CATALOG, DELTA_CONFIG), COMMON_STRUCTURE 15 (DATA_CATALOG, DATA_DOMAIN, I18N, ISO_CODE), COMMON_DATA 16 (ACCELERATOR, BUSINESS_TERM, CANONICAL_ENTITY), HIERARCHY 17 (GEO_STRUCTURE, ORG_STRUCTURE, TEMPORAL_STRUCTURE), BUSINESS_PROCESS 20, DATA_QUALITY 60, DATA_SOURCE 70, GOVERNANCE 80, TRANSFORMATION 110.
- **Visualizador**: code en árbol, bolas de estado (5 colores), tema claro/oscuro, iconos Tabler.
- **ER por término** operativo con principios conceptuales (METADATO-14): FK como relaciones (no columnas), técnicos y ubicación física ocultos, dependiente vs no-dependiente, cardinalidad 1:N/0:N, notación pata de gallo, cajas propia/externa/catálogo. Término **CATALOG** cerrado como referencia (METADATO-16).

## Pendientes abiertos
- `_meta.total_entities` del modelo declara 195 vs. **193 reales**; sanear.
- **lifecycle_state**: hacerlo obligatorio y universal (falta en `storage_layer`; opcional en `storage_location`); valorar incorporarlo por construcción vía `TYD_AUDIT`.
- Poblar `business_term_canonical_entity` con la entidad principal (`is_primary`) de cada término (hoy vacío → ER usa fallback).
- **BK vs PK**: introducir la distinción clave de negocio / clave técnica (hoy todo es PK).
- Valorar marcar la FK de ubicación física con flag explícito en el atributo (hoy se oculta por nombre en el ER).
- Mostrar valores dentro de las cajas de catálogo del ER (hoy solo el nombre).
- `business_term.owner_business_domain_code` eliminado; si se requiere dominio propietario, definir tabla `business_domain` (no existe).
- GEO_STRUCTURE y TEMPORAL_STRUCTURE sin entidades; resto de aceleradores sin entidades.
- i18n de términos, aceleradores, D00 e ISO_CODE sin traducir.

## Historial de versiones
- **v1.0 (Julio 2026):** creación del proyecto «DATUM metadato». Hereda el estado del metamodelo tras DATUM-108 (DATUM-Producto). Establece gobierno propio (par 99/18-METADATO) y el rol de bootstrap del Control Plane de los JSON.
- **v1.1 (Julio 2026):** decisiones METADATO-3..8. Jerarquía por acelerador (D20 raíz), saneamiento de `canonical_accelerator` y `business_term`, seed de 6 aceleradores + 13 términos, reclasificación de D00/D05 a términos, visualizador por acelerador.
- **v1.2 (Julio 2026):** decisiones METADATO-9..16. Saneamiento a 193 entidades, estado unificado LIFECYCLE_STATE, `display_order`, reestructuración de términos (COMMON_STRUCTURE/COMMON_DATA/HIERARCHY), ER por término y **principios de modelado del ER conceptual** (FK como relaciones, dependencia/cardinalidad, ocultación de técnicos y ubicación física), término CATALOG cerrado.

---
*Fin de `99-METADATO-control.md` v1.2.*
