#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPILADOR GENÉRICO de la vista de match — 100% dirigido por metadato.
Lee: match_rule_set + match_rule + match_rule_condition (config de la entidad)
     + match_function_impl (plantilla SQL de cada función, del seed del metadato).
Emite: (1) la SQL de matching y (2) su registro como canonical_view tipo MATCHING
       + la entrada compiled_ddl, para cargarla.
El mismo código sirve para cliente, country o cualquier otro: solo cambia el metadato.
"""
import json, re

FUZZY_CUT = 0.90

def load_func_sql(carga_path):
    """Lee la implementación de cada MATCH_FUNCTION del seed del metadato."""
    seed = json.load(open(carga_path))["seed"]
    return {r["match_function_code"]: r["sql_template"] for r in seed.get("match_function_impl", [])}

def _fn(func_sql, code, a, b):
    tmpl = func_sql[code]                                  # p.ej. "jw({a},{b}) >= {cut}"
    return tmpl.replace("{a}", a).replace("{b}", b).replace("{cut}", str(FUZZY_CUT))

def _operand(cond, side):
    if cond.get("canonical_expression"):
        return cond["canonical_expression"].replace("{side}", side)
    return f"{side}.{cond['canonical_attribute_code']}"

def _compare(cond, func_sql):
    if cond.get("match_entity_code") in (None, cond["_root_entity"]):
        return _fn(func_sql, cond["match_function_code"], _operand(cond,"i"), _operand(cond,"m"))
    sat, fk = cond["match_entity_code"], cond["_sat_fk"]
    rf = cond.get("row_filter")
    rf_e = f" AND ({rf.replace('{side}','se')})" if rf else ""
    rf_m = f" AND ({rf.replace('{side}','sm')})" if rf else ""
    cmp_ = _fn(func_sql, cond["match_function_code"], f"se.{cond['canonical_attribute_code']}", f"sm.{cond['canonical_attribute_code']}")
    ex = (f"EXISTS (SELECT 1 FROM {sat} se JOIN {sat} sm ON {cmp_}{rf_e}{rf_m} "
          f"WHERE se.{fk}=i.src_row_id AND sm.{fk}=m.master_id)")
    return ex if cond.get("cardinality_code","ANY")=="ANY" else f"/*ALL*/ {ex}"

def _compile_rule(rule, conds, func_sql):
    if rule["nature_code"]=="DETERMINISTIC":
        pred=" AND ".join(_compare(c,func_sql) for c in conds)
        return f"CASE WHEN {pred} THEN 1 ELSE 0 END AS {rule['code'].lower()}_hit","hard"
    req=[c for c in conds if c.get("is_required")]; wtd=[c for c in conds if not c.get("is_required")]
    gate=" AND ".join(_compare(c,func_sql) for c in req) or "TRUE"
    score=" + ".join(f"{c['weight']} * (CASE WHEN {_compare(c,func_sql)} THEN 1 ELSE 0 END)" for c in wtd) or "1.0"
    return f"CASE WHEN {gate} THEN {score} ELSE NULL END AS {rule['code'].lower()}_score","score"

def compile_sql(rule_set, rules, conds_by_rule, root_entity, master_table, staging_table, func_sql):
    for r in rules:
        for c in conds_by_rule[r["code"]]: c["_root_entity"]=root_entity
    rules=sorted(rules,key=lambda r:r["rule_order"])
    cols,kinds=[],[]
    for r in rules:
        col,kind=_compile_rule(r,conds_by_rule[r["code"]],func_sql); cols.append("    "+col); kinds.append((r,kind))
    auto,review=rule_set["auto_match_threshold"],rule_set["review_threshold"]
    br=[]
    cm=rule_set["combine_mode_code"]
    if cm=="FIRST_MATCH":
        for r,k in kinds:
            if k=="hard": br.append(f"WHEN {r['code'].lower()}_hit = 1 THEN 'AUTO'")
            else: br+=[f"WHEN {r['code'].lower()}_score >= {auto} THEN 'AUTO'",f"WHEN {r['code'].lower()}_score >= {review} THEN 'REVIEW'"]
    elif cm=="BEST_SCORE":
        best="GREATEST("+",".join((f"{r['code'].lower()}_hit*1.0" if k=='hard' else f"COALESCE({r['code'].lower()}_score,0)") for r,k in kinds)+")"
        br=[f"WHEN {best} >= {auto} THEN 'AUTO'",f"WHEN {best} >= {review} THEN 'REVIEW'"]
    else:
        allc=" AND ".join((f"{r['code'].lower()}_hit=1" if k=='hard' else f"{r['code'].lower()}_score >= {auto}") for r,k in kinds)
        br=[f"WHEN {allc} THEN 'AUTO'"]
    verdict="\n      ".join(br)
    bl=rule_set.get("blocking_expression")
    join_on=(f"({bl.replace('{side}','m')}) = ({bl.replace('{side}','i')})" if bl else "TRUE")
    return f"""WITH incoming AS (SELECT * FROM {staging_table}),
