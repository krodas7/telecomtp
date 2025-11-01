# 🗄️ ROADMAP DE BASE DE DATOS - Sistema ARCA Construcción

## 📋 Resumen General

Este documento detalla **qué datos se guardan en la base de datos** para cada módulo del sistema.

---

## 🏗️ 1. MÓDULO DE PROYECTOS

### Tabla: `Proyecto`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único del proyecto | ✅ Automático |
| `nombre` | String | Nombre del proyecto | ✅ Usuario ingresa |
| `descripcion` | Text | Descripción detallada | ✅ Usuario ingresa |
| `cliente` | ForeignKey | Cliente asociado | ✅ Usuario selecciona |
| `fecha_inicio` | Date | Fecha de inicio | ✅ Usuario ingresa |
| `estado` | Choices | planificacion/en_progreso/completado/en_pausa | ✅ Usuario selecciona |
| `activo` | Boolean | Si está activo | ✅ Usuario marca |
| `colaboradores` | ManyToMany | Colaboradores asignados | ✅ Usuario asigna |
| `presupuesto` | Decimal | Presupuesto estimado | ✅ Usuario ingresa |
| `costo_real` | Decimal | Costo real acumulado | ✅ Se calcula automáticamente |

**Relaciones:**
- 1 Proyecto → N Facturas
- 1 Proyecto → N Gastos/Egresos
- 1 Proyecto → N Cotizaciones
- 1 Proyecto → N Anticipos
- 1 Proyecto → N Archivos
- 1 Proyecto → N Colaboradores (Many-to-Many)
- 1 Proyecto → N Planillas Liquidadas
- 1 Proyecto → 1 Configuración de Planilla

---

## 👥 2. MÓDULO DE CLIENTES

### Tabla: `Cliente`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `razon_social` | String | Nombre/razón social | ✅ Usuario ingresa |
| `codigo_fiscal` | String | RUC/NIT | ✅ Usuario ingresa |
| `direccion` | Text | Dirección | ✅ Usuario ingresa |
| `telefono` | String | Teléfono | ✅ Usuario ingresa |
| `email` | Email | Correo electrónico | ✅ Usuario ingresa |
| `activo` | Boolean | Si está activo | ✅ Usuario marca |
| `fecha_registro` | DateTime | Fecha de creación | ✅ Automático |

**Relaciones:**
- 1 Cliente → N Proyectos
- 1 Cliente → N Facturas
- 1 Cliente → N Cotizaciones
- 1 Cliente → N Anticipos

---

## 💼 3. MÓDULO DE COLABORADORES

### Tabla: `Colaborador`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `nombre` | String | Nombre completo | ✅ Usuario ingresa |
| `dpi` | String | DPI/Cédula | ✅ Usuario ingresa |
| `direccion` | Text | Dirección | ✅ Usuario ingresa |
| `telefono` | String | Teléfono | ✅ Usuario ingresa |
| `email` | Email | Correo | ✅ Usuario ingresa |
| `salario` | Decimal | Salario mensual | ✅ Usuario ingresa |
| `fecha_contratacion` | Date | Fecha de contratación | ✅ Usuario ingresa |
| `fecha_vencimiento_contrato` | Date | Vencimiento de contrato | ✅ Usuario ingresa |
| `aplica_bono_general` | Boolean | Si recibe bono general | ✅ Usuario marca |
| `aplica_bono_produccion` | Boolean | Si recibe bono de producción | ✅ Usuario marca |
| `aplica_retenciones` | Boolean | Si tiene retenciones | ✅ Usuario marca |
| `activo` | Boolean | Si está activo | ✅ Usuario marca |

**Relaciones:**
- N Colaboradores → N Proyectos (Many-to-Many)
- 1 Colaborador → N Anticipos de Proyecto

---

## 💰 4. MÓDULO DE FACTURAS

