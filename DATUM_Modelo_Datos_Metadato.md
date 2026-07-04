# DATUM · Modelo de Datos del Metadato

> Fuente única del metamodelo. Total entidades: **194**.
> Generado desde `DATUM_Modelo_Datos_Metadato.json`. Estructura: dominio → subdominio → entidad → atributos.

## D0  (31 entidades)

### D00 · Implementación física catálogos  (4)

#### `physical_catalog`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| storage_layer_code | TYD_CODE |  | storage_layer |  |
| storage_location_code | TYD_CODE |  | storage_location |  |
| physical_name | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value | RECORD_STATUS ⚙︎ |
| assigned_catalog_code | TYD_CODE |  | physical_catalog |  |
| assigned_schema_code | TYD_CODE |  | physical_schema |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `physical_schema`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| physical_catalog_code | TYD_CODE | 🔑 | physical_catalog |  |
| code | TYD_CODE | 🔑 |  |  |
| physical_name | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value | RECORD_STATUS ⚙︎ |
| assigned_catalog_code | TYD_CODE |  | physical_catalog |  |
| assigned_schema_code | TYD_CODE |  | physical_schema |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `storage_layer`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| bucket_uri_location | TYD_URL |  |  |  |
| sort_order | TYD_INT |  |  |  |
| assigned_catalog_code | TYD_CODE |  | physical_catalog |  |
| assigned_schema_code | TYD_CODE |  | physical_schema |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `storage_location`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| storage_layer_code | TYD_CODE |  | storage_layer |  |
| container_path | TYD_STRING |  |  |  |
| status_code | TYD_CODE |  | reference_value | RECORD_STATUS ⚙︎ |
| assigned_catalog_code | TYD_CODE |  | physical_catalog |  |
| assigned_schema_code | TYD_CODE |  | physical_schema |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D01 · Catálogos de datos  (4)

#### `metamodel_domain` — 🔶 CUARENTENA

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| code_alpha | TYD_NAME |  |  |  |
| schema_name | TYD_CODE |  |  |  |
| sort_order | TYD_INT |  |  |  |
| is_substrate | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `reference_catalog`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| category_code | TYD_CODE |  | reference_category |  |
| is_ordered | TYD_BOOLEAN |  |  |  |
| min_active_values | TYD_INT |  |  |  |
| external_authority_code | TYD_CODE |  | STANDARD_AUTHORITY |  |
| external_standard_ref | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `reference_category` — 🔶 CUARENTENA

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| metamodel_domain_code | TYD_CODE |  | metamodel_domain |  |
| sort_order | TYD_INT |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `reference_value`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| reference_catalog_code | TYD_CODE | 🔑 | reference_catalog |  |
| code | TYD_CODE | 🔑 |  |  |
| sort_order | TYD_INT |  |  |  |
| is_default | TYD_BOOLEAN |  |  |  |
| is_terminal | TYD_BOOLEAN |  |  |  |
| valid_from | TYD_DATE |  |  |  |
| valid_to | TYD_DATE |  |  |  |
| external_code | TYD_CODE |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D02 · Tipos de datos  (7)

