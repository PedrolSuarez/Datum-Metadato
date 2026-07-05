# 99 · Control de sincronización — Proyecto «DATUM metadato»

**Versión:** v1.3 — Julio 2026
**Propósito:** estado consolidado del metamodelo DATUM y de los aceleradores/modelos cargables. Los JSON son bootstrap del Control Plane.

## Regla de oro
La fuente de verdad es el **documento en disco**, no este registro. Nada se canoniza sin "registro oficial" del founder. Ficheros completos, nunca parches.

## Estado consolidado (tras METADATO-16..21, v1.3)
- Metamodelo: **194 entidades**. Fuente: `DATUM_Modelo_Datos_Metadato.json`. (Eliminada `canonical_attribute_constraint` — METADATO-17.)
- **Campo técnico universal `system` (TYD_SYSTEM)** en todas las entidades: encapsula ancla i18n (`row_uuid`), ciclo de vida (`lifecycle_state_code` → LIFECYCLE_STATE) y auditoría. No visible en ER; visible en entidad física.
- **Formato-documento canónico universal** definido (METADATO-16): representación exacta de una entidad canónica (cabecera `entity_metadata` con valores reales del seed + arrays `attributes`/`keys`/`relations`/`constraints`/`partitions`). Se deriva del modelo. Piloto validado: término **DATA_CATALOG** (reference_category, reference_catalog, reference_value). El visualizador se ajusta a estos JSON.
- **`canonical_attribute`** (16 campos): añadido `is_visible_er` (visibilidad ER movida al metamodelo); eliminado `physical_column_name` (es el propio `code`). Constraints por atributo → van por TYD; constraints de negocio → solo a nivel entidad.
- **`canonical_entity`** (11 campos): reincorporado `physical_catalog_code` (FK a physical_catalog). FK universales de toda entidad: término (business_term_code), patrón Delta (config_pattern_code), ubicación física (physical_catalog_code + physical_schema_code, FK compuesta). Todas `is_visible_er:false` en el documento.
- **Configuración Delta**: `delta_property` con 20 propiedades; patrón `DEFAULT` obligatorio. **Catálogos de datos**: `reference_catalog` con FK obligatoria a acelerador; catálogo `STANDARD_AUTHORITY`. `external_authority_code` saneado a metadata-first.
- **Patrón de visualización maestro-detalle** (METADATO-20): UX auto-generada, solo presentación del documento, sin lógica. Cabecera + bloque i18n + pestañas (Atributos/Keys/Relations/Constraints/Partitions) + Editar (wizard pendiente). i18n gestionado desde el multiidioma general (object_text, SHORT/SUMMARY/FUNCTIONAL × es/en/fr/pt); cada rótulo de la UX se resuelve por i18n (por SHORT).

## Aceleradores incorporados
| Acelerador | Estado | Notas |
|---|---|---|
| Metadato (METADATA) | ACTIVO | el metamodelo mismo; 194 entidades |
| Observabilidad (OBSERVABILITY) | REGISTRADO (0 entidades) | catálogo físico `observability` |
| Financiero (FINANCE) | REGISTRADO (0 entidades) | catálogo físico `business` |
| RRHH (HR) | REGISTRADO (0 entidades) | — |
| Legal (LEGAL) | REGISTRADO (0 entidades) | — |
| Marketing (MARKETING) | REGISTRADO (0 entidades) | — |

## Pendientes abiertos
- **Cerrar formato-documento**: incluir en `relations` las relaciones universales a business_term y config_pattern (no solo physical_schema), todas no visibles ER. Quedó aplicada solo la física en el documento entregado.
- **Generalizar el formato-documento** al resto de términos (término a término, saneando FK en cada tanda). DATA_CATALOG es la plantilla validada.
- **Sanear las 168 FK a reference_value sin refcat**: por tandas, acopladas a cada término/acelerador (contrato: fk_target=reference_value + reference_catalog=<CAT> + catalog_ref_metadata_only=true).
- **UX maestro-detalle**: llevar el mockup a página real Next.js `/dashboard/entidad/[code]`; construir wizard de edición (objetivo mayor aparte).
- **Reorganización del seed en N ficheros por naturaleza** (METADATO-21): posterior al formato-documento.
- **PROBLEMA DE INTEGRIDAD conocido**: `physical_schema_code`="metadata" en el seed, pero "metadata" no es esquema válido (reales: d0..d14, storage, process…). Ajuste aplazado por Pedro.
- Representación en ER de la FK a `LIFECYCLE_STATE` (encapsulada en TYD_SYSTEM).
- i18n de reference_category y tablas nuevas (sin traducir).
- `system` en la visualización: incorporarlo cuando se disponga del tipo de dato.
- Traducción de valores por fuente (sustituto de external_code); catálogos de valores enumerados de delta_property (2ª pasada); matriz config_pattern_delta_default; poblar business_term_canonical_entity con is_primary; `_meta.total_entities` vs. real.

## Historial de versiones
- **v1.0 (Julio 2026):** creación del proyecto. Gobierno propio (par 99/18-METADATO), JSON como bootstrap.
- **v1.1 (Julio 2026):** METADATO-3..8. Jerarquía por acelerador (D20 raíz), saneamientos, seed de aceleradores/términos, visualizador por acelerador.
- **v1.2 (Julio 2026):** METADATO-9..15. `TYD_SYSTEM`; `delta_property` (20 propiedades); patrón `DEFAULT`; catálogos de datos; `object_delta_override`; ACCELERATOR→COMMON_STRUCTURE; visualizador alineado.
- **v1.3 (Julio 2026):** METADATO-16..21. Formato-documento canónico universal (piloto DATA_CATALOG); eliminación de `canonical_attribute_constraint`; `is_visible_er` + eliminación de `physical_column_name`; reincorporación de `physical_catalog_code` + relaciones técnicas universales; patrón de visualización maestro-detalle; reorganización del seed en N ficheros (acordado, pendiente).

---
*Fin de `99-METADATO-control.md` v1.3.*
