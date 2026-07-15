# Runner DATUM — compiladores de plataforma (NO es metadato)

Estos ficheros son **código del runner/plataforma**, no metadato. Leen el metadato del modelo
y emiten el SQL que se ejecuta. Su sitio natural es el **repositorio** (Datum-Metadato), junto
al runner. Se guardan aquí como copia de seguridad. Regla de oro: **cambiar comportamiento =
cambiar metadato, no tocar este código.**

## `compile_transformation.py` — compilador de la vista de CARGA (término Definición)
- **Lee:** `transformation` + `transformation_field` + `_filter` + `_join` + `_variant`.
- **Emite:** el SQL de carga + `canonical_view` (tipo `CANONICAL`) + `compiled_ddl`.
  - `role=PRINCIPAL` → **INSERT** (golden source, inserta la fila).
  - `role=ENRICHMENT` → **MERGE** por PK canónica (completa atributos).
- **Cubre:** expresión por campo, **agregación** (GROUP BY derivado de la ausencia de función +
  HAVING), filtros **WHERE/HAVING**, **joins**, **DISTINCT** y **unpivot** (campos variantes →
  `UNION ALL` por `variant_order`).
- **Cuándo:** parte del runner; recompila automáticamente al cambiar el metadato. No usa UDF
  (SQL estándar).

## `compile_match_view.py` — compilador de la vista de MATCH (término Matching)
- **Lee:** `match_rule_set` + `match_rule` + `match_rule_condition` + `match_function_impl`.
- **Emite:** el SQL de matching + `canonical_view` (tipo `MATCHING`) + `compiled_ddl`.
- **Cubre:** blocking, reglas deterministas (filtro duro) y probabilísticas (score con puerta
  `is_required` + pesos), satélites 1:N (`EXISTS`/ANY con `row_filter`), `combine_mode`
  (FIRST_MATCH/BEST_SCORE/ALL), umbrales auto/review, DISTINCT + ambigüedad.
- **Cuándo:** parte del runner; recompila al cambiar el metadato del match. **No a mano.**

## `datum_match_udfs.py` — las 3 UDF a instalar (solo para Match)
- Define/registra `norm`, `jw` (Jaro-Winkler) y `metaphone` — las que NO son nativas de Spark.
  Dos opciones: PySpark + `jellyfish`, o JVM + Apache Commons (`commons-text`, `commons-codec`).
- **Cuándo:** se instala **UNA vez** al montar la plataforma (o si se añade una función `UDF`
  nueva). `EXACT`, `SOUNDEX`, `LEVENSHTEIN` son nativas/derivadas — no se instalan.
- El metadato manda: `match_function_impl.impl_kind_code = UDF` marca qué construir.

## En resumen
| Fichero | Término | Uso | ¿UDF? |
|---|---|---|---|
| `compile_transformation.py` | Definición | automático al cambiar metadato | no |
| `compile_match_view.py` | Matching | automático al cambiar metadato | usa las de abajo |
| `datum_match_udfs.py` | Matching | instalar 1 vez | define norm/jw/metaphone |