#### `data_type_domain_composite`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| materialization_code | TYD_CODE |  | reference_value |  |
| classification_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_type_domain_dq_rule`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_type_domain_code | TYD_CODE | 🔑 | data_type_domain_simple |  |
| dq_rule_code | TYD_CODE | 🔑 | dq_rule |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_type_domain_field`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| composite_code | TYD_CODE | 🔑 | data_type_domain_composite |  |
| field_code | TYD_CODE | 🔑 |  |  |
| referenced_simple_code | TYD_CODE |  | data_type_domain_simple |  |
| is_required | TYD_BOOLEAN |  |  |  |
| cardinality_code | TYD_CODE |  | reference_value |  |
| sort_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_type_domain_simple`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| parent_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| generic_type_code | TYD_CODE |  | generic_data_type |  |
| max_length | TYD_INT |  |  |  |
| precision | TYD_INT |  |  |  |
| scale | TYD_INT |  |  |  |
| regex_pattern | TYD_REGEX_PATTERN |  |  |  |
| classification_code | TYD_CODE |  | reference_value |  |
| is_pii_by_default | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_type_domain_ui_control`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_type_domain_code | TYD_CODE | 🔑 | data_type_domain_simple |  |
| ui_context_code | TYD_CODE | 🔑 | reference_value |  |
| ui_control_code | TYD_CODE |  | reference_value |  |
| is_overridable | TYD_BOOLEAN |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_type_mapping`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| generic_type_code | TYD_CODE | 🔑 | generic_data_type |  |
| technology_code | TYD_CODE | 🔑 | technology |  |
| data_type_code | TYD_CODE |  | data_type |  |
| audit | TYD_AUDIT |  |  |  |

#### `generic_data_type`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D03 · Multiidioma (i18n)  (3)

#### `object_text`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| object_type_code | TYD_CODE | 🔑 | object_type |  |
| text_field_kind_code | TYD_CODE | 🔑 | text_field_kind |  |
| language_code | TYD_CODE | 🔑 | language |  |
| content | TYD_TEXT_DESCRIPTION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `object_type`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `text_field_kind`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| sort_order | TYD_INT |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D04 · Códigos ISO  (5)

#### `country`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| code_alpha3 | TYD_CODE |  |  |  |
| numeric_code | TYD_INT |  |  |  |
| primary_currency_code | TYD_CODE |  | currency |  |
| primary_language_code | TYD_CODE |  | language |  |
| phone_prefix | TYD_CODE |  |  |  |
| tld | TYD_CODE |  |  |  |
| continent_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `country_subdivision`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| country_code | TYD_CODE |  | country |  |
| parent_subdivision_code | TYD_CODE |  | country_subdivision |  |
| subdivision_category_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `currency`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| numeric_code | TYD_INT |  |  |  |
| symbol | TYD_UI_LABEL |  |  |  |
| decimal_places | TYD_INT |  |  |  |
| is_active_globally | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `language`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| code_iso_639_3 | TYD_CODE |  |  |  |
| native_name | TYD_NAME |  |  |  |
| direction_code | TYD_CODE |  |  |  |
| is_active_in_datum | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `unit_of_measure`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| category_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D05 · Configuración física de tabla  (4)

#### `config_pattern`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `config_pattern_delta_default`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| config_pattern_code | TYD_CODE | 🔑 | config_pattern |  |
| delta_property_code | TYD_CODE | 🔑 | delta_property |  |
| property_value | TYD_EXPRESSION |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `delta_property`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| value_logical_type_code | TYD_CODE |  | reference_value |  |
| allowed_values_reference_catalog_code | TYD_CODE |  | reference_catalog |  |
| technical_default | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `object_delta_override`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| object_type_code | TYD_CODE | 🔑 | object_type |  |
| layer_code | TYD_CODE | 🔑 | reference_value |  |
| delta_property_code | TYD_CODE | 🔑 | delta_property |  |
| property_value | TYD_EXPRESSION |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D06 · Versión y aprobación  (2)

#### `object_approval`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| object_type_code | TYD_CODE | 🔑 | object_type |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| requested_at | TYD_TIMESTAMP |  |  |  |
| decided_at | TYD_TIMESTAMP |  |  |  |
| approver_role_code | TYD_CODE |  | reference_value |  |
| is_current | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `object_version`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| object_type_code | TYD_CODE | 🔑 | object_type |  |
| version_number | TYD_INT | 🔑 |  |  |
| version_status_code | TYD_CODE |  | reference_value |  |
| is_current | TYD_BOOLEAN |  |  |  |
| valid_from | TYD_TIMESTAMP |  |  |  |
| valid_to | TYD_TIMESTAMP |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D07 · Patrones de workflow  (2)

#### `workflow_pattern`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| purpose_code | TYD_CODE |  | reference_value |  |
| is_automated | TYD_BOOLEAN |  |  |  |
| sla_total_minutes | TYD_INT |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `workflow_pattern_step`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| workflow_pattern_code | TYD_CODE | 🔑 | workflow_pattern |  |
| code | TYD_CODE | 🔑 |  |  |
| sequence_order | TYD_INT |  |  |  |
| runner_type_code | TYD_CODE |  | reference_value |  |
| is_optional | TYD_BOOLEAN |  |  |  |
| is_parallel_with_previous | TYD_BOOLEAN |  |  |  |
| sla_minutes | TYD_INT |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D1  (5 entidades)

### E · Reglas de negocio  (1)

#### `business_rule`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| subject_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| subject_object_type_code | TYD_CODE |  | object_type |  |
| rule_kind_code | TYD_CODE |  | reference_value |  |
| declared_value | TYD_EXPRESSION |  |  |  |
| severity_code | TYD_CODE |  | reference_value |  |
| maturity_dimension_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### Organización (organigrama real)  (2)

#### `business_unit`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| parent_business_unit_code | TYD_CODE |  | business_unit |  |
| business_unit_kind_code | TYD_CODE |  | reference_value |  |
| is_governance_operator | TYD_BOOLEAN |  |  |  |
| is_critical | TYD_BOOLEAN |  |  |  |
| maturity_level_code | TYD_CODE |  | reference_value |  |
| maturity_target_code | TYD_CODE |  | reference_value |  |
| topology_code | TYD_CODE |  | reference_value |  |
| cost_center_code | TYD_CODE |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `business_unit_role_assignment`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| business_unit_code | TYD_CODE | 🔑 | business_unit |  |
| role_profile_code | TYD_CODE | 🔑 | reference_value |  |
| idp_role_ref | TYD_NAME |  |  |  |
| valid_from | TYD_DATE |  |  |  |
| valid_to | TYD_DATE |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### Procesos  (2)

#### `business_process`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| parent_process_code | TYD_CODE |  | business_process |  |
| business_unit_code | TYD_CODE |  | business_unit |  |
| workflow_pattern_code | TYD_CODE |  | workflow_pattern |  |
| is_critical | TYD_BOOLEAN |  |  |  |
| frequency_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `business_process_term`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| business_process_code | TYD_CODE | 🔑 | business_process |  |
| business_term_code | TYD_CODE | 🔑 | business_term |  |
| audit | TYD_AUDIT |  |  |  |

## D2  (31 entidades)

### A.bis · BK hash / desanonimización  (2)

#### `canonical_entity_bk_alias`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| previous_hash | TYD_BK_HASH | 🔑 |  |  |
| current_hash | TYD_BK_HASH |  |  |  |
| change_reason_code | TYD_CODE |  | reference_value |  |
| previous_bk_in_clear_encrypted | TYD_ENCRYPTED |  |  |  |
| current_bk_in_clear_encrypted | TYD_ENCRYPTED |  |  |  |
| changed_at | TYD_TIMESTAMP |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_entity_bk_lookup_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| lookup_strategy_code | TYD_CODE |  | reference_value |  |
| physical_catalog_code | TYD_CODE |  | physical_catalog |  |
| physical_schema_code | TYD_CODE |  | physical_schema |  |
| physical_table_name | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D20 · Términos de Negocio  (6)

#### `business_term`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| owner_business_domain_code | TYD_CODE |  | business_domain |  |
| parent_term_code | TYD_CODE |  | business_term |  |
| is_pii_related | TYD_BOOLEAN |  |  |  |
| is_regulatory | TYD_BOOLEAN |  |  |  |
| regulatory_reference | TYD_TEXT_SUMMARY |  |  |  |
| approved_by_committee_at | TYD_DATE |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `business_term_canonical_entity` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| business_term_code | TYD_CODE | 🔑 | business_term |  |
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| role_code | TYD_CODE |  | reference_value |  |
| is_primary | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `business_term_related`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_term_code | TYD_CODE | 🔑 | business_term |  |
| target_term_code | TYD_CODE | 🔑 | business_term |  |
| relation_type_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

#### `business_term_synonym`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| business_term_code | TYD_CODE | 🔑 | business_term |  |
| synonym | TYD_NAME | 🔑 |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_attribute_business_term` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| business_term_code | TYD_CODE | 🔑 | business_term |  |
| mapping_kind_code | TYD_CODE |  | reference_value |  |
| is_essential | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D21 · Entidad Canónica  (10)

