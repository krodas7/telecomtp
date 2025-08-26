#!/bin/bash

# Script de Despliegue para Sistema de Construcción en Producción
# Autor: Sistema de Construcción
# Fecha: $(date)
# Versión: 1.0

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración del proyecto
PROJECT_NAME="sistema_construccion"
PROJECT_DIR="/var/www/sistema_construccion"
VENV_DIR="$PROJECT_DIR/venv"
BACKUP_DIR="$PROJECT_DIR/backups"
LOGS_DIR="$PROJECT_DIR/logs"
TEMP_DIR="$PROJECT_DIR/temp"
MEDIA_DIR="$PROJECT_DIR/media"
STATIC_DIR="$PROJECT_DIR/staticfiles"

# Configuración del servidor
SERVER_USER="www-data"
SERVER_GROUP="www-data"
NGINX_SITE="sistema_construccion"
SUPERVISOR_CONFIG="sistema_construccion"

# Función para logging
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

# Función para verificar permisos de root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Este script debe ejecutarse como root"
    fi
}

# Función para verificar dependencias
check_dependencies() {
    log "Verificando dependencias del sistema..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        error "Python3 no está instalado"
    fi
    
    # Verificar pip
    if ! command -v pip3 &> /dev/null; then
        error "pip3 no está instalado"
    fi
    
    # Verificar Nginx
    if ! command -v nginx &> /dev/null; then
        error "Nginx no está instalado"
    fi
    
    # Verificar Supervisor
    if ! command -v supervisord &> /dev/null; then
        error "Supervisor no está instalado"
    fi
    
    # Verificar Redis (opcional)
    if ! command -v redis-server &> /dev/null; then
        warn "Redis no está instalado (opcional para caché)"
    fi
    
    log "Dependencias verificadas correctamente"
}

# Función para crear directorios del proyecto
create_directories() {
    log "Creando directorios del proyecto..."
    
    mkdir -p "$PROJECT_DIR"
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$LOGS_DIR"
    mkdir -p "$TEMP_DIR"
    mkdir -p "$MEDIA_DIR"
    mkdir -p "$STATIC_DIR"
    
    # Crear directorios de respaldo específicos
    mkdir -p "$BACKUP_DIR/auto"
    mkdir -p "$BACKUP_DIR/manual"
    mkdir -p "$BACKUP_DIR/emergency"
    mkdir -p "$BACKUP_DIR/security"
    
    # Crear directorios de logs específicos
    mkdir -p "$LOGS_DIR/django"
    mkdir -p "$LOGS_DIR/gunicorn"
    mkdir -p "$LOGS_DIR/nginx"
    mkdir -p "$LOGS_DIR/supervisor"
    
    log "Directorios creados correctamente"
}

# Función para configurar permisos
setup_permissions() {
    log "Configurando permisos..."
    
    # Cambiar propietario de todos los archivos del proyecto
    chown -R "$SERVER_USER:$SERVER_GROUP" "$PROJECT_DIR"
    
    # Configurar permisos de directorios
    find "$PROJECT_DIR" -type d -exec chmod 755 {} \;
    
    # Configurar permisos de archivos
    find "$PROJECT_DIR" -type f -exec chmod 644 {} \;
    
    # Configurar permisos de ejecución para scripts
    find "$PROJECT_DIR" -name "*.sh" -exec chmod +x {} \;
    find "$PROJECT_DIR" -name "*.py" -exec chmod +x {} \;
    
    # Configurar permisos especiales para directorios críticos
    chmod 750 "$LOGS_DIR"
    chmod 750 "$BACKUP_DIR"
    chmod 750 "$MEDIA_DIR"
    
    log "Permisos configurados correctamente"
}

# Función para crear entorno virtual
create_virtualenv() {
    log "Creando entorno virtual..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR"
        log "Entorno virtual creado"
    else
        log "Entorno virtual ya existe"
    fi
    
    # Activar entorno virtual e instalar dependencias
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r "$PROJECT_DIR/requirements.txt"
    
    log "Entorno virtual configurado correctamente"
}

# Función para configurar base de datos
setup_database() {
    log "Configurando base de datos..."
    
    cd "$PROJECT_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Aplicar migraciones
    python manage.py migrate --settings=sistema_construccion.production_settings
    
    # Crear superusuario si no existe
    if ! python manage.py shell --settings=sistema_construccion.production_settings -c "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).exists()" 2>/dev/null | grep -q "True"; then
        log "Creando superusuario..."
        python manage.py createsuperuser --settings=sistema_construccion.production_settings --noinput || warn "No se pudo crear superusuario automáticamente"
    fi
    
    # Recolectar archivos estáticos
    python manage.py collectstatic --settings=sistema_construccion.production_settings --noinput
    
    log "Base de datos configurada correctamente"
}