### Tabla: `Factura`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `numero_factura` | String | Número único | ✅ Usuario ingresa |
| `proyecto` | ForeignKey | Proyecto asociado | ✅ Usuario selecciona |
| `cliente` | ForeignKey | Cliente | ✅ Usuario selecciona |
| `fecha_emision` | Date | Fecha de emisión | ✅ Usuario ingresa |
| `fecha_vencimiento` | Date | Fecha de vencimiento | ✅ Usuario ingresa |
| `monto_subtotal` | Decimal | Subtotal | ✅ Usuario ingresa |
| `porcentaje_itbms` | Decimal | % de ITBMS (0%, 3.5%, 7%) | ✅ Usuario selecciona |
| `monto_iva` | Decimal | Monto de ITBMS | ✅ Se calcula automáticamente |
| `monto_total` | Decimal | Total de la factura | ✅ Se calcula automáticamente |
| `monto_pagado` | Decimal | Monto cobrado | ✅ Usuario ingresa |
| `estado` | Choices | emitida/pagada/vencida/cancelada | ✅ Usuario selecciona |
| `descripcion` | Text | Descripción | ✅ Usuario ingresa |

**Relaciones:**
- N Facturas → 1 Proyecto
- N Facturas → 1 Cliente

---

## 💵 5. MÓDULO DE ANTICIPOS

### Tabla: `Anticipo`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `cliente` | ForeignKey | Cliente | ✅ Usuario selecciona |
| `proyecto` | ForeignKey | Proyecto | ✅ Usuario selecciona |
| `factura` | ForeignKey | Factura (opcional) | ✅ Usuario selecciona |
| `monto_total` | Decimal | Monto total del anticipo | ✅ Usuario ingresa |
| `monto_aplicado` | Decimal | Monto aplicado a factura | ✅ Usuario ingresa |
| `monto_aplicado_proyecto` | Decimal | Monto aplicado a proyecto | ✅ Usuario ingresa |
| `saldo_pendiente` | Decimal | Saldo restante | ✅ Se calcula automáticamente |
| `fecha_anticipo` | Date | Fecha del anticipo | ✅ Usuario ingresa |
| `fecha_aplicacion` | Date | Fecha de aplicación | ✅ Automático al aplicar |
| `estado` | Choices | pendiente/aplicado/liquidado | ✅ Usuario/Sistema |
| `aplicado_al_proyecto` | Boolean | Si fue aplicado | ✅ Automático |
| `observaciones` | Text | Notas | ✅ Usuario ingresa |

### Tabla: `AnticipoProyecto`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `proyecto` | ForeignKey | Proyecto | ✅ Usuario selecciona |
| `colaborador` | ForeignKey | Colaborador | ✅ Usuario selecciona |
| `monto` | Decimal | Monto del anticipo | ✅ Usuario ingresa |
| `fecha_anticipo` | Date | Fecha | ✅ Usuario ingresa |
| `estado` | Choices | pendiente/liquidado/cancelado | ✅ Usuario/Sistema |
| `fecha_liquidacion` | Date | Fecha de liquidación | ✅ Automático al liquidar |
| `observaciones` | Text | Notas | ✅ Usuario ingresa |

**Relaciones:**
- N Anticipos → 1 Cliente
- N Anticipos → 1 Proyecto
- N Anticipos → 1 Factura (opcional)
- N AnticiposProyecto → 1 Proyecto
- N AnticiposProyecto → 1 Colaborador

---

## 📊 6. MÓDULO DE EGRESOS/GASTOS

