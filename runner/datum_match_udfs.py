# ============================================================================
# UDF de matching para el Data Plane (Databricks / PySpark).
# Se registran UNA VEZ como librería de plataforma. El compilador de la vista
# de match las llama por el nombre que declara match_function_impl.udf_ref.
#
# Resumen de qué hay que construir:
#   EXACT, SOUNDEX, LEVENSHTEIN  -> NO se construyen (nativas de Spark / derivadas)
#   norm                          -> UDF mínima propia (acentos + puntuación)
#   jw (Jaro-Winkler)             -> UDF fina sobre librería (jellyfish o commons-text)
#   metaphone                     -> UDF fina sobre librería (jellyfish o commons-codec)
# ============================================================================

# --- Opción A · PySpark + jellyfish (pip install jellyfish) ------------------
import unicodedata, re, jellyfish
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DoubleType

spark = SparkSession.builder.getOrCreate()

def norm(s):
    if s is None: return None
    s = unicodedata.normalize("NFKD", s)                    # descompone acentos
    s = "".join(c for c in s if not unicodedata.combining(c))  # los quita
    s = re.sub(r"[^0-9A-Za-z ]", "", s)                     # quita puntuación
    return s.upper().strip()

def jw(a, b):
    if a is None or b is None: return 0.0
    return float(jellyfish.jaro_winkler_similarity(a, b))

def metaphone(s):
    return None if s is None else jellyfish.metaphone(s)

# registro con los nombres que usa el metadato (match_function_impl.udf_ref)
spark.udf.register("norm",      norm,      StringType())
spark.udf.register("jw",        jw,        DoubleType())
spark.udf.register("metaphone", metaphone, StringType())
# soundex() y levenshtein() ya son nativas de Spark SQL -> no se registran.

# --- Opción B · JVM + Apache Commons (sin escribir el algoritmo) -------------
# Añadir al cluster:  org.apache.commons:commons-text  y  commons-codec:commons-codec
# y una UDF Scala de 2 líneas por función, p.ej.:
#
#   import org.apache.commons.text.similarity.JaroWinklerSimilarity
#   val jws = new JaroWinklerSimilarity()
#   spark.udf.register("jw", (a:String,b:String) => jws.apply(a,b))
#
#   import org.apache.commons.codec.language.Metaphone
#   val mp = new Metaphone()
#   spark.udf.register("metaphone", (s:String) => mp.metaphone(s))
#
# Ventaja JVM: sin overhead de UDF Python por fila (más rápido a gran escala).
