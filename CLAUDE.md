# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Naturaleza del repositorio

No es un proyecto de código: no hay `build`, `lint` ni `tests`. Es el hogar único del **metamodelo DATUM** (~194 entidades, D0–D14) y de los **aceleradores** (modelos cargables: observabilidad, finance, rrhh…). Los ficheros JSON tienen **doble naturaleza**: son la fuente de definición y también los **artefactos ejecutables de bootstrap del Control Plane** de DATUM.

Idioma de trabajo: **español**. Toda la doctrina, control y decisiones están en español; respetarlo en comunicación y en cualquier contenido nuevo.

## Principio rector (absoluto, heredado)

- **El disco es la única fuente de verdad.** Antes de proponer o modificar cualquier cosa, leer el estado real desde disco. Nunca inventar nombres de tabla/campo — verificar en el JSON del modelo.
- **Ficheros siempre completos, nunca parches.** Las entregas se hacen sustituyendo el fichero entero.
- **Nada se registra oficialmente** hasta que el founder ordene explícitamente "registro oficial". Hasta entonces, todo es propuesta.
- **Una sesión = un objetivo.**
- El metamodelo es un sistema integrado por FK: antes de tocar una entidad, cargar el mapa completo y verificar dependencias.

## Protocolo de arranque de sesión

Leer, en este orden, para confirmar estado antes de proponer nada:
1. `MASTER_arranque_DATUM_metadato.md` — propósito, principio rector, protocolo.
2. `99-METADATO-control.md` — estado consolidado actual (versión, aceleradores, cuarentena, i18n).
3. `18-METADATO-decisiones.md` — decisiones METADATO-n vigentes.
4. `HERENCIA_DATUM_Producto.md` — decisiones DATUM-n heredadas que definen el metamodelo.
5. `INDICE_ficheros_proyecto.md` — mapa de ficheros y su rol.

## Orden de carga (bootstrap del Control Plane)

Los JSON no son documentación; son el arranque de un despliegue. Orden estricto:
1. `DATUM_Catalogos.json` — catálogos de valores (incl. `RECORD_STATUS`).
2. `DATUM_Carga_Inicial_Metadato.json` — seed: `physical_catalog → physical_schema → storage_layer → storage_location → canonical_entity`.
3. `DATUM_Modelo_Datos_Metadato.json` — estructura sobre la que se aplican los seeds.
4. Bloques de carga de cada acelerador activo (mismo patrón).

Cambiar cualquiera de estos ficheros altera el bootstrap real; tratarlos con el mismo cuidado que código de producción.

## Convenciones del metamodelo

- `code` inmutable, en **MAYÚSCULAS + inglés** (DATUM-64). Identidad de fila por `code`; nunca renombrar `code`.
- Clave natural en todo el metamodelo (DATUM-34), AUDIT composite (DATUM-35).
- Sistema de tipos canónico `TYD_*` (DATUM-37).
- Sin descripciones embebidas: solo `code` + i18n en fichero aparte (`DATUM_i18n_D2.json`, actualmente solo D2 cubierto; D00/nuevos subdominios/catálogos físicos SIN traducir).
- FK a catálogo: value materializado + `reference_catalog` en metadato con `catalog_ref_metadata_only=true`.
- 6 catálogos físicos previstos: `databricks`, `metadato` (→ d0..d14), `observability`, `source`, `commondata`, `business`.

## Cómo se añade un acelerador nuevo

Ver `PLANTILLA_acelerador.md`. Cada acelerador declara sobre el metamodelo: entidades canónicas (business_term → entidad → claves → relaciones → constraints), ubicación física (catálogo/esquema), carga inicial seed y su i18n (es/en/fr/pt). Se registra como decisión METADATO-n al recibir "registro oficial".

## Numeración de decisiones

- `METADATO-n` — decisiones propias de este proyecto (arrancan en METADATO-1).
- `DATUM-n` — decisiones heredadas de DATUM-Producto; NO se crean nuevas aquí. El índice de las heredadas relevantes está en `HERENCIA_DATUM_Producto.md`.

## Fuera de alcance en este repo

Nada de doctrina de negocio, oferta, pricing ni GTM: eso vive en DATUM-Producto/Dirección. Aquí solo metamodelo + aceleradores + su carga.

## Visualización

`DATUM_entregable_pagina_canonica.zip` contiene una demo Next.js (`/dashboard/canonico`) que renderiza árbol dominio→subdominio→entidad, ER interactivo y datos de carga. Se actualiza apuntando sus `/public/*.json` a los ficheros de este proyecto.