### Tabla: `Gasto`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `proyecto` | ForeignKey | Proyecto | ✅ Usuario selecciona |
| `categoria` | ForeignKey | Categoría de gasto | ✅ Usuario selecciona |
| `descripcion` | Text | Descripción del gasto | ✅ Usuario ingresa |
| `monto` | Decimal | Monto del gasto | ✅ Usuario ingresa |
| `fecha_gasto` | Date | Fecha del gasto | ✅ Usuario ingresa |
| `factura_proveedor` | String | No. de factura | ✅ Usuario ingresa |
| `proveedor` | String | Nombre del proveedor | ✅ Usuario ingresa |
| `comprobante` | File | Archivo de comprobante | ✅ Usuario sube |
| `aprobado` | Boolean | Si está aprobado | ✅ Usuario aprueba |
| `fecha_aprobacion` | DateTime | Fecha de aprobación | ✅ Automático al aprobar |
| `aprobado_por` | ForeignKey | Usuario que aprobó | ✅ Automático |
| `observaciones` | Text | Notas | ✅ Usuario ingresa |

### Tabla: `CategoriaGasto`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `nombre` | String | Nombre de la categoría | ✅ Usuario ingresa |
| `descripcion` | Text | Descripción | ✅ Usuario ingresa |
| `color` | String (Hex) | Color para la UI | ✅ Usuario selecciona |
| `icono` | String | Clase de FontAwesome | ✅ Usuario selecciona |
| `activo` | Boolean | Si está activa | ✅ Usuario marca |

**Relaciones:**
- N Gastos → 1 Proyecto
- N Gastos → 1 CategoriaGasto
- 1 CategoriaGasto → N Gastos

---

## 📝 7. MÓDULO DE COTIZACIONES

### Tabla: `Cotizacion`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `numero_cotizacion` | String | COT-2025-0001 | ✅ Se genera automáticamente |
| `proyecto` | ForeignKey | Proyecto | ✅ Usuario selecciona |
| `cliente` | ForeignKey | Cliente | ✅ Usuario selecciona |
| `titulo` | String | Título de la cotización | ✅ Usuario ingresa |
| `fecha_emision` | Date | Fecha de emisión | ✅ Usuario ingresa |
| `fecha_vencimiento` | Date | Fecha de vencimiento | ✅ Usuario ingresa (opcional) |
| `monto_subtotal` | Decimal | Subtotal | ✅ Se calcula de los items |
| `monto_iva` | Decimal | ITBMS | ✅ Se calcula automáticamente |
| `monto_total` | Decimal | Total | ✅ Se calcula automáticamente |
| `estado` | Choices | enviada/aceptada/rechazada | ✅ Usuario/Sistema |
| `fecha_aceptacion` | Date | Fecha de aceptación | ✅ Automático al aprobar |
| `terminos_condiciones` | Text | Términos y condiciones | ✅ Usuario ingresa |
| `creado_por` | ForeignKey | Usuario creador | ✅ Automático |
| `modificado_por` | ForeignKey | Usuario modificador | ✅ Automático |
| `fecha_creacion` | DateTime | Fecha de creación | ✅ Automático |
| `fecha_modificacion` | DateTime | Fecha de modificación | ✅ Automático |

### Tabla: `ItemCotizacion`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `cotizacion` | ForeignKey | Cotización asociada | ✅ Automático |
| `descripcion` | String | Descripción del item | ✅ Usuario ingresa |
| `cantidad` | Decimal | Cantidad | ✅ Usuario ingresa |
| `precio_unitario` | Decimal | Precio de venta | ✅ Usuario ingresa |
| `precio_costo` | Decimal | Precio de costo | ✅ Usuario ingresa |
| `total` | Decimal | Total del item | ✅ Se calcula automáticamente |
| `orden` | Integer | Orden de visualización | ✅ Automático |
| `creado_en` | DateTime | Fecha de creación | ✅ Automático |

### Tabla: `ItemReutilizable`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `descripcion` | String | Descripción del item | ✅ Usuario ingresa |
| `categoria` | String | Categoría | ✅ Usuario ingresa |
| `precio_unitario` | Decimal | Precio de venta | ✅ Usuario ingresa |
| `precio_costo` | Decimal | Precio de costo | ✅ Usuario ingresa |
| `activo` | Boolean | Si está activo | ✅ Usuario marca |
| `notas` | Text | Notas adicionales | ✅ Usuario ingresa |
| `creado_por` | ForeignKey | Usuario creador | ✅ Automático |
| `fecha_creacion` | DateTime | Fecha de creación | ✅ Automático |