#### `canonical_attribute`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| code | TYD_CODE | 🔑 |  |  |
| attribute_order | TYD_INT |  |  |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| materialization_mode_code | TYD_CODE |  | reference_value |  |
| referenced_entity_code | TYD_CODE |  | canonical_entity |  |
| physical_column_name | TYD_NAME |  |  |  |
| is_pii | TYD_BOOLEAN |  |  |  |
| is_sensitive | TYD_BOOLEAN |  |  |  |
| security_classification_code | TYD_CODE |  | reference_value |  |
| is_nullable | TYD_BOOLEAN |  |  |  |
| is_unique | TYD_BOOLEAN |  |  |  |
| column_default | TYD_EXPRESSION |  |  |  |
| is_auto_increment | TYD_BOOLEAN |  |  |  |
| is_generated | TYD_BOOLEAN |  |  |  |
| generation_expression | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_attribute_constraint`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| code | TYD_CODE | 🔑 |  |  |
| constraint_type_code | TYD_CODE |  | reference_value |  |
| expression | TYD_TEXT_SUMMARY |  |  |  |
| min_value | TYD_TEXT_SUMMARY |  |  |  |
| max_value | TYD_TEXT_SUMMARY |  |  |  |
| allowed_values_reference_catalog_code | TYD_CODE |  | reference_catalog |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_entity`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| business_term_code | TYD_CODE |  | business_term |  |
| config_pattern_code | TYD_CODE |  | config_pattern |  |
| physical_catalog_code | TYD_CODE |  | physical_catalog |  |
| physical_schema_code | TYD_CODE |  | physical_schema |  |
| is_pii | TYD_BOOLEAN |  |  |  |
| is_sensitive | TYD_BOOLEAN |  |  |  |
| security_classification_code | TYD_CODE |  | reference_value |  |
| estimated_annual_volume | TYD_BIGINT_VOLUME |  |  |  |
| access_frequency_code | TYD_CODE |  | reference_value |  |
| canonical_accelerator_code | TYD_CODE |  | canonical_accelerator |  |
| lifecycle_state_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_entity_constraint`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| code | TYD_CODE | 🔑 |  |  |
| constraint_type_code | TYD_CODE |  | reference_value |  |
| expression | TYD_EXPRESSION |  |  |  |
| error_message_text | TYD_TEXT_SUMMARY |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_entity_constraint_attribute`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_constraint_code | TYD_CODE | 🔑 | canonical_entity_constraint |  |
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| position_in_constraint | TYD_INT |  |  |  |
| role_in_expression_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_key`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| code | TYD_CODE | 🔑 |  |  |
| key_type_code | TYD_CODE |  | reference_value |  |
| is_used_for_matching | TYD_BOOLEAN |  |  |  |
| referenced_entity_code | TYD_CODE |  | canonical_entity |  |
| referenced_key_code | TYD_CODE |  | canonical_key |  |
| on_delete_action_code | TYD_CODE |  | reference_value |  |
| on_update_action_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_key_attribute`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_key_code | TYD_CODE | 🔑 | canonical_key |  |
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| referenced_attribute_code | TYD_CODE |  | canonical_attribute |  |
| position_in_key | TYD_INT |  |  |  |
| is_descending | TYD_BOOLEAN |  |  |  |
| partition_transform | TYD_EXPRESSION |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_relation` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| relation_kind_code | TYD_CODE |  | reference_value |  |
| source_canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| target_canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| is_identifying | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_relation_attribute_map` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_relation_code | TYD_CODE | 🔑 | canonical_relation |  |
| source_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| target_attribute_code | TYD_CODE |  | canonical_attribute |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_relation_end` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_relation_code | TYD_CODE | 🔑 | canonical_relation |  |
| end_role_code | TYD_CODE | 🔑 | reference_value |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| cardinality_max | TYD_CODE |  | reference_value |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### E · Consumo desde organización (D1→D2)  (1)

#### `canonical_entity_business_process` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| business_process_code | TYD_CODE | 🔑 | business_process |  |
| role_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### F · Versionado del modelo  (3)

#### `canonical_attribute_version` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| version_label | TYD_NAME | 🔑 |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| is_current | TYD_BOOLEAN |  |  |  |
| change_reason | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_entity_version` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_entity_code | TYD_CODE | 🔑 | canonical_entity |  |
| version_label | TYD_NAME | 🔑 |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| is_current | TYD_BOOLEAN |  |  |  |
| change_reason | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_model_change` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| change_kind_code | TYD_CODE |  | reference_value |  |
| target_entity_code | TYD_CODE |  | canonical_entity |  |
| target_attribute_code | TYD_CODE |  | canonical_attribute |  |
| is_breaking | TYD_BOOLEAN |  |  |  |
| announced_at | TYD_TIMESTAMP |  |  |  |
| description | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### G · Vistas canónicas / expresión  (5)

#### `canonical_view`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| owner_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| owner_object_type_code | TYD_CODE |  | object_type |  |
| business_process_code | TYD_CODE |  | business_process |  |
| business_term_code | TYD_CODE |  | business_term |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| view_kind_code | TYD_CODE |  | reference_value |  |
| target_layer_code | TYD_CODE |  | reference_value |  |
| write_mode_code | TYD_CODE |  | reference_value |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `expression`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| owner_object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| owner_object_type_code | TYD_CODE | 🔑 | object_type |  |
| code | TYD_CODE | 🔑 |  |  |
| expression_type_code | TYD_CODE |  | reference_value |  |
| root_node_code | TYD_CODE |  | expression_node |  |
| audit | TYD_AUDIT |  |  |  |

#### `expression_node`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| expression_code | TYD_CODE | 🔑 | expression |  |
| code | TYD_CODE | 🔑 |  |  |
| parent_node_code | TYD_CODE |  | expression_node |  |
| node_kind_code | TYD_CODE |  | reference_value |  |
| operator_code | TYD_CODE |  | reference_value |  |
| function_code | TYD_CODE |  | function_catalog |  |
| node_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `expression_operand`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| expression_node_code | TYD_CODE | 🔑 | expression_node |  |
| operand_order | TYD_INT | 🔑 |  |  |
| operand_kind_code | TYD_CODE |  | reference_value |  |
| source_attribute_code | TYD_CODE |  | source_attribute |  |
| canonical_attribute_code | TYD_CODE |  | canonical_attribute |  |
| literal_value | TYD_EXPRESSION |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `function_catalog`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| arity | TYD_INT |  |  |  |
| return_logical_type_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### G2 · Lifecycle  (2)

#### `lifecycle_phase_approval_rule` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| lifecycle_policy_code | TYD_CODE | 🔑 | lifecycle_policy |  |
| phase_code | TYD_CODE | 🔑 | reference_value |  |
| approver_role_code | TYD_CODE |  | reference_value |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `lifecycle_policy` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| retention_days | TYD_INT |  |  |  |
| archive_after_days | TYD_INT |  |  |  |
| purge_after_days | TYD_INT |  |  |  |
| requires_approval | TYD_BOOLEAN |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### H · Extensibilidad  (2)

#### `canonical_attribute_attribute` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| canonical_attribute_code | TYD_CODE |  | canonical_attribute |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_entity_attribute` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `canonical_accelerator` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| accelerator_version | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value | RECORD_STATUS ⚙︎ |
| entity_count | TYD_INT |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D3  (43 entidades)

### A · Sistemas y conexiones  (4)

