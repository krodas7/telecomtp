#!/bin/bash

# ============================================================================
# SCRIPT DE LIMPIEZA - Droplet DigitalOcean Existente
# ============================================================================
# Limpia completamente el droplet para un despliegue desde cero

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

print_status "🧹 Iniciando limpieza del droplet..."

# Detener todos los servicios
print_status "⏹️ Deteniendo servicios..."
sudo systemctl stop sistema-arca 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl stop postgresql 2>/dev/null || true
sudo systemctl stop redis-server 2>/dev/null || true
sudo systemctl stop gunicorn 2>/dev/null || true

print_success "✅ Servicios detenidos"

# Eliminar archivos del proyecto
print_status "🗑️ Eliminando archivos del proyecto..."
sudo rm -rf /var/www/sistema-arca 2>/dev/null || true
sudo rm -rf /home/arca 2>/dev/null || true

print_success "✅ Archivos del proyecto eliminados"

# Eliminar configuraciones de servicios
print_status "🗑️ Eliminando configuraciones de servicios..."
sudo rm -f /etc/nginx/sites-available/sistema-arca 2>/dev/null || true
sudo rm -f /etc/nginx/sites-enabled/sistema-arca 2>/dev/null || true
sudo rm -f /etc/systemd/system/sistema-arca.service 2>/dev/null || true
sudo rm -f /etc/supervisor/conf.d/sistema-arca.conf 2>/dev/null || true

print_success "✅ Configuraciones eliminadas"

# Eliminar usuario del sistema
print_status "🗑️ Eliminando usuario del sistema..."
sudo userdel -r arca 2>/dev/null || true

print_success "✅ Usuario eliminado"

# Limpiar base de datos
print_status "🗑️ Limpiando base de datos..."
sudo -u postgres dropdb sistema_arca 2>/dev/null || true
sudo -u postgres dropuser arca 2>/dev/null || true

print_success "✅ Base de datos limpiada"

# Limpiar logs
print_status "🗑️ Limpiando logs..."
sudo rm -rf /var/log/sistema-arca 2>/dev/null || true

print_success "✅ Logs limpiados"

# Recargar configuraciones
print_status "🔄 Recargando configuraciones..."
sudo systemctl daemon-reload
sudo systemctl reload nginx 2>/dev/null || true

print_success "✅ Configuraciones recargadas"

# Verificar limpieza
print_status "🔍 Verificando limpieza..."
if [ ! -d "/var/www/sistema-arca" ] && [ ! -d "/home/arca" ]; then
    print_success "✅ Droplet completamente limpio"
else
    print_warning "⚠️ Algunos archivos pueden no haberse eliminado completamente"
fi

print_success "🎉 Limpieza completada. El droplet está listo para un nuevo despliegue."
print_status "📋 Próximos pasos:"
print_status "   1. Ejecutar el script de despliegue: ./deploy_digitalocean_final.sh"
print_status "   2. Configurar el dominio en Hostinger"
print_status "   3. Configurar SSL con Let's Encrypt"
