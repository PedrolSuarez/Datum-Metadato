#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DATUM · observability_emitter.py  (código de RUNNER — plataforma, NO metadato)
Emisor genérico de la telemetría de ejecución (population_mode=RUNNER_TELEMETRY).
Lo invoca el harness en hooks de ciclo de vida; ningún runner escribe su propio INSERT.
Dirigido por metadato:
  - run / run_step: telemetría universal del harness (columnas leídas del modelo).
  - telemetría de dominio: runner_capability.emits_observability_entity.
Regla de oro: cambiar comportamiento = cambiar metadato, no este código. (METADATO-50)
"""
import json, uuid, datetime

def load(p): return json.load(open(p, encoding="utf-8"))

# ---------- resolución física desde el metadato (canonical_entity seed) ----------
def _phys_index(seed):
    return {r["code"]: (r["physical_catalog_code"], r["physical_schema_code"]) for r in seed["canonical_entity"]}

def physical_name(entity, phys):
    cat, sch = phys.get(entity, ("observability", "process"))
    return f"{cat}.{sch}.{entity}"

def _cols(model, entity):
    return [a["name"] for a in model["entities"][entity]["attributes"] if a["name"] != "system"]

def _emits_index(seed):
    return {r["runner_type_code"]: r.get("emits_observability_entity") for r in seed["runner_capability"]}


class ObservabilityEmitter:
    """Un emisor por corrida del harness. `execute(sql, params)` lo inyecta la plataforma
    (spark.sql / JDBC); en dry-run se limita a acumular las sentencias."""

    def __init__(self, base_path, execute=None):
        self.model = load(f"{base_path}/DATUM_Modelo_Datos_Metadato.json")
        self.seed  = load(f"{base_path}/DATUM_Carga_Inicial_Metadato.json")["seed"]
        self.phys  = _phys_index(self.seed)
        self.emits = _emits_index(self.seed)
        self.run_cols  = _cols(self.model, "run")
        self.step_cols = _cols(self.model, "run_step")
        self._exec = execute or (lambda sql, params: self._buffer.append(sql))
        self._buffer = []

    # -- helpers de SQL (MERGE inmutable: INSERT al abrir, MERGE de cierre) --
    def _insert(self, entity, row):
        t = physical_name(entity, self.phys)
        cols = ", ".join(row.keys())
        vals = ", ".join(f":{k}" for k in row)
        self._exec(f"INSERT INTO {t} ({cols}) VALUES ({vals})", row)

    def _merge_close(self, entity, key, row):
        t = physical_name(entity, self.phys)
        setc = ", ".join(f"t.{k} = s.{k}" for k in row if k not in key)
        onc  = " AND ".join(f"t.{k} = s.{k}" for k in key)
        cols = ", ".join(row.keys()); vals = ", ".join(f"s.{k}" for k in row)
        src  = " , ".join(f":{k} AS {k}" for k in row)
        self._exec(
            f"MERGE INTO {t} t USING (SELECT {src}) s ON {onc} "
            f"WHEN MATCHED THEN UPDATE SET {setc}", row)

    # ---------------- hooks de ciclo de vida ----------------
    def on_run_start(self, *, run_id, business_process, workflow_pattern=None,
                     trigger_type="SCHEDULED", now=None, correlation_id=None):
        now = now or datetime.datetime.utcnow()
        self._insert("run", {
            "run_id": run_id, "root_run_id": run_id, "parent_run_id": None,
            "execution_level_code": "WORKFLOW", "linked_business_process_code": business_process,
            "linked_workflow_pattern_code": workflow_pattern, "trigger_type_code": trigger_type,
            "execution_date": now, "started_at": now, "run_status_code": "RUNNING",
            "correlation_id": correlation_id, "ingested_at": now})
        return run_id

    def on_step_start(self, *, run_id, root_run_id, runner_type, sequence_order,
                      canonical_entity=None, pattern_step=None, now=None):
        now = now or datetime.datetime.utcnow()
        step_id = str(uuid.uuid4())
        self._insert("run_step", {
            "run_id": run_id, "step_run_id": step_id, "root_run_id": root_run_id,
            "parent_run_id": run_id, "execution_level_code": "RUNNER",
            "runner_type_code": runner_type, "linked_canonical_entity_code": canonical_entity,
            "linked_workflow_pattern_step_code": pattern_step, "sequence_order": sequence_order,
            "execution_date": now, "started_at": now, "run_status_code": "RUNNING"})
        return step_id

    def on_step_end(self, *, run_id, step_run_id, status="COMPLETED", verdict=None,
                    read=0, processed=0, failed=0, started_at=None, now=None):
        now = now or datetime.datetime.utcnow()
        self._merge_close("run_step", ["run_id", "step_run_id"], {
            "run_id": run_id, "step_run_id": step_run_id, "run_status_code": status,
            "crossing_result_code": verdict, "ended_at": now,
            "duration_seconds": int((now - started_at).total_seconds()) if started_at else None,
            "records_read": read, "records_processed": processed, "records_failed": failed})

    def on_run_end(self, *, run_id, status="COMPLETED", read=0, processed=0, failed=0,
                   started_at=None, now=None):
        now = now or datetime.datetime.utcnow()
        self._merge_close("run", ["run_id"], {
            "run_id": run_id, "run_status_code": status, "ended_at": now,
            "duration_seconds": int((now - started_at).total_seconds()) if started_at else None,
            "records_read": read, "records_processed": processed, "records_failed": failed})

    # -------- telemetría de dominio (runner_capability.emits) --------
    def emit_domain(self, *, runner_type, row):
        """Escribe la observabilidad de dominio que el runner declara emitir.
        p.ej. RUNNER_DQ -> dq_run_result ; RUNNER_LOAD_CANONICAL -> golden_record_fusion."""
        target = self.emits.get(runner_type)
        if not target:
            return None            # este runner no emite dominio: solo run/run_step
        self._insert(target, row)  # append inmutable
        return target


if __name__ == "__main__":
    # DRY-RUN: traza de una corrida de ejemplo (uc_audit_ingest) sin Spark.
    import sys
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    t0 = datetime.datetime(2026, 7, 21, 3, 0, 0)
    em = ObservabilityEmitter(base)                       # execute=None -> buffer
    rid = "11111111-1111-1111-1111-111111111111"
    em.on_run_start(run_id=rid, business_process="uc_audit_ingest",
                    workflow_pattern="uc_audit_ingest_pattern", now=t0)
    sid = em.on_step_start(run_id=rid, root_run_id=rid, runner_type="RUNNER_INGEST",
                           sequence_order=1, canonical_entity="uc_access_audit", now=t0)
    em.on_step_end(run_id=rid, step_run_id=sid, status="COMPLETED",
                   read=1000, processed=1000, failed=0, started_at=t0,
                   now=t0 + datetime.timedelta(seconds=42))
    # dominio: el INGEST de discovery emitiría source_discovery_run
    em.emit_domain(runner_type="RUNNER_INGEST",
                   row={"discovery_run_id": "d-1", "run_id": rid, "source_system_code": "databricks_system",
                        "run_status_code": "COMPLETED"})
    em.on_run_end(run_id=rid, status="COMPLETED", read=1000, processed=1000, started_at=t0,
                  now=t0 + datetime.timedelta(seconds=45))
    print(f"-- {len(em._buffer)} sentencias emitidas --")
    for s in em._buffer:
        print(s + ";")