#### `source_connection` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_system_code | TYD_CODE |  | source_system |  |
| connection_protocol_code | TYD_CODE |  | reference_value |  |
| host | TYD_NAME |  |  |  |
| port | TYD_INT |  |  |  |
| landing_strategy_code | TYD_CODE |  | reference_value |  |
| schema_detection_mode_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_connection_credential` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_connection_code | TYD_CODE |  | source_connection |  |
| credential_kind_code | TYD_CODE |  | reference_value |  |
| key_vault_reference | TYD_NAME |  |  |  |
| valid_from | TYD_TIMESTAMP |  |  |  |
| valid_until | TYD_TIMESTAMP |  |  |  |
| rotation_period_days | TYD_INT |  |  |  |
| custodian_role_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_connection_token_state` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_connection_code | TYD_CODE | 🔑 | source_connection |  |
| token_kind_code | TYD_CODE |  | reference_value |  |
| issued_at | TYD_TIMESTAMP |  |  |  |
| expires_at | TYD_TIMESTAMP |  |  |  |
| key_vault_reference | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_system`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| system_kind_code | TYD_CODE |  | reference_value |  |
| technology_code | TYD_CODE |  | technology |  |
| business_unit_code | TYD_CODE |  | business_unit |  |
| connection_secret_ref | TYD_TEXT_SUMMARY |  |  |  |
| environment_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### B · Entidades y atributos  (2)

#### `source_attribute`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| code | TYD_CODE | 🔑 |  |  |
| attribute_order | TYD_INT |  |  |  |
| native_type | TYD_NAME |  |  |  |
| logical_type_code | TYD_CODE |  | reference_value |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| is_nullable | TYD_BOOLEAN |  |  |  |
| is_primary_key | TYD_BOOLEAN |  |  |  |
| is_unique | TYD_BOOLEAN |  |  |  |
| native_default | TYD_TEXT_SUMMARY |  |  |  |
| is_pii_detected | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_system_code | TYD_CODE | 🔑 | source_system |  |
| code | TYD_CODE | 🔑 |  |  |
| parent_source_entity_code | TYD_CODE |  | source_entity |  |
| entity_kind_code | TYD_CODE |  | reference_value |  |
| is_container | TYD_BOOLEAN |  |  |  |
| is_capturable | TYD_BOOLEAN |  |  |  |
| is_golden_source | TYD_BOOLEAN |  |  |  |
| config_pattern_code | TYD_CODE |  | config_pattern |  |
| completeness_status_code | TYD_CODE |  | reference_value |  |
| discovered_at | TYD_TIMESTAMP |  |  |  |
| file_format_code | TYD_CODE |  | reference_value |  |
| file_path_pattern | TYD_TEXT_SUMMARY |  |  |  |
| file_sheet_name | TYD_NAME |  |  |  |
| file_delimiter | TYD_NAME |  |  |  |
| api_path_template | TYD_TEXT_SUMMARY |  |  |  |
| stream_topic_name | TYD_NAME |  |  |  |
| db_object_type_code | TYD_CODE |  | reference_value |  |
| is_in_scope | TYD_BOOLEAN |  |  |  |
| scope_reason_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### C · Especialización por tipo  (11)

#### `multi_record` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| record_discriminator_field | TYD_NAME |  |  |  |
| record_type_value | TYD_NAME | 🔑 |  |  |
| record_layout | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_api_endpoint_parameter` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| param_name | TYD_NAME | 🔑 |  |  |
| param_location_code | TYD_CODE |  | reference_value |  |
| param_data_type_code | TYD_CODE |  | reference_value |  |
| is_required | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_api_graphql_query` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| query_text | TYD_EXPRESSION |  |  |  |
| operation_name | TYD_NAME |  |  |  |
| response_root_path | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_api_soap_operation` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| wsdl_url | TYD_NAME |  |  |  |
| operation_name | TYD_NAME |  |  |  |
| soap_action | TYD_NAME |  |  |  |
| namespace | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_archive_container` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| archive_format_code | TYD_CODE |  | reference_value |  |
| encoding | TYD_NAME |  |  |  |
| member_pattern | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_api_endpoint` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| http_method_code | TYD_CODE |  | reference_value |  |
| endpoint_path | TYD_NAME |  |  |  |
| pagination_kind_code | TYD_CODE |  | reference_value |  |
| response_root_path | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_database` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| database_name | TYD_NAME |  |  |  |
| schema_name | TYD_NAME |  |  |  |
| object_name | TYD_NAME |  |  |  |
| object_kind_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_excel_workbook` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| sheet_name | TYD_NAME |  |  |  |
| header_row | TYD_INT |  |  |  |
| cell_range | TYD_NAME |  |  |  |
| sheet_purpose_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_file` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| file_path | TYD_NAME |  |  |  |
| file_format_code | TYD_CODE |  | reference_value |  |
| encoding | TYD_NAME |  |  |  |
| has_header | TYD_BOOLEAN |  |  |  |
| delimiter | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_stream_topic` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| topic_name | TYD_NAME |  |  |  |
| serialization_format_code | TYD_CODE |  | reference_value |  |
| schema_registry_reference | TYD_NAME |  |  |  |
| consumer_group | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_webhook` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| event_kind | TYD_NAME |  |  |  |
| callback_path | TYD_NAME |  |  |  |
| signature_verification_kind_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Claves y constraints de origen  (2)

#### `source_key`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| code | TYD_CODE | 🔑 |  |  |
| key_type_code | TYD_CODE |  | reference_value |  |
| referenced_source_entity_code | TYD_CODE |  | source_entity |  |
| is_discovered | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_key_attribute`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_key_code | TYD_CODE | 🔑 | source_key |  |
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| referenced_source_attribute_code | TYD_CODE |  | source_attribute |  |
| position_in_key | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Golden source y vínculo  (4)

#### `golden_source` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| business_term_code | TYD_CODE |  | business_term |  |
| source_entity_code | TYD_CODE |  | source_entity |  |
| is_golden_source | TYD_BOOLEAN |  |  |  |
| precedence | TYD_INT |  |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| ratified_by_committee | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_business_term` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| business_term_code | TYD_CODE | 🔑 | business_term |  |
| coverage_kind_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_canonical_entity_hint` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| confidence_score_pct | TYD_INT |  |  |  |
| is_confirmed | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_relation` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| left_source_entity_code | TYD_CODE |  | source_entity |  |
| right_source_entity_code | TYD_CODE |  | source_entity |  |
| relation_kind_code | TYD_CODE |  | reference_value |  |
| join_expression | TYD_EXPRESSION |  |  |  |
| semantic_role | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### E · Captura  (2)

#### `source_entity_capture_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| capture_mode_code | TYD_CODE |  | reference_value |  |
| landing_strategy_code | TYD_CODE |  | reference_value |  |
| incremental_watermark_attribute_code | TYD_CODE |  | source_attribute |  |
| cdc_mechanism_code | TYD_CODE |  | reference_value |  |
| schedule_cron | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_partition_strategy`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| partition_attribute_code | TYD_CODE |  | source_attribute |  |
| partition_transform | TYD_EXPRESSION |  |  |  |
| partition_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### F · Discovery y drift  (2)

#### `source_discovery_drift` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_discovery_run_code | TYD_CODE |  | source_discovery_run |  |
| source_entity_code | TYD_CODE |  | source_entity |  |
| drift_kind_code | TYD_CODE |  | reference_value |  |
| severity_code | TYD_CODE |  | reference_value |  |
| acceptance_status_code | TYD_CODE |  | reference_value |  |
| detail | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_discovery_run` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_system_code | TYD_CODE |  | source_system |  |
| started_at | TYD_TIMESTAMP |  |  |  |
| finished_at | TYD_TIMESTAMP |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| detection_mode_code | TYD_CODE |  | reference_value |  |
| entities_discovered | TYD_INT |  |  |  |
| triggered_by_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### G · Calidad en origen  (1)

#### `source_attribute_quality_hint` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| quality_dimension_code | TYD_CODE | 🔑 | reference_value |  |
| hint_value | TYD_NAME |  |  |  |
| declared_by_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### H · Versionado  (2)

