# Runner de Matching — código de plataforma (NO es metadato)

Estos dos ficheros son **código del runner/plataforma**, no metadato. Leen el metadato
(`match_rule_set`, `match_rule`, `match_rule_condition`, `match_function_impl`) y ejecutan
el match. Su sitio es el **repositorio** (Datum-Metadato), junto al runner. Se guardan aquí
como copia de seguridad.

## `compile_match_view.py` — el compilador de la vista de match
- **Qué hace:** dado el metadato de una entidad, emite (1) la SQL de matching y (2) su registro
  como `canonical_view` tipo `MATCHING` + la entrada `compiled_ddl` (`CREATE OR REPLACE VIEW …`).
- **100% dirigido por metadato:** lee las plantillas de función de `match_function_impl` (nada
  hardcodeado). El mismo código sirve para cliente, country o cualquier entidad.
- **Cuándo se usa:** es parte del runner. Se ejecuta **automáticamente** en cada ejecución;
  cuando cambias metadato del match (una regla, condición, umbral, función), el runner recompila
  la vista en la siguiente corrida. **No se ejecuta a mano.**

## `datum_match_udfs.py` — las 3 funciones a instalar
- **Qué hace:** define/registra las UDF que el match necesita y que NO son nativas de Spark:
  `norm` (limpiar acentos/mayúsculas/puntuación), `jw` (Jaro-Winkler) y `metaphone`.
  Trae dos opciones: PySpark + `jellyfish`, o JVM + Apache Commons (`commons-text`, `commons-codec`).
- **Cuándo se usa:** se instala **UNA sola vez** al montar la plataforma. Solo se vuelve a tocar
  si se añade una función nueva de tipo `UDF`. `EXACT`, `SOUNDEX`, `LEVENSHTEIN` son nativas/derivadas
  y no requieren instalación.
- **El metadato manda:** `match_function_impl.impl_kind_code` = `UDF` marca qué construir (con su
  `udf_ref`); `NATIVE`/`COMPOSED` no requieren montaje.

## Regla de oro
- Metadato (JSON, lo canoniza Pedro) = la *información*.
- Estos dos ficheros (repo) = *quien la lee y ejecuta*.
- Cambiar comportamiento del match = cambiar metadato, **no** tocar este código.
