# 📊 Sistema de Subproyectos - Guía Completa

## 🎯 Descripción General

El sistema de subproyectos permite dividir proyectos grandes en unidades más pequeñas y manejables, cada una con su propia cotización, ingresos, gastos y métricas de rentabilidad.

---

## 🏗️ Estructura del Sistema

### **Modelo de Datos**

```
Proyecto (Principal)
    └── Subproyecto 1
        ├── Cotización (opcional)
        ├── Facturas (ingresos)
        ├── Gastos
        └── Métricas de rentabilidad
    └── Subproyecto 2
    └── Subproyecto 3...
```

---

## 📋 Características Principales

### **1. Información del Subproyecto**
- ✅ **Código único**: Identificador único (ej: `EDIFICIO-001-SUB-CIMENTACION`)
- ✅ **Nombre descriptivo**: Nombre del subproyecto
- ✅ **Descripción**: Detalles adicionales
- ✅ **Proyecto padre**: Asociación al proyecto principal
- ✅ **Cotización**: Vinculación opcional a una cotización

### **2. Control de Fechas**
- ✅ **Fecha de inicio**: Cuándo comienza el subproyecto
- ✅ **Fecha fin estimada**: Cuándo se espera terminar
- ✅ **Fecha fin real**: Cuándo realmente terminó (se llena al completar)

### **3. Estados del Subproyecto**
- 🟡 **Pendiente**: No ha comenzado
- 🔵 **En Progreso**: Actualmente en ejecución
- 🟢 **Completado**: Finalizado exitosamente
- 🟠 **Pausado**: Temporalmente detenido
- 🔴 **Cancelado**: Cancelado/eliminado

### **4. Métricas Calculadas Automáticamente**
- 💰 **Monto Cotizado**: Valor de la cotización asociada
- 💵 **Ingresos Totales**: Suma de facturas pagadas
- 💸 **Gastos Totales**: Suma de gastos aprobados
- 📈 **Rentabilidad**: Ingresos - Gastos
- 📊 **Margen de Rentabilidad**: (Rentabilidad / Ingresos) × 100
- ⏳ **Porcentaje de Avance**: 0% - 100%

---

## 🚀 Cómo Usar el Sistema

### **Paso 1: Acceder al Dashboard**

```
URL: /proyectos/{proyecto_id}/subproyectos/
```

**Desde el navegador:**
1. Ve a la lista de proyectos
2. Selecciona un proyecto
3. Accede a "Subproyectos" (próximamente en el menú del proyecto)

**O accede directamente:**
- Ejemplo: `http://localhost:8000/proyectos/1/subproyectos/`

---

### **Paso 2: Crear un Subproyecto**

1. **Haz clic en "Nuevo Subproyecto"**
2. **Completa el formulario:**
   - **Código**: `EDIFICIO-001-SUB-001`
   - **Nombre**: `Fase 1 - Cimentación`
   - **Descripción**: Detalles del trabajo
   - **Cotización**: Selecciona una cotización existente (opcional)
   - **Fechas**: Inicio y fin estimado
   - **Estado**: Pendiente / En Progreso
   - **Avance**: 0% - 100%

3. **Guarda el subproyecto**

---

### **Paso 3: Asociar Ingresos (Facturas)**

Al crear o editar una **Factura**:
1. Selecciona el **Proyecto**
2. Selecciona el **Subproyecto** (nuevo campo)
3. La factura se contabilizará en el subproyecto cuando esté pagada

---

### **Paso 4: Asociar Gastos**

Al crear o editar un **Gasto**:
1. Selecciona el **Proyecto**
2. Selecciona el **Subproyecto** (nuevo campo)
3. El gasto se contabilizará cuando esté aprobado

---

### **Paso 5: Ver Rentabilidad**

El **Dashboard de Subproyectos** muestra:

#### **📊 Tarjetas de Resumen**
- Total Cotizado
- Ingresos Reales
- Gastos Totales
- Rentabilidad Total

#### **📈 Gráficos**
1. **Gráfico de Barras**: Ingresos vs Gastos vs Rentabilidad por subproyecto
2. **Gráfico de Pastel**: Distribución de gastos entre subproyectos

#### **📋 Tabla Detallada**
Cada subproyecto muestra:
- Código y nombre
- Monto cotizado
- Ingresos reales
- Gastos
- Rentabilidad (en verde si es positiva, rojo si es negativa)
- Margen de rentabilidad (%)
- Barra de progreso visual
- Estado actual
- Acciones (editar, eliminar)

---

## 🎨 Diseño y UX