#### `source_attribute_version` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| version_label | TYD_NAME | 🔑 |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| is_current | TYD_BOOLEAN |  |  |  |
| change_reason | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_entity_version` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| version_label | TYD_NAME | 🔑 |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| is_current | TYD_BOOLEAN |  |  |  |
| change_reason | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### J · Discovery completo y profiling  (6)

#### `discovery_rule` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| rule_kind_code | TYD_CODE |  | reference_value |  |
| target_data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| rule_expression | TYD_EXPRESSION |  |  |  |
| is_enabled | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `discovery_rule_evaluation` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| discovery_rule_code | TYD_CODE | 🔑 | discovery_rule |  |
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| source_discovery_run_code | TYD_CODE | 🔑 | source_discovery_run |  |
| matched | TYD_BOOLEAN |  |  |  |
| score_pct | TYD_INT |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_attribute_detected_type_domain` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| confidence_score_pct | TYD_INT |  |  |  |
| is_confirmed | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_attribute_profile` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| profiled_at | TYD_TIMESTAMP | 🔑 |  |  |
| null_count | TYD_INT |  |  |  |
| distinct_count | TYD_INT |  |  |  |
| min_value | TYD_NAME |  |  |  |
| max_value | TYD_NAME |  |  |  |
| top_n_values | TYD_NAME |  |  |  |
| pii_detected | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_discovery_config` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_system_code | TYD_CODE |  | source_system |  |
| discovery_frequency_hours | TYD_INT |  |  |  |
| profiling_depth_code | TYD_CODE |  | reference_value |  |
| pii_auto_detection | TYD_BOOLEAN |  |  |  |
| is_enabled | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_discovery_sampling_result` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_discovery_run_code | TYD_CODE | 🔑 | source_discovery_run |  |
| source_entity_code | TYD_CODE | 🔑 | source_entity |  |
| rows_sampled | TYD_INT |  |  |  |
| sample_strategy_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### K · Data contracts (UNE)  (2)

#### `source_data_contract`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_system_code | TYD_CODE |  | source_system |  |
| contract_status_code | TYD_CODE |  | reference_value |  |
| valid_from | TYD_TIMESTAMP |  |  |  |
| valid_to | TYD_TIMESTAMP |  |  |  |
| responsibilities_text | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `source_data_contract_sla`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_data_contract_code | TYD_CODE | 🔑 | source_data_contract |  |
| sla_type_code | TYD_CODE | 🔑 | reference_value |  |
| target_value | TYD_TEXT_SUMMARY |  |  |  |
| breach_action_text | TYD_TEXT_SUMMARY |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### Runners  (3)

#### `runner_discover` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| runner_kind_code | TYD_CODE |  | reference_value |  |
| source_system_code | TYD_CODE |  | source_system |  |
| schedule_cron | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `runner_ingest_managed` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| runner_kind_code | TYD_CODE |  | reference_value |  |
| source_system_code | TYD_CODE |  | source_system |  |
| schedule_cron | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `runner_ingest_streaming` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| runner_kind_code | TYD_CODE |  | reference_value |  |
| source_system_code | TYD_CODE |  | source_system |  |
| schedule_cron | TYD_NAME |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### Tipos de datos  (2)

#### `data_type`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| technology_code | TYD_CODE | 🔑 | technology |  |
| code | TYD_CODE | 🔑 |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `technology`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| category_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D4  (24 entidades)

### A · Reglas  (2)

#### `transformation_rule`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| transformation_type_code | TYD_CODE |  | reference_value |  |
| is_deterministic | TYD_BOOLEAN |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `transformation_rule_parameter`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_rule_code | TYD_CODE | 🔑 | transformation_rule |  |
| code | TYD_CODE | 🔑 |  |  |
| logical_type_code | TYD_CODE |  | reference_value |  |
| is_required | TYD_BOOLEAN |  |  |  |
| default_value | TYD_EXPRESSION |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### B · Mappings  (5)

#### `mapping_condition` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_mapping_code | TYD_CODE | 🔑 | transformation_mapping |  |
| condition_order | TYD_INT | 🔑 |  |  |
| condition_kind_code | TYD_CODE |  | reference_value |  |
| join_type_code | TYD_CODE |  | reference_value |  |
| left_source_entity_code | TYD_CODE |  | source_entity |  |
| right_source_entity_code | TYD_CODE |  | source_entity |  |
| source_entity_relation_code | TYD_CODE |  | source_entity_relation |  |
| condition_expression | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `mapping_input` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_mapping_code | TYD_CODE | 🔑 | transformation_mapping |  |
| input_order | TYD_INT | 🔑 |  |  |
| source_entity_code | TYD_CODE |  | source_entity |  |
| source_attribute_code | TYD_CODE |  | source_attribute |  |
| role_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `mapping_output` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_mapping_code | TYD_CODE | 🔑 | transformation_mapping |  |
| output_order | TYD_INT | 🔑 |  |  |
| canonical_attribute_code | TYD_CODE |  | canonical_attribute |  |
| output_expression | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `mapping_parameter_value` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_mapping_code | TYD_CODE | 🔑 | transformation_mapping |  |
| transformation_rule_parameter_code | TYD_CODE | 🔑 | transformation_rule_parameter |  |
| param_value | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `transformation_mapping` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| transformation_rule_code | TYD_CODE |  | transformation_rule |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| canonical_attribute_code | TYD_CODE |  | canonical_attribute |  |
| primary_source_entity_code | TYD_CODE |  | source_entity |  |
| application_point_code | TYD_CODE |  | reference_value |  |
| implementation_kind_code | TYD_CODE |  | reference_value |  |
| is_multi_source | TYD_BOOLEAN |  |  |  |
| respects_source_of_record | TYD_BOOLEAN |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### C · Pipelines  (3)

#### `pipeline_dependency`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_pipeline_step_code | TYD_CODE | 🔑 | transformation_pipeline_step |  |
| depends_on_step_code | TYD_CODE | 🔑 | transformation_pipeline_step |  |
| dependency_type_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

#### `transformation_pipeline`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| business_process_code | TYD_CODE |  | business_process |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| schedule_cron | TYD_NAME |  |  |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `transformation_pipeline_step`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_pipeline_code | TYD_CODE | 🔑 | transformation_pipeline |  |
| code | TYD_CODE | 🔑 |  |  |
| step_kind_code | TYD_CODE |  | reference_value |  |
| canonical_view_code | TYD_CODE |  | canonical_view |  |
| dq_rule_code | TYD_CODE |  | reference_value |  |
| write_mode_code | TYD_CODE |  | reference_value |  |
| step_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Tipos específicos  (4)

#### `encryption_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| encryption_algorithm_code | TYD_CODE |  | reference_value |  |
| key_reference | TYD_TEXT_SUMMARY |  |  |  |
| dpo_approval_status_code | TYD_CODE |  | reference_value |  |
| ciso_approval_status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `masking_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| masking_method_code | TYD_CODE |  | reference_value |  |
| dpo_approval_status_code | TYD_CODE |  | reference_value |  |
| applies_from | TYD_TIMESTAMP |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `reference_mapping_set`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_reference_catalog_code | TYD_CODE |  | reference_catalog |  |
| target_reference_catalog_code | TYD_CODE |  | reference_catalog |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `reference_mapping_set_entry`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| reference_mapping_set_code | TYD_CODE | 🔑 | reference_mapping_set |  |
| source_value | TYD_NAME | 🔑 |  |  |
| target_value | TYD_NAME |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### E · Vínculo source→canonical  (1)

#### `source_attribute_canonical_attribute_map` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| source_attribute_code | TYD_CODE | 🔑 | source_attribute |  |
| canonical_attribute_code | TYD_CODE | 🔑 | canonical_attribute |  |
| transformation_mapping_code | TYD_CODE |  | transformation_mapping |  |
| is_golden_source | TYD_BOOLEAN |  |  |  |
| mapping_confidence_code | TYD_CODE |  | reference_value |  |
| is_auto_suggested | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### F · Ejecución  (2)

#### `transformation_run`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| transformation_pipeline_code | TYD_CODE |  | transformation_pipeline |  |
| started_at | TYD_TIMESTAMP |  |  |  |
| finished_at | TYD_TIMESTAMP |  |  |  |
| run_status_code | TYD_CODE |  | reference_value |  |
| triggered_by | TYD_NAME |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `transformation_run_step`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_run_code | TYD_CODE | 🔑 | transformation_run |  |
| transformation_pipeline_step_code | TYD_CODE | 🔑 | transformation_pipeline_step |  |
| step_status_code | TYD_CODE |  | reference_value |  |
| rows_affected | TYD_INT |  |  |  |
| started_at | TYD_TIMESTAMP |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### G · Versionado SCD2  (2)

#### `transformation_mapping_version` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_mapping_code | TYD_CODE | 🔑 | transformation_mapping |  |
| version_label | TYD_NAME | 🔑 |  |  |
| content_hash | TYD_CODE |  |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| is_current | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `transformation_rule_version` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| transformation_rule_code | TYD_CODE | 🔑 | transformation_rule |  |
| version_label | TYD_NAME | 🔑 |  |  |
| content_hash | TYD_CODE |  |  |  |
| effective_from | TYD_TIMESTAMP |  |  |  |
| effective_until | TYD_TIMESTAMP |  |  |  |
| is_current | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### H · Artefacto de materialización (DDL)  (1)

#### `compiled_ddl`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| object_type_code | TYD_CODE | 🔑 | object_type |  |
| ddl_kind_code | TYD_CODE |  | reference_value |  |
| compiled_ddl_text | TYD_EXPRESSION |  |  |  |
| query_status_code | TYD_CODE |  | reference_value |  |
| source_metadata_hash | TYD_NAME |  |  |  |
| signature | TYD_NAME |  |  |  |
| compiled_at | TYD_TIMESTAMP |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### H · Extensibilidad  (4)

#### `mapping_attribute` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| transformation_mapping_code | TYD_CODE |  | transformation_mapping |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `mapping_attribute_value` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| mapping_attribute_code | TYD_CODE | 🔑 | mapping_attribute |  |
| owner_code | TYD_CODE | 🔑 |  |  |
| attribute_value | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `rule_attribute` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| transformation_rule_code | TYD_CODE |  | transformation_rule |  |
| data_type_domain_code | TYD_CODE |  | data_type_domain_simple |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `rule_attribute_value` — 🧩 derivada

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| rule_attribute_code | TYD_CODE | 🔑 | rule_attribute |  |
| owner_code | TYD_CODE | 🔑 |  |  |
| attribute_value | TYD_EXPRESSION |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D5  (2 entidades)

### Vistas canónicas declarativas  (2)

#### `impact_analysis`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| lineage_view_definition_code | TYD_CODE |  | lineage_view_definition |  |
| change_kind_code | TYD_CODE |  | reference_value |  |
| purpose_text | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `lineage_view_definition`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| anchor_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| anchor_object_type_code | TYD_CODE |  | object_type |  |
| direction_code | TYD_CODE |  | reference_value |  |
| max_depth | TYD_INT |  |  |  |
| scope_text | TYD_TEXT_SUMMARY |  |  |  |
| rendered_view_code | TYD_CODE |  | canonical_view |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D6  (9 entidades)

### B · Dimensiones  (1)

#### `dimension`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| source_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| source_object_type_code | TYD_CODE |  | object_type |  |
| business_view_code | TYD_CODE |  | canonical_view |  |
| analysis_hierarchy_text | TYD_TEXT_SUMMARY |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Remediación  (1)

#### `dq_quarantine_policy`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| max_quarantine_days | TYD_INT |  |  |  |
| auto_escalate | TYD_BOOLEAN |  |  |  |
| on_expiration_action_code | TYD_CODE |  | reference_value |  |
| requires_dpo_approval_for_dismiss | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### ISO 25040 · Definición  (1)

#### `dq_evaluation_specification`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| method_text | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### ISO · Puentes  (1)

#### `dq_dimension_to_iso_characteristic`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| dimension_code | TYD_CODE | 🔑 | reference_value |  |
| iso_characteristic_code | TYD_CODE | 🔑 | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

### UNE Q1 · Definición  (2)

#### `data_quality_requirement`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| canonical_entity_code | TYD_CODE |  | canonical_entity |  |
| requirement_text | TYD_TEXT_SUMMARY |  |  |  |
| priority_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `dq_implementation_plan`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| data_quality_requirement_code | TYD_CODE |  | data_quality_requirement |  |
| target_date | TYD_TIMESTAMP |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### UNE Q3 · Definición  (3)

#### `dq_assurance_procedure`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| procedure_text | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `dq_audit_plan`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| frequency_code | TYD_CODE |  | reference_value |  |
| dq_assurance_procedure_code | TYD_CODE |  | dq_assurance_procedure |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `dq_certification_criteria`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| certification_level_code | TYD_CODE |  | reference_value |  |
| min_score_pct | TYD_DECIMAL |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D7  (6 entidades)

### A · Hechos acumulativos  (2)

#### `accumulative_fact`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| business_term_code | TYD_CODE |  | business_term |  |
| source_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| source_object_type_code | TYD_CODE |  | object_type |  |
| time_grain_code | TYD_CODE |  | reference_value |  |
| materialization_mode_code | TYD_CODE |  | reference_value |  |
| aggregation_view_code | TYD_CODE |  | canonical_view |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `accumulative_fact_dimension`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| accumulative_fact_code | TYD_CODE | 🔑 | accumulative_fact |  |
| dimension_code | TYD_CODE | 🔑 | dimension |  |
| dimension_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### C · KPIs  (2)

#### `kpi`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| kpi_type_code | TYD_CODE |  | reference_value |  |
| subject_kind_code | TYD_CODE |  | reference_value |  |
| accumulative_fact_code | TYD_CODE |  | accumulative_fact |  |
| calculation_view_code | TYD_CODE |  | canonical_view |  |
| unit_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `kpi_dependency`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| kpi_code | TYD_CODE | 🔑 | kpi |  |
| depends_on_kpi_code | TYD_CODE | 🔑 | kpi |  |
| dependency_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Data Products  (2)

#### `data_product`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| business_term_code | TYD_CODE |  | business_term |  |
| certification_tier_code | TYD_CODE |  | reference_value |  |
| common_dimension_set_text | TYD_TEXT_SUMMARY |  |  |  |
| publication_status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_product_fact`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_product_code | TYD_CODE | 🔑 | data_product |  |
| accumulative_fact_code | TYD_CODE | 🔑 | accumulative_fact |  |
| perspective_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

