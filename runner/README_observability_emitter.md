# runner/observability_emitter — Emisor de observabilidad (plataforma, NO metadato)

> Componente de plataforma, escrito una vez, que puebla la observabilidad de tipo **RUNNER_TELEMETRY** (`run`, `run_step`, `run_term`, `run_entity` + la telemetría de dominio de cada runner). Regla de oro: cambiar comportamiento = cambiar metadato (`runner_capability`), no este código.

## Qué NO es
- **No es un INSERT por runner.** Duplicaría código en los 9 runners y rompería "el runner no cambia".
- **No es una UDF.** Las UDF transforman valores fila a fila dentro del SQL (p.ej. el gate `dq_column_incident`, M-36). Registrar el ciclo de una corrida es una escritura de frontera de ejecución, no una operación por-fila.

## Qué es
Un **emisor genérico** en el harness (orquestador / clase base de runner), invocado en *hooks* de ciclo de vida. Todos los runners lo heredan por ejecutarse dentro del harness.

## Hooks de ciclo de vida
| Hook | Escritura | Tabla |
|---|---|---|
| `on_run_start` | INSERT (status=RUNNING, started_at, root/parent_run_id, execution_level, linked_business_process, trigger_type, ingested_at) | `run` |
| `on_step_start` | INSERT (status=RUNNING, runner_type, linked_canonical_entity, sequence_order) | `run_step` |
| `on_step_end` | MERGE (status final, ended_at, duration, records_read/processed/failed, crossing_result) | `run_step` |
| `on_run_end` | MERGE (status final, métricas agregadas, ended_at) | `run` |

`run_term` / `run_entity` se emiten desde `on_step_end` cuando el step toca un término/entidad canónica.

## Dirigido por metadato
- **`run`/`run_step`** = telemetría **universal del harness** (no de un `runner_type` concreto): siempre se emiten.
- **Telemetría de dominio** = el emisor lee **`runner_capability.emits_observability_entity`** para saber qué añade cada runner al terminar su trabajo, y la escribe con el mismo mecanismo:
  - `RUNNER_INGEST` → `source_discovery_run` (+ los 4 discovery-obs)
  - `RUNNER_DQ` / `_TERM` / `_PROCESS` → `dq_run_result` (+ `dq_run_failed_records`)
  - `RUNNER_LOAD_CANONICAL` → `golden_record_fusion` (+ match/contribution)
  - `RUNNER_KPI` / `_HIERARCHY` / `_PROCESS` → `datum_internal_kpi_value`
- Añadir un runner o una observabilidad nueva = **una fila de `runner_capability`**, no código de emisión.

## Semántica de escritura
- `run` / `run_step`: **INSERT al abrir + MERGE al cerrar** (append inmutable de la traza; el MERGE solo completa el cierre, no reescribe historia). Coherente con `population_mode=RUNNER_TELEMETRY` y `is_append_only=1`.
- La telemetría de dominio (`dq_run_result`, `golden_record_*`…): **append**.
- Autocontenido (M-35): el emisor nunca rompe el circuito — si falla la escritura de traza, registra y avisa; el estado del run refleja COMPLETED_WITH_* / ERROR.

## Frontera con los otros modos de población
- **GATE_UDF** (`dq_column_incident`): NO lo emite este componente; es la UDF compilada del gate PRE_WRITE.
- **DERIVED_SCHEDULED** (dq_incident, cost_anomaly…): procesos programados propios (M-49), no el emisor.
- **UC_VIEW / SOURCE_INGEST / APP_TRANSACTION**: fuera del emisor (vistas, ingesta UC, escrituras de app).
