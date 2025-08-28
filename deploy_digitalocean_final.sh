#!/bin/bash

# ============================================================================
# SCRIPT DE DESPLIEGUE FINAL - Sistema ARCA Construcción
# ============================================================================
# Optimizado para DigitalOcean + Dominio Hostinger
# Ejecutar en servidor Ubuntu 22.04 LTS

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si se ejecuta como root
if [[ $EUID -eq 0 ]]; then
   print_error "Este script no debe ejecutarse como root"
   exit 1
fi

# Variables configurables
APP_NAME="sistema-arca"
APP_USER="arca"
APP_DIR="/var/www/$APP_NAME"
REPO_URL="https://github.com/krodas7/sistema-arca.git"
DOMAIN_NAME="[TU-DOMINIO.com]"  # CAMBIAR POR TU DOMINIO REAL

print_status "🚀 Iniciando despliegue del Sistema ARCA Construcción..."
print_status "📍 Ubicación: $APP_DIR"
print_status "🌐 Dominio: $DOMAIN_NAME"

# ============================================================================
# PASO 1: PREPARACIÓN DEL SISTEMA
# ============================================================================

print_status "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

print_status "🔧 Instalando dependencias del sistema..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    nginx \
    postgresql \
    postgresql-contrib \
    git \
    curl \
    wget \
    unzip \
    htop \
    ufw \
    fail2ban \
    certbot \
    python3-certbot-nginx \
    redis-server \
    supervisor

# ============================================================================
# PASO 2: CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

print_status "🔒 Configurando firewall..."
sudo ufw --force enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22

print_status "🛡️ Configurando fail2ban..."
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# ============================================================================
# PASO 3: CONFIGURACIÓN DE POSTGRESQL
# ============================================================================

print_status "🗄️ Configurando PostgreSQL..."
sudo systemctl enable postgresql
sudo systemctl start postgresql

# Crear base de datos y usuario
sudo -u postgres psql << EOF
CREATE DATABASE arca_construccion;
CREATE USER arca_user WITH PASSWORD 'ARCA_2025_Super_Secure_Password_Change_This';
ALTER ROLE arca_user SET client_encoding TO 'utf8';
ALTER ROLE arca_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE arca_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE arca_construccion TO arca_user;
\q
EOF

# ============================================================================
# PASO 4: CONFIGURACIÓN DE REDIS
# ============================================================================

print_status "🔴 Configurando Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# ============================================================================
# PASO 5: CREAR USUARIO Y DIRECTORIOS
# ============================================================================

print_status "👤 Creando usuario del sistema..."
if ! id "$APP_USER" &>/dev/null; then
    sudo useradd -m -s /bin/bash $APP_USER
    sudo usermod -aG sudo $APP_USER
    print_success "Usuario $APP_USER creado"
else
    print_warning "Usuario $APP_USER ya existe"
fi

print_status "📁 Creando directorios de la aplicación..."
sudo mkdir -p $APP_DIR
sudo chown $APP_USER:$APP_USER $APP_DIR

# ============================================================================
# PASO 6: CLONAR REPOSITORIO
# ============================================================================

print_status "📥 Clonando repositorio..."
cd $APP_DIR
sudo -u $APP_USER git clone $REPO_URL .

# ============================================================================
# PASO 7: CONFIGURAR ENTORNO VIRTUAL
# ============================================================================

print_status "🐍 Configurando entorno virtual..."
sudo -u $APP_USER python3 -m venv venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip

print_status "📚 Instalando dependencias Python..."
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements_production.txt

# ============================================================================
# PASO 8: CONFIGURAR VARIABLES DE ENTORNO
# ============================================================================

print_status "⚙️ Configurando variables de entorno..."
sudo -u $APP_USER cp production.env .env

