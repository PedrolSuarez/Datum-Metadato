#!/usr/bin/env python3
"""verify_full.py — Verificador integral del estado DATUM Metadato (solo lectura).
Uso: python3 verify_full.py [carpeta]   (por defecto, la carpeta del script)
Cubre lo exigido en ARRANQUE_saneamiento_FINANCE_HR.md · sección «Verificación».
"""
import json, sys, os, re, glob, hashlib, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
def load(n): return json.load(open(os.path.join(ROOT, n), encoding="utf-8"))
ERR, WARN = [], []
def err(s): ERR.append(s)
def warn(s): WARN.append(s)
def b(x): return str(x).strip().lower() in ("1", "true")
def h16(s): return hashlib.sha256(s.encode()).hexdigest()[:16]

model = load("datum_modelo_canonico.json")["entities"]
cats = load("datum_catalogos.json")["catalogs"]
seed = load("datum_carga_inicial.json")["seed"]
i18n = load("DATUM_i18n_D2.json")["i18n"]

ESTADOS_OK = {"CONFIRMADO", "PENDIENTE", "PROPUESTO", "FROM_VISOR", "DEFINIDO", "CUARENTENA", "ACTIVE"}

# ---------- 1. Modelo: FK, catálogos, PK ----------
n_fk = n_refcat = 0
for en, e in model.items():
    attrs = e.get("attributes", [])
    if not any(b(a.get("pk")) for a in attrs): err(f"[PK] {en}: sin PK")
    for a in attrs:
        ft, rc = a.get("fk_target"), a.get("reference_catalog")
        if ft:
            n_fk += 1
            if ft != "reference_value" and ft not in model: err(f"[FK] {en}.{a['name']} -> {ft} inexistente")
        if rc:
            n_refcat += 1
            if rc not in cats: err(f"[CAT] {en}.{a['name']} -> catálogo {rc} inexistente")
            if ft != "reference_value": err(f"[CAT] {en}.{a['name']}: reference_catalog={rc} pero fk_target={ft!r}")
        fc = a.get("fk_composite")
        if fc and fc.get("target") not in model: err(f"[FKC] {en}.{a['name']} -> {fc.get('target')} inexistente")

# ---------- 2. Catálogos ----------
usage = collections.defaultdict(set)
for en, e in model.items():
    for a in e.get("attributes", []):
        if a.get("reference_catalog"): usage[a["reference_catalog"]].add(f"{en}.{a['name']}")
est = collections.Counter()
for cn, c in cats.items():
    if not c.get("canonical_accelerator"): err(f"[CAT] {cn}: sin canonical_accelerator")
    if not c.get("category"): err(f"[CAT] {cn}: sin category")
    st = c.get("estado"); est[st] += 1
    if st not in ESTADOS_OK: err(f"[CAT] {cn}: estado {st!r} fuera de vocabulario")
    if not c.get("values"): warn(f"[CAT] {cn}: sin valores")
    elif all(not str(t).strip() for t in c["values"].values()): warn(f"[CAT] {cn}: valores sin etiqueta")
    for u in c.get("usado_en", []) or []:
        if "." in u:
            en, an = u.split(".", 1)
            if en in model and not any(a["name"] == an for a in model[en]["attributes"]): warn(f"[CAT] {cn}: usado_en obsoleto {u}")

# ---------- 3. Seed ↔ modelo ----------
seed_ent = {r["code"]: r for r in seed["canonical_entity"]}
for c in model:
    if c not in seed_ent: err(f"[SEED] entidad {c} en modelo y no en seed")
for c in seed_ent:
    if c not in model: err(f"[SEED] entidad {c} en seed y no en modelo")
terms = {r["code"]: r for r in seed["business_term"]}
accs = {r["code"]: r for r in seed["canonical_accelerator"]}
for tc, t in terms.items():
    p = t.get("parent_term_code")
    if p and p not in terms: err(f"[TERM] {tc}: parent_term_code {p} inexistente")
    if t.get("canonical_accelerator_code") not in accs: err(f"[TERM] {tc}: acelerador {t.get('canonical_accelerator_code')} inexistente")
real_cnt = collections.Counter()
for c, r in seed_ent.items():
    bt = r.get("business_term_code")
    if not bt or bt not in terms: err(f"[SEED] {c}: business_term_code {bt!r} inexistente")
    else: real_cnt[terms[bt]["canonical_accelerator_code"]] += 1
    mbt = model[c].get("business_term") if c in model else None
    if mbt and mbt != bt: warn(f"[SEED] {c}: business_term modelo={mbt} seed={bt}")
