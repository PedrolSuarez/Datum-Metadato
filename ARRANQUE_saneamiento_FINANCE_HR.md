# ARRANQUE · Saneamiento de FINANCE y HR

**Objetivo de la sesión:** canonizar los catálogos de **FINANCE** y **HR** y cerrar la deuda estructural de esos dos aceleradores. Es **saneamiento de lo existente**, no modelo nuevo: no se añaden entidades ni se diseñan aceleradores.

> Una sesión = un objetivo. Si aparece diseño nuevo, se anota y se saca a otra sesión.

## Precondición (estado heredado, tras METADATO-106, v1.82)

- **952 entidades · 1.086 catálogos · 17.816 objetos i18n · 16 restricciones · 19 aceleradores.**
- Auditoría a cero: 0 huérfanos i18n, 0 FK ni catálogos rotos, 0 i18n ausente, 0 entidades sin PK, 19/19 aceleradores con recuento declarado = real.
- El verificador integral está en `/tmp/verify_full.py` de la sesión anterior — **hay que rehacerlo**, `/tmp` no sobrevive. Lo que debe comprobar está en la sección «Verificación» de abajo.

## El problema

FINANCE y HR son los dos aceleradores más antiguos y arrastran deuda que los demás no tienen. Inventario en **`INVENTARIO_catalogos_sin_canonizar.json`**:

| Síntoma | n | Reparto |
|---|---:|---|
| Catálogos con **valores sin etiqueta** (código sin texto legible) | **393** | FINANCE 269 · HR 99 · PROCUREMENT 15 · otros 10 |
| Catálogos marcados **«volcado del visor, canonización pendiente»** | **346** | FINANCE 276 · HR 61 · MARKETING 8 · GLOBAL 1 |
| De los marcados, **sin uso en el modelo** | **32** | candidatos directos a retirada |
| Catálogos **sin ningún valor** | 15 | MARKETING 8 · HEALTHCARE 7 |
| `estado: PENDIENTE` | 8 | MARKETING |

Los dos grandes se solapan: es la misma deuda. Un catálogo con valores sin etiqueta **no se puede traducir ni mostrar** — el visor solo enseña el código.

Deuda adicional ya conocida de esos dos aceleradores:

- **HR va en esquema v2** (`datum_terminos_modelo__HHRR_v1.json`: clave `terminos`, atributos en `attrs`, **sin bloque `dq_referential_integrity`**). Por eso sus **138 referencias a catálogo no tienen regla REFERENTIAL derivada**. HR está por lo demás impecable: 76 nodos, 0 desfasados.
- **FINANCE**: 7 nodos de maestros compartidos (`country`, `currency`, `business_unit`…) listan solo un subconjunto de atributos. Quedó como aviso no bloqueante, sin decidir si es intencionado.

## Agenda propuesta (a validar antes de ejecutar)

1. **Los 32 sin uso** — pasada barata: confirmar que ninguno se usa y retirarlos con copia de seguridad. Es el patrón ya probado en M-105/106.
2. **Triaje de los 393 sin etiqueta** — separar: (a) los que solo necesitan etiqueta en 4 idiomas, (b) los que son volcados duplicados de otro catálogo ya canonizado, (c) los que en realidad deberían ser **FK a una entidad** y no catálogo.
3. **Migración de HR a esquema v3** — decisión aparte: si se migra, sus 138 referencias ganan regla derivada; si no, queda documentado por qué.
4. **Los 7 nodos parciales de FINANCE** — decidir si el subconjunto es intencionado.

## Avisos aprendidos en la sesión anterior (leer antes de tocar)

Estos tres tipos de error se dieron **en esta misma clase de trabajo**. No son hipotéticos:

1. **No sobrescribir un catálogo sin comprobar si el nombre ya existe.** `RESERVATION_STATUS` era de WAREHOUSE y se aplastó al crear uno de SITE. Antes de crear un catálogo: comprobar el nombre y quién lo usa.
2. **No «sincronizar» ficheros de términos contra el modelo sin mirar qué se pierde.** Al hacerlo se aplastaron 10 FK reales de FINANCE (`analytical_dimension_value`, `accounting_period`, `governance_role`) y se estuvo a punto de borrar la definición FINANCE de `account_balance_snapshot`, que resultó ser una **colisión de nombre con BANKING**, no un desfase.
3. **No aplicar una regla en bloque sin verificar caso por caso.** De 10 conflictos aparentemente iguales, 9 se resolvieron de una forma y el décimo (`DISCLOSURE_PERIOD`) requería lo contrario. En FINANCE/HR, con 393 casos, esto va a volver a pasar.

**Regla de trabajo:** cualquier operación masiva (etiquetar, retirar, migrar) se hace con copia de seguridad previa (`datum_i18n_bajas_backup.json` es el precedente: salvó 19 traducciones que ya se habían dado de baja) y con revalidación objeto a objeto justo antes de escribir.

## Ficheros que se tocan

- `datum_catalogos.json` — el grueso del trabajo
- `datum_modelo_canonico.json` — solo si algún catálogo pasa a ser FK de entidad
- `DATUM_i18n_D2.json` + partición SHORT/detalle del visor
- `datum_terminos_modelo__FINANCE_CORPORATE_v1.json` y `__HHRR_v1.json`
- `datum_carga_inicial.json` — si cambia algún `entity_count` o se retiran catálogos sembrados

## Verificación (rehacer el comprobador)

Debe cubrir, sobre el estado completo:

- FK rotas · catálogos inexistentes · todo atributo con `reference_catalog` lleva `fk_target: "reference_value"`
- Todo catálogo con `canonical_accelerator` y `category`; `estado` dentro del vocabulario canónico
- Modelo ↔ seed 1:1 en ambos sentidos; `business_term` y `parent_term_code` existentes
- i18n: 0 ausentes (entidad, atributo, valor) y 0 huérfanos
- Ficheros de términos: **leer v3 (`terms`/`attributes`) y v2 (`terminos`/`attrs`)** — omitir v2 dejó a HR sin verificar durante toda una sesión
- Nodos alineados con el modelo atributo a atributo, con `fk_target`, `reference_catalog`, `mandatory` y `pk`; `keys` y `dq_referential_integrity` cubriendo todas las FK
- Restricciones: entidad existente y **cada atributo citado en la expresión existe**
- Aceleradores: `entity_count` declarado = real

## Registro

Sería **METADATO-107**. Nada se registra hasta orden explícita de Pedro. Los ficheros completos van a outputs; Pedro canoniza en el Project.
