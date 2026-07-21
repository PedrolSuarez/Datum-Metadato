# -*- coding: utf-8 -*-
# METADATO-44 · Merge idempotente sobre el estado VIVO: regla de refresco por demanda.
# Modelo+seed (business_process_input + frescura por tabla) y docs 18/99. Salida a _merge_out/.
import json,os
B=os.path.dirname(os.path.abspath(__file__))+"/.."
def loadj(p):
    raw=open(p,'rb').read(); crlf=raw.count(b'\r\n')>raw.count(b'\n')//2
    return json.loads(raw.decode('utf-8')),crlf
def dumpj(o,p,crlf):
    t=json.dumps(o,ensure_ascii=False,indent=1)
    if crlf: t=t.replace('\n','\r\n')
    open(p,'w',encoding='utf-8',newline='').write(t)
def loadt(p):
    raw=open(p,'rb').read(); crlf=raw.count(b'\r\n')>raw.count(b'\n')//2
    return raw.decode('utf-8').replace('\r\n','\n'),crlf
def dumpt(t,p,crlf):
    if crlf: t=t.replace('\n','\r\n')
    open(p,'w',encoding='utf-8',newline='').write(t)
def repl(t,a,b):
    assert t.count(a)>=1, "NO ENCONTRADO: "+a[:60]
    return t.replace(a,b,1)

# ===== MODELO =====
m,mc=loadj(B+"/DATUM_Modelo_Datos_Metadato.json"); e=m['entities']
sce=e['source_data_contract_entity']['attributes']; have={a['name'] for a in sce}
fr=[{"name":"freshness_operator_code","tyd":"TYD_CODE","mandatory":0,"pk":0,"fk_target":"reference_value","reference_catalog":"OPERATOR","catalog_ref_metadata_only":True,"desc":"override de frescura por tabla: operador (catalogo OPERATOR); si null hereda el FRESHNESS del contrato"},
 {"name":"freshness_value","tyd":"TYD_DECIMAL","mandatory":0,"pk":0,"fk_target":None,"desc":"override de frescura por tabla: valor umbral (si null hereda del contrato)"},
 {"name":"freshness_unit_code","tyd":"TYD_CODE","mandatory":0,"pk":0,"fk_target":"reference_value","reference_catalog":"SLA_UNIT","catalog_ref_metadata_only":True,"desc":"override de frescura por tabla: unidad (catalogo SLA_UNIT)"}]
nf=[a for a in fr if a['name'] not in have]
if nf:
    i=next(k for k,a in enumerate(sce) if a['name']=='system'); e['source_data_contract_entity']['attributes']=sce[:i]+nf+sce[i:]
if 'business_process_input' not in e:
    e['business_process_input']={"subdomain":"BUSINESS_PROCESS","type":"MDM meta",
     "desc":"Entrada aguas arriba de un proceso: entidad canonica que LEE (no produce) y frescura maxima que necesita de ella. Alimenta la regla de refresco por demanda (umbral efectivo = min(demanda, supply)).",
     "attributes":[
      {"name":"business_process_code","tyd":"TYD_CODE","mandatory":1,"pk":1,"fk_target":"business_process","desc":"proceso consumidor (dependencia)","is_identifying":True,"on_delete":"RESTRICT","on_update":"RESTRICT","fk_composite":{"target":"business_process","columns":[{"source":"business_process_code","target":"code"}]}},
      {"name":"canonical_entity_code","tyd":"TYD_CODE","mandatory":1,"pk":1,"fk_target":"canonical_entity","is_visible_er":True,"desc":"entidad canonica que el proceso lee aguas arriba"},
      {"name":"max_staleness_value","tyd":"TYD_DECIMAL","mandatory":0,"pk":0,"fk_target":None,"desc":"frescura maxima aceptable para este proceso (nullable = sin demanda propia; hereda supply)"},
      {"name":"max_staleness_unit_code","tyd":"TYD_CODE","mandatory":0,"pk":0,"fk_target":"reference_value","reference_catalog":"SLA_UNIT","catalog_ref_metadata_only":True,"desc":"unidad de max_staleness (catalogo SLA_UNIT)"},
      {"name":"is_blocking","tyd":"TYD_BOOLEAN","mandatory":0,"pk":0,"fk_target":None,"desc":"si stale e irrefrescable: bloquea el proceso (1) o sirve last-known (0=defecto)"},
      {"name":"system","tyd":"TYD_SYSTEM","mandatory":1,"pk":0,"fk_target":None}],
     "domain":"","business_term":"BUSINESS_PROCESS"}
m['_meta']['materialized_entities']=len(e); m['_meta']['total_attributes']=sum(len(v['attributes']) for v in e.values())
dumpj(m,B+"/_merge_out/DATUM_Modelo_Datos_Metadato.json",mc)

# ===== SEED =====
d,dc=loadj(B+"/DATUM_Carga_Inicial_Metadato.json"); seed=d['seed']
if not any(isinstance(r,dict) and r.get('code')=='business_process_input' for r in seed['canonical_entity']):
    seed['canonical_entity'].append({"code":"business_process_input","business_term_code":"BUSINESS_PROCESS","config_pattern_code":"DEFAULT","physical_schema_code":"metadata","is_pii":"0","is_sensitive":"0","security_classification_code":"PUBLIC","estimated_annual_volume":"","access_frequency_code":"RARELY","physical_catalog_code":"metadato","partition_strategy_code":"NONE"})
    for r in seed.get('canonical_accelerator',[]):
        if isinstance(r,dict) and r.get('code')=='METADATA': r['entity_count']=r.get('entity_count',0)+1
dumpj(d,B+"/_merge_out/DATUM_Carga_Inicial_Metadato.json",dc)

# ===== 18 DECISIONES =====
t18,c18=loadt(B+"/18-METADATO-decisiones.md")
if 'METADATO-44' not in t18:
    M44=open(B+"/_merge_out/_m44.md",encoding='utf-8').read()
    t18=repl(t18,"**Versión:** v1.16","**Versión:** v1.20")
    t18=repl(t18,"*Fin de `18-METADATO-decisiones.md` v1.19.*", M44+"\n\n*Fin de `18-METADATO-decisiones.md` v1.20.*")
dumpt(t18,B+"/_merge_out/18-METADATO-decisiones.md",c18)

# ===== 99 CONTROL =====
t99,c99=loadt(B+"/99-METADATO-control.md")
if 'METADATO-44' not in t99:
    ST=open(B+"/_merge_out/_m44_99state.md",encoding='utf-8').read()
    HI=open(B+"/_merge_out/_m44_99hist.md",encoding='utf-8').read()
    t99=repl(t99,"**Versión:** v1.19 — ","**Versión:** v1.20 — ")
    t99=repl(t99,"(tras METADATO-16..43, v1.19)","(tras METADATO-16..44, v1.20)")
    t99=repl(t99,"**311 entidades**, **2714 atributos**","**312 entidades**, **2723 atributos**")
    t99=repl(t99,"## Aceleradores incorporados", ST+"## Aceleradores incorporados")
    t99=repl(t99,"*Fin de `99-METADATO-control.md` v1.19.*", HI+"*Fin de `99-METADATO-control.md` v1.20.*")
dumpt(t99,B+"/_merge_out/99-METADATO-control.md",c99)
print("OK modelo:",m['_meta']['materialized_entities'],"/",m['_meta']['total_attributes'])
print("18 tiene M-44:", 'METADATO-44' in t18, "| 99 tiene M-44:", 'METADATO-44' in t99)
