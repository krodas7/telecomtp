#!/bin/bash
# =====================================================
# Script de Despliegue Automático de Cambios
# Sistema ARCA Construcción
# =====================================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
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

# Función para confirmar acción
confirm() {
    read -p "$(echo -e ${YELLOW}$1${NC}) [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "No se encontró manage.py. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

print_status "🚀 Iniciando proceso de despliegue de cambios..."

# Paso 1: Verificar estado del repositorio
print_status "📋 Verificando estado del repositorio..."
git status

# Paso 2: Agregar todos los cambios
print_status "📁 Agregando cambios al staging area..."
git add .

# Paso 3: Verificar qué se va a commitear
print_status "🔍 Cambios que se van a commitear:"
git status --porcelain

if ! confirm "¿Continuar con el commit de estos cambios?"; then
    print_warning "Operación cancelada por el usuario."
    exit 0
fi

# Paso 4: Crear commit con mensaje descriptivo
print_status "💾 Creando commit..."
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="🔄 Actualización automática - $TIMESTAMP

- Sistema de planillas múltiples implementado
- Selector de planilla integrado en trabajadores diarios
- Formularios simplificados (solo nombre requerido)
- Sistema de respaldos verificado y funcional
- Mejoras en UI/UX y funcionalidad

Generado automáticamente el $(date '+%d/%m/%Y a las %H:%M:%S')"

git commit -m "$COMMIT_MSG"

# Paso 5: Subir cambios al repositorio limpio
print_status "📤 Subiendo cambios al repositorio limpio..."
git push origin-nuevo cleanup-project

# Paso 6: Verificar que el push fue exitoso
if [ $? -eq 0 ]; then
    print_success "✅ Cambios subidos exitosamente al repositorio limpio"
else
    print_error "❌ Error al subir cambios"
    exit 1
fi

# Paso 7: Mostrar resumen
print_success "🎉 ¡Despliegue completado exitosamente!"
echo
print_status "📊 Resumen:"
echo "  • Repositorio: https://github.com/krodas7/sistema-arca-limpio"
echo "  • Rama: cleanup-project"
echo "  • Commit: $(git rev-parse --short HEAD)"
echo "  • Fecha: $(date '+%d/%m/%Y %H:%M:%S')"
echo

# Paso 8: Opción para desplegar a producción
if confirm "¿Deseas desplegar estos cambios a producción en DigitalOcean?"; then
    print_status "🚀 Iniciando despliegue a producción..."
    
    # Verificar que existe el script de despliegue
    if [ -f "deploy_production.sh" ]; then
        chmod +x deploy_production.sh
        ./deploy_production.sh
    else
        print_warning "Script de despliegue a producción no encontrado."
        print_status "Puedes desplegar manualmente usando:"
        echo "  git clone https://github.com/krodas7/sistema-arca-limpio.git"
        echo "  cd sistema-arca-limpio"
        echo "  git checkout cleanup-project"
        echo "  # Seguir proceso de despliegue en DigitalOcean"
    fi
else
    print_status "📝 Cambios guardados en el repositorio. Puedes desplegar más tarde."
fi

print_success "✨ Proceso completado. ¡Hasta la próxima!"
