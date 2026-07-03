# Plantilla · Definición de un acelerador (modelo cargable) sobre el metamodelo

> Un acelerador (OBSERVABILITY, FINANCE, RRHH…) es un paquete que se enchufa al metamodelo. Sigue el patrón metadata-first y la ubicación física ya definida.

## 1. Identidad
- code del acelerador (ej. FINANCE), catálogo físico destino (business / observability / …).

## 2. Entidades canónicas (D2)
Por cada entidad del acelerador, siguiendo la cadena D20→D21:
- término de negocio (business_term) → entidad canónica → claves → relaciones → constraints.
- FK a catálogo: value materializado + `reference_catalog` en metadato (`catalog_ref_metadata_only=true`).

## 3. Ubicación física
- catálogo físico + esquema (business → fact/dataproduct/dataset/dimension; observability → process/quality/audit).
- external location / S3 se resuelve por despliegue (Terraform); segmento cliente en la ruta.

## 4. Carga inicial (bootstrap)
- filas seed de las entidades del acelerador, en un JSON de carga propio, con orden de dependencia.

## 5. i18n
- textos (entidad, atributos, valores) en es/en/fr/pt. Sin descripciones embebidas — solo code + i18n.

## 6. Registro
- se registra como decisión METADATO-n con "registro oficial".
