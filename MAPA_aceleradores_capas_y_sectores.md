# Mapa de aceleradores — capas, sectores y estructura de operaciones

> Documento de **arquitectura del modelo** (no de oferta). Describe cómo se organizan los aceleradores, qué necesita un cliente según su negocio, la estructura de operaciones (emplazamientos / puntos de venta) y dónde están los huecos. **Empaquetado, oferta y pricing quedan fuera** — viven en Producto/Dirección.
>
> Fuente: dependencias y entidades reales del modelo en disco.

---

## 1. Principio rector

- **Corporativo y comercial son transversales.** Toda empresa lleva contabilidad, personas, compras, contratos, y vende algo. Se reutilizan tal cual.
- **Las operaciones son SIEMPRE sectoriales.** No existe un "operaciones genérico": la forma de producir y entregar lo que se vende cambia con el sector. Lo "industrial" no es la excepción genérica — es un sector cuya operación resultó muy reutilizable.

## 2. Las capas

| Capa | Nombre práctico | Contenido | ¿Siempre? |
|---|---|---|---|
| **Fundación** | — | METADATA (metamodelo + maestros comunes) · OBSERVABILITY | Siempre |
| **Corporativo** | **ERP** (núcleo admin) | FINANCE · HR · LEGAL · COMPRAS (PROCUREMENT) | Siempre |
| **Comercial** | **CRM** | MARKETING · COMMERCIAL (cliente, catálogo, precio, **pedido**) | Siempre |
| **Operaciones** | — | Estructura de emplazamientos + operación sectorial + cadena de suministro + add-ons | El sectorial que corresponda |

> Aviso: "ERP" en sentido clásico (SAP…) **incluye también operaciones** (MM/WM/PP/SD). Aquí "ERP" = el núcleo administrativo; el ERP completo se solapa con Operaciones.

**Todo enraíza en la compañía = `legal_entity`** (la sociedad, con jerarquía de grupo vía `parent`/`ultimate_parent`). No existe una entidad "company" aparte.

## 3. Operaciones, descompuesta

1. **Estructura de emplazamientos** (acelerador nuevo — el backbone; ver §4).
2. **Operación sectorial** — lo que se ejecuta *en* el punto y es irreducible del sector (vender en tienda, atender al paciente, originar un préstamo, dar una habitación) + **manufactura** (opcional) + **calidad** (operativa).
3. **Cadena de suministro** — el flujo *entre* emplazamientos y con proveedor/cliente.
4. **Add-ons** — Postventa (SERVICE) · Proyectos (PROJECT).

## 4. El acelerador nuevo: Estructura de emplazamientos (`SITE`)

Es el **corazón nuevo** y el hueco principal del modelo actual. Generaliza lo que hoy está por cuadruplicado (`branch`, `location`, `warehouse`, `channel`).

### Maestros
- **Reutilizados (ya existen, cuelgan de `legal_entity`):** `work_center` (centro de trabajo, HR) · `warehouse` (almacén, con tipo y jerarquía zona→bin) · `brand` (marca).
- **Nuevo: `punto_de_venta`** — la **generalización** de tienda, supermercado, restaurante, sucursal, colegio, clínica/hospital. Atributos: **tipo** (`POINT_TYPE`: tienda/súper/hospital/…), **marca**, **`work_center`**, **físico/digital**.

### Localización y sus roles (clave)
Una **localización** puede desempeñar uno, dos o los tres roles — no son 1:1:
- **Punto de venta** (vende) · **Centro de trabajo** (trabaja gente) · **Almacén** (guarda stock).
- Tienda = los tres · CD = centro + almacén (sin venta) · Web = punto de venta digital (sin centro físico, apunta a HQ) · Oficina/planta = centro (+ almacén), sin venta.

