# 🚀 Carga de Datos Masivos - Sistema de Construcción

Este conjunto de scripts permite cargar el sistema de construcción con datos masivos y realistas para probar todas las funcionalidades, incluyendo el módulo de IA, dashboard con gráficos, y generación de reportes.

## 📋 Contenido

- **`cargar_datos_masivos.py`** - Generador principal de datos del sistema
- **`generar_datos_ia.py`** - Generador de datos específicos para IA
- **`instalar_datos_completos.py`** - Instalador automático que ejecuta todo
- **`README_CARGA_DATOS.md`** - Este archivo de instrucciones

## 🎯 Objetivos

1. **Generar datos masivos** para probar rendimiento del sistema
2. **Crear datos realistas** para el dashboard y gráficos
3. **Preparar datos de entrenamiento** para los modelos de IA
4. **Generar casos de prueba** para análisis de riesgos
5. **Simular escenarios reales** de construcción

## 📊 Datos Generados

### Datos Principales del Sistema
- **200 Clientes** con información realista
- **80 Proyectos** con diferentes estados y presupuestos
- **50 Facturas** con variados estados y montos
- **20 Anticipos** para diferentes proyectos
- **300 Gastos** distribuidos por categorías
- **30 Colaboradores** con perfiles completos
- **100 Logs de Actividad** del sistema

### Datos Específicos para IA
- **Historial de costos** con variaciones temporales
- **Patrones de riesgos** para detección automática
- **Métricas de rendimiento** para análisis predictivo
- **Casos de prueba** para validar algoritmos de IA

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
```bash
python instalar_datos_completos.py
```

### Opción 2: Instalación Manual
```bash
# Paso 1: Generar datos masivos
python cargar_datos_masivos.py

# Paso 2: Generar datos para IA
python generar_datos_ia.py
```

## ⚠️ Requisitos Previos

### 1. Dependencias de Python
```bash
pip install -r requirements.txt
```

### 2. Dependencias Específicas para IA
```bash
pip install numpy pandas scikit-learn
```

### 3. Base de Datos
- Asegúrate de que las migraciones estén aplicadas:
```bash
python manage.py migrate
```

### 4. Entorno Virtual (Recomendado)
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🔧 Configuración

### 1. Verificar Configuración de Django
Asegúrate de que `sistema_construccion.settings` esté configurado correctamente.

### 2. Base de Datos
Los scripts funcionan con SQLite por defecto. Si usas otra base de datos, verifica la configuración.

### 3. Permisos
Asegúrate de tener permisos de escritura en el directorio del proyecto.

## 📱 Uso del Sistema

### 1. Acceder al Sistema
- **URL**: http://127.0.0.1:8000/
- **Usuario**: `admin`
- **Contraseña**: `admin123`

### 2. Navegar por el Dashboard
- **Dashboard Principal**: Vista general del sistema
- **Dashboard de IA**: Módulo de inteligencia artificial
- **Reportes**: Generación de reportes personalizados

### 3. Probar Funcionalidades de IA
- **Predicción de Costos**: Análisis ML de costos de proyectos
- **Detección de Riesgos**: Identificación automática de riesgos
- **Generación de Reportes**: Reportes inteligentes del sistema
- **Chatbot IA**: Asistente inteligente para consultas

## 🧪 Casos de Prueba Incluidos

### 1. Proyecto de Alto Riesgo
- **Nombre**: "Proyecto de Alto Riesgo - Pruebas IA"
- **Características**: Incidentes de seguridad, problemas de calidad
- **Propósito**: Probar detección automática de riesgos

### 2. Proyecto con Sobrecostos
- **Nombre**: "Proyecto con Sobrecostos - Pruebas IA"
- **Características**: Gastos excesivos por materiales
- **Propósito**: Probar detección de sobrecostos

### 3. Proyecto Exitoso
- **Nombre**: "Proyecto Exitoso - Pruebas IA"
- **Características**: Eficiencia en mano de obra, completado a tiempo
- **Propósito**: Probar análisis de éxito

