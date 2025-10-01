#!/bin/bash
# =====================================================
# Script de Verificación Pre-Push
# Verifica que todo esté funcionando antes de subir
# =====================================================

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "No se encontró manage.py. Ejecuta desde la raíz del proyecto."
    exit 1
fi

print_status "🔍 Verificando sistema antes del push..."

# 1. Verificar que Django funciona
print_status "1. Verificando Django..."
python3 manage.py check
if [ $? -eq 0 ]; then
    print_success "Django check OK"
else
    print_error "Django check falló"
    exit 1
fi

# 2. Verificar migraciones
print_status "2. Verificando migraciones..."
python3 manage.py showmigrations --plan | grep -q "\[ \]"
if [ $? -eq 0 ]; then
    print_warning "Hay migraciones pendientes"
    python3 manage.py migrate
    print_success "Migraciones aplicadas"
else
    print_success "Migraciones OK"
fi

# 3. Verificar sintaxis de Python
print_status "3. Verificando sintaxis Python..."
python3 -m py_compile core/models.py core/views.py core/forms_simple.py
if [ $? -eq 0 ]; then
    print_success "Sintaxis Python OK"
else
    print_error "Error de sintaxis Python"
    exit 1
fi

# 4. Verificar que no hay archivos temporales
print_status "4. Verificando archivos temporales..."
TEMP_FILES=$(find . -name "*.pyc" -o -name "__pycache__" -o -name "*.log" | wc -l)
if [ $TEMP_FILES -gt 0 ]; then
    print_warning "Encontrados $TEMP_FILES archivos temporales"
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    print_success "Archivos temporales limpiados"
else
    print_success "No hay archivos temporales"
fi

# 5. Verificar estado de Git
print_status "5. Verificando estado de Git..."
git status --porcelain | wc -l > /tmp/changes_count
CHANGES=$(cat /tmp/changes_count)
if [ $CHANGES -gt 0 ]; then
    print_success "Hay $CHANGES cambios para commitear"
    print_status "Cambios detectados:"
    git status --porcelain
else
    print_warning "No hay cambios para commitear"
fi

# 6. Verificar que el servidor puede iniciar
print_status "6. Verificando que el servidor puede iniciar..."
timeout 10s python3 manage.py runserver 0.0.0.0:8002 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 3
kill $SERVER_PID 2>/dev/null || true
print_success "Servidor puede iniciar correctamente"

print_success "🎉 ¡Todas las verificaciones pasaron!"
print_status "El sistema está listo para el push"