### Relaciones
- `punto_de_venta.work_center_id` (obligatorio: el físico, o el HQ si es digital)
- `punto_de_venta.marca_id`
- `punto_venta ↔ almacén` (**N:M**: un CD sirve a varias tiendas)
- `warehouse.work_center_id` (**opcional**: null si el almacén no tiene personal propio)
- `warehouse.parent_warehouse_id` (**auto-jerarquía**: planta → sub-almacenes lógicos → zonas → ubicaciones; `warehouse_zone` y `storage_bin` **ya existen**)
- **Geografía automática** desde la dirección: `supra_zone → country → region → province` (ya existe en METADATA). La jerarquía *comercial/de gestión* (zona de un responsable) sería otra cosa, opcional.

### Los 5 módulos del acelerador
1. **Estructura** — `punto_de_venta` (maestro), tipo, marca, jerarquías.
2. **Emplazamiento & almacén** — las relaciones de arriba + jerarquía de almacén.
3. **Capacidad, disponibilidad & reserva** — capacidad agregada = **atributo**; capacidad como recursos individuales (habitaciones, mesas, plazas) = **hijos del punto**. **Disponibilidad = hueco libre (`slot`)**; **reserva = compromiso del hueco (`appointment`)**; consultar disponibilidad = una consulta previa. Sanidad ya tiene `slot`/`appointment`/`schedule` → se generaliza a hotel/mesa/aula.
4. **Gestión del punto** — calendario/horarios de apertura, estado operativo (abierto/cerrado/obras), **planificación de turnos (WFM / cuadrante) contra la demanda del punto + captura de asistencia (fichaje)**.
5. **Activos & mantenimiento** — **no es un módulo de SITE**: EAM es acelerador propio y SITE lo usa. El emplazamiento aporta el anclaje (`equipment.point_of_sale_id` / `work_center_id`); equipos, planes, órdenes de trabajo y repuestos siguen en EAM. Ver §8.

### Fuera de este acelerador (en cada sectorial)
- **La operación ejecutada en el punto** (la venta operativa/TPV, la atención, el préstamo) = operación **sectorial**.
- **HR** conserva el maestro de la persona: empleado, contrato, jornada, adscripción a `work_center`, política de turnos. *(El cuadrante y el fichaje sí son operación del punto — módulo 4.)*

## 5. Primitivas compartidas (reutilizables entre sectores)

- **La localización / red de emplazamientos** (§4): sustituye a `branch`/`location`/`warehouse`/`channel` duplicados.
- **Capacidad + disponibilidad + reserva**: hoteles, viajes, restauración, sanidad (ya lo tiene), educación comparten "reservar una capacidad limitada y perecedera". Es una primitiva de servicios, no un módulo por sector.
- **Logística física** (almacenar/mover/reponer): casi universal (hasta una sucursal necesita efectivo, una clínica material).
- **Manufactura**: común en producto y comida, **ausente** en servicios/finanzas. Opcional, no universal.

## 6. Sectores — existentes y huecos

| Sector | Núcleo operativo | Estado |
|---|---|---|
| Banca | cuentas, pagos, préstamos, tarjetas, valores… | ✅ BANKING |
| Seguros | pólizas, coberturas, siniestros, reaseguro… | ✅ INSURANCE |
| Salud | paciente, clínico, medicación, diagnóstico… | ✅ HEALTHCARE |
| Industrial | fabricar–almacenar–distribuir + calidad + EAM | ✅ (genéricos MANUFACTURING/WAREHOUSE/SUPPLY_CHAIN/QUALITY/EAM) |
| Retail (súper, tiendas) | TPV/tienda, surtido, promociones, fidelización | ⛔ Hueco — sectorial RETAIL |
| Restauración | receta/escandallo, cocina, mesa/comanda, delivery | ⛔ Hueco — FOODSERVICE |
| Educación | matrícula, currículo, evaluación, expediente, plazas | ⛔ Hueco — EDUCATION |
| Agencias de viajes | booking, itinerario, proveedores, emisión | ⛔ Hueco — TRAVEL |
| Hoteles | PMS: reserva, ocupación, tarifas, housekeeping | ⛔ Hueco — HOSPITALITY |

