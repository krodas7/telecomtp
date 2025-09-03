#!/bin/bash

# Script de configuración completa para Droplet de DigitalOcean
# Sistema de Construcción Django con modo offline

echo "🚀 Iniciando configuración del droplet..."

# Actualizar sistema
echo "📦 Actualizando sistema..."
apt update && apt upgrade -y

# Instalar dependencias básicas
echo "🔧 Instalando dependencias básicas..."
apt install -y curl wget git nginx postgresql postgresql-contrib python3 python3-pip python3-venv python3-dev libpq-dev build-essential

# Instalar Node.js (para herramientas de frontend si es necesario)
echo "📦 Instalando Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Crear usuario para la aplicación
echo "👤 Creando usuario de aplicación..."
useradd -m -s /bin/bash sistema
usermod -aG sudo sistema

# Configurar PostgreSQL
echo "🗄️ Configurando PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE sistema_construccion;"
sudo -u postgres psql -c "CREATE USER sistema_user WITH PASSWORD 'sistema_password_2024';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sistema_construccion TO sistema_user;"
sudo -u postgres psql -c "ALTER USER sistema_user CREATEDB;"

# Configurar Nginx
echo "🌐 Configurando Nginx..."
cat > /etc/nginx/sites-available/sistema-construccion << 'EOF'
server {
    listen 80;
    server_name _;
    
    location /static/ {
        alias /var/www/sistema-construccion/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/sistema-construccion/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
EOF

# Habilitar sitio
ln -sf /etc/nginx/sites-available/sistema-construccion /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Crear directorio de la aplicación
echo "📁 Creando directorios..."
mkdir -p /var/www/sistema-construccion
chown -R sistema:sistema /var/www/sistema-construccion

# Configurar firewall
echo "🔥 Configurando firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

# Instalar Certbot para SSL
echo "🔒 Instalando Certbot..."
apt install -y certbot python3-certbot-nginx

# Configurar respaldos automáticos
echo "💾 Configurando respaldos automáticos..."
mkdir -p /var/backups/sistema-construccion
cat > /etc/cron.d/sistema-backup << 'EOF'
# Respaldo diario a las 2:00 AM
0 2 * * * sistema /var/www/sistema-construccion/backup_script.sh
EOF

# Crear script de respaldo
cat > /var/www/sistema-construccion/backup_script.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/sistema-construccion"
APP_DIR="/var/www/sistema-construccion"

cd $APP_DIR
source venv/bin/activate

# Respaldo de base de datos
python manage.py dumpdata > $BACKUP_DIR/db_backup_$DATE.json

# Respaldo de archivos media
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# Mantener solo los últimos 7 respaldos
find $BACKUP_DIR -name "db_backup_*.json" -mtime +7 -delete
find $BACKUP_DIR -name "media_backup_*.tar.gz" -mtime +7 -delete

echo "Respaldo completado: $DATE"
EOF

chmod +x /var/www/sistema-construccion/backup_script.sh
chown sistema:sistema /var/www/sistema-construccion/backup_script.sh

# Configurar monitoreo básico
echo "📊 Configurando monitoreo..."
apt install -y htop iotop nethogs

# Crear script de monitoreo
cat > /var/www/sistema-construccion/monitor.sh << 'EOF'
#!/bin/bash
echo "=== Estado del Sistema ==="
echo "Fecha: $(date)"
echo "Uptime: $(uptime)"
echo "Memoria: $(free -h)"
echo "Disco: $(df -h /)"
echo "Servicios:"
systemctl is-active nginx
systemctl is-active postgresql
echo "========================"
EOF

chmod +x /var/www/sistema-construccion/monitor.sh

echo "✅ Configuración del droplet completada!"
echo "📋 Próximos pasos:"
echo "1. Clonar repositorio desde GitHub"
echo "2. Configurar aplicación Django"
echo "3. Configurar SSL con Certbot"
echo "4. Probar modo offline"
