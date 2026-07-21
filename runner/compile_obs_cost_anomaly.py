#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATUM · compile_obs_cost_anomaly.py  (código de RUNNER — plataforma, NO metadato)
Proceso DERIVED_SCHEDULED `obs_cost_anomaly` (METADATO-49): detecta anomalías de coste
comparando el coste diario por dimensión funcional contra su línea base móvil (media+kσ, 30d),
leyendo uc_billing_usage. Emite filas en observability.process.cost_anomaly.
Ejemplo-plantilla de la lógica de cómputo de un proceso de derivación.
Regla de oro: el umbral (k, ventana, dimensión) es metadato/config, no se hardcodea el motor.
"""
import json, sys

def load(p): return json.load(open(p, encoding="utf-8"))
def phys(entity, seed):
    for r in seed["canonical_entity"]:
        if r["code"] == entity:
            return f'{r["physical_catalog_code"]}.{r["physical_schema_code"]}.{entity}'
    return f"observability.uc.{entity}"

# Config del proceso (sería seed: business_process/params). Umbral y ventana.
CFG = {"window_days": 30, "k_sigma": 3.0, "dimension_expr": "custom_tags['cost_center']"}

def compile_sql(base):
    seed = load(f"{base}/DATUM_Carga_Inicial_Metadato.json")["seed"]
    src = phys("uc_billing_usage", seed)      # fuente (M-48: cost_anomaly lee UC, sin copia cruda)
    dst = phys("cost_anomaly", seed)          # destino observability.process.cost_anomaly
    dim = CFG["dimension_expr"]; W = CFG["window_days"]; K = CFG["k_sigma"]
    # 1) coste diario por dimensión (usage_quantity como proxy; un JOIN a uc_billing_list_prices da €)
    # 2) baseline móvil media/σ sobre los W días previos (excluye el día evaluado)
    # 3) anomalía si observed > media + Kσ ; severidad por magnitud de la desviación
    return f"""INSERT INTO {dst}
  (cost_anomaly_uuid, detection_time, functional_dimension_code, observed_cost,
   expected_cost, deviation_pct, severity, status)
WITH daily AS (
  SELECT {dim} AS dim, usage_date AS d, SUM(usage_quantity) AS cost
  FROM {src}
  GROUP BY {dim}, usage_date
),
base AS (
  SELECT dim, d, cost,
         AVG(cost)    OVER w AS mu,
         STDDEV(cost) OVER w AS sigma
  FROM daily
  WINDOW w AS (PARTITION BY dim ORDER BY d
               ROWS BETWEEN {W} PRECEDING AND 1 PRECEDING)
)
SELECT uuid()                                             AS cost_anomaly_uuid,
       current_timestamp()                                AS detection_time,
       dim                                                AS functional_dimension_code,
       cost                                               AS observed_cost,
       mu                                                 AS expected_cost,
       ROUND(100.0 * (cost - mu) / NULLIF(mu, 0), 2)      AS deviation_pct,
       CASE WHEN cost > mu + {K + 2} * sigma THEN 'ERROR'
            WHEN cost > mu + {K} * sigma     THEN 'WARNING'
            ELSE 'INFO' END                               AS severity,
       'OPEN'                                             AS status
FROM base
WHERE sigma IS NOT NULL
  AND cost > mu + {K} * sigma
  AND d = current_date() - INTERVAL 1 DAY;"""      # solo el día recién cerrado

if __name__ == "__main__":
    print(compile_sql(sys.argv[1] if len(sys.argv) > 1 else "."))