Nota: COMMERCIAL hoy es venta **B2B** (pedido, cotización, contrato); no cubre venta masiva B2C (TPV, tienda), por eso retail/restauración/hostelería quedan cojos con solo genéricos → necesitan su sectorial + la estructura de emplazamientos (§4).

## 7. Regla de implantación — backbone obligatorio + capa variable

**Backbone obligatorio (siempre, en toda implantación):**

1. **Fundación (DATUM)** = METADATA + OBSERVABILITY. El metamodelo y la vigilancia.
2. **ERP** (corporativo) = FINANCE · HR · LEGAL · COMPRAS. Toda empresa lleva finanzas, personas, sociedad, compras.
3. **CRM** (comercial) = MARKETING · COMMERCIAL. Toda empresa vende / tiene clientes.
4. **WAREHOUSE** (almacén). Maestro obligatorio propio — toda empresa dispone de algo que compra/almacena; **siempre existe**.
5. **SITE** (estructura de emplazamientos). El maestro `punto_de_venta` que **usa** los demás maestros (`work_center`, `almacén`, `marca`) y los compone por FK. **No los posee.**

**Capa variable (según el negocio):**

6. **Operación sectorial** → el sector de su negocio (banca, retail, salud…). Un banco lleva el backbone pero **no** MANUFACTURING.
7. **Cadena de suministro** + **add-ons** (postventa, proyectos) → si aplican.

> "Obligatorio" es a nivel **capa**: siempre está en su núcleo; la **profundidad** (cuántos sub-módulos/entidades) escala con el tamaño de la empresa (una consultora de 5 personas tiene ERP, pero apenas COMPRAS).

**Maestros — no se extrae un módulo "core"; cada maestro vive en su capa, y SITE los USA (no los contiene):** `customer` → CRM · `legal_entity`/`employee`/`work_center` → ERP/HR · `almacén` → WAREHOUSE · `brand` → CRM · `punto_de_venta` → SITE · `currency`/`country` → Fundación. SITE referencia `work_center` + `almacén` + `marca` y añade `punto_de_venta`.

## 8. EAM y QUALITY — resuelto (revisado en Fase 3d)

> La versión anterior de esta sección decía «EAM se absorbe entero en SITE» y «QUALITY se parte en general/operativa». Al ir a ejecutarlo se contrastó contra el modelo en disco y **ninguna de las dos cosas se sostenía**. Queda así:

- **EAM → NO se absorbe. Acelerador propio; SITE lo usa.** `equipment` ancla a `fixed_asset` (FINANCE), `production_line` (MANUFACTURING) y `warehouse`: es una capacidad transversal que *está ubicada en* un emplazamiento, no una parte de la estructura del emplazamiento. Absorberlo repetiría el error corregido con WAREHOUSE (*«es obligatorio y siempre tiene que estar; no es de SITE, SITE lo usa»*). Lo que faltaba de verdad era el **anclaje**, ya añadido: `equipment.point_of_sale_id` y `equipment.work_center_id` (ambos opcionales), para que un equipo pueda colgar de una tienda, una clínica, una oficina o una planta.
- **QUALITY → NO se parte.** Las 5 entidades (`quality_specification`, `quality_inspection`, `quality_inspection_line`, `non_conformance`, `corrective_action`) anclan todas a `product`, `stock_lot`, `goods_receipt` y `production_order`: son **calidad operativa de producto** en manufactura y recepción. No existe hoy una mitad corporativa que separar; la partición propuesta no estaba en los datos. (El «calidad general transversal» de la versión anterior confundía calidad de producto con calidad de dato, y el **DQ** está decidido como reglas derivadas del metamodelo, no como tablas.)
- **Calidad del punto — resuelta por anclaje, sin entidades nuevas.** El hueco era real, pero QUALITY ya lo soportaba casi entero: en `quality_inspection` y `non_conformance` el producto y el lote **ya eran opcionales**, `NONCONFORMANCE_SOURCE` ya tenía `CUSTOMER` e `INSPECTION_RESULT` ya era apto/no apto/condicional. Sólo faltaba el sujeto «punto»:
  - `quality_inspection.point_of_sale_id` — el control ejecutado en el punto (apertura, higiene, limpieza, imagen de marca…).
  - `non_conformance.point_of_sale_id` — la incidencia detectada en el punto; la queja de cliente es `source = CUSTOMER`. `corrective_action` (CAPA) cuelga de ahí sin tocar nada.
  - `quality_specification` pasa a ser **criterio de producto o de punto**: `product_id` deja de ser obligatorio y gana `point_of_sale_id` (nulo = aplica a todos los puntos) e `inspection_kind_value_id`, que es lo que **agrupa el protocolo/checklist** (la checklist de apertura de un restaurante = sus criterios con `kind = OPENING`).
  - `quality_inspection_line.observation` — anotación libre del ítem, que una checklist necesita.
  - `INSPECTION_KIND` gana los tipos de punto: `OPENING`, `CLOSING`, `HYGIENE`, `CLEANLINESS`, `SAFETY`, `BRAND_STANDARD`, `SITE_AUDIT`.
  - *Consecuencia a decidir:* la obligatoriedad de `quality_specification.product_id` pasa a ser **condicional** (obligatorio si el sujeto es producto). Como las reglas DQ se derivan del metamodelo, queda pendiente cómo se expresa una obligatoriedad condicional.
- Criterio que queda: **una capacidad transversal no se absorbe en SITE; se ancla a SITE.** Vale igual para WAREHOUSE, EAM y QUALITY.

## 8bis. Decisiones tomadas y pendientes

**Tomadas:**
- Nombre del acelerador de emplazamientos = **`SITE`**.
- **No** se extrae un módulo "core"; el núcleo maestro se gestiona en su capa (ver §7).
- Backbone obligatorio = **DATUM + ERP + CRM + SITE**; el resto es capa variable (§7).

**Pendiente (otra sesión):**
- **Producto**: vive en Comercial/CRM de forma genérica; su especialización por sector se matiza en otra sesión.

## 8ter. Producto — modelo común + clasificación por familia

Decisión cerrada. El producto vive en **Comercial/CRM** de forma genérica, y los sectores lo especializan **sin duplicar**.

**Una sola ficha común `product`** (ya existe) — identidad + catálogo: `product_code`, `product_name`, marca, `is_sellable`, pertenencia a catálogo. Vale para **físico, financiero, asegurador y servicio** — un producto es un producto. *No se renombra a "oferta"* (ese término ya lo usan la promoción de marketing y la cotización al cliente).

**Clasificación por `product_family` (jerárquico), NO por catálogos de tipo sectoriales.** El `product` ya trae `product_family` (árbol vía `parent_family_id`, con `hierarchy_purpose` para varios árboles). Un **único árbol de familias para todos los sectores**:

```
Banca → Depósito/ahorro · Financiación retail · Tarjetas · Financiación corporativa ·
        Trade finance · Inversión · Custodia · Tesorería · Mercados(FX/derivados)
Seguros → No Vida (Auto, Hogar…) · Vida (Riesgo, Ahorro…)
Retail → Alimentación → Lácteos → Yogur …
```

Con esto **se retiran `BANKING_PRODUCT_KIND`, `LINE_OF_BUSINESS` y demás catálogos de clasificación sectorial** — pasan a ser nodos del árbol de familias.

**Dos ejes distintos (el "kind" sectorial los mezclaba):**
- **Clasificación comercial** → `product_family` (jerárquica, genérica).
- **Naturaleza gruesa** → `product_kind` (físico / servicio / financiero / asegurador), genérico.
- **Arquetipo / comportamiento** (qué params y qué contrato aplican: hipoteca→LTV+garantía) → se resuelve por la **especialización que lleva el producto**, no por un catálogo por sector.