# Editar .env con valores reales
sudo -u $APP_USER sed -i "s/your-super-secret-key-change-this-in-production-2025/$(openssl rand -hex 32)/" .env
sudo -u $APP_USER sed -i "s/your_secure_password_here/ARCA_2025_Super_Secure_Password_Change_This/" .env
sudo -u $APP_USER sed -i "s/arca_construccion/arca_construccion/" .env
sudo -u $APP_USER sed -i "s/arca_user/arca_user/" .env

# ============================================================================
# PASO 9: CONFIGURAR DJANGO
# ============================================================================

print_status "🔄 Ejecutando migraciones..."
cd $APP_DIR
export DJANGO_SETTINGS_MODULE=sistema_construccion.production_settings
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py migrate

print_status "📁 Recolectando archivos estáticos..."
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py collectstatic --noinput

print_status "👑 Creando superusuario..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@arca.com', 'Admin2025!')" | sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py shell

# ============================================================================
# PASO 10: CONFIGURAR GUNICORN
# ============================================================================

print_status "🦄 Configurando Gunicorn..."
sudo -u $APP_USER mkdir -p $APP_DIR/logs

# Crear archivo de configuración de Gunicorn
sudo -u $APP_USER tee $APP_DIR/gunicorn.conf.py > /dev/null << 'GUNICORN_CONFIG'
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
GUNICORN_CONFIG

# ============================================================================
# PASO 11: CONFIGURAR SERVICIO SYSTEMD
# ============================================================================

print_status "🔧 Configurando servicio systemd..."
sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null << SERVICE_CONFIG
[Unit]
Description=Sistema ARCA Construcción Gunicorn
After=network.target postgresql.service redis-server.service

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=sistema_construccion.production_settings"
ExecStart=$APP_DIR/venv/bin/gunicorn --config gunicorn.conf.py sistema_construccion.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE_CONFIG

# Habilitar y iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME

# ============================================================================
# PASO 12: CONFIGURAR NGINX
# ============================================================================