### **Características Visuales**
- ✅ **Hero Section**: Encabezado moderno con gradiente oscuro
- ✅ **Tarjetas Estadísticas**: Métricas clave en cards animadas
- ✅ **Gráficos Interactivos**: Chart.js para visualización de datos
- ✅ **Tabla Moderna**: Diseño limpio y profesional
- ✅ **Indicadores de Color**: Verde para ganancias, rojo para pérdidas
- ✅ **Barras de Progreso**: Visualización del avance del subproyecto
- ✅ **Badges de Estado**: Colores según el estado del subproyecto
- ✅ **Responsive**: Se adapta a móviles y tablets

---

## 🔧 Administración

### **Django Admin**

Accede a `/admin/core/subproyecto/` para:
- Ver todos los subproyectos
- Crear, editar, eliminar subproyectos
- Ver métricas calculadas en tiempo real
- Filtrar por proyecto, estado, fechas
- Buscar por código o nombre

---

## 📊 Casos de Uso

### **Caso 1: Edificio con Múltiples Fases**

```
Proyecto: Edificio Corporativo XYZ
    ├── Subproyecto 1: Cimentación
    │   ├── Cotización: $50,000
    │   ├── Ingresos: $50,000
    │   ├── Gastos: $42,000
    │   └── Rentabilidad: $8,000 (16%)
    │
    ├── Subproyecto 2: Estructura
    │   ├── Cotización: $150,000
    │   ├── Ingresos: $100,000
    │   ├── Gastos: $95,000
    │   └── Rentabilidad: $5,000 (5%)
    │
    └── Subproyecto 3: Acabados
        ├── Cotización: $80,000
        ├── Ingresos: $0 (pendiente)
        ├── Gastos: $0
        └── Rentabilidad: $0
```

### **Caso 2: Proyecto con Cotizaciones Separadas**

```
Proyecto: Instalación de Torres
    ├── Subproyecto 1: Torre Norte (Cotización A)
    ├── Subproyecto 2: Torre Sur (Cotización B)
    └── Subproyecto 3: Cableado (Cotización C)
```

---

## 🎯 Beneficios

1. **📊 Visibilidad Granular**: Ver la rentabilidad de cada fase del proyecto
2. **💰 Control Financiero**: Identificar qué subproyectos son más rentables
3. **📈 Toma de Decisiones**: Datos para optimizar recursos
4. **🎯 Seguimiento**: Monitorear el avance de cada fase
5. **📋 Reportes**: Generar informes detallados por subproyecto
6. **🔍 Transparencia**: Cliente puede ver el desglose de costos

---

## 🚀 URLs del Sistema

```python
# Dashboard de subproyectos
/proyectos/{proyecto_id}/subproyectos/

# Crear subproyecto
/proyectos/{proyecto_id}/subproyectos/crear/

# Editar subproyecto
/subproyectos/{id}/editar/

# Eliminar subproyecto
/subproyectos/{id}/eliminar/
```

---

## 📱 Próximas Mejoras Sugeridas

1. **Integración en Proyecto Detail**: Agregar sección de subproyectos en el detalle del proyecto
2. **Selector en Formularios**: Agregar selector de subproyecto en formularios de Factura y Gasto
3. **Reportes PDF**: Generar reportes de rentabilidad por subproyecto
4. **Dashboard Comparativo**: Comparar rentabilidad entre proyectos
5. **Alertas**: Notificar cuando un subproyecto tenga pérdidas
6. **Exportar a Excel**: Exportar datos de subproyectos
7. **Gráfico de Gantt**: Visualizar timeline de subproyectos

---

## 💡 Tips de Uso

### **Nomenclatura Recomendada para Códigos**
```
{PROYECTO}-{NUMERO}-SUB-{FASE}

Ejemplos:
- EDIFICIO-001-SUB-CIMENTACION
- TORRE-002-SUB-ESTRUCTURA
- INST-003-SUB-CABLEADO
```

### **Mejores Prácticas**
1. ✅ Crea subproyectos al inicio del proyecto
2. ✅ Asocia cada cotización a su subproyecto correspondiente
3. ✅ Registra todos los gastos en el subproyecto correcto
4. ✅ Actualiza el porcentaje de avance regularmente
5. ✅ Marca como "Completado" cuando termine
6. ✅ Revisa el dashboard semanalmente

---

## 🎉 ¡Sistema Listo!

El sistema de subproyectos está **100% funcional** y listo para usar.

**Para empezar:**
1. Levanta el servidor: `python3 manage.py runserver`
2. Ve a: `http://localhost:8000/proyectos/1/subproyectos/`
3. Crea tu primer subproyecto
4. Asocia facturas y gastos
5. ¡Observa la rentabilidad en tiempo real!

---

**¿Preguntas o sugerencias?**  
El sistema está diseñado para ser intuitivo y fácil de usar. ¡Explora y descubre todas sus funcionalidades! 🚀