**Fichita sectorial = solo parámetros de catálogo** (rangos y config estándar), enganchada al `product` común por `product_id`. Nunca valores por cliente. Ejemplo banca (`banking_product`): rangos de interés/plazo/importe, `rate_type`+`reference_index`, comisiones (hijo `banking_product_fee`), y específicos mínimos (hipoteca `max_ltv`, tarjeta `grace_period_days`).

**Lo que varía por cliente NO va en el producto** — ya existe la cadena **cotización → contrato**: `insurance_quote`/`product_application` (la oferta específica) → `loan_arrangement`/`account_arrangement`/`insurance_policy` + `premium`/`coverage` (el contrato con los valores finales).

**El precio NO se unifica:** físico usa `price_list`/`price`; financiero/asegurador usa parámetros + cálculo por contrato. El `product` común une **identidad y catálogo**, no el mecanismo de precio.

**Acciones estructurales (pendientes de construir):**
1. Enganchar `banking_product`, `insurance_product`, `charge_item_definition`/`medication` al `product` común (`product_id`) — hoy van sueltos.
2. Definir el **árbol de familias** por sector (empezando por banca, taxonomía ampliada: retail + corporativa + trade + inversión + custodia + tesorería + mercados).
3. Retirar los catálogos de clasificación sectorial (`BANKING_PRODUCT_KIND`, `LINE_OF_BUSINESS`…), migrando sus valores a familias.
4. Reducir la fichita sectorial a solo parámetros (p. ej. `banking_product.interest_rate` escalar → rango).

### Producto — Seguros (detalle)

Aplicado el patrón. En seguros la parte de catálogo **ya está bien estructurada** como hijos del producto.

- **Clasificación → familia** (fuera `LINE_OF_BUSINESS` como catálogo): `Seguros → No Vida (Auto, Hogar, RC, Salud, Viaje, Patrimoniales, Transporte, Mascotas, Decesos…) · Vida (Riesgo, Ahorro, Unit-Linked, Rentas)`. **Dos árboles** vía `hierarchy_purpose`: comercial (ramo) y regulatorio (Solvencia II LoB).
- **Fichita sectorial = coberturas ofertadas + factores** (no rangos de precio, como banca):
  - `product_coverage_option` (hijo, ya existe) → enriquecer con `default_deductible`, `limit_min`/`limit_max`.
  - `rating_factor` (hijo, ya existe).
  - `insurance_product`: divisa, referencia de suscripción/regulatoria; se le **quita** `line_of_business` (→ familia) y se le **añade** `product_id`.
- **Vida/inversión:** `unit_link_fund` = **producto** (vehículo invertible, familia Vida > Unit-Linked); `annuity` y `fund_allocation` = **instancias** de la póliza.
- **Contrato ya completo:** `insurance_quote → insurance_policy → coverage → premium`. No se toca.
- **Clave del sector:** el precio no es un rango en el producto — se **calcula** con `rating_factor` sobre datos del cliente (en la cotización). La fichita de seguros es *"qué cubre + cómo se tarifica"*.

### Producto — Salud (detalle)

El sector donde "producto" menos se parece a un producto comercial. Dos particularidades:

- **Dos naturalezas en el mismo sector:**
  - **Servicio** → `healthcare_service` (categoría: consulta externa, hospitalización, urgencias, diagnóstico, cirugía, rehab, primaria) + su tarifa `charge_item_definition` (`base_price`).
  - **Físico/consumible** → `medication` (ATC, forma) + `medication_knowledge` (vía, receta), `nutrition_product`, dispositivos. **Con stock** (`pharmacy_inventory`), como el retail.
  - Ambos usan el `product` común; el físico además engancha stock. Es el caso que justifica que el genérico valga para físico **y** servicio.
