#!/bin/bash

# Script de despliegue para el Sistema de Construcción
# Uso: ./deploy.sh

echo "🚀 INICIANDO DESPLIEGUE DEL SISTEMA DE CONSTRUCCIÓN"
echo "=================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    print_error "No se encontró manage.py. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

print_status "Directorio del proyecto verificado"

# 1. Activar entorno virtual (si existe)
if [ -d "venv" ]; then
    print_status "Activando entorno virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    print_status "Activando entorno virtual..."
    source .venv/bin/activate
else
    print_warning "No se encontró entorno virtual. Continuando sin él..."
fi

# 2. Instalar/actualizar dependencias
print_status "Instalando dependencias..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_status "Dependencias instaladas correctamente"
else
    print_error "Error instalando dependencias"
    exit 1
fi

# 3. Aplicar migraciones
print_status "Aplicando migraciones de base de datos..."
python manage.py migrate

if [ $? -eq 0 ]; then
    print_status "Migraciones aplicadas correctamente"
else
    print_error "Error aplicando migraciones"
    exit 1
fi

# 4. Recopilar archivos estáticos
print_status "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

if [ $? -eq 0 ]; then
    print_status "Archivos estáticos recopilados correctamente"
else
    print_error "Error recopilando archivos estáticos"
    exit 1
fi

# 5. Verificar configuración
print_status "Verificando configuración de Django..."
python manage.py check --deploy

if [ $? -eq 0 ]; then
    print_status "Configuración verificada correctamente"
else
    print_warning "Advertencias en la configuración (revisar arriba)"
fi

# 6. Crear superusuario si no existe
print_status "Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    print('Creando superusuario por defecto...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuario creado: admin / admin123')
else:
    print('Superusuario ya existe')
"

# 7. Mostrar información del despliegue
echo ""
echo "🎉 DESPLIEGUE COMPLETADO EXITOSAMENTE"
echo "====================================="
echo ""
echo "📋 Información del despliegue:"
echo "   - Proyecto: Sistema de Construcción Django"
echo "   - Django: $(python -c 'import django; print(django.get_version())')"
echo "   - Python: $(python --version)"
echo ""
echo "🔑 Credenciales de acceso:"
echo "   - Usuario: admin"
echo "   - Password: admin123"
echo ""
echo "🚀 Para iniciar el servidor:"
echo "   - Desarrollo: python manage.py runserver"
echo "   - Producción: gunicorn sistema_construccion.wsgi:application"
echo ""
echo "📁 Archivos importantes:"
echo "   - requirements.txt: Dependencias del proyecto"
echo "   - gunicorn.conf.py: Configuración de Gunicorn"
echo "   - nginx.conf: Configuración de Nginx"
echo "   - deploy_guide.md: Guía completa de despliegue"
echo ""
print_status "¡El sistema está listo para usar!"
