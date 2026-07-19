#!/usr/bin/env python3
"""
DATUM · compile_dq_checks.py  (código de RUNNER — plataforma, NO metadato)
Autogenera las comprobaciones DQ de una entidad canónica recorriendo el metamodelo.
100% dirigido por dq_check_type: no hay tabla de reglas; se COMPILAN desde la estructura.
Regla de oro: cambiar comportamiento = cambiar metadato, no este código.
"""
import json, sys

def load(path): return json.load(open(path, encoding="utf-8"))

def load_tyd_catalog(base):
    # Los TYD (= data_type_domain) con su formato: regex, longitud/precisión, obligatoriedad.
    try:
        d = load(f"{base}/datum_datatypes.json")
    except Exception:
        return {}
    return { s["code"]: s for s in d.get("simples", []) }

def index_reference_values(seed):
    m = {}
    for r in seed.get("reference_value", []):
        m.setdefault(r["reference_catalog_code"], []).append(r["code"])
    return m

def identity_mode_of(entity_code, model, seed):
    # identity_mode vive en canonical_entity (fusión M-34). Buscar en seed; si no, "—".
    for r in seed.get("canonical_entity", []):
        if r["code"] == entity_code:
            return r.get("identity_mode_code") or "—"
    return "—"

def domain_validations_index(seed):
    # data_type_domain_validation: dueño = dominio TYD (owner_object_type=DATA_DOMAIN).
    idx = {}
    for r in seed.get("data_type_domain_validation", []):
        dom = r.get("data_type_domain_code") or r.get("owner_object_row_uuid")
        idx.setdefault(dom, []).append(r)
    return idx

def compile_entity(ecode, model, cats, seed, tyd_cat):
    e = model["entities"].get(ecode)
    if not e: 
        return {"entity": ecode, "error": "no existe"}
    attrs = [a for a in e.get("attributes", []) if a["name"] != "system"]
    rv = index_reference_values(seed)
    vidx = domain_validations_index(seed)
    entset = set(model["entities"])
    tyd_domains = set()
    IGN = {"reference_value","object_type","(polimórfico)","(D8)",None}
    checks = []

    # helper para on_fail derivado (resumen; la resolución fina la hace el runner con los campos)
    def add(ctype, dim, target, predicate, on_fail, sev, extra=None):
        c = {"check_type":ctype,"dq_dimension":dim,"target":target,
             "predicate":predicate,"on_fail":on_fail,"severity":sev}
        if extra: c.update(extra)
        checks.append(c)

    # --- UNIQUENESS: PK (y UN si hubiera canonical_key) ---
    pk_cols = [a["name"] for a in attrs if a.get("pk")]
    if pk_cols:
        add("UNIQUENESS","UNIQUENESS",f"{ecode}({', '.join(pk_cols)})",
            f"UNIQUE({', '.join(pk_cols)})","REJECT (o dedup si survivorship_rule)","ERROR")

    # --- por atributo ---
    for a in attrs:
        an = a["name"]; tgt = f"{ecode}.{an}"
        # MANDATORY (obligatoriedad simple)
        if a.get("mandatory") in (1,"1",True):
            add("MANDATORY_SIMPLE","COMPLETENESS",tgt,f"{an} IS NOT NULL",
                "AUTO_REMEDIATE si column_default; si no REJECT","ERROR")
        # REFERENTIAL — catálogo (IR de catálogos)
        rc = a.get("reference_catalog")
        if rc and a.get("catalog_ref_metadata_only"):
            n = len(rv.get(rc, []))
            add("REFERENTIAL","CONSISTENCY",tgt,
                f"{an} ∈ reference_value[{rc}]  ({n} valores)",
                "según on_miss_code","ERROR",{"ir_kind":"CATALOG","catalog":rc})
        # REFERENTIAL — entidad (IR de MDM/RDM)
        tfk = a.get("fk_target")
        comp = a.get("fk_composite")
        ent_tgt = None
        if tfk and tfk not in IGN and tfk in entset: ent_tgt = tfk
        elif comp and comp.get("target") in entset: ent_tgt = comp.get("target")
        if ent_tgt:
            mode = identity_mode_of(ent_tgt, model, seed)
            kind = {"MDM_SURROGATE":"MDM","RDM_STANDARD":"RDM","BK_HASH":"BK","INHERITED":"INHERITED"}.get(mode, mode)
            add("REFERENTIAL","CONSISTENCY",tgt,
                f"{an} existe en {ent_tgt}  [identidad {kind}]",
                "según on_miss_code del destino","ERROR",{"ir_kind":"ENTITY","ref_entity":ent_tgt,"identity":kind})
        # FORMAT — desde el dominio de tipo = el TYD del atributo (regex/longitud del catálogo TYD)
        dom = a.get("tyd")
        if dom and dom not in ("TYD_SYSTEM",):
            t = tyd_cat.get(dom, {})
            reg = (t.get("regex") or "").strip()
            lp  = (t.get("long_prec") or "").strip()
            has_regex = reg and reg not in ("—","-")
            has_len   = lp and lp not in ("—","-","ilimitado","prec —")
            if has_regex or has_len:
                partes=[]
                if has_regex: partes.append(f"regex {reg}")
                if has_len:   partes.append(f"long/prec {lp}")
                add("FORMAT","VALIDITY",tgt,
                    f"{an} cumple {dom} ({'; '.join(partes)})",
                    "AUTO_REMEDIATE si normalización; si no REJECT","ERROR",{"domain":dom})
            else:
                tyd_domains.add(dom)

    fmt_pend = sorted(d for d in tyd_domains if not vidx.get(d))
    return {"entity":ecode,"total_checks":len(checks),"checks":checks,"format_pending_domains":fmt_pend}

def main():
    base = sys.argv[1] if len(sys.argv)>1 else "/home/claude/build"
    model = load(f"{base}/DATUM_Modelo_Datos_Metadato.json")
    cats  = load(f"{base}/DATUM_Catalogos.json")
    seed  = load(f"{base}/DATUM_Carga_Inicial_Metadato.json")["seed"]
    tyd_cat = load_tyd_catalog(base)
    targets = sys.argv[2:] or ["business_rule"]
    for ec in targets:
        res = compile_entity(ec, model, cats, seed, tyd_cat)
        print("="*90)
        print(f"ENTIDAD: {res['entity']}   →   {res.get('total_checks','?')} comprobaciones DQ autogeneradas")
        print("="*90)
        by = {}
        for c in res.get("checks",[]):
            by.setdefault(c["check_type"],[]).append(c)
        for ct in ["STRUCTURE","MANDATORY_SIMPLE","UNIQUENESS","REFERENTIAL","FORMAT"]:
            for c in by.get(ct,[]):
                extra = c.get("catalog") or c.get("ref_entity") or c.get("domain") or ""
                print(f"  [{c['check_type']:16s}] {c['dq_dimension']:12s} {c['target']}")
                print(f"       ⇒ {c['predicate']}")
                print(f"       on_fail: {c['on_fail']}  ·  sev: {c['severity']}")
        fp = res.get("format_pending_domains") or []
        if fp:
            print(f"  [FORMAT          ] VALIDITY     · 0 activos — dominios TYD sin validaciones sembradas:")
            print(f"       {', '.join(fp)}")
            print(f"       (al sembrar data_type_domain_validation por TYD, el generador emite estos checks)")
        print()

if __name__ == "__main__":
    main()
