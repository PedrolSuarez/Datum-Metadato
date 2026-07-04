# MASTER · Arranque del proyecto «DATUM metadato»

## Propósito del proyecto
«DATUM metadato» es el hogar único del **metamodelo DATUM** y de **todos los modelos de datos cargables** (aceleradores): metadato base, observabilidad, financiero, rrhh, marketing, legal, etc. Sirve a la vez para:
1. **Definir** el metamodelo (las ~194 entidades del sistema de gobierno).
2. **Definir cada acelerador/modelo** que se incorpora a DATUM (observabilidad, financiero…).
3. **Cargar**: los JSON de este proyecto SON el **bootstrap del Control Plane de DATUM** — lo que se carga para arrancar un despliegue.

> NO contiene doctrina de negocio, oferta, pricing ni GTM. Eso vive en los proyectos de Producto/Dirección. Aquí solo metamodelo + modelos de datos + su carga.

## Principio rector (heredado, absoluto)
- **El disco es la única fuente de verdad.** Antes de proponer o modificar cualquier cosa: leer el estado real desde disco.
- **Nada se registra oficialmente** hasta que el founder ordene explícitamente "registro oficial".
- **Ficheros siempre completos**, nunca parches.
- **Una sesión = un objetivo.**
- El metamodelo es un sistema integrado por FK: antes de tocar una tabla, cargar el mapa completo y verificar dependencias. Nunca inventar nombres de tabla/campo — verificar en disco.

## Doble naturaleza de los JSON (CRÍTICO)
Los ficheros JSON de este proyecto no son documentación: son **artefactos ejecutables de bootstrap** del Control Plane. Orden de carga de un despliegue:
1. `DATUM_Catalogos.json` — catálogos de valores.
2. `DATUM_Carga_Inicial_Metadato.json` — seed de ubicación física (physical_catalog → physical_schema → storage_layer → storage_location → canonical_entity) y demás semillas.
3. El modelo (`DATUM_Modelo_Datos_Metadato.json`) define la estructura que esas semillas pueblan.
Cada **acelerador** añade su propio bloque de carga siguiendo el mismo patrón.

## Protocolo de arranque de sesión
1. Leer ficheros de control (`99-METADATO-control.md`, `18-METADATO-decisiones.md`) desde disco → confirmar estado.
2. Verificar inventario real vs. memoria.
3. Proponer agenda. Ejecutar solo tras validación del founder.
4. Entregar ficheros completos a outputs; el founder canoniza en el Project.

## Cómo se incorpora un acelerador nuevo
Cada acelerador (p.ej. FINANCE, RRHH, OBSERVABILITY) se define como un paquete que declara, sobre el metamodelo:
- sus **entidades canónicas** (business_term → entidad → claves → relaciones → constraints),
- su **ubicación física** (catálogo/esquema Databricks: business→fact/dataproduct…, etc.),
- su **carga inicial** (seed) en el JSON de bootstrap,
- su **i18n** (es/en/fr/pt).
Ver `PLANTILLA_acelerador.md`.

## Visualización
El proyecto incluye la página «Modelo canónico» (demo Next.js `/dashboard/canonico`) para **visualizar todo lo que se incluya**: árbol dominio→subdominio→entidad (por code), ER interactivo por subdominio, datos de carga inicial por entidad, badges de cuarentena/derivada. Se actualiza apuntándola a los JSON de este proyecto.
