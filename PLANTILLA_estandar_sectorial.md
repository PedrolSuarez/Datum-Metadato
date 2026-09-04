# Plantilla · Alta de un estándar sectorial sobre el modelo canónico

> Un estándar sectorial (FHIR salud, BIAN banca, ACORD seguros, ISO 20022…) **no es otro modelo**: es una **capa de correspondencia (crosswalk) + perfil** sobre el canónico, que sigue siendo la verdad semántica única. Reutiliza el andamiaje de METADATO-87 (`sector_standard`, `canonical_standard_entity_map`, `canonical_standard_attribute_map`). El piloto **FHIR** es el ejemplo trabajado.

## 1. Identidad del estándar
- Alta en catálogo `SECTORAL_TEMPLATE` (ya trae FHIR/BIAN/ACORD/AEAT/SEPA/EDI; añade el que falte).
- Autoridad en `STANDARD_AUTHORITY` (HL7, BIAN, ACORD, SWIFT, ISO, SNOMED, LOINC…).
- Fila en `sector_standard`: `code`, `sector_template_value_id`, `standard_authority_value_id`, `standard_name`, `version`, `applicable_industry_sector_value_id` (`PRIMARY_INDUSTRY_SECTOR`), `specification_uri`, `status_value_id` (`STANDARD_STATUS`), vigencia.

## 2. Decisión: solape vs. extensión
- **Solape** — el estándar cubre conceptos que el canónico ya tiene → solo crosswalk (ej. `legal_entity`→FHIR *Organization*). No se crean entidades.
- **Extensión** — el sector aporta entidades que el canónico no tiene → **acelerador sectorial nuevo** (patrón `PLANTILLA_acelerador.md`, D20→D21), diseñado alineado al estándar (ej. acelerador HEALTHCARE para FHIR). Nunca se toca el core para meter conceptos de un sector.

## 3. Crosswalk de entidad (`canonical_standard_entity_map`)
Por cada entidad canónica que corresponde a un recurso/objeto del estándar:
- `sector_standard_id`, `canonical_entity_code`, `standard_resource_name` (ej. `patient`↔`Patient`), `map_relation_value_id` (`MAPPING_RELATION`: 1:1/1:N/N:1/N:M), `map_direction_value_id` (`MAP_DIRECTION`: IMPORT/EXPORT/BIDIRECTIONAL), `is_required_by_standard`, `coverage_note`, vigencia.

## 4. Crosswalk de atributo (`canonical_standard_attribute_map`)
Por cada atributo canónico ↔ elemento del estándar:
- `entity_map_id`, `canonical_entity_code`, `canonical_attribute_name`, `standard_element_path` (ej. `Patient.name.family`), `map_relation_value_id`, `map_direction_value_id`, `transform_expression` (unidades/formato/concat), `unit`, `cardinality_min/max`, `is_required_by_standard`.

## 5. Enlace de terminología (value sets)
- Catálogos de valores enlazados al estándar con `reference_catalog.external_authority_code` (→`STANDARD_AUTHORITY`) y `external_standard_ref`.
- Cerrados si el value set es fijo (ej. FHIR `administrative-gender`); **abiertos** si es una terminología grande y externa (SNOMED CT, LOINC), con `tipo_valor=ABIERTO` y valores por instalación.
- En el crosswalk de atributo, apuntar `bound_reference_catalog_code` + `standard_value_set_uri`.

## 6. Perfil y conformidad (DQ derivada, **no** modelada)
- No se crea tabla de perfil. La conformidad se deriva de `is_required_by_standard` + `cardinality_min/max` + los value sets enlazados, y se compila como reglas DQ (igual que el resto de reglas del metamodelo).

## 7. Sectorización de la empresa
- **Tenant**: la empresa que usa DATUM opera en un sector → activa el/los estándar(es) por **configuración de instalación** (`config_pattern`/`delta_property`). Recordar D00: no hay tabla `client` (segmento de ruta / Terraform).
- **Partes del modelo** (`legal_entity`, `customer`, `supplier`): clasificación sectorial con `CLASSIFICATION_SCHEME` (CNAE/NACE/NAICS/GICS…) y `PRIMARY_INDUSTRY_SECTOR`.

## 8. Carga inicial (bootstrap)
- Filas seed en `carga_inicial`: `sector_standard`, `canonical_standard_entity_map`, `canonical_standard_attribute_map` (ids deterministas por `uuid5`). Si hay extensión, su acelerador aporta su propio bloque de carga.

## 9. i18n
- Textos (entidad, atributos, valores) en es/en/fr/pt en `datum_i18n_d2.json`, con `acc` por objeto (el detalle se parte por acelerador). Sin descripciones embebidas — solo `code` + i18n.

## 10. Registro
- Se registra como decisión METADATO-n con **"registro oficial"**. Verificar antes: 0 FK/refs rotas, crosswalks con entidad/atributo canónicos existentes, value sets enlazados a autoridad válida.

---
*Ejemplo de referencia: METADATO-87 (andamiaje + acelerador HEALTHCARE + piloto FHIR: 7 crosswalks de entidad + 31 de atributo, bidireccional).*