for ac, a in accs.items():
    if int(a.get("entity_count", -1)) != real_cnt[ac]: err(f"[ACC] {ac}: entity_count declarado {a.get('entity_count')} ≠ real {real_cnt[ac]}")
seed_cat = {r["code"] for r in seed["reference_catalog"]}
for r in seed["reference_catalog"]:
    if r["code"] not in cats: err(f"[SEED] reference_catalog {r['code']} no está en datum_catalogos.json")
for r in seed["reference_value"]:
    rc = r["reference_catalog_code"]
    if rc not in cats: err(f"[SEED] reference_value {rc}:{r['code']} catálogo inexistente")
    elif r["code"] not in cats[rc].get("values", {}): err(f"[SEED] reference_value {rc}:{r['code']} no está en el catálogo")
schemas = {(r["physical_catalog_code"], r["code"]) for r in seed["physical_schema"]}; schema_missing = []
for c, r in seed_ent.items():
    if (r.get("physical_catalog_code"), r.get("physical_schema_code")) not in schemas:
        schema_missing.append(c)

if schema_missing: warn(f"[SEED] {len(schema_missing)} entidades con esquema físico no sembrado (problema conocido 'metadata'): {sorted(set(seed_ent[c].get('physical_schema_code') for c in schema_missing))}")

# ---------- 4. Restricciones ----------
SQLKW = {"or","and","not","is","null","in","like","between","case","when","then","else","end","true","false","exists"}
for r in seed.get("canonical_entity_constraint", []):
    en = r["canonical_entity_code"]
    if en not in model: err(f"[CONS] {r['code']}: entidad {en} inexistente"); continue
    names = {a["name"] for a in model[en]["attributes"]}
    expr = re.sub(r"'[^']*'", "", r["expression"])
    for tok in set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr)):
        if tok.lower() in SQLKW: continue
        if tok not in names: err(f"[CONS] {en}.{r['code']}: atributo {tok} no existe")

# ---------- 5. i18n ----------
expected = {}
for en, e in model.items():
    expected[h16(f"datum:CANONICAL_ENTITY:{en}")] = f"entidad {en}"
    for a in e.get("attributes", []): expected[h16(f"datum:CANONICAL_ATTRIBUTE:{en}.{a['name']}")] = f"atributo {en}.{a['name']}"
for cn, c in cats.items():
    for v in (c.get("values") or {}): expected[h16(f"datum:REFERENCE_VALUE:{cn}:{v}")] = f"valor {cn}:{v}"
missing = [d for k, d in expected.items() if k not in i18n]
orphans = [k for k in i18n if k not in expected]
for d in missing[:50]: err(f"[I18N] ausente: {d}")
if len(missing) > 50: err(f"[I18N] … y {len(missing)-50} ausentes más")
for k in orphans[:50]: err(f"[I18N] huérfano: {k} {i18n[k].get('object_type')} {i18n[k].get('entity') or i18n[k].get('catalog') or ''} {i18n[k].get('code')}")
if len(orphans) > 50: err(f"[I18N] … y {len(orphans)-50} huérfanos más")
n_empty = 0
for k, v in i18n.items():
    sh = (v.get("texts") or {}).get("SHORT") or {}
    if any(not str(sh.get(l, "")).strip() for l in ("es", "en", "fr", "pt")): n_empty += 1
if n_empty: warn(f"[I18N] {n_empty} objetos con SHORT vacío en algún idioma")