## D8  (21 entidades)

### B · Roles y RBAC  (1)

#### `governance_role`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| scope_kind_code | TYD_CODE |  | reference_value |  |
| is_builtin | TYD_BOOLEAN |  |  |  |
| description_ref | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### C · Access Grants  (4)

#### `data_access_grant`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| governance_role_code | TYD_CODE |  | governance_role |  |
| grant_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| grant_object_type_code | TYD_CODE |  | object_type |  |
| access_level_code | TYD_CODE |  | reference_value |  |
| valid_from | TYD_TIMESTAMP |  |  |  |
| valid_to | TYD_TIMESTAMP |  |  |  |
| decision_note | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_access_grant_approval`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_access_grant_code | TYD_CODE | 🔑 | data_access_grant |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| approved_by_role_code | TYD_CODE |  | governance_role |  |
| decided_at | TYD_TIMESTAMP |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_access_grant_condition`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_access_grant_code | TYD_CODE | 🔑 | data_access_grant |  |
| access_policy_code | TYD_CODE |  | access_policy |  |
| audit | TYD_AUDIT |  |  |  |

#### `effective_permission_cache`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| principal_ref | TYD_NAME | 🔑 |  |  |
| grant_object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| access_level_code | TYD_CODE |  | reference_value |  |
| computed_at | TYD_TIMESTAMP |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Audit (config)  (1)

