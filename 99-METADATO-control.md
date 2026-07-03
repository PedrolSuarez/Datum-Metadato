# 99 · Control de sincronización — Proyecto «DATUM metadato»

**Versión:** v1.0 — Julio 2026
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
| Metadato (base) | ACTIVO | modelo + catálogos + carga inicial | el metamodelo mismo |
| Observabilidad | PENDIENTE | — | catálogo físico `observability` ya previsto |
| Financiero | PENDIENTE | — | catálogo físico `business` |
| RRHH | PENDIENTE | — | — |

## Historial de versiones
- **v1.0 (Julio 2026):** creación del proyecto «DATUM metadato». Hereda el estado del metamodelo tras DATUM-108 (DATUM-Producto). Establece gobierno propio (par 99/18-METADATO) y el rol de bootstrap del Control Plane de los JSON.

---
*Fin de `99-METADATO-control.md` v1.0.*
