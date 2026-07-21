### Regla de refresco de ingesta por demanda (METADATO-44) — 312 / 2723
- **Ingesta Databricks nativo**: watermark/checkpoint del runtime; DATUM los **observa** por `uc_lakeflow_pipeline_update_timeline` (`result_state`/`period_end_time`) y `uc_access_table_lineage`. Puente `source_entity`→`transformation`→canónica; sin `pipeline_id` propio.
- **Regla derivada** (no tabla), por `source_entity` en la demanda: **AWAIT** (in-flight) / **REFRESH-cold** / **SERVE** / **REFRESH** / **BREACH** (`breach_action`, autocontenido). `last_loaded_at` = `run`/`run_step` COMPLETED + `period_end_time`.
- **Dedup por `source_entity`**: una actualización de pipeline sirve a N procesos; el más exigente marca el ritmo. Umbral efectivo = `min(supply, demanda)`; demanda incoherente → incidencia.
- **Modelo**: `source_data_contract_entity` += frescura por tabla (operator/value/unit, override del contrato); nueva **`business_process_input`** (weak de business_process; PK `[business_process_code, canonical_entity_code]` + max_staleness + is_blocking) = lo que el proceso lee aguas arriba. Sin catálogos nuevos.
- **Coordinación**: veredicto {SERVE,REFRESH,AWAIT,BREACH} → catálogo `REFRESH_DECISION` + campo en `run` se añaden en **OBSERVABILITY** (otra sesión).

