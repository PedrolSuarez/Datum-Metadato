# DATUM · Procesos y UDFs de la observabilidad — qué hay que gestionar

> Derivado del contrato de población (METADATO-47/48). La lista concreta es corta: **no son 61 procesos**, sino un puñado. Cada tabla declara en metadato cómo se alimenta (`population_mode_code`), así que esto se computa solo.

## Resumen (133 tablas de OBSERVABILITY)

| Modo de población | Nº | Qué hay que construir |
|---|---|---|
| RUNNER_TELEMETRY | 27 | Nada nuevo: lo emite el propio runner (instrumentación del harness) |
| GATE_UDF | 1 | **1 UDF** (el gate PRE_WRITE, ya diseñado en M-36) |
| DERIVED_SCHEDULED | 9 | **9 procesos programados** (definidos en M-49) |
| UC_VIEW | 4 | **4 vistas** sobre `uc_*` (definidas por M-48; falta compilar el SELECT) |
| SOURCE_INGEST | 72 | 1 ingesta (UC), **ya montada** en M-42/43 |
| APP_TRANSACTION | 20 | Nada: las escribe la aplicación / sistemas externos (no es pipeline DATUM) |

**Total a construir: 1 UDF + 9 procesos + 4 vistas.** El resto ya está o no es tuyo.

---

## A) La UDF (1)

| UDF | Produce | Dónde |
|---|---|---|
| Gate PRE_WRITE (FORMAT + MANDATORY) | `dq_column_incident` | UDF compilada por columna en STAGING (M-36). Emite una fila por columna con veredicto {PASS/WARNING/ERROR} y acción {CAST/DEFAULT_APPLIED/NORMALIZED/REJECTED}. Ya especificada. |

## B) Los procesos programados (9) — definidos en M-49

Cada uno = `business_process` (schedule) + `workflow_pattern` + step (runner). La **lógica de cómputo** (umbral, agregación) es el detalle que falta rellenar por proceso.

| Proceso | Produce | Runner | Cadencia | Lee de |
|---|---|---|---|---|
| `obs_dq_incident` | `dq_incident` | RUNNER_DQ | evento | `dq_run_result` fallidos sin auto-remediar |
| `obs_incident` | `incident` | RUNNER_KPI | horaria | `run_step`(ERROR) + `dq_incident` |
| `obs_alert` | `alert` | RUNNER_KPI | horaria | `run_step`, `dq_run_result`, `cost_anomaly` |
| `obs_cost_anomaly` | `cost_anomaly` | RUNNER_KPI | diaria | `uc_billing_usage` |
| `obs_budget_breach` | `budget_breach` | RUNNER_KPI | diaria | `uc_billing_usage` + presupuesto |
| `obs_metamodel_snapshot_run` | `metamodel_snapshot_run` | RUNNER_KPI | quincenal | el propio metamodelo (M-40) |
| `obs_platform_health_snapshot` | `platform_health_snapshot` | RUNNER_KPI | diaria | `run`/`run_step` + `dq_run_result` |
| `obs_datum_internal_kpi_value` | `datum_internal_kpi_value` | RUNNER_KPI | diaria | telemetría agregada |
| `obs_anomaly_detection` | `anomaly_detection` | RUNNER_KPI | diaria | `access_event` (vista sobre `uc_access_audit`) |

## C) Las vistas (4) — definidas por M-48, falta compilar el SELECT

| Vista | Sobre | Lógica |
|---|---|---|
| `access_event` | `uc_access_audit` | SELECT (passthrough; acceso solo por Databricks) |
| `access_event_aggregate` | `uc_access_audit` | agregación por principal × target × periodo |
| `resource_consumption` | `uc_billing_usage` | SELECT (consumo técnico por recurso/periodo) |
| `cost_aggregate` | `uc_billing_usage` | agregación por dimensión funcional (chargeback) |

## D) Telemetría del runner (27) — NO es un proceso, es el harness

El runner escribe su propia observabilidad al ejecutar. Declarado en `runner_capability.emits_observability_entity`:

| Runner | Emite |
|---|---|
| RUNNER_INGEST | `source_discovery_run` (+ los 4 discovery-obs) |
| RUNNER_DQ / _TERM / _PROCESS | `dq_run_result` (+ `dq_run_failed_records`) |
| RUNNER_LOAD_CANONICAL | `golden_record_*` |
| RUNNER_KPI / _HIERARCHY / _PROCESS | `datum_internal_kpi_value` |
| Orquestador (harness) | `run` / `run_step` / `run_term` / `run_entity` |

Lo único a construir aquí es la **instrumentación de emisión en el framework de runners** (una vez, dirigida por metadato) — no un proceso por tabla.

## E) Escritas por la app / sistemas externos (20) — NO son pipeline DATUM

`data_subject`, `consent_record`, `consent_evidence`, `consent_withdrawal`, `data_subject_request`, `dsr_action`, `dsr_response`, `data_breach` (app DPO/consentimiento); `support_ticket`, `incident_action`, `incident_post_mortem`, `breaking_change_notification`, `committee_session`, `reactivation_request`, `access_review_finding` (gobierno/ticketing); `api_call`, `ui_navigation`, `export_event`, `communication_sent`, `policy_evaluation_log` (gateway/app).

Estas las escribe quien opera (la app, el sistema de tickets, el gateway), no un runner DATUM. Si algún sistema externo debe volcarse, sería una **ingesta** tipo UC (source→canonical), no un proceso de derivación.
