# Índice · Ficheros a incluir en el proyecto «DATUM metadato»

## A. Gobierno (control) — se canonizan en el Project
- `99-METADATO-control.md` — estado consolidado (v1.0)
- `18-METADATO-decisiones.md` — decisiones METADATO-n (v1.0)
- `MASTER_arranque_DATUM_metadato.md` — arranque, principio rector, protocolo

## B. Metamodelo — CONTEXTO + BOOTSTRAP (doble naturaleza)
| Fichero | Rol | Bootstrap CP |
|---|---|:--:|
| `DATUM_Modelo_Datos_Metadato.json` | estructura (194 entidades) | define esquema |
| `DATUM_Modelo_Datos_Metadato.md` | versión legible/visualizable | no |
| `DATUM_Catalogos.json` | catálogos de valores (incl. RECORD_STATUS) | **SÍ (1º)** |
| `DATUM_Carga_Inicial_Metadato.json` | seed de ubicación física + autorregistro | **SÍ (2º)** |
| `DATUM_i18n_D2.json` | traducciones (solo D2 por ahora) | no |

## C. Visualización
- `DATUM_entregable_pagina_canonica.zip` — página «Modelo canónico» (Next.js) para ver todo lo que se incluya. Apuntar sus `/public/*.json` a los ficheros de B.

## D. Aceleradores (se irán añadiendo)
- `PLANTILLA_acelerador.md` — cómo definir cada modelo cargable
- (futuro) `ACC_observability.json`, `ACC_finance.json`, `ACC_rrhh.json`… cada uno con: entidades, ubicación física, carga inicial, i18n.

## Orden de carga (bootstrap Control Plane)
1. `DATUM_Catalogos.json`
2. `DATUM_Carga_Inicial_Metadato.json` (physical_catalog → physical_schema → storage_layer → storage_location → canonical_entity)
3. Bloques de carga de cada acelerador activo.
