# 🚀 Despliegue en SmartASP - Sistema de Construcción

## 📋 Información del Hosting

- **Proveedor**: SmartASP
- **Tipo**: Hosting Compartido Windows
- **Base de Datos**: SQL Server
- **Dominio**: Hostinger
- **Python**: 3.9+ (verificar en panel de control)

## 🔧 Requisitos Previos

### 1. Acceso a SmartASP
- Panel de Control activo
- Acceso FTP habilitado
- Base de datos SQL Server creada

### 2. Dominio en Hostinger
- Dominio configurado y apuntando a SmartASP
- DNS propagado correctamente

### 3. Software Local
- Python 3.8+ instalado
- Git (opcional)
- Compresor de archivos (7-Zip, WinRAR)

## 🚀 Pasos de Despliegue

### **Paso 1: Preparación Local**

```bash
# 1. Clonar o descargar el proyecto
git clone <tu-repositorio>
cd sistema-construccion-django

# 2. Ejecutar script de preparación
python deploy/smartasp_deploy.py

# 3. Verificar archivos creados
ls -la
# Deberías ver:
# - .env
# - web.config
# - SMARTASP_DEPLOY_GUIDE.md
```

### **Paso 2: Configuración del Archivo .env**

Editar el archivo `.env` con tus credenciales reales:

```env
# Configuración para SmartASP
ENVIRONMENT=smartasp
DEBUG=False

# Base de datos SQL Server
DB_ENGINE=sql_server.pyodbc
DB_NAME=tu_base_datos
DB_USER=tu_usuario_db
DB_PASSWORD=tu_password_db
DB_HOST=tu_host_sqlserver
DB_PORT=1433

# Email (Hostinger)
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@tu-dominio.com
EMAIL_HOST_PASSWORD=tu_password_email
DEFAULT_FROM_EMAIL=tu_email@tu-dominio.com

# Dominio
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Secret Key (generar uno nuevo)
SECRET_KEY=tu_secret_key_aqui
```

### **Paso 3: Generar Secret Key**

```python
# En Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### **Paso 4: Preparar Archivos para Subida**

```bash
# Crear archivo ZIP excluyendo carpetas innecesarias
# Excluir: venv/, __pycache__/, .git/, .env (contiene credenciales)

# En Windows (PowerShell):
Compress-Archive -Path * -DestinationPath sistema_construccion_smartasp.zip -Exclude venv,__pycache__,.git,.env