**Relaciones:**
- N Cotizaciones → 1 Proyecto
- N Cotizaciones → 1 Cliente
- 1 Cotización → N ItemsCotizacion

---

## 💼 8. MÓDULO DE PLANILLAS

### Tabla: `PlanillaLiquidada`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `proyecto` | ForeignKey | Proyecto | ✅ Automático |
| `mes` | Integer | Mes (1-12) | ✅ Usuario selecciona |
| `año` | Integer | Año (2025) | ✅ Usuario selecciona |
| `quincena` | Integer | Primera/Segunda quincena | ✅ Usuario selecciona |
| `fecha_liquidacion` | DateTime | Fecha de liquidación | ✅ Automático |
| `total_salarios` | Decimal | Total salarios quincenales | ✅ Se calcula automáticamente |
| `total_anticipos` | Decimal | Total anticipos descontados | ✅ Se calcula automáticamente |
| `total_planilla` | Decimal | Total a pagar | ✅ Se calcula automáticamente |
| `cantidad_personal` | Integer | Cantidad de personal | ✅ Se calcula automáticamente |
| `liquidada_por` | ForeignKey | Usuario que liquidó | ✅ Automático |
| `observaciones` | Text | Observaciones | ✅ Usuario ingresa |

### Tabla: `ConfiguracionPlanilla`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `proyecto` | OneToOne | Proyecto | ✅ Automático |
| `retencion_seguro_social` | Decimal | Monto fijo mensual ($) | ✅ Usuario ingresa |
| `retencion_seguro_educativo` | Decimal | Monto fijo mensual ($) | ✅ Usuario ingresa |
| `bono_general` | Decimal | Bono fijo mensual ($) | ✅ Usuario ingresa |
| `bono_produccion` | Decimal | Bono % sobre salario | ✅ Usuario ingresa |
| `aplicar_retenciones` | Boolean | Si aplica retenciones | ✅ Usuario marca |
| `aplicar_bonos` | Boolean | Si aplica bonos | ✅ Usuario marca |
| `modificado_por` | ForeignKey | Usuario modificador | ✅ Automático |
| `creado_en` | DateTime | Fecha de creación | ✅ Automático |
| `modificado_en` | DateTime | Fecha de modificación | ✅ Automático |

**Relaciones:**
- N PlanillasLiquidadas → 1 Proyecto
- 1 ConfiguracionPlanilla → 1 Proyecto (OneToOne)

---

## 📁 9. MÓDULO DE ARCHIVOS

### Tabla: `Archivo`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `proyecto` | ForeignKey | Proyecto asociado | ✅ Usuario selecciona |
| `nombre` | String | Nombre del archivo | ✅ Usuario ingresa |
| `archivo` | FileField | Archivo subido | ✅ Usuario sube |
| `tipo` | Choices | documento/plano/imagen/otro | ✅ Usuario selecciona |
| `descripcion` | Text | Descripción | ✅ Usuario ingresa |
| `fecha_subida` | DateTime | Fecha de carga | ✅ Automático |
| `subido_por` | ForeignKey | Usuario que subió | ✅ Automático |
| `tamaño` | Integer | Tamaño en bytes | ✅ Automático |

**Relaciones:**
- N Archivos → 1 Proyecto

---

## 📅 10. MÓDULO DE EVENTOS (Dashboard)

### Tabla: `EventoCalendario`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `titulo` | String | Título del evento | ✅ Usuario ingresa |
| `descripcion` | Text | Descripción | ✅ Usuario ingresa |
| `fecha_inicio` | Date | Fecha de inicio | ✅ Usuario ingresa |
| `fecha_fin` | Date | Fecha de fin | ✅ Usuario ingresa |
| `tipo` | Choices | reunion/llamada/visita/otro | ✅ Usuario selecciona |
| `color` | String (Hex) | Color del evento | ✅ Usuario selecciona |
| `todo_el_dia` | Boolean | Si es todo el día | ✅ Usuario marca |
| `creado_por` | ForeignKey | Usuario creador | ✅ Automático |
| `creado_en` | DateTime | Fecha de creación | ✅ Automático |
| `actualizado_en` | DateTime | Fecha de actualización | ✅ Automático |

