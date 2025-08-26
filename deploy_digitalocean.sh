#!/bin/bash

# Script de Despliegue para Sistema ARCA Construcción en DigitalOcean
# Ejecutar en el servidor Ubuntu 22.04 LTS

echo "🚀 Iniciando despliegue del Sistema ARCA Construcción..."
echo "=================================================="

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias..."
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git curl wget unzip

# Instalar Node.js para build de assets (opcional)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Crear usuario para la aplicación
echo "👤 Creando usuario del sistema..."
sudo useradd -m -s /bin/bash arca
sudo usermod -aG sudo arca

# Crear directorio de la aplicación
echo "📁 Creando directorio de la aplicación..."
sudo mkdir -p /var/www/sistema-arca
sudo chown arca:arca /var/www/sistema-arca

# Cambiar al usuario arca
sudo -u arca bash << 'EOF'

# Clonar repositorio
echo "📥 Clonando repositorio..."
cd /var/www/sistema-arca
git clone https://github.com/tu-usuario/sistema-arca-construccion.git .

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configurar base de datos
echo "🗄️ Configurando base de datos..."
sudo -u postgres psql -c "CREATE DATABASE arca_construccion;"
sudo -u postgres psql -c "CREATE USER arca_user WITH PASSWORD 'tu-password-super-seguro';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE arca_construccion TO arca_user;"

# Configurar variables de entorno
echo "⚙️ Configurando variables de entorno..."
cp env_production.txt .env
# Editar .env con valores reales

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
python manage.py migrate
python manage.py collectstatic --noinput

# Crear superusuario
echo "👑 Creando superusuario..."
python manage.py createsuperuser

# Configurar Gunicorn
echo "🦄 Configurando Gunicorn..."
mkdir -p logs
cat > gunicorn.conf.py << 'GUNICORN_CONFIG'
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
GUNICORN_CONFIG

# Configurar servicio systemd
echo "🔧 Configurando servicio systemd..."
sudo tee /etc/systemd/system/sistema-arca.service > /dev/null << 'SERVICE_CONFIG'
[Unit]
Description=Sistema ARCA Construcción Gunicorn
After=network.target

[Service]
User=arca
Group=arca
WorkingDirectory=/var/www/sistema-arca
Environment="PATH=/var/www/sistema-arca/venv/bin"
ExecStart=/var/www/sistema-arca/venv/bin/gunicorn --config gunicorn.conf.py sistema_construccion.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE_CONFIG

EOF

# Configurar Nginx
echo "🌐 Configurando Nginx..."
sudo tee /etc/nginx/sites-available/sistema-arca > /dev/null << 'NGINX_CONFIG'
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    client_max_body_size 100M;

    location /static/ {
        alias /var/www/sistema-arca/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/sistema-arca/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
NGINX_CONFIG

# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/sistema-arca /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Configurar firewall
echo "🔥 Configurando firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable

# Iniciar servicios
echo "🚀 Iniciando servicios..."
sudo systemctl daemon-reload
sudo systemctl enable sistema-arca
sudo systemctl start sistema-arca
sudo systemctl restart nginx

# Verificar estado
echo "✅ Verificando estado de servicios..."
sudo systemctl status sistema-arca --no-pager
sudo systemctl status nginx --no-pager

echo "🎉 ¡Despliegue completado!"
echo "=================================================="
echo "🌐 URL: http://tu-dominio.com"
echo "🔧 Admin: http://tu-dominio.com/admin"
echo "📱 PWA: Instalable desde el navegador móvil"
echo ""
echo "📋 Próximos pasos:"
echo "1. Configurar dominio DNS"
echo "2. Configurar SSL con Let's Encrypt"
echo "3. Configurar backup automático"
echo "4. Configurar monitoreo"
echo ""
echo "🔒 Recuerda cambiar las contraseñas por defecto!"
