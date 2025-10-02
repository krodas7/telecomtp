#!/bin/bash

# Script de despliegue completo para nuevo droplet
# Sistema ARCA - Despliegue limpio desde cero

echo "🚀 DESPLIEGUE COMPLETO - SISTEMA ARCA"
echo "====================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

show_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

show_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

show_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Actualizar sistema
show_message "📦 Actualizando sistema..."
apt update && apt upgrade -y
show_success "Sistema actualizado"

# 2. Instalar dependencias
show_message "📦 Instalando dependencias..."
apt install -y python3 python3-pip python3-venv nginx git supervisor
show_success "Dependencias instaladas"

# 3. Crear usuario arca
show_message "👤 Creando usuario arca..."
useradd -m -s /bin/bash arca
usermod -aG sudo arca
show_success "Usuario arca creado"

# 4. Crear directorio del proyecto
show_message "📁 Creando directorio del proyecto..."
mkdir -p /var/www/sistema-arca
chown arca:arca /var/www/sistema-arca
show_success "Directorio creado"

# 5. Clonar repositorio
show_message "📥 Clonando repositorio..."
cd /var/www/sistema-arca
sudo -u arca git clone https://github.com/krodas7/arca-sistema.git .
show_success "Repositorio clonado"

# 6. Crear entorno virtual
show_message "🐍 Creando entorno virtual..."
sudo -u arca python3 -m venv venv
show_success "Entorno virtual creado"

# 7. Activar entorno virtual e instalar dependencias
show_message "📦 Instalando dependencias Python..."
sudo -u arca bash -c "source venv/bin/activate && pip install -r requirements.txt"
show_success "Dependencias Python instaladas"

# 8. Configurar base de datos
show_message "🗄️ Configurando base de datos..."
sudo -u arca bash -c "source venv/bin/activate && python manage.py migrate"
show_success "Base de datos configurada"

# 9. Crear superusuario
show_message "👑 Creando superusuario..."
sudo -u arca bash -c "source venv/bin/activate && python manage.py createsuperuser --noinput --username admin --email admin@construccionesarca.net"
show_success "Superusuario creado"

# 10. Recopilar archivos estáticos
show_message "📁 Recopilando archivos estáticos..."
sudo -u arca bash -c "source venv/bin/activate && python manage.py collectstatic --noinput"
show_success "Archivos estáticos recopilados"

# 11. Configurar nginx
show_message "🌐 Configurando nginx..."
cat > /etc/nginx/sites-available/sistema-arca << 'EOF'
server {
    listen 80;
    server_name construccionesarca.net www.construccionesarca.net;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/sistema-arca/staticfiles/;
    }

    location /media/ {
        alias /var/www/sistema-arca/media/;
    }
}
EOF

ln -sf /etc/nginx/sites-available/sistema-arca /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
show_success "Nginx configurado"

# 12. Configurar gunicorn
show_message "🔄 Configurando gunicorn..."
cat > /etc/systemd/system/sistema-arca.service << 'EOF'
[Unit]
Description=Sistema de Construcciones ARCA
After=network.target

[Service]
User=arca
Group=arca
WorkingDirectory=/var/www/sistema-arca
Environment="PATH=/var/www/sistema-arca/venv/bin"
ExecStart=/var/www/sistema-arca/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 sistema_construccion.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable sistema-arca
systemctl start sistema-arca
show_success "Gunicorn configurado"

# 13. Configurar firewall
show_message "🔥 Configurando firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable
show_success "Firewall configurado"

# 14. Verificar estado
show_message "✅ Verificando estado..."
systemctl status sistema-arca --no-pager -l
systemctl status nginx --no-pager -l

show_success "🎉 DESPLIEGUE COMPLETADO EXITOSAMENTE"
show_message "🌐 El sistema está disponible en: http://construccionesarca.net"
show_message "📊 Dashboard: http://construccionesarca.net/dashboard/"
show_message "👥 Usuarios: http://construccionesarca.net/usuarios/dashboard/"
show_message "🔑 Usuario admin creado (cambiar contraseña en el panel)"

echo "====================================="
echo "✅ SISTEMA ARCA DESPLEGADO COMPLETAMENTE"
echo "====================================="
