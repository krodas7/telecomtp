#!/bin/bash
# =====================================================
# Script de Sincronización Rápida
# Para cambios menores y actualizaciones rápidas
# =====================================================

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[SYNC]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Ejecuta desde la raíz del proyecto"
    exit 1
fi

print_status "🔄 Sincronización rápida iniciada..."

# Agregar cambios
git add .

# Commit rápido
git commit -m "⚡ Sync rápido - $(date '+%H:%M:%S')" || echo "No hay cambios para commitear"

# Push al repositorio limpio
git push origin-nuevo cleanup-project

print_success "✅ Sincronización completada"