cand AS (SELECT i.src_row_id, i.*, m.master_id, m.* FROM incoming i JOIN {master_table} m ON {join_on}),
ev AS (SELECT src_row_id, master_id,
{','.join(chr(10)+c for c in cols)}
  FROM cand),
verd AS (SELECT src_row_id, master_id, CASE
      {verdict}
      ELSE NULL END AS status FROM ev)
SELECT src_row_id,
  CASE WHEN COUNT(*) FILTER (WHERE status IN ('AUTO','REVIEW'))>1 THEN 'REVIEW'
       WHEN BOOL_OR(status='AUTO') THEN 'AUTO'
       WHEN BOOL_OR(status='REVIEW') THEN 'REVIEW' ELSE 'NEW' END AS verdict,
  MAX(master_id) FILTER (WHERE status='AUTO') AS matched_master_id
FROM verd GROUP BY src_row_id"""

def as_canonical_view(root_entity, rule_set_code, sql):
    """Envuelve la SQL como canonical_view tipo MATCHING + su compiled_ddl (cargable)."""
    vcode=f"{root_entity.upper()}_MATCH_VIEW"
    canonical_view={"code":vcode,"canonical_entity_code":root_entity,"view_kind_code":"MATCHING",
                    "target_layer_code":"CANONICAL","write_mode_code":"OVERWRITE","approval_status_code":"DRAFT"}
    compiled_ddl={"object_type_code":"canonical_view","object_code":vcode,"ddl_kind_code":"CREATE_VIEW",
                  "compiled_ddl_text":f"CREATE OR REPLACE VIEW {vcode} AS\n{sql};"}
    return {"canonical_view":canonical_view,"compiled_ddl":compiled_ddl}

# ---------------------------------------------------------------------------
if __name__=="__main__":
    func_sql=load_func_sql("DATUM_Carga_Inicial_Metadato.json")   # ← implementaciones DEL METADATO
    print("# funciones leídas del metadato:", func_sql, "\n")
    rule_set={"code":"CLIENTE_MATCH","combine_mode_code":"FIRST_MATCH","auto_match_threshold":0.85,"review_threshold":0.65,
              "blocking_expression":"UPPER(SUBSTR({side}.nombre,1,4))||{side}.cp"}
    rules=[{"code":"R_NIF","rule_order":1,"nature_code":"DETERMINISTIC"},
           {"code":"R_PERSONA","rule_order":2,"nature_code":"PROBABILISTIC"}]
    conds={"R_NIF":[{"canonical_attribute_code":"nif","match_function_code":"EXACT_NORMALIZED","is_required":True}],
      "R_PERSONA":[
        {"canonical_attribute_code":"nombre","match_function_code":"JARO_WINKLER","is_required":True},
        {"canonical_attribute_code":"ap1","match_function_code":"JARO_WINKLER","is_required":True},
        {"canonical_attribute_code":"ap2","match_function_code":"JARO_WINKLER","is_required":True},
        {"canonical_attribute_code":"valor","match_function_code":"EXACT_NORMALIZED","is_required":False,"weight":0.3,
         "match_entity_code":"persona_contacto","_sat_fk":"persona","row_filter":"{side}.tipo='EMAIL' AND {side}.is_current"},
        {"canonical_attribute_code":"valor","match_function_code":"EXACT","is_required":False,"weight":0.2,
         "match_entity_code":"persona_contacto","_sat_fk":"persona","row_filter":"{side}.tipo='PHONE' AND {side}.is_current"}]}
    sql=compile_sql(rule_set,rules,conds,"cliente","cliente_master","stg_cliente",func_sql)
    reg=as_canonical_view("cliente","CLIENTE_MATCH",sql)
    print("-- canonical_view (tipo MATCHING) a cargar:")
    print(json.dumps(reg["canonical_view"],ensure_ascii=False,indent=1))
    print("\n-- compiled_ddl.compiled_ddl_text:")
    print(reg["compiled_ddl"]["compiled_ddl_text"])