- **Precio mediado por pagador:** la tarifa (`charge_item_definition`) es el catálogo; lo que se cobra depende de la **cobertura/claim**. Mismo patrón: catálogo = tarifa; valor real = per-instancia.
- **Clasificación → familia:** `Salud → Servicios (por categoría) · Productos (Medicamentos por ATC · Nutrición · Dispositivos)`. El **ATC** es un árbol clínico propio vía `hierarchy_purpose`, aparte del comercial.
- **Fichita:** servicio = categoría + organización + tarifa; medicamento = ATC/forma/vía/receta (`medication_knowledge`); `formulary_item` = pertenencia del medicamento al catálogo de la organización (equivalente sanitario de `product_catalog_item`).
- **Acciones:** enganchar `healthcare_service`/`medication`/`nutrition_product` al `product` común · árbol de familias Salud · `charge_item_definition` como tarifa · stock de físicos vía `pharmacy_inventory`.

### Producto — cierre

El trío (banca · seguros · salud) queda con **un mismo patrón**: `product` común (identidad + catálogo) + **clasificación por `product_family`** (un árbol por `hierarchy_purpose`) + **fichita sectorial de solo parámetros** enganchada por `product_id` + la **cadena por-instancia (cotización/tarifa → contrato/claim)** que ya existe. Los catálogos de clasificación pura (`BANKING_PRODUCT_KIND`, `LINE_OF_BUSINESS`) se retiran a favor de nodos de familia; **`SERVICE_CATEGORY` se conserva** (decisión Fase 3: opción 1) porque tipifica el servicio, no solo lo clasifica. **Producto: diseño cerrado, pendiente de construir.**

## 8bis. Estado de construcción (entregado, sin registrar)

Ejecución de "ajustar todo según lo cerrado" — entregado a outputs, visor y repo; **pendiente de registro oficial (sería M-105)**:

- **Fase 1** — FK del producto común: `product_id` en `banking_product`, `insurance_product`, `healthcare_service`, `medication`, `nutrition_product`; `parent_warehouse_id` y `work_center_id` en `warehouse`.
- **Fase 2a** — banca: `banking_product` enriquecido + `banking_product_fee`; catálogos `RATE_TYPE`, `REFERENCE_INDEX`, `FEE_KIND`, `FEE_FREQUENCY`; se retira `BANKING_PRODUCT_KIND`.
- **Fase 2b** — seguros: `insurance_product` y `product_coverage_option` enriquecidos; se retira `LINE_OF_BUSINESS`.
- **Fase 3a** — acelerador **SITE**: `point_of_sale` + `point_of_sale_warehouse` (N:M); catálogos `POS_TYPE`, `POS_STATUS`, `POS_WAREHOUSE_ROLE`.
- **Fase 3b** — SITE módulo *capacidad, disponibilidad y reserva* (término `SITE_BOOKING`): `bookable_resource` (recurso reservable, hijo del punto), `availability_slot` (hueco libre/ocupado, generaliza `slot`), `reservation` (compromiso, generaliza `appointment`); capacidad agregada = atributo `total_capacity` en `point_of_sale`; catálogos `RESOURCE_TYPE`, `RESOURCE_STATUS`, `AVAILABILITY_STATUS`, `RESERVATION_STATUS`. Sanidad conserva su `schedule`/`slot`/`appointment` FHIR; la primitiva SITE cubre hotel/mesa/aula.