#### `data_access_review`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| frequency_code | TYD_CODE |  | reference_value |  |
| scope_text | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### E · Bases legales  (2)

#### `legal_basis`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| article_ref | TYD_NAME |  |  |  |
| description_ref | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `processing_purpose`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| legal_basis_code | TYD_CODE |  | legal_basis |  |
| is_primary | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### G18 · Sharing interno  (1)

#### `data_sharing_request`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| from_owner_role_code | TYD_CODE |  | governance_role |  |
| to_business_unit_code | TYD_CODE |  | business_unit |  |
| shared_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| shared_object_type_code | TYD_CODE |  | object_type |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### G3 · Incidentes  (1)

#### `incident_type_definition`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| severity_sla_text | TYD_TEXT_SUMMARY |  |  |  |
| workflow_text | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### H · Cesiones y encargos  (3)

#### `data_processing_agreement`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| external_organization_code | TYD_CODE |  | reference_value |  |
| safeguards_text | TYD_TEXT_SUMMARY |  |  |  |
| governed_document_code | TYD_CODE |  | governed_document |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `data_sharing_agreement`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| external_organization_code | TYD_CODE |  | reference_value |  |
| legal_basis_code | TYD_CODE |  | legal_basis |  |
| valid_from | TYD_TIMESTAMP |  |  |  |
| governed_document_code | TYD_CODE |  | governed_document |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `international_data_transfer`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| destination_country_code | TYD_CODE |  | reference_value |  |
| safeguard_code | TYD_CODE |  | reference_value |  |
| governed_document_code | TYD_CODE |  | governed_document |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### I · ROPA  (1)

#### `processing_activity_record`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| processing_purpose_code | TYD_CODE |  | processing_purpose |  |
| data_categories_text | TYD_TEXT_SUMMARY |  |  |  |
| retention_text | TYD_TEXT_SUMMARY |  |  |  |
| exigible_by_regulator | TYD_BOOLEAN |  |  |  |
| governed_document_code | TYD_CODE |  | governed_document |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### J · Políticas ABAC  (2)

#### `access_policy`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| target_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| target_object_type_code | TYD_CODE |  | object_type |  |
| filter_dimension_code | TYD_CODE |  | dimension |  |
| principal_attribute_key | TYD_NAME |  |  |  |
| policy_expression_view_code | TYD_CODE |  | canonical_view |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `access_policy_target`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| access_policy_code | TYD_CODE | 🔑 | access_policy |  |
| target_object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| target_object_type_code | TYD_CODE |  | object_type |  |
| audit | TYD_AUDIT |  |  |  |

### K · Facetas genéricas y motor de evaluación (DATUM-49/50)  (5)

#### `assessment_pattern`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| object_type_code | TYD_CODE |  | object_type |  |
| assessment_type_code | TYD_CODE |  | reference_value |  |
| level_reference_catalog_code | TYD_CODE |  | reference_catalog |  |
| scoring_method_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `assessment_pattern_threshold`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| assessment_pattern_code | TYD_CODE | 🔑 | assessment_pattern |  |
| code | TYD_CODE | 🔑 |  |  |
| score_from | TYD_DECIMAL |  |  |  |
| score_to | TYD_DECIMAL |  |  |  |
| level_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `assessment_question`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| assessment_pattern_code | TYD_CODE | 🔑 | assessment_pattern |  |
| code | TYD_CODE | 🔑 |  |  |
| question_order | TYD_INT |  |  |  |
| weight | TYD_DECIMAL |  |  |  |
| answer_scale_code | TYD_CODE |  | reference_value |  |
| is_mandatory | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `object_assessment`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| object_type_code | TYD_CODE | 🔑 | object_type |  |
| assessment_pattern_code | TYD_CODE | 🔑 | assessment_pattern |  |
| assessment_date | TYD_DATE | 🔑 |  |  |
| next_assessment_date | TYD_DATE |  |  |  |
| total_score | TYD_DECIMAL |  |  |  |
| level_code | TYD_CODE |  | reference_value |  |
| is_current | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `object_assessment_answer`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| object_assessment_row_uuid | TYD_UUID | 🔑 | object_assessment |  |
| assessment_question_code | TYD_CODE | 🔑 | assessment_question |  |
| raw_score | TYD_DECIMAL |  |  |  |
| weighted_score | TYD_DECIMAL |  |  |  |
| answer_note | TYD_TEXT_SUMMARY |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D9  (8 entidades)

### A · Exposición  (2)

#### `data_exposure`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| data_product_code | TYD_CODE |  | data_product |  |
| recipient_kind_code | TYD_CODE |  | reference_value |  |
| mechanism_code | TYD_CODE |  | reference_value |  |
| owner_business_unit_code | TYD_CODE |  | business_unit |  |
| approval_status_code | TYD_CODE |  | reference_value |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `exposure_consumer`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_exposure_code | TYD_CODE | 🔑 | data_exposure |  |
| consumer_principal_code | TYD_CODE | 🔑 | reference_value |  |
| access_grant_ref | TYD_UUID |  | (D8) |  |
| sla_text | TYD_TEXT_SUMMARY |  |  |  |
| valid_from | TYD_TIMESTAMP |  |  |  |
| valid_to | TYD_TIMESTAMP |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### B · Config por mecanismo  (3)

