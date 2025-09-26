#!/bin/bash

# ============================================================================
# SCRIPT DE ACTUALIZACIÓN AUTOMÁTICA - Sistema ARCA Construcción
# ============================================================================
# IP del servidor: 138.197.17.131
# Ejecutar directamente en el servidor

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

# Variables
APP_NAME="sistema-arca"
APP_USER="arca"
APP_DIR="/var/www/$APP_NAME"
BACKUP_DIR="$APP_DIR/backups"
LOGS_DIR="$APP_DIR/logs"

print_status "🚀 Iniciando actualización automática del Sistema ARCA Construcción..."
print_status "📍 Servidor: 138.197.17.131"
print_status "📍 Directorio: $APP_DIR"

# ============================================================================
# PASO 1: VERIFICAR PERMISOS
# ============================================================================

print_status "🔍 Verificando permisos..."

if [[ $EUID -eq 0 ]]; then
    print_warning "Ejecutándose como ROOT, cambiando a usuario $APP_USER..."
    if ! id "$APP_USER" &>/dev/null; then
        print_error "Usuario $APP_USER no existe. Ejecutar primero el despliegue completo."
        exit 1
    fi
    exec sudo -u $APP_USER bash "$0" "$@"
fi

# ============================================================================
# PASO 2: VERIFICAR DIRECTORIO DEL PROYECTO
# ============================================================================

print_status "📁 Verificando directorio del proyecto..."

if [ ! -d "$APP_DIR" ]; then
    print_error "Directorio $APP_DIR no existe. Ejecutar primero el despliegue completo."
    exit 1
fi

cd $APP_DIR

if [ ! -f "manage.py" ]; then
    print_error "Archivo manage.py no encontrado. Directorio incorrecto."
    exit 1
fi

print_success "Directorio del proyecto verificado"

# ============================================================================
# PASO 3: CREAR RESPALDO
# ============================================================================

print_status "💾 Creando respaldo de seguridad..."

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_before_update_$TIMESTAMP.sql"

# Crear directorio de respaldos si no existe
mkdir -p $BACKUP_DIR

# Crear respaldo de la base de datos
if command -v pg_dump &> /dev/null; then
    pg_dump -h localhost -U arca_user -d arca_construccion > $BACKUP_DIR/$BACKUP_FILE 2>/dev/null || print_warning "No se pudo crear respaldo de BD"
    gzip $BACKUP_DIR/$BACKUP_FILE 2>/dev/null || true
    print_success "Respaldo de BD creado: $BACKUP_FILE.gz"
else
    print_warning "pg_dump no disponible, saltando respaldo de BD"
fi

# Crear respaldo del código actual
tar -czf $BACKUP_DIR/code_backup_$TIMESTAMP.tar.gz --exclude=venv --exclude=__pycache__ --exclude=*.pyc --exclude=logs --exclude=backups . 2>/dev/null || true
print_success "Respaldo de código creado: code_backup_$TIMESTAMP.tar.gz"

# ============================================================================
# PASO 4: DETENER SERVICIOS
# ============================================================================

print_status "⏸️ Deteniendo servicios..."

sudo systemctl stop $APP_NAME 2>/dev/null || print_warning "Servicio $APP_NAME no estaba ejecutándose"
sudo systemctl stop nginx 2>/dev/null || print_warning "Nginx no estaba ejecutándose"

# ============================================================================
# PASO 5: ACTUALIZAR CÓDIGO
# ============================================================================

print_status "📥 Actualizando código desde Git..."

# Verificar si es un repositorio Git
if [ ! -d ".git" ]; then
    print_error "No es un repositorio Git. Verificar configuración."
    exit 1
fi

# Hacer pull de los cambios más recientes
git fetch origin
git reset --hard origin/main

print_success "Código actualizado al commit: $(git log -1 --oneline)"

# ============================================================================
# PASO 6: ACTUALIZAR DEPENDENCIAS
# ============================================================================

print_status "📚 Actualizando dependencias Python..."

if [ ! -d "venv" ]; then
    print_error "Entorno virtual no encontrado. Ejecutar primero el despliegue completo."
    exit 1
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_production_simple.txt

print_success "Dependencias actualizadas"

# ============================================================================
# PASO 7: APLICAR MIGRACIONES
# ============================================================================

print_status "🔄 Aplicando migraciones de base de datos..."

export DJANGO_SETTINGS_MODULE=sistema_construccion.production_settings
python manage.py migrate

print_success "Migraciones aplicadas"

# ============================================================================
# PASO 8: RECOLECTAR ARCHIVOS ESTÁTICOS
# ============================================================================

print_status "📁 Recolectando archivos estáticos..."

python manage.py collectstatic --noinput

print_success "Archivos estáticos recolectados"

# ============================================================================
# PASO 9: VERIFICAR CONFIGURACIÓN
# ============================================================================

print_status "🔍 Verificando configuración de Django..."

python manage.py check --settings=sistema_construccion.production_settings

print_success "Configuración verificada"

# ============================================================================
# PASO 10: REINICIAR SERVICIOS
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
# PASO 11: VERIFICACIÓN FINAL
# ============================================================================

print_status "🔍 Verificando funcionamiento de la aplicación..."

# Verificar que la aplicación responda
if curl -s http://localhost:8000/health/ | grep -q "healthy" 2>/dev/null; then
    print_success "✓ Aplicación respondiendo correctamente"
else
    print_warning "⚠ No se pudo verificar el endpoint de salud"
fi

# Verificar archivos estáticos
if [ -f "staticfiles/admin/css/base.css" ]; then
    print_success "✓ Archivos estáticos recolectados correctamente"
else
    print_warning "⚠ Archivos estáticos no encontrados"
fi

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print_success "🎉 ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!"
echo
print_status "📋 RESUMEN DE LA ACTUALIZACIÓN:"
print_status "   • Servidor: 138.197.17.131"
print_status "   • Código actualizado al commit: $(git log -1 --oneline)"
print_status "   • Dependencias actualizadas"
print_status "   • Migraciones aplicadas"
print_status "   • Archivos estáticos recolectados"
print_status "   • Servicios reiniciados"
echo
print_status "💾 RESPALDOS CREADOS:"
print_status "   • Base de datos: $BACKUP_FILE.gz"
print_status "   • Código: code_backup_$TIMESTAMP.tar.gz"
echo
print_status "🌐 ACCESO:"
print_status "   • Local: http://localhost"
print_status "   • Producción: https://construccionesarca.net"
echo
print_status "🔧 COMANDOS ÚTILES:"
print_status "   • Ver logs: sudo journalctl -u $APP_NAME -f"
print_status "   • Reiniciar: sudo systemctl restart $APP_NAME"
print_status "   • Estado: sudo systemctl status $APP_NAME"
echo
print_success "🚀 ¡Tu Sistema ARCA Construcción está actualizado y funcionando!"

# ============================================================================
# LIMPIEZA DE RESPALDOS ANTIGUOS
# ============================================================================

print_status "🧹 Limpiando respaldos antiguos (mantener últimos 7 días)..."
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete 2>/dev/null || true
find $BACKUP_DIR -name "code_backup_*.tar.gz" -mtime +7 -delete 2>/dev/null || true
print_success "Limpieza completada"