### Tabla: `NotaPostit`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `evento` | ForeignKey | Evento asociado | ✅ Automático |
| `contenido` | Text | Contenido de la nota | ✅ Usuario ingresa |
| `color` | String (Hex) | Color del post-it | ✅ Usuario selecciona |
| `creado_por` | ForeignKey | Usuario creador | ✅ Automático |
| `creado_en` | DateTime | Fecha de creación | ✅ Automático |

**Relaciones:**
- 1 Evento → N NotasPostit

---

## 📦 11. MÓDULO DE INVENTARIO

### Tabla: `ProductoInventario`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `codigo` | String | Código único | ✅ Usuario ingresa |
| `nombre` | String | Nombre del producto | ✅ Usuario ingresa |
| `descripcion` | Text | Descripción | ✅ Usuario ingresa |
| `categoria` | ForeignKey | Categoría | ✅ Usuario selecciona |
| `unidad_medida` | String | und/kg/m/l/etc | ✅ Usuario selecciona |
| `cantidad_disponible` | Decimal | Stock actual | ✅ Usuario ingresa |
| `cantidad_minima` | Decimal | Stock mínimo | ✅ Usuario ingresa |
| `precio_compra` | Decimal | Precio de compra | ✅ Usuario ingresa |
| `precio_venta` | Decimal | Precio de venta | ✅ Usuario ingresa |
| `activo` | Boolean | Si está activo | ✅ Usuario marca |

### Tabla: `MovimientoInventario`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `producto` | ForeignKey | Producto | ✅ Usuario selecciona |
| `tipo` | Choices | entrada/salida/ajuste | ✅ Usuario selecciona |
| `cantidad` | Decimal | Cantidad del movimiento | ✅ Usuario ingresa |
| `proyecto` | ForeignKey | Proyecto (opcional) | ✅ Usuario selecciona |
| `fecha` | DateTime | Fecha del movimiento | ✅ Automático |
| `usuario` | ForeignKey | Usuario que registró | ✅ Automático |
| `observaciones` | Text | Notas | ✅ Usuario ingresa |

**Relaciones:**
- N Productos → 1 Categoría
- N Movimientos → 1 Producto
- N Movimientos → 1 Proyecto (opcional)

---

## 👤 12. MÓDULO DE USUARIOS

### Tabla: `User` (Django default)
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `username` | String | Nombre de usuario | ✅ Usuario ingresa |
| `email` | Email | Correo | ✅ Usuario ingresa |
| `password` | String (hash) | Contraseña encriptada | ✅ Usuario ingresa |
| `first_name` | String | Nombre | ✅ Usuario ingresa |
| `last_name` | String | Apellido | ✅ Usuario ingresa |
| `is_active` | Boolean | Si está activo | ✅ Admin marca |
| `is_staff` | Boolean | Si es staff | ✅ Admin marca |
| `is_superuser` | Boolean | Si es superusuario | ✅ Admin marca |
| `date_joined` | DateTime | Fecha de registro | ✅ Automático |
| `last_login` | DateTime | Último login | ✅ Automático |

### Tabla: `LogActividad`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `usuario` | ForeignKey | Usuario | ✅ Automático |
| `accion` | String | Tipo de acción | ✅ Automático |
| `modulo` | String | Módulo afectado | ✅ Automático |
| `descripcion` | Text | Descripción detallada | ✅ Automático |
| `ip_address` | String | IP del usuario | ✅ Automático |
| `fecha` | DateTime | Fecha y hora | ✅ Automático |

**Relaciones:**
- Todos los modelos tienen relación con User (creado_por, modificado_por, etc.)