# En Linux/Mac:
zip -r sistema_construccion_smartasp.zip . -x "venv/*" "__pycache__/*" ".git/*" ".env"
```

### **Paso 5: Subir a SmartASP**

#### **Opción A: Panel de Control**
1. Acceder al Panel de Control de SmartASP
2. Ir a "File Manager"
3. Navegar a la carpeta raíz del hosting
4. Subir el archivo ZIP
5. Extraer el contenido

#### **Opción B: FTP**
1. Conectar via FTP (FileZilla, WinSCP)
2. Navegar a la carpeta raíz
3. Subir archivos del proyecto
4. Subir archivo `.env` por separado

### **Paso 6: Configuración en SmartASP**

#### **6.1 Base de Datos**
1. Panel de Control → SQL Server
2. Crear nueva base de datos
3. Anotar: nombre, usuario, password, host
4. Actualizar archivo `.env`

#### **6.2 Variables de Entorno**
1. Panel de Control → Environment Variables
2. Agregar variables del archivo `.env`
3. Reiniciar aplicación

#### **6.3 Dominio**
1. Panel de Control → Domains
2. Apuntar dominio a la carpeta del proyecto
3. Configurar SSL si está disponible

### **Paso 7: Verificación**

#### **7.1 Health Check**
```
https://tu-dominio.com/health/
```
Debería devolver:
```json
{
    "status": "healthy",
    "environment": "smartasp",
    "timestamp": 1234567890,
    "version": "1.0.0"
}
```

#### **7.2 Dashboard Principal**
```
https://tu-dominio.com/
```
- Verificar que cargue correctamente
- Probar login con superusuario
- Verificar funcionalidades principales

#### **7.3 Logs**
Revisar archivos de log en la carpeta `logs/`:
- `django_smartasp.log`
- `wsgi_smartasp.log`

## 🔍 Solución de Problemas

### **Error: Base de Datos**
```
django.db.utils.OperationalError: ('08001', '[08001] [unixODBC][FreeTDS][SQL Server]Unable to connect to data source')
```

**Solución:**
1. Verificar credenciales en `.env`
2. Confirmar que SQL Server esté activo
3. Verificar firewall y puertos

### **Error: Archivos Estáticos**
```
404 Not Found - /static/css/style.css
```

**Solución:**
1. Ejecutar `python manage.py collectstatic`
2. Verificar permisos de carpeta `staticfiles/`
3. Confirmar configuración en `web.config`

### **Error: Importación de Módulos**
```
ModuleNotFoundError: No module named 'sql_server'
```

**Solución:**
1. Instalar dependencias: `pip install -r requirements_smartasp.txt`
2. Verificar versión de Python
3. Reiniciar aplicación

### **Error: Permisos**
```
PermissionError: [Errno 13] Permission denied
```

**Solución:**
1. Verificar permisos de carpetas
2. Contactar soporte de SmartASP
3. Usar rutas relativas en lugar de absolutas

## 📊 Monitoreo y Mantenimiento

### **Logs Importantes**
- `logs/django_smartasp.log` - Errores de Django
- `logs/wsgi_smartasp.log` - Errores del servidor
- `logs/access.log` - Accesos al sistema

### **Backups Automáticos**
- Configurados en `smartasp_settings.py`
- Frecuencia: cada 24 horas
- Retención: 30 días
- Ubicación: carpeta `backups/`

### **Monitoreo de Salud**
- Endpoint: `/health/`
- Verificación automática cada 10 minutos
- Alertas por email en caso de fallo

## 🔐 Seguridad

### **Configuraciones Implementadas**
- Headers de seguridad automáticos
- Protección CSRF habilitada
- Validación de entrada estricta
- Logs de auditoría
- Encriptación de contraseñas

### **Recomendaciones Adicionales**
1. Cambiar contraseñas por defecto
2. Usar HTTPS siempre
3. Mantener dependencias actualizadas
4. Revisar logs regularmente

## 📞 Soporte

### **SmartASP**
- Panel de Control: [panel.smartasp.net](https://panel.smartasp.net)
- Soporte Técnico: 24/7
- Documentación: [docs.smartasp.net](https://docs.smartasp.net)

### **Hostinger**
- Panel de Control: [hpanel.hostinger.com](https://hpanel.hostinger.com)
- Soporte: Chat en vivo, tickets
- DNS: [dns.hostinger.com](https://dns.hostinger.com)

### **Sistema de Construcción**
- Documentación: `README.md`
- Guías: carpeta `deploy/`
- Logs: carpeta `logs/`

## 🎯 Checklist de Despliegue

- [ ] Script de preparación ejecutado
- [ ] Archivo `.env` configurado
- [ ] Base de datos SQL Server creada
- [ ] Archivos subidos a SmartASP
- [ ] Variables de entorno configuradas
- [ ] Dominio apuntando correctamente
- [ ] Health check funcionando
- [ ] Dashboard accesible
- [ ] Login funcionando
- [ ] Funcionalidades principales verificadas
- [ ] Logs configurados
- [ ] Backups automáticos funcionando

## 🚀 ¡Listo para Producción!

Una vez completado el checklist, tu sistema estará funcionando en SmartASP con tu dominio de Hostinger.

**URL de Acceso**: `https://tu-dominio.com`

**Panel de Administración**: `https://tu-dominio.com/admin/`

**Documentación**: Revisar archivos en la carpeta `deploy/`

---

*¿Necesitas ayuda? Revisa los logs en la carpeta `logs/` o contacta al soporte técnico.*