# ---------- 6. Ficheros de términos (v3 terms/attributes · v2 terminos/attrs) ----------
tstats = {}
for f in sorted(glob.glob(os.path.join(ROOT, "datum_terminos_modelo__*.json"))):
    fn = os.path.basename(f); d = json.load(open(f, encoding="utf-8"))
    if "terms" in d: ver, tl, ak = "v3", d["terms"], "attributes"
    elif "terminos" in d: ver, tl, ak = "v2", d["terminos"], "attrs"
    else: err(f"[TERMS] {fn}: esquema desconocido"); continue
    nodes = desf = fk_sin_regla = fk_sin_key = refcat = pend = 0; parcial = []; sin_regla_det = []
    for t in tl:
        for e in t.get("entities", []):
            nodes += 1; eid = e.get("entity_id")
            if eid not in model: err(f"[TERMS] {fn}: nodo {eid} no existe en el modelo"); continue
            ma = {a["name"]: a for a in model[eid]["attributes"]}
            ta = {a["name"]: a for a in e.get(ak, [])}
            only_t = set(ta) - set(ma); only_m = set(ma) - set(ta)
            if only_t: desf += 1; err(f"[TERMS] {fn}: {eid} atributos solo en términos: {sorted(only_t)[:8]}")
            if only_m and not only_t: parcial.append((eid, len(ta), len(ma)))
            for n, a in ta.items():
                if n not in ma: continue
                m = ma[n]
                for fld in ("fk_target", "reference_catalog"):
                    if (a.get(fld) or None) != (m.get(fld) or None):
                        desf += 1; err(f"[TERMS] {fn}: {eid}.{n} {fld} términos={a.get(fld)!r} modelo={m.get(fld)!r}")
                for fld in ("mandatory", "pk"):
                    if b(a.get(fld)) != b(m.get(fld)):
                        desf += 1; err(f"[TERMS] {fn}: {eid}.{n} {fld} términos={a.get(fld)!r} modelo={m.get(fld)!r}")
                if a.get("reference_catalog"): refcat += 1
            keys_on = {k.get("via_attr") for k in e.get("keys", []) if k.get("via_attr")}
            rules_on = {r.get("on") for r in e.get("dq_referential_integrity", []) or []}
            for n, a in ta.items():
                if a.get("fk_target"):
                    if a.get("pending_party_role"): pend += 1; continue
                    if n not in keys_on: fk_sin_key += 1
                    if n not in rules_on:
                        fk_sin_regla += 1
                        if ver == "v3": sin_regla_det.append(f"{eid}.{n}->{a['fk_target']}")
    tstats[fn] = dict(ver=ver, terminos=len(tl), nodos=nodes, desfasados=desf, refs_catalogo=refcat, fk_sin_key=fk_sin_key, fk_sin_regla=fk_sin_regla, pendientes_party=pend, parciales=parcial)
    if ver == "v2": warn(f"[TERMS] {fn}: esquema v2, sin dq_referential_integrity ({fk_sin_regla} FK sin regla derivada)")
    elif fk_sin_regla: err(f"[TERMS] {fn}: {fk_sin_regla} FK sin regla REFERENTIAL: {sin_regla_det}")
    if fk_sin_key: warn(f"[TERMS] {fn}: {fk_sin_key} FK sin entrada en keys")
    for eid, nt, nm in parcial: warn(f"[TERMS] {fn}: nodo parcial {eid} ({nt}/{nm} atributos)")

# ---------- Resumen ----------
print("=== DATUM verify_full ===")
print(f"entidades {len(model)} · atributos {sum(len(e['attributes']) for e in model.values())} · FK {n_fk} · refs a catálogo {n_refcat}")
print(f"catálogos {len(cats)} (sembrados {len(seed_cat)}) · estados {dict(est)}")
print(f"i18n {len(i18n)} · esperados {len(expected)} · ausentes {len(missing)} · huérfanos {len(orphans)}")
print(f"restricciones {len(seed.get('canonical_entity_constraint', []))} · aceleradores {len(accs)} · términos {len(terms)}")
for fn, s in tstats.items():
    print(f"  {fn}: {s['ver']} · {s['terminos']} términos · {s['nodos']} nodos · desfasados {s['desfasados']} · refcat {s['refs_catalogo']} · FK sin regla {s['fk_sin_regla']} · FK party pendientes {s['pendientes_party']} · parciales {len(s['parciales'])}")
print(f"\nERRORES: {len(ERR)}   AVISOS: {len(WARN)}")
show_all = "--all" in sys.argv
for s in (ERR if show_all else ERR[:80]): print("  E", s)
wl = [w for w in WARN if not w.startswith("[CAT]")] if not show_all else WARN
for s in wl[:80]: print("  W", s)
cw = collections.Counter(w.split("]")[0] + "]" + (" sin valores" if "sin valores" in w else " sin etiqueta" if "sin etiqueta" in w else " usado_en obsoleto" if "obsoleto" in w else "") for w in WARN if w.startswith("[CAT]"))
if cw and not show_all: print("  W [CAT] resumen:", dict(cw), "(--all para el detalle)")
sys.exit(1 if ERR else 0)