# Función para configurar Nginx
setup_nginx() {
    log "Configurando Nginx..."
    
    # Copiar configuración del sitio
    cp "$PROJECT_DIR/nginx/$NGINX_SITE.conf" "/etc/nginx/sites-available/$NGINX_SITE"
    
    # Habilitar el sitio
    ln -sf "/etc/nginx/sites-available/$NGINX_SITE" "/etc/nginx/sites-enabled/"
    
    # Verificar configuración de Nginx
    if nginx -t; then
        log "Configuración de Nginx válida"
    else
        error "Configuración de Nginx inválida"
    fi
    
    # Reiniciar Nginx
    systemctl restart nginx
    systemctl enable nginx
    
    log "Nginx configurado correctamente"
}

# Función para configurar Supervisor
setup_supervisor() {
    log "Configurando Supervisor..."
    
    # Copiar configuración de Supervisor
    cp "$PROJECT_DIR/supervisor/$SUPERVISOR_CONFIG.conf" "/etc/supervisor/conf.d/"
    
    # Crear directorio de logs de Supervisor
    mkdir -p "/var/log/supervisor"
    
    # Recargar configuración de Supervisor
    supervisorctl reread
    supervisorctl update
    
    # Iniciar todos los programas del grupo
    supervisorctl start sistema_construccion_group:*
    
    log "Supervisor configurado correctamente"
}

# Función para configurar SSL (Let's Encrypt)
setup_ssl() {
    log "Configurando SSL..."
    
    # Verificar si certbot está instalado
    if ! command -v certbot &> /dev/null; then
        warn "Certbot no está instalado. Instalando..."
        apt update
        apt install -y certbot python3-certbot-nginx
    fi
    
    # Solicitar dominio
    read -p "Ingrese el dominio para el certificado SSL: " DOMAIN
    
    if [ -n "$DOMAIN" ]; then
        # Obtener certificado SSL
        certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email admin@"$DOMAIN"
        
        # Configurar renovación automática
        echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
        
        log "SSL configurado para dominio: $DOMAIN"
    else
        warn "No se especificó dominio, SSL no configurado"
    fi
}

# Función para configurar firewall
setup_firewall() {
    log "Configurando firewall..."
    
    # Verificar si ufw está instalado
    if command -v ufw &> /dev/null; then
        # Permitir SSH
        ufw allow ssh
        
        # Permitir HTTP y HTTPS
        ufw allow 80
        ufw allow 443
        
        # Habilitar firewall
        ufw --force enable
        
        log "Firewall configurado correctamente"
    else
        warn "ufw no está instalado, firewall no configurado"
    fi
}

# Función para configurar respaldos automáticos
setup_backups() {
    log "Configurando respaldos automáticos..."
    
    # Crear script de respaldo
    cat > "$PROJECT_DIR/backup_script.sh" << 'EOF'
#!/bin/bash
# Script de respaldo automático

PROJECT_DIR="/var/www/sistema_construccion"
BACKUP_DIR="$PROJECT_DIR/backups/auto"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Crear respaldo de la base de datos
cd "$PROJECT_DIR"
source venv/bin/activate
python manage.py dumpdata --settings=sistema_construccion.production_settings \
    --exclude contenttypes \
    --exclude sessions \
    --output "$BACKUP_DIR/db_backup_$TIMESTAMP.json"

# Crear respaldo de archivos de media
tar -czf "$BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz" -C "$PROJECT_DIR" media/

# Crear respaldo de archivos críticos
tar -czf "$BACKUP_DIR/critical_files_backup_$TIMESTAMP.tar.gz" \
    manage.py \
    requirements.txt \
    sistema_construccion/settings.py \
    core/models.py \
    core/views.py

# Limpiar respaldos antiguos (mantener solo los últimos 7 días)
find "$BACKUP_DIR" -name "*.json" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Respaldo completado: $TIMESTAMP"
EOF
    
    # Hacer ejecutable el script
    chmod +x "$PROJECT_DIR/backup_script.sh"
    
    # Agregar al crontab (cada 6 horas)
    (crontab -l 2>/dev/null; echo "0 */6 * * * $PROJECT_DIR/backup_script.sh") | crontab -
    
    log "Respaldos automáticos configurados"
}