---

## ⚙️ 13. MÓDULO DE SISTEMA

### Tabla: `ConfiguracionSistema`
| Campo | Tipo | Descripción | Se Guarda |
|-------|------|-------------|-----------|
| `id` | Integer | ID único | ✅ Automático |
| `nombre_empresa` | String | Nombre de la empresa | ✅ Admin ingresa |
| `logo` | ImageField | Logo de la empresa | ✅ Admin sube |
| `telefono` | String | Teléfono | ✅ Admin ingresa |
| `email` | Email | Correo | ✅ Admin ingresa |
| `direccion` | Text | Dirección | ✅ Admin ingresa |
| `moneda` | String | USD/GTQ/etc | ✅ Admin selecciona |
| `timezone` | String | Zona horaria | ✅ Admin selecciona |

---

## 📊 RESUMEN DE ALMACENAMIENTO

### ✅ Se Guarda en Base de Datos:
1. ✅ **Todos los proyectos** con su información completa
2. ✅ **Todos los clientes** con datos de contacto
3. ✅ **Todos los colaboradores** con salarios y configuración de bonos/retenciones
4. ✅ **Todas las facturas** con cálculos de ITBMS
5. ✅ **Todos los anticipos** (cliente y proyecto)
6. ✅ **Todos los gastos/egresos** con comprobantes
7. ✅ **Todas las cotizaciones** con items detallados
8. ✅ **Items reutilizables** para cotizaciones futuras
9. ✅ **Planillas liquidadas** con histórico completo
10. ✅ **Configuraciones de planilla** por proyecto
11. ✅ **Archivos subidos** (físicamente en media/, metadata en DB)
12. ✅ **Eventos del calendario** con notas post-it
13. ✅ **Movimientos de inventario** con trazabilidad completa
14. ✅ **Log de actividades** de usuarios
15. ✅ **Configuración del sistema**

### ❌ NO se Guarda (Datos Calculados en Tiempo Real):
1. ❌ **Rentabilidad**: Se calcula de Ingresos - Gastos
2. ❌ **Tendencias**: Se calculan comparando meses
3. ❌ **Estadísticas del dashboard**: Se calculan de los datos existentes
4. ❌ **Totales de categorías**: Se suman de los gastos
5. ❌ **Gráficos**: Se generan de los datos al cargar la página

---

## 🔄 FLUJO DE DATOS

```
1. Usuario ingresa datos → Django Form → Validación
2. Si es válido → Se guarda en DB (SQLite/PostgreSQL)
3. Se genera Log de Actividad
4. Se actualizan totales y cálculos relacionados
5. Se muestra mensaje de éxito
```

---

## 🛡️ INTEGRIDAD DE DATOS

### Protecciones Implementadas:
- ✅ **Validación de formularios** antes de guardar
- ✅ **Foreign Keys** con `on_delete=CASCADE` o `SET_NULL`
- ✅ **Unique constraints** (ej: numero_cotizacion, codigo_fiscal)
- ✅ **Campos requeridos** vs opcionales
- ✅ **Valores por defecto** para evitar NULL
- ✅ **Auditoria**: creado_por, modificado_por, fechas
- ✅ **Soft delete**: activo=False en lugar de borrar

---

## 📌 NOTAS IMPORTANTES

1. **Los anticipos se ELIMINAN** después de liquidar la planilla (no deben persistir)
2. **Las cotizaciones generan número automático** al guardar
3. **Los totales se calculan automáticamente** (no se ingresan manualmente)
4. **Los archivos se guardan físicamente** en `media/` y metadata en DB
5. **El service worker NO cachea** datos de la DB, solo archivos estáticos
6. **Todos los módulos tienen timestamps** (fecha_creacion, fecha_modificacion)
7. **Todos los cambios importantes se registran** en LogActividad

---

**Fecha de Generación**: 2025-11-02  
**Versión del Sistema**: 3.0  
**Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)

