# Herencia de DATUM-Producto — Decisiones de METAMODELO (extracto para «DATUM metadato»)

> Extracto filtrado del `18-DATUM-decisiones.md` de DATUM-Producto. Incluye SOLO las decisiones que definen el metamodelo (estructura, dominios, catálogos, reglas del modelo). **Se excluyen** las de herramienta/demo (visores, Dataplane App), oferta/GTM/negocio y proceso documental interno.
> El detalle completo de cada decisión está en el `18-DATUM-decisiones.md` de Producto; aquí queda el índice de herencia con su enunciado, para saber qué está ya definido y dónde buscar.

## Fundacionales del modelo
- **DATUM-13** — Modelo de DATUM y jerarquía documental de tres niveles.
- **DATUM-18** — Clasificación A/B/C de dominios y renumeración D13/D14/D15(+D16).
- **DATUM-19** — Catálogos internos (D0) vs. RDM de cliente (D2/common_data); equivalencia RDM↔dimensión; jerarquías estándar precargadas.
- **DATUM-34** — Metamodelo con **clave natural**.
- **DATUM-35** — `code` inmutable + AUDIT composite.
- **DATUM-37** — Sistema de tipos canónico (`TYD_*`).

## Semántica canónica (D2)
- **DATUM-20** — Documentación de objetos: descripción corta + funcional extensa.
- **DATUM-22** — `business_term` como agregador semántico del negocio.
- **DATUM-24** — El Golden Record gobierna su aprovisionamiento (MDM avanzado).
- **DATUM-28** — Refinamiento dimensional: copo de nieve declarativo.
- **DATUM-47 / DATUM-50** — Cierre de D2 (Canónico).
- **DATUM-80** — Integridad referencial de conjunto y sustitución de FK por hash (anonimización canónica).

## Fuentes y transformación (D3/D4)
- **DATUM-23** — Jerarquía de contención genérica de fuente (árbol multi-tecnología).
- **DATUM-25** — Recomposición de D3 (Sources).
- **DATUM-69** — Autodescubrimiento de fuentes como workflow recursivo.
- **DATUM-70** — Patrones de proceso de negocio (modos de carga).
- **DATUM-71** — La transformación se modela en el step; autogeneración de FROM/JOIN.
- **DATUM-72** — Frontera declarativo (D4) / observacional; se eliminan `transformation_run` y `run_step`.
- **DATUM-76** — Definición funcional del `runner_transform`.
- **DATUM-77** — Modo normal / reproceso (landing vs operational).
- **DATUM-78** — `cast_and_validate` + `source_format_profile` (D3).
- **DATUM-81 / DATUM-82 / DATUM-83** — Matching código origen→canónico; matching probabilístico; verificación y merge/split de identidad.

## Calidad y evaluaciones (D6/D8)
- **DATUM-79** — Reglas de calidad derivadas del metadato canónico (D2); eliminación de `dq_rule`; vista canónica de calidad por entidad.
- **DATUM-84** — `runner_dq` genérico dirigido por la vista de reglas (multi-grano).
- **DATUM-74** — Unificación de todas las evaluaciones en el motor genérico de D8.
- **DATUM-29** — Oficina del Dato, custodia en 3 capas y mapeo a roles técnicos.
- **DATUM-44** — Doctrina de gobierno de D1 (anclaje a estructura real + `GOVERNANCE_TOPOLOGY`).

## Observabilidad y ejecución (familia A)
- **DATUM-36** — Trazabilidad jerárquica de ejecución (`TYD_EXECUTION_TRACE`).
- **DATUM-38** — Reglas de observabilidad.
- **DATUM-55** — Pack de observabilidad declarado; reglas DQ derivadas.
- **DATUM-63 / DATUM-66** — Catálogos de observabilidad (D66 ABIERTA: integración en D0).
- **DATUM-75** — Árbol de ejecución recursivo único (`execution_run`).
- **DATUM-31** — Reconceptualización de D11 (As-Is del metamodelo).
- **DATUM-32** — Disolución de D12 (observabilidad = circuito normal).
- **DATUM-33** — Disolución de D13 (BCDR = observabilidad).

## Métricas / Data Products (D7)
- **DATUM-27** — D7 como motor universal de métricas/data products por sujeto.

## Auto-gobierno y catálogos
- **DATUM-26** — Auto-gobierno recursivo del metamodelo (DATUM aplicado a DATUM).
- **DATUM-62** — Doctrina de aceleradores y patrón de clasificación del metamodelo.
- **DATUM-64** — Normalización de `code` a MAYÚSCULAS + inglés.
- **DATUM-65** — Clasificación normativa de catálogos (UNE/DAMA/ISO/RGPD) — con reanclaje pendiente.
- **DATUM-73** — Patrón de Gobierno de Cambios del Metamodelo (backlog Comité del Dato).
- **DATUM-21 / DATUM-40** — i18n centralizado; i18n por `row_uuid`.
- **DATUM-101** — Modelo canónico de catálogos, identidad por hash de BK, i18n polimórfico central, dimensiones/jerarquías con tabla de miembros.

## Aceleradores ya incorporados (referencia de patrón, NO de negocio)
- **DATUM-102** — Acelerador `BRAND_AND_PRODUCT_v1` (ficheros F1–F4).
- **DATUM-104** — Acelerador `HHRR_v1` (ficheros F1–F4).

## Estado más reciente
- **DATUM-108** — Submodelo de ubicación física (D00), motor de catálogos minimizado, metadata-first, codificación de subdominios D0/D2. **Es el punto de partida de «DATUM metadato».**

---
## EXCLUIDO de esta herencia (se queda en DATUM-Producto)
- Herramienta/demo: DATUM-85 (visor negocio), 103, 105, 106, 107 (Dataplane App, mockups).
- Proceso documental / gobierno interno: DATUM-1..12, 14, 15, 16, 17, 67, 5, 7.
- Oferta / negocio / GTM: nada de esto pertenece al metamodelo.
