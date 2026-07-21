#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATUM · compile_uc_views.py  (código de RUNNER — plataforma, NO metadato)
Compila las entidades de observabilidad con population_mode=UC_VIEW a CREATE OR REPLACE VIEW
sobre su uc_* de origen (canonical_entity.derived_from_entity). Sin tabla física ni ETL. (METADATO-48/51)
El mapeo columna->expresión de cada vista es lo único específico; el motor es genérico.
Regla de oro: cambiar comportamiento = cambiar metadato / el mapeo, no el motor.
"""
import json, sys

def load(p): return json.load(open(p, encoding="utf-8"))

def phys(entity, seed):
    for r in seed["canonical_entity"]:
        if r["code"] == entity:
            return f'{r["physical_catalog_code"]}.{r["physical_schema_code"]}.{entity}'
    return f"observability.uc.{entity}"

# Mapeo por vista: columna_destino -> expresión SQL sobre la uc_* de origen.
# (Acceso solo por Databricks, M-48: access_channel es constante DATABRICKS.)
MAPPINGS = {
 "access_event": {
    "access_event_uuid":   "event_id",
    "event_time":          "event_time",
    "event_date":          "event_date",
    "principal_id":        "user_identity:email",          # struct UC -> principal
    "service_name":        "service_name",
    "action_name":         "action_name",
    "target_datum_code":   "request_params:full_name",     # objeto accedido (resoluble a code DATUM)
    "access_channel":      "'DATABRICKS'",                  # constante (M-48)
    "source_ip_address":   "source_ip_address",
    "session_id":          "session_id",
    "result_status":       "response:status_code",
    "source_audit_event_id":"event_id",
 },
 "resource_consumption": {   # passthrough técnico sobre uc_billing_usage
    "*": "passthrough",
 },
 # access_event_aggregate / cost_aggregate: agregaciones (GROUP_BY abajo)
 "access_event_aggregate": {"__agg__": True},
 "cost_aggregate":         {"__agg__": True},
}
# Especificación de las vistas de agregación (dimensiones + medidas)
AGG_SPEC = {
 "access_event_aggregate": {
    "group": ["principal_id := user_identity:email", "target_datum_code := request_params:full_name",
              "period := date_trunc('day', event_time)"],
    "measures": ["access_count := count(*)"],
 },
 "cost_aggregate": {
    "group": ["functional_dimension_code := custom_tags['cost_center']",
              "period := usage_date"],
    "measures": ["total_usage := sum(usage_quantity)"],
 },
}

def _alias(pair):                      # "dst := expr"  ->  (dst, expr)
    d, e = pair.split(":=", 1); return d.strip(), e.strip()

def compile_view(entity, seed):
    src_entity = next((r.get("derived_from_entity") for r in seed["canonical_entity"] if r["code"] == entity), None)
    if not src_entity:
        return f"-- {entity}: sin derived_from_entity, se omite"
    src = phys(src_entity, seed); dst = phys(entity, seed)
    m = MAPPINGS.get(entity, {})
    if m.get("__agg__"):
        spec = AGG_SPEC[entity]
        gcols = [_alias(g) for g in spec["group"]]
        mcols = [_alias(x) for x in spec["measures"]]
        sel = [f"{e} AS {d}" for d, e in gcols] + [f"{e} AS {d}" for d, e in mcols]
        grp = ", ".join(e for _, e in gcols)
        return (f"CREATE OR REPLACE VIEW {dst} AS\n  SELECT " + ",\n         ".join(sel) +
                f"\n  FROM {src}\n  GROUP BY {grp};")
    if m.get("*") == "passthrough":
        return f"CREATE OR REPLACE VIEW {dst} AS SELECT * FROM {src};"
    sel = [f"{expr} AS {dst_col}" for dst_col, expr in m.items()]
    return f"CREATE OR REPLACE VIEW {dst} AS\n  SELECT " + ",\n         ".join(sel) + f"\n  FROM {src};"

def main(base):
    seed = load(f"{base}/DATUM_Carga_Inicial_Metadato.json")["seed"]
    views = [r["code"] for r in seed["canonical_entity"] if r.get("population_mode_code") == "UC_VIEW"]
    print(f"-- {len(views)} vistas UC_VIEW a compilar: {views}\n")
    for v in views:
        print(compile_view(v, seed)); print()

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