# Función para configurar monitoreo
setup_monitoring() {
    log "Configurando monitoreo..."
    
    # Crear script de monitoreo
    cat > "$PROJECT_DIR/monitor_script.sh" << 'EOF'
#!/bin/bash
# Script de monitoreo del sistema

PROJECT_DIR="/var/www/sistema_construccion"
LOGS_DIR="$PROJECT_DIR/logs"
ALERT_EMAIL="admin@tu-dominio.com"

# Verificar uso de disco
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "ALERTA: Uso de disco alto: ${DISK_USAGE}%" | mail -s "Alerta Sistema Construcción" "$ALERT_EMAIL"
fi

# Verificar uso de memoria
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "ALERTA: Uso de memoria alto: ${MEMORY_USAGE}%" | mail -s "Alerta Sistema Construcción" "$ALERT_EMAIL"
fi

# Verificar logs de error
ERROR_COUNT=$(grep -c "ERROR" "$LOGS_DIR/django/django.log" 2>/dev/null || echo "0")
if [ "$ERROR_COUNT" -gt 100 ]; then
    echo "ALERTA: Muchos errores en logs: $ERROR_COUNT" | mail -s "Alerta Sistema Construcción" "$ALERT_EMAIL"
fi

echo "Monitoreo completado: $(date)"
EOF
    
    # Hacer ejecutable el script
    chmod +x "$PROJECT_DIR/monitor_script.sh"
    
    # Agregar al crontab (cada 15 minutos)
    (crontab -l 2>/dev/null; echo "*/15 * * * * $PROJECT_DIR/monitor_script.sh") | crontab -
    
    log "Monitoreo configurado"
}

# Función para verificar el despliegue
verify_deployment() {
    log "Verificando despliegue..."
    
    # Verificar que Nginx esté funcionando
    if systemctl is-active --quiet nginx; then
        log "✓ Nginx está funcionando"
    else
        error "✗ Nginx no está funcionando"
    fi
    
    # Verificar que Supervisor esté funcionando
    if systemctl is-active --quiet supervisor; then
        log "✓ Supervisor está funcionando"
    else
        error "✗ Supervisor no está funcionando"
    fi
    
    # Verificar que la aplicación esté funcionando
    if curl -s http://localhost/health/ | grep -q "healthy"; then
        log "✓ Aplicación está funcionando"
    else
        error "✗ Aplicación no está funcionando"
    fi
    
    # Verificar archivos estáticos
    if [ -f "$STATIC_DIR/admin/css/base.css" ]; then
        log "✓ Archivos estáticos recolectados"
    else
        error "✗ Archivos estáticos no recolectados"
    fi
    
    log "Despliegue verificado correctamente"
}

# Función para mostrar información del sistema
show_system_info() {
    log "Información del sistema:"
    echo "  - Proyecto: $PROJECT_NAME"
    echo "  - Directorio: $PROJECT_DIR"
    echo "  - Usuario: $SERVER_USER"
    echo "  - Grupo: $SERVER_GROUP"
    echo "  - Entorno virtual: $VENV_DIR"
    echo "  - Logs: $LOGS_DIR"
    echo "  - Respaldos: $BACKUP_DIR"
    echo "  - Archivos estáticos: $STATIC_DIR"
    echo "  - Media: $MEDIA_DIR"
}

# Función para mostrar comandos útiles
show_useful_commands() {
    log "Comandos útiles:"
    echo "  - Ver logs de la aplicación: tail -f $LOGS_DIR/django/django.log"
    echo "  - Ver logs de Gunicorn: tail -f $LOGS_DIR/gunicorn/gunicorn_error.log"
    echo "  - Ver logs de Nginx: tail -f /var/log/nginx/error.log"
    echo "  - Ver logs de Supervisor: tail -f /var/log/supervisor/sistema_construccion_stdout.log"
    echo "  - Reiniciar aplicación: supervisorctl restart sistema_construccion"
    echo "  - Reiniciar Nginx: systemctl restart nginx"
    echo "  - Verificar estado: supervisorctl status"
    echo "  - Crear respaldo manual: $PROJECT_DIR/backup_script.sh"
    echo "  - Monitorear sistema: $PROJECT_DIR/monitor_script.sh"
}

# Función principal
main() {
    log "=== INICIANDO DESPLIEGUE DE PRODUCCIÓN ==="
    
    # Verificar permisos de root
    check_root
    
    # Verificar dependencias
    check_dependencies
    
    # Crear directorios
    create_directories
    
    # Configurar permisos
    setup_permissions
    
    # Crear entorno virtual
    create_virtualenv
    
    # Configurar base de datos
    setup_database
    
    # Configurar Nginx
    setup_nginx
    
    # Configurar Supervisor
    setup_supervisor
    
    # Configurar SSL (opcional)
    read -p "¿Desea configurar SSL con Let's Encrypt? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_ssl
    fi
    
    # Configurar firewall
    setup_firewall
    
    # Configurar respaldos automáticos
    setup_backups
    
    # Configurar monitoreo
    setup_monitoring
    
    # Verificar despliegue
    verify_deployment
    
    # Mostrar información
    show_system_info
    show_useful_commands
    
    log "=== DESPLIEGUE COMPLETADO EXITOSAMENTE ==="
    log "El sistema está listo para producción"
    log "Acceda a http://localhost o https://tu-dominio.com"
}

# Ejecutar función principal
main "$@"



