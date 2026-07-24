# ARRANQUE · Estructura organizativa + procesos de negocio

**Objetivo de la sesión:** cargar la **estructura organizativa** (`business_unit`) y sus **procesos de negocio** (`business_process`), y asociar cada proceso a los **términos de cada acelerador** que gobierna (vía `business_process_term`). Es **carga de instancias sobre tablas ya existentes**, no estructura nueva del metamodelo.

## Precondición (estado heredado)
- Metamodelo **cerrado y coherente** (v1.41, tras METADATO-16..65): 290 entidades, 2605 atributos, 133 catálogos (todos CONFIRMADO). METADATA 158 / OBSERVABILITY 132. Auditoría a cero: 0 bare, 0 catálogo inexistente, 0 FK colgantes, seed↔modelo 290=290.
- Metadato y Observabilidad se consideran **terminados**.

## Tablas sobre las que se trabaja (ya existen, no crear)
- `business_unit` (término ORG_STRUCTURE): organigrama por `parent_business_unit_code`; `business_unit_kind_code`→BUSINESS_UNIT_KIND; `is_governance_operator`; `topology_code`→GOVERNANCE_TOPOLOGY; `cost_center_code`.
- `business_process` (término BUSINESS_PROCESS): `business_unit_code` (unidad responsable), `parent_process_code`, `workflow_pattern_code`→workflow_pattern, `frequency_code`→FREQUENCY, `trigger_kind_code`→TRIGGER_KIND, `schedule_cron`.
- `business_process_term` (puente proceso↔término): asocia un `business_process` a uno o varios `business_term`.

## Árbol organizativo a cargar (business_unit)
```
Gobierno del dato            (raíz; is_governance_operator = true)
├── Governance Lead
│   ├── Metadato Manager
│   └── Data Quality Manager
└── Arquitectura del dato    (nivel técnico)
    └── Técnico del metadato
```

## Responsabilidad unidad → términos (PROPUESTA a confirmar con Pedro)
- **Metadato Manager** → definición del metadato a nivel de MODELO DE DATOS: `CANONICAL_ENTITY`, `BUSINESS_TERM`, `VIEWS`, `VERSIONING`, `COMMON_STRUCTURE`, `HIERARCHY` (GEO_STRUCTURE/TEMPORAL_STRUCTURE), `ORG_STRUCTURE`, `BUSINESS_PROCESS`.
- **Data Quality Manager** → calidad y evaluaciones: `DATA_QUALITY`, `ASSESSMENT_ENGINE`, `LIFECYCLE`.
- **Técnico del metadato** (bajo Arquitectura del dato) → lo técnico exclusivo del metadato + TODA la observabilidad y su carga: acelerador `OBSERVABILITY` completo (todos sus términos hijos de DATUM/UNITY_CATALOG), `DATABRICKS`, `LOAD_CANONICAL`, `ORCHESTRATION`.

> Nota: los términos de SECURITY, EXPOSURE, GDPR_DPO, DATA_AGREEMENTS, DOCUMENTATION, ANALYTICS, DATA_SOURCE, UX no están asignados en la propuesta anterior — decidir en la sesión a qué unidad/proceso corresponden (o si quedan fuera de este primer alcance).

## Decisiones a cerrar al arrancar
1. Confirmar/ajustar el mapeo unidad→término de arriba y cubrir los términos no asignados.
2. Granularidad de `business_process`: ¿un proceso por término, por grupo de términos, o por actividad (definir modelo / definir calidad / ejecutar assessment / cargar observabilidad)?
3. Valores de `BUSINESS_UNIT_KIND` y `GOVERNANCE_TOPOLOGY` para cada unidad; qué unidades son `is_governance_operator`.
4. `workflow_pattern`, `frequency` y `trigger` por defecto de los procesos (o dejarlos sin poblar en la primera carga).

## Protocolo
Arranque estándar: leer `99-METADATO-control.md` y `18-METADATO-decisiones.md` desde disco → confirmar estado → validar inventario → proponer agenda → ejecutar solo tras validación de Pedro. Carga sobre `seed` (business_unit → business_process → business_process_term). Registrar como decisión METADATO-n con "registro oficial". Propagar al visualizador y validar (0 FK colgantes; seed↔modelo).
