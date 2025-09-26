#!/bin/bash

# ============================================================================
# SCRIPT DE ACTUALIZACIÓN RÁPIDA - Sistema ARCA Construcción
# ============================================================================
# Para actualizar el servidor DigitalOcean con los cambios más recientes
# Ejecutar en el servidor Ubuntu 22.04 LTS

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

# Variables configurables
APP_NAME="sistema-arca"
APP_USER="arca"
APP_DIR="/var/www/$APP_NAME"
BACKUP_DIR="$APP_DIR/backups"
LOGS_DIR="$APP_DIR/logs"

print_status "🚀 Iniciando actualización del Sistema ARCA Construcción..."
print_status "📍 Ubicación: $APP_DIR"

# ============================================================================
# PASO 1: CREAR RESPALDO ANTES DE ACTUALIZAR
# ============================================================================

print_status "💾 Creando respaldo de seguridad..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_before_update_$TIMESTAMP.sql"

# Crear respaldo de la base de datos
if command -v pg_dump &> /dev/null; then
    sudo -u $APP_USER pg_dump -h localhost -U arca_user -d arca_construccion > $BACKUP_DIR/$BACKUP_FILE
    sudo -u $APP_USER gzip $BACKUP_DIR/$BACKUP_FILE
    print_success "Respaldo de BD creado: $BACKUP_FILE.gz"
else
    print_warning "pg_dump no disponible, saltando respaldo de BD"
fi

# Crear respaldo del código actual
sudo -u $APP_USER tar -czf $BACKUP_DIR/code_backup_$TIMESTAMP.tar.gz -C $APP_DIR --exclude=venv --exclude=__pycache__ --exclude=*.pyc --exclude=logs --exclude=backups .
print_success "Respaldo de código creado: code_backup_$TIMESTAMP.tar.gz"

# ============================================================================
# PASO 2: DETENER SERVICIOS
# ============================================================================

print_status "⏸️ Deteniendo servicios..."
sudo systemctl stop $APP_NAME || print_warning "Servicio $APP_NAME no estaba ejecutándose"
sudo systemctl stop nginx || print_warning "Nginx no estaba ejecutándose"

# ============================================================================
# PASO 3: ACTUALIZAR CÓDIGO
# ============================================================================

print_status "📥 Actualizando código desde Git..."
cd $APP_DIR

# Hacer pull de los cambios más recientes
sudo -u $APP_USER git fetch origin
sudo -u $APP_USER git reset --hard origin/main

print_success "Código actualizado al commit: $(sudo -u $APP_USER git log -1 --oneline)"

# ============================================================================
# PASO 4: ACTUALIZAR DEPENDENCIAS
# ============================================================================

print_status "📚 Actualizando dependencias Python..."
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r requirements_production_simple.txt

print_success "Dependencias actualizadas"

# ============================================================================
# PASO 5: APLICAR MIGRACIONES
# ============================================================================

print_status "🔄 Aplicando migraciones de base de datos..."
cd $APP_DIR
export DJANGO_SETTINGS_MODULE=sistema_construccion.production_settings
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py migrate

print_success "Migraciones aplicadas"

# ============================================================================
# PASO 6: RECOLECTAR ARCHIVOS ESTÁTICOS
# ============================================================================

print_status "📁 Recolectando archivos estáticos..."
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py collectstatic --noinput

print_success "Archivos estáticos recolectados"

# ============================================================================
# PASO 7: VERIFICAR CONFIGURACIÓN
# ============================================================================

print_status "🔍 Verificando configuración de Django..."
sudo -u $APP_USER $APP_DIR/venv/bin/python manage.py check --settings=sistema_construccion.production_settings

print_success "Configuración verificada"

# ============================================================================
# PASO 8: REINICIAR SERVICIOS
# ============================================================================

print_status "🔄 Reiniciando servicios..."

# Reiniciar aplicación
sudo systemctl start $APP_NAME
sudo systemctl enable $APP_NAME

# Reiniciar Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Verificar que los servicios estén funcionando
sleep 5

if sudo systemctl is-active --quiet $APP_NAME; then
    print_success "Servicio $APP_NAME iniciado correctamente"
else
    print_error "Error iniciando servicio $APP_NAME"
    sudo systemctl status $APP_NAME --no-pager -l
    exit 1
fi

if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx iniciado correctamente"
else
    print_error "Error iniciando Nginx"
    sudo systemctl status nginx --no-pager -l
    exit 1
fi

# ============================================================================
# PASO 9: VERIFICACIÓN FINAL
# ============================================================================

print_status "🔍 Verificando funcionamiento de la aplicación..."

# Verificar que la aplicación responda
if curl -s http://localhost:8000/health/ | grep -q "healthy" 2>/dev/null; then
    print_success "✓ Aplicación respondiendo correctamente"
else
    print_warning "⚠ No se pudo verificar el endpoint de salud"
fi

# Verificar archivos estáticos
if [ -f "$APP_DIR/staticfiles/admin/css/base.css" ]; then
    print_success "✓ Archivos estáticos recolectados correctamente"
else
    print_warning "⚠ Archivos estáticos no encontrados"
fi

# Verificar logs recientes
print_status "📋 Últimas líneas de logs:"
sudo tail -n 5 $LOGS_DIR/gunicorn_error.log 2>/dev/null || print_warning "Log de Gunicorn no disponible"

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print_success "🎉 ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!"
echo
print_status "📋 RESUMEN DE LA ACTUALIZACIÓN:"
print_status "   • Código actualizado al commit: $(sudo -u $APP_USER git log -1 --oneline)"
print_status "   • Dependencias actualizadas"
print_status "   • Migraciones aplicadas"
print_status "   • Archivos estáticos recolectados"
print_status "   • Servicios reiniciados"
echo
print_status "💾 RESPALDOS CREADOS:"
print_status "   • Base de datos: $BACKUP_FILE.gz"
print_status "   • Código: code_backup_$TIMESTAMP.tar.gz"
echo
print_status "🔧 COMANDOS ÚTILES:"
print_status "   • Ver logs: sudo journalctl -u $APP_NAME -f"
print_status "   • Reiniciar: sudo systemctl restart $APP_NAME"
print_status "   • Estado: sudo systemctl status $APP_NAME"
print_status "   • Logs de Gunicorn: tail -f $LOGS_DIR/gunicorn_error.log"
echo
print_status "🌐 ACCESO:"
print_status "   • Local: http://localhost"
print_status "   • Producción: https://construccionesarca.net"
echo
print_success "🚀 ¡Tu Sistema ARCA Construcción está actualizado y funcionando!"

# ============================================================================
# LIMPIEZA DE RESPALDOS ANTIGUOS (OPCIONAL)
# ============================================================================

print_status "🧹 Limpiando respaldos antiguos (mantener últimos 7 días)..."
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete 2>/dev/null || true
find $BACKUP_DIR -name "code_backup_*.tar.gz" -mtime +7 -delete 2>/dev/null || true
print_success "Limpieza completada"







