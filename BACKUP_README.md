# 🔒 Sistema de Respaldo Automático - Sistema de Construcción

## 📋 Descripción General

Este sistema implementa un respaldo automático completo del sistema de construcción, incluyendo:
- **Base de datos SQLite** completa
- **Archivos de media** (documentos, imágenes, etc.)
- **Archivos de configuración** importantes
- **Logs del sistema**
- **Compresión automática** de respaldos
- **Limpieza automática** de respaldos antiguos

## 🚀 Características Principales

### ✅ **Respaldo Completo**
- Base de datos con verificación de integridad
- Archivos de media y configuración
- Logs del sistema
- Compresión ZIP automática

### ✅ **Automatización**
- Comando de Django integrado
- Script independiente para Windows
- Configuración de tareas programadas
- Limpieza automática de respaldos antiguos

### ✅ **Seguridad**
- Verificación de integridad de la BD
- Reportes detallados de cada respaldo
- Manejo de errores robusto
- Logs de auditoría

## 📁 Estructura de Archivos

```
sistema-construccion-django/
├── backups/
│   ├── manual/          # Respaldos manuales
│   └── automatico/      # Respaldos automáticos
├── core/management/commands/
│   └── crear_respaldo.py    # Comando Django
├── scripts/
│   ├── backup_automatico.py         # Script completo
│   ├── backup_windows_simple.py     # Script Windows (recomendado)
│   ├── configurar_backup_windows.bat # Configurador Windows
│   └── backup_windows.bat           # Script batch Windows
└── logs/
    └── backup.log       # Logs de respaldo
```

## 🛠️ Métodos de Respaldo

### 1. **Comando Django (Recomendado para desarrollo)**

```bash
# Respaldo completo
python manage.py crear_respaldo --type full --compress

# Solo base de datos
python manage.py crear_respaldo --type db

# Solo archivos media
python manage.py crear_respaldo --type media

# Con retención personalizada
python manage.py crear_respaldo --retention 7
```

### 2. **Script Independiente (Recomendado para producción)**

```bash
# Respaldo completo
python scripts/backup_windows_simple.py --type full --compress

# Solo base de datos
python scripts/backup_windows_simple.py --type db

# Con retención personalizada
python scripts/backup_windows_simple.py --retention 7
```

### 3. **Script Batch para Windows**

```bash
# Ejecutar directamente
scripts\backup_windows.bat

# O configurar como tarea programada
```

## ⚙️ Configuración Automática

### **Windows Task Scheduler**

1. **Ejecutar como Administrador:**
   ```cmd
   scripts\configurar_backup_windows.bat
   ```

2. **Configurar tarea programada:**
   - Abrir "Programador de tareas" (`taskschd.msc`)
   - Importar tarea desde `scripts\backup_task.xml`
   - Configurar cuenta de usuario
   - La tarea se ejecutará diariamente a las 2:00 AM

### **Configuración Manual de Cron (Linux/Mac)**

```bash
# Editar crontab
crontab -e

# Agregar línea para respaldo diario a las 2:00 AM
0 2 * * * cd /ruta/al/proyecto && python scripts/backup_automatico.py --compress
```

## 📊 Tipos de Respaldo

| Tipo | Descripción | Incluye |
|------|-------------|---------|
| `db` | Solo base de datos | Base de datos SQLite |
| `media` | Solo archivos media | Documentos, imágenes, etc. |
| `full` | Respaldo completo | BD + Media + Config + Logs |

## 🔧 Opciones de Configuración

### **Parámetros del Script**

- `--type`: Tipo de respaldo (`db`, `media`, `full`)
- `--compress`: Comprimir respaldo (por defecto: True)
- `--retention`: Días de retención (por defecto: 30)
- `--project-root`: Ruta del proyecto

### **Configuración de Retención**

- **30 días**: Configuración por defecto
- **7 días**: Para sistemas con poco espacio
- **90 días**: Para sistemas con mucho espacio

## 📈 Monitoreo y Reportes

### **Logs del Sistema**

Los logs se guardan en:
- `logs/backup.log` - Logs detallados
- `backups/automatico/reporte_respaldo_*.json` - Reportes JSON

### **Verificación de Respaldos**

Cada respaldo incluye:
- ✅ Verificación de integridad de la BD
- 📊 Tamaño total del respaldo
- 📝 Lista de archivos respaldados
- 🕒 Timestamp de creación
- 📋 Estado del respaldo

## 🚨 Solución de Problemas

### **Error: "Base de datos no encontrada"**
- Verificar que `db.sqlite3` existe en la raíz del proyecto
- Verificar permisos de lectura

### **Error: "Acceso denegado"**
- Ejecutar como Administrador en Windows
- Verificar permisos de escritura en carpeta `backups`

### **Error: "No se pudo eliminar directorio temporal"**
- Normal en Windows, no afecta el respaldo
- Los archivos se limpian automáticamente

### **Error: "Problema de integridad en respaldo de BD"**
- Verificar que la BD no esté corrupta
- Intentar respaldo manual de la BD

## 📋 Verificación del Sistema

### **1. Verificar Comando Django**
```bash
python manage.py help | findstr respaldo
# Debe mostrar: crear_respaldo
```

### **2. Verificar Scripts**
```bash
python scripts/backup_windows_simple.py --help
# Debe mostrar las opciones disponibles
```

### **3. Probar Respaldo Manual**
```bash
python manage.py crear_respaldo --type db
# Debe crear un respaldo en backups/manual/
```

### **4. Verificar Estructura de Carpetas**
```
backups/
├── manual/          # Respaldos manuales
└── automatico/      # Respaldos automáticos
```

## 🔒 Seguridad y Mantenimiento

### **Recomendaciones de Seguridad**

1. **Respaldos en ubicación externa**
   - Copiar carpeta `backups` a disco externo
   - Usar servicios en la nube (Google Drive, Dropbox)

2. **Verificación regular**
   - Probar restauración mensualmente
   - Verificar integridad de respaldos

3. **Monitoreo de espacio**
   - Configurar retención apropiada
   - Limpiar respaldos antiguos manualmente si es necesario

### **Mantenimiento del Sistema**

1. **Revisar logs semanalmente**
   - Verificar que no hay errores
   - Monitorear tamaño de respaldos

2. **Actualizar scripts**
   - Mantener scripts actualizados
   - Probar después de actualizaciones del sistema

3. **Verificar permisos**
   - Asegurar que el usuario tiene permisos de escritura
   - Verificar que las tareas programadas funcionan

## 📞 Soporte y Contacto

### **Problemas Comunes**

- **Respaldo no se ejecuta**: Verificar tarea programada
- **Error de permisos**: Ejecutar como Administrador
- **Espacio insuficiente**: Ajustar retención de respaldos

### **Logs de Debug**

Para problemas complejos, revisar:
- `logs/backup.log`
- Reportes JSON en `backups/automatico/`
- Salida de consola del script

---

## 🎯 Resumen de Comandos Rápidos

```bash
# Respaldo manual completo
python manage.py crear_respaldo --type full --compress

# Respaldo automático
python scripts/backup_windows_simple.py --type full --compress

# Configurar Windows (como Administrador)
scripts\configurar_backup_windows.bat

# Verificar respaldos
dir backups\automatico
```

**¡El sistema de respaldo automático está listo y funcionando!** 🚀
