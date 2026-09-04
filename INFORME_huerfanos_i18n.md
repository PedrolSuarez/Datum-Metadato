# Huérfanos i18n — diagnóstico y limpieza

Estado de partida: **398 objetos i18n** sin correspondencia en el modelo. Al abrirlos resultó que **no eran una sola cosa**, y que una parte no era basura.

## Qué se ha hecho (no destructivo, ya aplicado)

**Reparación de 206 registros mal rellenados.** Eran i18n de atributos del metamodelo guardados como `entity: null` y `code: "<entidad>.<atributo>"`, en vez de `entity: "<entidad>"` y `code: "<atributo>"`. Se comprobó primero que **la clave sha256 ya era correcta en los 206** (el script aborta si alguna no reproduce), así que no había que reindexar nada: solo rellenar bien los campos.

No se dio de alta ni de baja ningún objeto: el fichero sigue con **18.105** entradas. El efecto es que 126 de ellos dejan de caer en `MISC` y se atribuyen a `METADATA`:

| | antes | después |
|---|---|---|
| MISC | 244 | **118** |
| METADATA | 1.754 | **1.880** |

## Qué NO es basura (27 objetos) — no tocar

Entidades y atributos que **sí existen en el metamodelo** (`canonical_entity_version`, `canonical_attribute_version`, `canonical_entity_attribute`, `discovery_rule_evaluation`, `dq_governance_execution`…). Aparecían como huérfanos solo porque la comprobación inicial los contrastaba contra el modelo canónico de negocio y no contra el metamodelo. Error de la comprobación, no del dato.

**Aviso sobre el criterio:** `canonical_entity_bk_lookup_config` no está en **ninguno** de los dos ficheros de modelo, pero sí lo referencian los catálogos canonizados del Project (`IDENTITY_MODE`, `ON_MISS`, `SURROGATE_STRATEGY`). Por eso la lista de "no existe en el modelo" no basta como prueba de basura: los ficheros de modelo están incompletos respecto de lo que el resto del metadato da por vivo.

## Qué queda sin resolver: 324 objetos

De ellos **27 son legítimos** (arriba) y **294 son candidatos a baja**, en cinco grupos:

| n | grupo | qué es |
|---:|---|---|
| 106 | Atributo retirado de entidad viva | La entidad existe; el atributo ya no |
| 100 | Valor retirado de catálogo vivo | El catálogo existe; ese código ya no |
| 64 | Atributo de entidad desconocida | Ni en modelo canónico, ni en metamodelo, ni referenciada por catálogos |
| 15 | Atributo retirado de entidad del metamodelo | Ídem que el primero, en tablas del metamodelo |
| 9 | Entidad desconocida | Tabla que no reconoce ninguna fuente |

### La causa principal está identificada

En los 121 atributos retirados, los nombres que más se repiten son **`audit` (20)** y **`row_uuid` (16)**, más `status_code` / `lifecycle_state_code` (4). Son exactamente los atributos que **METADATO-9 plegó dentro del compuesto `system`**. Es decir: son el residuo de aquella refactorización, cuyo i18n nunca se limpió. El resto son renombrados sueltos.

### Las 9 entidades desconocidas

`business_term_canonical_entity` · `canonical_attribute_business_term` · `canonical_attribute_constraint` · `canonical_entity_bk_alias` · `canonical_entity_business_process` · `canonical_entity_constraint_attribute` · `canonical_relation_end` · `data_product_subscription` · `party`

Casi todas tienen pinta de tablas de un diseño anterior del metamodelo. **`party` es el caso a mirar con lupa**: el catálogo `PARTY_ROLE` (`_GLOBAL_`) dice literalmente que registra dependencias *«mientras no exista el maestro»*, o sea que `party` está **previsto y no creado**. Su i18n puede ser preparatorio, no residuo.

## Decisión tomada y aplicada

Alcance aprobado: **solo los de origen vivo**, más `TEXT_FIELD_KIND`. Se conservan `party` y las 73 entradas de entidades desconocidas.

| | objetos |
|---|---:|
| Atributos retirados de entidades que existen | 121 |
| Valores retirados de catálogos que existen | 100 |
| `TEXT_FIELD_KIND` | 3 |
| **Total dado de baja** | **224** |

Antes de borrar, cada objeto se **revalidó de nuevo uno a uno** contra el modelo y los catálogos: si alguno hubiera resultado corresponder a algo vivo, el script abortaba sin tocar el fichero. Los 224 pasaron la revalidación.

Fichero i18n: **18.105 → 17.881**. Copia de seguridad completa de lo retirado en **`datum_i18n_bajas_backup.json`**; para revertir basta reinsertar su bloque `i18n`.

### Estado final

| | inicio | final |
|---|---:|---:|
| Objetos sin resolver | 398 | **100** |
| — de ellos, metamodelo legítimo | 27 | 27 |
| — de ellos, entidades desconocidas conservadas a propósito (incl. `party`) | 73 | 73 |
| — basura | 298 | **0** |
| MISC | 244 | **100** |

Comprobado además que **no se ha borrado de más**: las 951 entidades del modelo, todos sus atributos y todos los valores de los 1.088 catálogos siguen teniendo i18n completo en los cuatro idiomas.

## Lo que queda abierto

Las **73 entradas de entidades desconocidas** siguen ahí, conservadas a propósito:

`business_term_canonical_entity` · `canonical_attribute_business_term` · `canonical_attribute_constraint` · `canonical_entity_bk_alias` · `canonical_entity_business_process` · `canonical_entity_constraint_attribute` · `canonical_relation_end` · `data_product_subscription` · `party`

Resolverlas requiere una fuente que hoy no existe: **un inventario fiable de las tablas vivas del metamodelo**. Los dos ficheros de modelo que hay se contradicen entre sí (171 frente a 312 entidades) y ninguno incluye `canonical_entity_bk_lookup_config`, que los catálogos canonizados sí dan por vivo. Mientras eso no se cierre, borrarlas sería adivinar.

`party` se conserva como preparatorio: el catálogo `PARTY_ROLE` declara que existe *«mientras no exista el maestro»*.

El detalle objeto a objeto, con la clave i18n exacta de cada uno, sigue en **`i18n_huerfanos_manifiesto.json`**.
