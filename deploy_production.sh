#!/bin/bash

# ========================================
# SCRIPT DE DESPLIEGUE AUTOMATIZADO
# Sistema de Construcciones ARCA
# ========================================

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

# Verificar que se ejecuta como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script debe ejecutarse como root"
    exit 1
fi

print_status "🚀 Iniciando despliegue del Sistema de Construcciones ARCA"

# ========================================
# 1. ACTUALIZAR SISTEMA
# ========================================
print_status "📦 Actualizando sistema..."
apt update -y
apt upgrade -y

# ========================================
# 2. INSTALAR DEPENDENCIAS
# ========================================
print_status "🔧 Instalando dependencias del sistema..."
apt install -y python3 python3-pip python3-venv python3-dev nginx git curl wget unzip
apt install -y build-essential libpq-dev postgresql-client

# ========================================
# 3. CREAR USUARIO ARCA
# ========================================
print_status "👤 Configurando usuario arca..."
if ! id "arca" &>/dev/null; then
    adduser --disabled-password --gecos "" arca
    usermod -aG sudo arca
    print_success "Usuario arca creado"
else
    print_warning "Usuario arca ya existe"
fi

# ========================================
# 4. CONFIGURAR DIRECTORIO DEL PROYECTO
# ========================================
print_status "📁 Configurando directorio del proyecto..."
PROJECT_DIR="/var/www/sistema-arca"
mkdir -p $PROJECT_DIR
chown -R arca:arca $PROJECT_DIR

# ========================================
# 5. CLONAR PROYECTO
# ========================================
print_status "📥 Clonando proyecto desde GitHub..."
cd $PROJECT_DIR
sudo -u arca git clone https://github.com/krodas7/sistema-arca-limpio.git .

# ========================================
# 6. CONFIGURAR ENTORNO VIRTUAL
# ========================================
print_status "🐍 Configurando entorno virtual de Python..."
sudo -u arca python3 -m venv venv
sudo -u arca bash -c "source venv/bin/activate && pip install --upgrade pip"

# ========================================
# 7. INSTALAR DEPENDENCIAS DE PYTHON
# ========================================
print_status "📚 Instalando dependencias de Python..."
sudo -u arca bash -c "source venv/bin/activate && pip install -r requirements.txt"

# ========================================
# 8. CONFIGURAR BASE DE DATOS
# ========================================
print_status "🗄️ Configurando base de datos..."
cd $PROJECT_DIR
sudo -u arca bash -c "source venv/bin/activate && python3 manage.py migrate"

# ========================================
# 9. RECOPILAR ARCHIVOS ESTÁTICOS
# ========================================
print_status "📁 Recopilando archivos estáticos..."
sudo -u arca bash -c "source venv/bin/activate && python3 manage.py collectstatic --noinput"

# ========================================
# 10. CONFIGURAR NGINX
# ========================================
print_status "🌐 Configurando Nginx..."
cat > /etc/nginx/sites-available/sistema-arca << 'EOF'
server {
    listen 80 default_server;
    server_name _;
    
    client_max_body_size 100M;

    location /static/ {
        alias /var/www/sistema-arca/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/sistema-arca/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
    }
}
EOF

# Habilitar sitio
ln -sf /etc/nginx/sites-available/sistema-arca /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Probar configuración
nginx -t

# ========================================
# 11. CONFIGURAR GUNICORN
# ========================================
print_status "⚙️ Configurando Gunicorn..."
cat > /etc/systemd/system/sistema-arca.service << 'EOF'
[Unit]
Description=Sistema de Construcciones ARCA
After=network.target

[Service]
Type=notify
User=arca
Group=arca
WorkingDirectory=/var/www/sistema-arca
Environment="PATH=/var/www/sistema-arca/venv/bin"
ExecStart=/var/www/sistema-arca/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 sistema_construccion.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# ========================================
# 12. CONFIGURAR FIREWALL
# ========================================
print_status "🔥 Configurando firewall..."
ufw --force enable
ufw allow ssh
ufw allow 80
ufw allow 443

# ========================================
# 13. INICIAR SERVICIOS
# ========================================
print_status "🚀 Iniciando servicios..."
systemctl daemon-reload
systemctl enable sistema-arca
systemctl start sistema-arca
systemctl restart nginx

# ========================================
# 14. VERIFICAR DESPLIEGUE
# ========================================
print_status "✅ Verificando despliegue..."
sleep 5

# Verificar que los servicios están corriendo
if systemctl is-active --quiet sistema-arca; then
    print_success "Gunicorn está corriendo"
else
    print_error "Gunicorn no está corriendo"
    systemctl status sistema-arca
fi

if systemctl is-active --quiet nginx; then
    print_success "Nginx está corriendo"
else
    print_error "Nginx no está corriendo"
    systemctl status nginx
fi

# Probar acceso local
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "302\|200"; then
    print_success "Aplicación responde correctamente"
else
    print_error "Aplicación no responde"
fi

# ========================================
# 15. MOSTRAR INFORMACIÓN FINAL
# ========================================
print_success "🎉 ¡Despliegue completado exitosamente!"
echo ""
echo "=========================================="
echo "📋 INFORMACIÓN DEL DESPLIEGUE"
echo "=========================================="
echo "🌐 URL: http://$(curl -s ifconfig.me)"
echo "📁 Directorio: $PROJECT_DIR"
echo "👤 Usuario: arca"
echo "🔧 Servicios:"
echo "   - Gunicorn: systemctl status sistema-arca"
echo "   - Nginx: systemctl status nginx"
echo ""
echo "📝 PRÓXIMOS PASOS:"
echo "1. Crear superusuario: sudo -u arca bash -c 'cd $PROJECT_DIR && source venv/bin/activate && python3 manage.py createsuperuser'"
echo "2. Acceder a la aplicación desde tu navegador"
echo "3. Verificar que todos los módulos funcionan correctamente"
echo ""
echo "🔍 COMANDOS ÚTILES:"
echo "   - Ver logs: journalctl -u sistema-arca -f"
echo "   - Reiniciar: systemctl restart sistema-arca"
echo "   - Estado: systemctl status sistema-arca"
echo "=========================================="

print_success "¡Despliegue finalizado! 🚀"