- **Fase 3c** — SITE módulo *gestión del punto* (término `SITE_OPERATION`): `point_opening_hours` (horario regular por día de la semana), `point_calendar_exception` (festivo/cierre/obras/horario especial, enlazable al `public_holiday_calendar` de HR), `shift_template` (definición de turno), `shift_assignment` (**el cuadrante**), `time_clock_entry` (**fichaje**, contrastable contra el cuadrante). Catálogos `POINT_CALENDAR_EXCEPTION_KIND`, `SHIFT_KIND`, `SHIFT_ASSIGNMENT_STATUS`, `CLOCK_DIRECTION`, `CLOCK_CAPTURE_METHOD` (SITE) y `DAY_OF_WEEK` (`_GLOBAL_`). Tipos `TYD_TIME_OF_DAY` y `TYD_DURATION_SECONDS`: ya existían en el catálogo canónico de tipos, sin uso previo — **no se ha tocado el sistema de tipos**.
  - *Frontera respetada:* HR no tenía turnos ni fichaje (sí ausencias, festivos, jornada en `employee_employment_terms`). El maestro del empleado, su contrato y su jornada siguen en HR; el cuadrante y el fichaje son operación del punto.
  - *Completado después:* la **previsión de demanda del punto** contra la que se cuadra. `point_demand_forecast` (demanda por fecha y **franja horaria**: afluencia, tickets, comensales, pacientes, con valor previsto y real para medir la precisión) y `point_staffing_requirement` (personas necesarias por franja y puesto, con la productividad usada en el cálculo). Catálogo `POINT_DEMAND_MEASURE`; se reutiliza `FORECAST_METHOD` de SUPPLY_CHAIN. La cadena queda **demanda prevista → necesidad de personal → cuadrante (`shift_assignment`)**; la comparación es por punto/fecha/franja, no por FK, porque un turno existe haya previsión o no.
  - *Por qué no se reutilizó `demand_forecast` (SUPPLY_CHAIN):* tiene `product_id` **obligatorio** y granularidad `TYD_DATE`. La demanda de un punto para cuadrar no es demanda de producto (es afluencia o tickets) y necesita franja horaria, no día. Relajar aquel hecho para que sirviera a los dos usos habría roto su semántica de reaprovisionamiento. Es el caso contrario al de calidad, donde el sujeto ya era opcional y la reutilización sí encajaba.

**Corrección aplicada sobre la Fase 3b:** el catálogo `RESERVATION_STATUS` ya existía y era de **WAREHOUSE** (`stock_reservation`, valores ACTIVE/FULFILLED/RELEASED/EXPIRED); la Fase 3b lo sobrescribió con valores de reserva de hueco. Se ha restaurado a WAREHOUSE y la reserva de SITE usa ahora **`BOOKING_STATUS`**. En la misma pasada se normalizaron `estado` y `category` en los 16 catálogos creados en esta tanda, que se habían quedado fuera de convención.

- **Fase 3d** — EAM y QUALITY, **revisada al contrastar con disco** (ver §8): EAM **no** se absorbe y QUALITY **no** se parte. Único cambio de modelo: `equipment` gana `point_of_sale_id` y `work_center_id` (opcionales) y su descripción refleja el anclaje al emplazamiento. Sin mover entidades, sin retirar aceleradores, sin catálogos nuevos.

- **Calidad del punto** — controles e incidencias en tienda/restaurante/clínica, resuelta **anclando QUALITY al punto** en vez de creando entidades: 5 atributos (`quality_inspection.point_of_sale_id`, `non_conformance.point_of_sale_id`, `quality_specification.point_of_sale_id` + `inspection_kind_value_id`, `quality_inspection_line.observation`), `quality_specification.product_id` pasa a opcional y `INSPECTION_KIND` gana 7 tipos de punto. **0 entidades nuevas.** Ver §8.

- **Previsión de demanda del punto** — cierra el hueco que dejó abierto la 3c: `point_demand_forecast` + `point_staffing_requirement` en `SITE_OPERATION`, catálogo `POINT_DEMAND_MEASURE`, reutilizando `FORECAST_METHOD`. **2 entidades nuevas.** Ver §4, módulo 4.

Modelo: **951 entidades**. Fase 3 cerrada; calidad del punto y previsión del punto cubiertas.

## 9. Frontera de este documento

Arquitectura del modelo: capas, dependencias, estructura de operaciones, cobertura y huecos. **Qué se empaqueta y se vende es de Producto/Dirección** y no se fija aquí.