print_status "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null << NGINX_CONFIG
server {
    listen 80;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;
    
    # Redirigir a HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN_NAME www.$DOMAIN_NAME;

    # SSL será configurado por Certbot
    # ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;

    # Archivos estáticos
    location /static/ {
        alias $APP_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }

    # Archivos media
    location /media/ {
        alias $APP_DIR/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header X-Content-Type-Options nosniff;
    }

    # Proxy a Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
NGINX_CONFIG

# Habilitar sitio
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Verificar configuración de Nginx
sudo nginx -t
sudo systemctl restart nginx

# ============================================================================
# PASO 13: CONFIGURAR SSL CON LET'S ENCRYPT
# ============================================================================

print_status "🔒 Configurando SSL con Let's Encrypt..."
# Nota: Solo ejecutar después de configurar DNS
print_warning "IMPORTANTE: Configura DNS en Hostinger antes de continuar"
print_warning "Tu dominio debe apuntar a: $(curl -s ifconfig.me)"

read -p "¿Ya configuraste DNS en Hostinger? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Obteniendo certificado SSL..."
    sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME
    
    # Configurar renovación automática
    (crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -
    
    print_success "SSL configurado correctamente"
else
    print_warning "SSL no configurado. Ejecutar manualmente después de configurar DNS:"
    print_warning "sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME"
fi

# ============================================================================
# PASO 14: CONFIGURAR SUPERVISOR PARA TAREAS EN SEGUNDO PLANO
# ============================================================================

print_status "👷 Configurando Supervisor..."
sudo tee /etc/supervisor/conf.d/$APP_NAME.conf > /dev/null << SUPERVISOR_CONFIG
[program:$APP_NAME-celery]
command=$APP_DIR/venv/bin/celery -A sistema_construccion worker -l info
directory=$APP_DIR
user=$APP_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$APP_DIR/logs/celery.log
environment=DJANGO_SETTINGS_MODULE="sistema_construccion.production_settings"

[program:$APP_NAME-beat]
command=$APP_DIR/venv/bin/celery -A sistema_construccion beat -l info
directory=$APP_DIR
user=$APP_USER
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=$APP_DIR/logs/celery-beat.log
environment=DJANGO_SETTINGS_MODULE="sistema_construccion.production_settings"
SUPERVISOR_CONFIG

sudo systemctl enable supervisor
sudo systemctl start supervisor
sudo supervisorctl reread
sudo supervisorctl update

# ============================================================================
# PASO 15: CONFIGURAR BACKUPS AUTOMÁTICOS
# ============================================================================

print_status "💾 Configurando backups automáticos..."
sudo -u $APP_USER mkdir -p $APP_DIR/backups

# Crear script de backup
sudo -u $APP_USER tee $APP_DIR/backup.sh > /dev/null << 'BACKUP_SCRIPT'
#!/bin/bash
BACKUP_DIR="/var/www/sistema-arca/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.sql"

# Backup de base de datos
pg_dump -h localhost -U arca_user -d arca_construccion > $BACKUP_DIR/$BACKUP_FILE

# Comprimir backup
gzip $BACKUP_DIR/$BACKUP_FILE

# Eliminar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Backup completado: $BACKUP_FILE.gz"
BACKUP_SCRIPT

sudo -u $APP_USER chmod +x $APP_DIR/backup.sh

# Agregar a crontab (backup diario a las 2 AM)
(crontab -u $APP_USER -l 2>/dev/null; echo "0 2 * * * $APP_DIR/backup.sh") | crontab -u $APP_USER -

# ============================================================================
# PASO 16: VERIFICACIÓN FINAL
# ============================================================================

print_status "🔍 Verificando servicios..."
sleep 5

# Verificar estado de servicios
print_status "Estado de servicios:"
sudo systemctl status $APP_NAME --no-pager -l
sudo systemctl status nginx --no-pager -l
sudo systemctl status postgresql --no-pager -l
sudo systemctl status redis-server --no-pager -l
sudo systemctl status supervisor --no-pager -l

# Verificar logs
print_status "Últimas líneas de logs:"
sudo tail -n 10 $APP_DIR/logs/django.log 2>/dev/null || print_warning "Log de Django no disponible aún"

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print_success "🎉 ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!"
echo
print_status "📋 RESUMEN DEL DESPLIEGUE:"
print_status "   • Aplicación: $APP_NAME"
print_status "   • Usuario: $APP_USER"
print_status "   • Directorio: $APP_DIR"
print_status "   • Base de datos: arca_construccion"
print_status "   • Puerto: 8000 (Gunicorn) + 80/443 (Nginx)"
print_status "   • SSL: Let's Encrypt (configurar DNS primero)"
echo
print_status "🔑 CREDENCIALES IMPORTANTES:"
print_status "   • Superusuario: admin / Admin2025!"
print_status "   • Base de datos: arca_user / ARCA_2025_Super_Secure_Password_Change_This"
echo
print_status "📱 ACCESO:"
print_status "   • Local: http://localhost"
print_status "   • Producción: https://$DOMAIN_NAME (después de configurar DNS)"
echo
print_status "📚 COMANDOS ÚTILES:"
print_status "   • Ver logs: sudo journalctl -u $APP_NAME -f"
print_status "   • Reiniciar: sudo systemctl restart $APP_NAME"
print_status "   • Estado: sudo systemctl status $APP_NAME"
print_status "   • Backup manual: sudo -u $APP_USER $APP_DIR/backup.sh"
echo
print_warning "⚠️  PRÓXIMOS PASOS:"
print_warning "   1. Configurar DNS en Hostinger para apuntar a: $(curl -s ifconfig.me)"
print_warning "   2. Esperar propagación DNS (hasta 48 horas)"
print_warning "   3. Ejecutar: sudo certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME"
print_warning "   4. Cambiar contraseñas por defecto"
print_warning "   5. Configurar monitoreo y alertas"
echo
print_success "🚀 ¡Tu Sistema ARCA Construcción está listo para producción!"

