# 18 · Decisiones — Proyecto «DATUM metadato»

**Versión:** v1.0 — Julio 2026
**Numeración:** METADATO-n (propia del proyecto, independiente de DATUM-n de Producto).

## Decisiones

### METADATO-1 — Creación del proyecto y gobierno propio — DECIDIDO
El metamodelo y los aceleradores se separan del proyecto DATUM-Producto (saturado) a un proyecto propio, «DATUM metadato». Gobierno propio: par de control `99-METADATO-control.md` + `18-METADATO-decisiones.md`, numeración METADATO-n. Hereda como estado inicial el resultado de DATUM-108 (metamodelo de 194 entidades, D00, 6 catálogos físicos, carga inicial, metadata-first). NO incluye doctrina de negocio/oferta/GTM (se queda en Producto/Dirección).

### METADATO-2 — Los JSON son bootstrap del Control Plane — DECIDIDO
Los ficheros JSON de este proyecto (`DATUM_Catalogos.json`, `DATUM_Carga_Inicial_Metadato.json`, `DATUM_Modelo_Datos_Metadato.json`) no son documentación: son el **artefacto de carga (bootstrap)** que arranca el Control Plane de DATUM. Orden de carga: catálogos → carga inicial (physical_catalog→schema→storage_layer→location→canonical_entity) sobre la estructura del modelo. Cada acelerador añade su bloque de carga siguiendo el mismo patrón.

---
*Fin de `18-METADATO-decisiones.md` v1.0.*
