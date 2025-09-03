#!/bin/bash

# Script de despliegue de la aplicación Django
# Ejecutar como usuario 'sistema'

echo "🚀 Desplegando aplicación Django..."

# Ir al directorio de la aplicación
cd /var/www/sistema-construccion

# Clonar repositorio (reemplazar con tu URL real)
echo "📥 Clonando repositorio..."
git clone https://github.com/krpdas7/sistema-construccion-django.git .

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variables de entorno
echo "⚙️ Configurando variables de entorno..."
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=tu_secret_key_muy_seguro_aqui
DATABASE_URL=postgresql://sistema_user:sistema_password_2024@localhost/sistema_construccion
ALLOWED_HOSTS=tu_dominio.com,tu_ip_droplet
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_email
EOF

# Configurar settings de producción
echo "🔧 Configurando settings de producción..."
cat > sistema_construccion/production_settings.py << 'EOF'
from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sistema_construccion',
        'USER': 'sistema_user',
        'PASSWORD': 'sistema_password_2024',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Archivos estáticos
STATIC_ROOT = '/var/www/sistema-construccion/staticfiles'
MEDIA_ROOT = '/var/www/sistema-construccion/media'

# Seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL (después de configurar Certbot)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/sistema-construccion/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
EOF

# Crear directorio de logs
sudo mkdir -p /var/log/sistema-construccion
sudo chown sistema:sistema /var/log/sistema-construccion

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superusuario creado: admin/admin123")
else:
    print("Superusuario ya existe")
EOF

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Inicializar roles y permisos
echo "🔐 Inicializando roles y permisos..."
python manage.py inicializar_roles

# Configurar Gunicorn
echo "🦄 Configurando Gunicorn..."
cat > gunicorn.conf.py << 'EOF'
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
user = "sistema"
group = "sistema"
tmp_upload_dir = None
errorlog = "/var/log/sistema-construccion/gunicorn_error.log"
accesslog = "/var/log/sistema-construccion/gunicorn_access.log"
loglevel = "info"
EOF

# Crear servicio systemd para Gunicorn
echo "⚙️ Configurando servicio systemd..."
sudo tee /etc/systemd/system/sistema-construccion.service > /dev/null << 'EOF'
[Unit]
Description=Sistema Construccion Django App
After=network.target

[Service]
User=sistema
Group=sistema
WorkingDirectory=/var/www/sistema-construccion
Environment="PATH=/var/www/sistema-construccion/venv/bin"
ExecStart=/var/www/sistema-construccion/venv/bin/gunicorn --config gunicorn.conf.py sistema_construccion.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd y iniciar servicios
echo "🔄 Iniciando servicios..."
sudo systemctl daemon-reload
sudo systemctl enable sistema-construccion
sudo systemctl start sistema-construccion
sudo systemctl restart nginx

# Verificar estado
echo "✅ Verificando estado de servicios..."
sudo systemctl status sistema-construccion --no-pager
sudo systemctl status nginx --no-pager

echo "🎉 ¡Despliegue completado!"
echo "📋 Próximos pasos:"
echo "1. Configurar dominio en DigitalOcean"
echo "2. Ejecutar: sudo certbot --nginx -d tu_dominio.com"
echo "3. Probar la aplicación"
echo "4. Probar modo offline"
