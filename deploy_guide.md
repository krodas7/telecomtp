# 🚀 **GUÍA DE DESPLIEGUE AL SERVIDOR**

## 📋 **Preparación del Proyecto**

### **1. Verificar Archivos de Configuración**

#### **A. settings.py - Configuración de Producción**
```python
# Configuraciones importantes para producción
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com', 'IP-del-servidor']

# Base de datos de producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # o mysql
        'NAME': 'nombre_bd_produccion',
        'USER': 'usuario_bd',
        'PASSWORD': 'password_bd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Archivos de media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### **B. requirements.txt - Dependencias**
```txt
Django==4.2.7
psycopg2-binary==2.9.7
Pillow==10.0.0
gunicorn==21.2.0
whitenoise==6.5.0
python-decouple==3.8
```

### **2. Archivos de Configuración para Servidor**

#### **A. .env (Variables de Entorno)**
```env
DEBUG=False
SECRET_KEY=tu-secret-key-super-seguro
DB_NAME=nombre_bd_produccion
DB_USER=usuario_bd
DB_PASSWORD=password_bd
DB_HOST=localhost
DB_PORT=5432
```

#### **B. gunicorn.conf.py**
```python
bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

#### **C. nginx.conf**
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /ruta/a/tu/proyecto;
    }
    
    location /media/ {
        root /ruta/a/tu/proyecto;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

## 🛠️ **Pasos para el Despliegue**

### **Paso 1: Preparar el Proyecto Local**

1. **Crear requirements.txt**
2. **Configurar settings.py para producción**
3. **Recopilar archivos estáticos**
4. **Hacer commit de todos los cambios**

### **Paso 2: Subir al Servidor**

1. **Conectar por SSH al servidor**
2. **Clonar el repositorio**
3. **Instalar dependencias**
4. **Configurar base de datos**
5. **Configurar servidor web**

### **Paso 3: Configurar Servidor**

1. **Instalar Python, PostgreSQL, Nginx**
2. **Configurar virtual environment**
3. **Configurar base de datos**
4. **Configurar archivos estáticos**
5. **Configurar SSL (opcional)**

## 📦 **Opciones de Despliegue**

### **Opción 1: Servidor VPS (Recomendado)**
- DigitalOcean, Linode, Vultr, etc.
- Control total del servidor
- Más económico a largo plazo

### **Opción 2: Plataformas de Despliegue**
- Heroku (fácil pero limitado)
- Railway (moderno y simple)
- PythonAnywhere (específico para Python)

### **Opción 3: Cloud Providers**
- AWS, Google Cloud, Azure
- Más complejo pero más escalable

## 🔧 **Comandos de Despliegue**

### **Local (Preparación)**
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Hacer migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Crear requirements.txt
pip freeze > requirements.txt
```

### **Servidor (Despliegue)**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar servidor
gunicorn sistema_construccion.wsgi:application
```

## ⚠️ **Consideraciones de Seguridad**

1. **Nunca subir archivos .env**
2. **Usar HTTPS en producción**
3. **Configurar firewall del servidor**
4. **Backups regulares de la base de datos**
5. **Actualizar dependencias regularmente**

## 📞 **Soporte Post-Despliegue**

- Monitoreo del servidor
- Logs de errores
- Backups automáticos
- Actualizaciones de seguridad