#### `exposure_api_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_exposure_code | TYD_CODE | 🔑 | data_exposure |  |
| canonical_view_code | TYD_CODE |  | canonical_view |  |
| api_style_code | TYD_CODE |  | reference_value |  |
| rate_limit_per_min | TYD_INT |  |  |  |
| versioning_policy_text | TYD_TEXT_SUMMARY |  |  |  |
| mask_pii_in_response | TYD_BOOLEAN |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `exposure_direct_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_exposure_code | TYD_CODE | 🔑 | data_exposure |  |
| shared_object_code | TYD_CODE |  | canonical_view |  |
| share_platform_code | TYD_CODE |  | reference_value |  |
| grant_level_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

#### `exposure_push_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_exposure_code | TYD_CODE | 🔑 | data_exposure |  |
| endpoint_kind_code | TYD_CODE |  | reference_value |  |
| endpoint_ref | TYD_TEXT_SUMMARY |  |  |  |
| schedule_cron | TYD_NAME |  |  |  |
| format_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

### C · Marketplace  (2)

#### `marketplace_listing`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| data_product_code | TYD_CODE |  | data_product |  |
| listing_mode_code | TYD_CODE |  | reference_value |  |
| terms_document_code | TYD_CODE |  | governed_document |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `marketplace_request`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| marketplace_listing_code | TYD_CODE |  | marketplace_listing |  |
| requester_principal_code | TYD_CODE |  | reference_value |  |
| owner_approval_status_code | TYD_CODE |  | reference_value |  |
| generated_exposure_code | TYD_CODE |  | data_exposure |  |
| requested_at | TYD_TIMESTAMP |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Cumplimiento  (1)

#### `exposure_compliance`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| data_exposure_code | TYD_CODE | 🔑 | data_exposure |  |
| legal_basis_code | TYD_CODE |  | reference_value |  |
| recipient_jurisdiction_code | TYD_CODE |  | reference_value |  |
| sectoral_template_code | TYD_CODE |  | reference_value |  |
| retention_in_destination | TYD_NAME |  |  |  |
| propagates_erasure | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D10  (11 entidades)

### A · Módulos y pantallas  (3)

#### `ui_module`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| title | TYD_NAME |  |  |  |
| requires_addon_code | TYD_CODE |  | reference_value |  |
| display_order | TYD_INT |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `ui_screen`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| ui_module_code | TYD_CODE |  | ui_module |  |
| presentation_pattern_code | TYD_CODE |  | presentation_pattern |  |
| bound_object_row_uuid | TYD_UUID |  | (polimórfico) |  |
| bound_object_type_code | TYD_CODE |  | object_type |  |
| render_mode_code | TYD_CODE |  | reference_value |  |
| title | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `ui_screen_breadcrumb_definition`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| ui_screen_code | TYD_CODE | 🔑 | ui_screen |  |
| level_order | TYD_INT | 🔑 |  |  |
| label_ref | TYD_NAME |  |  |  |
| parent_screen_code | TYD_CODE |  | ui_screen |  |
| audit | TYD_AUDIT |  |  |  |

### B · Permisos UI (RBAC)  (2)

#### `ui_role_permission`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| governance_role_code | TYD_CODE | 🔑 | governance_role |  |
| ui_screen_code | TYD_CODE | 🔑 | ui_screen |  |
| ui_module_code | TYD_CODE |  | ui_module |  |
| action_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |

#### `ui_role_permission_set`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| governance_role_code | TYD_CODE |  | governance_role |  |
| description_ref | TYD_TEXT_SUMMARY |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### C · Branding e i18n  (1)

#### `client_branding`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| logo_uri | TYD_TEXT_SUMMARY |  |  |  |
| primary_color | TYD_NAME |  |  |  |
| secondary_color | TYD_NAME |  |  |  |
| theme_code | TYD_CODE |  | reference_value |  |
| is_client_modified | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### D · Soporte/Ticketing  (2)

#### `support_module_config`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| support_tier_code | TYD_CODE |  | reference_value |  |
| channels_text | TYD_TEXT_SUMMARY |  |  |  |
| csm_ref | TYD_NAME |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `support_ticket_category`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| support_module_config_code | TYD_CODE |  | support_module_config |  |
| title | TYD_NAME |  |  |  |
| audit | TYD_AUDIT |  |  |  |

### E · Motor generativo (DATUM-30)  (3)

#### `pattern_slot`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| presentation_pattern_code | TYD_CODE | 🔑 | presentation_pattern |  |
| code | TYD_CODE | 🔑 |  |  |
| slot_kind_code | TYD_CODE |  | reference_value |  |
| is_required | TYD_BOOLEAN |  |  |  |
| slot_order | TYD_INT |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `presentation_pattern`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| functionality_kind_code | TYD_CODE |  | reference_value |  |
| description_ref | TYD_TEXT_SUMMARY |  |  |  |
| is_builtin | TYD_BOOLEAN |  |  |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `ui_screen_slot_binding`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| ui_screen_code | TYD_CODE | 🔑 | ui_screen |  |
| pattern_slot_code | TYD_CODE | 🔑 | pattern_slot |  |
| canonical_attribute_code | TYD_CODE |  | canonical_attribute |  |
| ui_control_override_code | TYD_CODE |  | reference_value |  |
| is_hidden | TYD_BOOLEAN |  |  |  |
| display_order_override | TYD_INT |  |  |  |
| label_override | TYD_NAME |  |  |  |
| audit | TYD_AUDIT |  |  |  |

## D14  (3 entidades)

### Documentación gobernada  (3)

#### `governed_document`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| code | TYD_CODE | 🔑 |  |  |
| document_type_code | TYD_CODE |  | reference_value |  |
| title | TYD_NAME |  |  |  |
| storage_kind_code | TYD_CODE |  | reference_value |  |
| external_uri | TYD_TEXT_SUMMARY |  |  |  |
| generated_from_view_code | TYD_CODE |  | canonical_view |  |
| requires_periodic_review | TYD_BOOLEAN |  |  |  |
| review_period_months | TYD_INT |  |  |  |
| last_reviewed_at | TYD_TIMESTAMP |  |  |  |
| status_code | TYD_CODE |  | reference_value |  |
| row_uuid | TYD_UUID |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `governed_document_link`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| governed_document_code | TYD_CODE | 🔑 | governed_document |  |
| linked_object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| linked_object_type_code | TYD_CODE |  | object_type |  |
| link_kind_code | TYD_CODE |  | reference_value |  |
| is_primary | TYD_BOOLEAN |  |  |  |
| audit | TYD_AUDIT |  |  |  |

#### `governed_document_owner`

| Atributo | TYD | PK | FK → | Catálogo (meta) |
|---|---|:--:|---|---|
| governed_document_code | TYD_CODE | 🔑 | governed_document |  |
| owner_object_row_uuid | TYD_UUID | 🔑 | (polimórfico) |  |
| owner_object_type_code | TYD_CODE |  | object_type |  |
| ownership_role_code | TYD_CODE |  | reference_value |  |
| audit | TYD_AUDIT |  |  |  |
