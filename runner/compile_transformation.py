#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPILADOR GENÉRICO de la vista de carga de una transformación (término Definición).
Lee el metadato: transformation + transformation_field + _filter + _join + _variant.
Emite: la SQL de carga y su registro como canonical_view (tipo CANONICAL) + compiled_ddl:
   - role=PRINCIPAL   -> INSERT (golden source; inserta la fila)
   - role=ENRICHMENT  -> MERGE por PK canónica (completa atributos)
Cubre: expresiones por campo, agregación (GROUP BY derivado + HAVING), filtros WHERE/HAVING,
joins, DISTINCT y unpivot (variantes -> UNION ALL). Mismo código para cualquier transformación.
"""
import json

OP = {"EQ":"=","NE":"<>","GT":">","GE":">=","LT":"<","LE":"<=","IN":"IN","NOT_IN":"NOT IN",
      "LIKE":"LIKE","NOT_LIKE":"NOT LIKE","BETWEEN":"BETWEEN","IS_NULL":"IS NULL","IS_NOT_NULL":"IS NOT NULL"}
JT = {"INNER":"INNER JOIN","LEFT":"LEFT JOIN","RIGHT":"RIGHT JOIN","FULL":"FULL JOIN"}

def _col_expr(f, variant_choice):
    ca = f["canonical_attribute_code"]
    if f.get("is_variant"):                                  # unpivot: valor del eje actual
        return variant_choice[ca]
    ag = f.get("aggregate_function_code")
    if ag:                                                   # agregación
        src = f.get("source_expression","")
        if ag == "COUNT" and not src: return "COUNT(*)"
        if ag == "COUNT_DISTINCT":    return f"COUNT(DISTINCT {src})"
        return f"{ag}({src})"
    return f.get("source_expression","")                    # campo simple (clave de group by si hay agg)

def _select_list(fields, variant_choice):
    return [f"{_col_expr(f,variant_choice)} AS {f['canonical_attribute_code']}" for f in fields]

def _predicates(filters, stage):
    conds = []
    for f in sorted([x for x in filters if x.get("filter_stage_code","WHERE")==stage], key=lambda x:x["filter_order"]):
        col = f.get("source_attribute_code") or f.get("expression")
        op  = OP[f["operator_code"]]
        conds.append(f"{col} {op}" if f["operator_code"] in ("IS_NULL","IS_NOT_NULL")
                     else f"{col} {op} {f.get('filter_value')}")
    return " AND ".join(conds)

def _from(t, joins):
    frm = f"{t['source_entity_code']} s"
    for j in sorted(joins, key=lambda x:x["join_order"]):
        frm += f"\n  {JT[j['join_type_code']]} {j['joined_source_entity_code']} ON {j['join_condition']}"
    return frm

def build_select(t, fields, filters, joins, variants):
    distinct = "DISTINCT " if t.get("is_distinct") else ""
    has_agg  = any(f.get("aggregate_function_code") for f in fields)
    frm, where, having = _from(t,joins), _predicates(filters,"WHERE"), _predicates(filters,"HAVING")
    group_keys = [f.get("source_expression","") for f in fields
                  if not f.get("aggregate_function_code") and not f.get("is_variant")]

    def one(vc):
        q = f"SELECT {distinct}\n  " + ",\n  ".join(_select_list(fields, vc)) + f"\nFROM {frm}"
        if where:  q += f"\nWHERE {where}"
        if has_agg and group_keys: q += "\nGROUP BY " + ", ".join(group_keys)
        if has_agg and having:     q += f"\nHAVING {having}"
        return q

    variant_fields = [f for f in fields if f.get("is_variant")]
    if variant_fields:                                       # UNPIVOT -> UNION ALL por variant_order
        orders = sorted({v["variant_order"] for v in variants})
        branches = []
        for k in orders:
            vc = {v["canonical_attribute_code"]: v["value_expression"] for v in variants if v["variant_order"]==k}
            branches.append(one(vc))
        return "\nUNION ALL\n".join(branches)
    return one(None)

def compile_transformation(t, fields, filters, joins, variants, canonical_pk):
    sel = build_select(t, fields, filters, joins, variants)
    ent = t["canonical_entity_code"]
    if t["role_code"] == "PRINCIPAL":                        # inserta desde la golden source
        ddl = f"INSERT INTO {ent}\n{sel};"
        kind, wmode = "INSERT", "APPEND"
    else:                                                    # ENRICHMENT -> MERGE por PK canónica
        on  = " AND ".join(f"t.{k}=x.{k}" for k in canonical_pk)
        setc= [f["canonical_attribute_code"] for f in fields if f["canonical_attribute_code"] not in canonical_pk]
        ddl = (f"MERGE INTO {ent} t\nUSING (\n{sel}\n) x\nON {on}\n"
               f"WHEN MATCHED THEN UPDATE SET " + ", ".join(f"t.{c}=x.{c}" for c in setc) + ";")
        kind, wmode = "MERGE", "MERGE"
    view = {"code":f"{t['code']}_VIEW","canonical_entity_code":ent,"view_kind_code":"CANONICAL",
            "target_layer_code":"CANONICAL","write_mode_code":wmode,"approval_status_code":"DRAFT"}
    return {"sql":sel,"canonical_view":view,
            "compiled_ddl":{"object_code":view["code"],"ddl_kind_code":kind,"compiled_ddl_text":ddl}}

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # CASO 1 · unpivot REDES_SOCIALES (role PRINCIPAL, campos variantes -> UNION ALL)
    t = {"code":"REDES_SOCIALES","canonical_entity_code":"redes_sociales","source_entity_code":"crm_cliente",
         "role_code":"PRINCIPAL","is_distinct":False}
    fields = [
      {"canonical_attribute_code":"cliente_id","source_expression":"s.id"},              # común
      {"canonical_attribute_code":"tipo_red","is_variant":True},                          # variante
      {"canonical_attribute_code":"valor","is_variant":True},                             # variante
    ]
    variants = [
      {"canonical_attribute_code":"tipo_red","variant_order":1,"value_expression":"'FACEBOOK'"},
      {"canonical_attribute_code":"valor","variant_order":1,"value_expression":"s.facebook"},
      {"canonical_attribute_code":"tipo_red","variant_order":2,"value_expression":"'TWITTER'"},
      {"canonical_attribute_code":"valor","variant_order":2,"value_expression":"s.twitter"},
    ]
    r = compile_transformation(t, fields, [], [], variants, ["cliente_id","tipo_red"])
    print("== CASO 1 · unpivot (PRINCIPAL) ==\n", r["compiled_ddl"]["compiled_ddl_text"], "\n")

    # CASO 2 · agregación VENTA_DIARIA (GROUP BY derivado + COUNT(*) + HAVING) role PRINCIPAL
    t2 = {"code":"VENTA_DIARIA","canonical_entity_code":"venta_diaria","source_entity_code":"tickets",
          "role_code":"PRINCIPAL","is_distinct":False}
    f2 = [
      {"canonical_attribute_code":"tienda","source_expression":"s.tienda"},               # clave (sin agg)
      {"canonical_attribute_code":"fecha","source_expression":"s.fecha"},                  # clave
      {"canonical_attribute_code":"num_tickets","aggregate_function_code":"COUNT","source_expression":""},  # COUNT(*)
      {"canonical_attribute_code":"importe_total","aggregate_function_code":"SUM","source_expression":"s.importe"},
    ]
    filt2 = [
      {"filter_order":1,"source_attribute_code":"s.estado","operator_code":"EQ","filter_value":"'OK'","filter_stage_code":"WHERE"},
      {"filter_order":2,"expression":"COUNT(*)","operator_code":"GT","filter_value":"0","filter_stage_code":"HAVING"},
    ]
    r2 = compile_transformation(t2, f2, filt2, [], [], ["tienda","fecha"])
    print("== CASO 2 · agregación (PRINCIPAL) ==\n", r2["compiled_ddl"]["compiled_ddl_text"], "\n")

    # CASO 3 · enriquecimiento (role ENRICHMENT -> MERGE por PK canónica)
    t3 = {"code":"CLIENTE_ENRICH_ERP","canonical_entity_code":"cliente","source_entity_code":"erp_cliente",
          "role_code":"ENRICHMENT","is_distinct":False}
    f3 = [
      {"canonical_attribute_code":"cliente_id","source_expression":"s.id"},               # PK canónica
      {"canonical_attribute_code":"segmento","source_expression":"s.segmento"},           # se completa
    ]
    r3 = compile_transformation(t3, f3, [], [], [], ["cliente_id"])
    print("== CASO 3 · enriquecimiento (ENRICHMENT/MERGE) ==\n", r3["compiled_ddl"]["compiled_ddl_text"])
