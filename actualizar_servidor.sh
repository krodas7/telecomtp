#!/bin/bash
# Script de Actualización Rápida para Servidor
# Ejecutar en el servidor después de subir los archivos

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Configuración
PROJECT_DIR="/var/www/sistema_construccion"
VENV_DIR="$PROJECT_DIR/venv"

log "=== INICIANDO ACTUALIZACIÓN RÁPIDA ==="

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    error "No se encontró manage.py. Ejecutar desde el directorio del proyecto."
fi

# Activar entorno virtual
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    log "Entorno virtual activado"
else
    warn "No se encontró entorno virtual en $VENV_DIR"
fi

# Instalar/actualizar dependencias
log "Instalando dependencias..."
pip install -r requirements_production.txt

# Aplicar migraciones
log "Aplicando migraciones..."
python manage.py migrate --settings=sistema_construccion.production_settings

# Recolectar archivos estáticos
log "Recolectando archivos estáticos..."
python manage.py collectstatic --settings=sistema_construccion.production_settings --noinput

# Verificar configuración
log "Verificando configuración..."
python manage.py check --settings=sistema_construccion.production_settings

# Reiniciar servicios
log "Reiniciando servicios..."
if command -v supervisorctl &> /dev/null; then
    supervisorctl restart sistema_construccion
    log "✓ Aplicación reiniciada"
else
    warn "Supervisor no encontrado, reiniciar manualmente"
fi

# Verificar que todo funcione
log "Verificando aplicación..."
if curl -s http://localhost/health/ | grep -q "healthy"; then
    log "✓ Aplicación funcionando correctamente"
else
    warn "No se pudo verificar el estado de la aplicación"
fi

log "=== ACTUALIZACIÓN COMPLETADA ==="
log "El sistema ha sido actualizado con los cambios más recientes"