### 4. Proyecto con Retrasos
- **Nombre**: "Proyecto con Retrasos - Pruebas IA"
- **Características**: Retrasos en cronograma, costos adicionales
- **Propósito**: Probar detección de retrasos

## 📈 Funcionalidades a Probar

### Dashboard y Gráficos
- [ ] Gráficos de proyectos por estado
- [ ] Gráficos de ingresos vs gastos
- [ ] Métricas de rendimiento
- [ ] Indicadores de riesgo

### Módulo de IA
- [ ] Predicción de costos
- [ ] Detección de riesgos
- [ ] Generación de reportes
- [ ] Análisis de insights

### Reportes del Sistema
- [ ] Reporte general del sistema
- [ ] Reporte de proyectos
- [ ] Reporte financiero
- [ ] Reporte de riesgos

### Rendimiento del Sistema
- [ ] Tiempo de carga de páginas
- [ ] Tiempo de generación de reportes
- [ ] Tiempo de análisis de IA
- [ ] Uso de memoria y CPU

## 🔍 Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install django
# o
pip install -r requirements.txt
```

### Error: "No module named 'numpy'"
```bash
pip install numpy pandas scikit-learn
```

### Error: "Database is locked"
- Cierra cualquier aplicación que esté usando la base de datos
- Reinicia el servidor Django

### Error: "Permission denied"
- Verifica permisos de escritura en el directorio
- Ejecuta como administrador si es necesario

### Error: "Table already exists"
- Los scripts usan `get_or_create`, no deberían dar este error
- Si persiste, elimina la base de datos y ejecuta las migraciones

## 📊 Monitoreo del Proceso

### Logs en Tiempo Real
Los scripts muestran progreso en tiempo real:
```
🚀 INICIANDO GENERACIÓN DE DATOS MASIVOS
============================================================
📋 PASO 1: Generando roles y usuarios...
📋 PASO 2: Generando categorías de gasto...
📋 PASO 3: Generando clientes...
Clientes creados: 50/200
Clientes creados: 100/200
...
```

### Verificación de Datos
Después de la instalación, puedes verificar los datos:
```python
# En el shell de Django
python manage.py shell

from core.models import *
print(f"Clientes: {Cliente.objects.count()}")
print(f"Proyectos: {Proyecto.objects.count()}")
print(f"Facturas: {Factura.objects.count()}")
```

## 🎯 Próximos Pasos

### 1. Probar el Sistema
- Inicia el servidor: `python manage.py runserver`
- Accede al dashboard: http://127.0.0.1:8000/
- Navega por todas las funcionalidades

### 2. Validar Funcionalidades de IA
- Genera reportes del sistema
- Prueba predicción de costos
- Verifica detección de riesgos
- Usa el chatbot IA

### 3. Analizar Rendimiento
- Monitorea tiempos de respuesta
- Verifica uso de recursos
- Identifica cuellos de botella

### 4. Personalizar Datos
- Modifica los scripts según tus necesidades
- Ajusta cantidades y tipos de datos
- Agrega nuevos casos de prueba

## 📞 Soporte

Si encuentras problemas:

1. **Revisa los logs** de error en la consola
2. **Verifica las dependencias** están instaladas
3. **Confirma la configuración** de Django
4. **Revisa permisos** de archivos y directorios

## 🔄 Actualización de Datos

Para actualizar o regenerar datos:

```bash
# Eliminar datos existentes (opcional)
python manage.py flush

# Regenerar datos
python instalar_datos_completos.py
```

## 📝 Notas Importantes

- **Los scripts son idempotentes**: Puedes ejecutarlos múltiples veces sin problemas
- **Datos realistas**: Los datos generados simulan escenarios reales de construcción
- **Rendimiento**: El sistema está optimizado para manejar la carga de datos generada
- **Seguridad**: Los scripts solo crean datos de prueba, no modifican configuraciones críticas

---

**¡El sistema está listo para pruebas de rendimiento y funcionalidad completa!** 🎉
