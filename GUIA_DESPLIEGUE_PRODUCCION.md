# 🚀 GUÍA COMPLETA DE DESPLIEGUE A PRODUCCIÓN

## **Sistema ARCA Construcción - Migración a Producción**

---

## **📋 PREREQUISITOS**

### **1. Sistema Operativo**
- **Ubuntu 20.04+ / CentOS 8+ / Debian 11+**
- **4GB RAM mínimo** (8GB recomendado)
- **20GB espacio en disco** mínimo
- **Acceso root o sudo**

### **2. Software Base**
- **Python 3.9+**
- **PostgreSQL 12+**
- **Redis 6+**
- **Nginx**
- **Git**

### **3. Dominio y SSL**
- **Dominio configurado** (ej: `tuempresa.com`)
- **Certificado SSL** (Let's Encrypt gratuito)

---

## **🔧 PASO 1: PREPARACIÓN DEL SERVIDOR**

### **1.1 Actualizar Sistema**
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git unzip
```

### **1.2 Instalar Python**
```bash
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y python3-dev build-essential libpq-dev
```

### **1.3 Instalar PostgreSQL**
```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### **1.4 Instalar Redis**
```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### **1.5 Instalar Nginx**
```bash
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

## **📁 PASO 2: PREPARACIÓN DEL PROYECTO**

### **2.1 Clonar Proyecto**
```bash
cd /opt
sudo git clone https://github.com/tu-usuario/sistema-construccion-django.git
sudo chown -R $USER:$USER sistema-construccion-django
cd sistema-construccion-django
```

### **2.2 Crear Entorno Virtual**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **2.3 Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp production.env .env

# Editar con tus valores
nano .env
```

**Configuración mínima en `.env`:**
```bash
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DB_NAME=arca_construccion
DB_USER=arca_user
DB_PASSWORD=tu_contraseña_segura
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

---

## **🚀 PASO 3: ACTIVACIÓN DE PRODUCCIÓN**

### **3.1 Ejecutar Script de Activación**
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar script de activación
python activate_production.py
```

**Este script hará:**
- ✅ Cargar variables de entorno
- ✅ Crear directorios necesarios
- ✅ Hacer backup de SQLite
- ✅ Instalar dependencias de producción
- ✅ Configurar WSGI de producción
- ✅ Verificar configuración

### **3.2 Verificar Instalación**
```bash
# Verificar que Django funciona
python manage.py check --deploy

# Verificar configuración
python manage.py check
```

---

## **🗄️ PASO 4: CONFIGURACIÓN DE BASE DE DATOS**

### **4.1 Crear Base de Datos PostgreSQL**
```bash
# Conectar como postgres
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE arca_construccion;
CREATE USER arca_user WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE arca_construccion TO arca_user;
ALTER USER arca_user CREATEDB;
\q
```

### **4.2 Migrar Datos**
```bash
# Ejecutar script de migración
python migrate_to_postgresql.py
```

**Este script hará:**
- ✅ Crear base de datos si no existe
- ✅ Crear usuario si no existe
- ✅ Ejecutar migraciones
- ✅ Recolectar archivos estáticos
- ✅ Crear superusuario

---

## **🌐 PASO 5: CONFIGURACIÓN DE NGINX**

### **5.1 Crear Configuración de Nginx**
```bash
sudo nano /etc/nginx/sites-available/arca-construccion
```

**Contenido:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirigir a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Static Files
    location /static/ {
        alias /opt/sistema-construccion-django/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files
    location /media/ {
        alias /opt/sistema-construccion-django/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

### **5.2 Activar Sitio**
```bash
# Crear enlace simbólico
sudo ln -s /etc/nginx/sites-available/arca-construccion /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx
```

---

## **⚙️ PASO 6: CONFIGURACIÓN DE GUNICORN**

### **6.1 Crear Servicio Systemd**
```bash
sudo nano /etc/systemd/system/arca-construccion.service
```

**Contenido:**
```ini
[Unit]
Description=ARCA Construccion Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/sistema-construccion-django
Environment="PATH=/opt/sistema-construccion-django/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=sistema_construccion.production_settings"
ExecStart=/opt/sistema-construccion-django/venv/bin/gunicorn --config gunicorn.conf.py sistema_construccion.wsgi_production:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

### **6.2 Activar Servicio**
```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar servicio
sudo systemctl enable arca-construccion

# Iniciar servicio
sudo systemctl start arca-construccion

# Verificar estado
sudo systemctl status arca-construccion
```

---

## **🔒 PASO 7: CONFIGURACIÓN DE SSL**

### **7.1 Instalar Certbot**
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### **7.2 Obtener Certificado SSL**
```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### **7.3 Configurar Renovación Automática**
```bash
# Verificar renovación automática
sudo certbot renew --dry-run

# Agregar a crontab
sudo crontab -e

# Agregar esta línea:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## **📊 PASO 8: MONITOREO Y LOGS**

### **8.1 Verificar Logs**
```bash
# Logs de Django
tail -f /opt/sistema-construccion-django/logs/django.log

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs del servicio
sudo journalctl -u arca-construccion -f
```

### **8.2 Monitoreo de Estado**
```bash
# Estado del servicio
sudo systemctl status arca-construccion

# Estado de Nginx
sudo systemctl status nginx

# Estado de PostgreSQL
sudo systemctl status postgresql

# Estado de Redis
sudo systemctl status redis-server
```

---

## **🔄 PASO 9: ACTUALIZACIONES Y MANTENIMIENTO**

### **9.1 Actualizar Código**
```bash
cd /opt/sistema-construccion-django
git pull origin main

# Activar entorno virtual
source venv/bin/activate

# Instalar nuevas dependencias
pip install -r requirements_production.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar estáticos
python manage.py collectstatic --noinput

# Reiniciar servicio
sudo systemctl restart arca-construccion
```

### **9.2 Backup Automático**
```bash
# Crear script de backup
sudo nano /opt/backup_script.sh
```

**Contenido del script:**
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/opt/sistema-construccion-django"

# Crear directorio de backup
mkdir -p $BACKUP_DIR

# Backup de base de datos
pg_dump -h localhost -U arca_user arca_construccion > $BACKUP_DIR/db_backup_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz -C $PROJECT_DIR media/

# Backup de código
tar -czf $BACKUP_DIR/code_backup_$DATE.tar.gz -C $PROJECT_DIR . --exclude=venv --exclude=*.pyc

# Limpiar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: $DATE"
```

**Hacer ejecutable y programar:**
```bash
chmod +x /opt/backup_script.sh

# Agregar a crontab (backup diario a las 2 AM)
sudo crontab -e
0 2 * * * /opt/backup_script.sh
```

---

## **✅ VERIFICACIÓN FINAL**

### **9.1 Checklist de Verificación**
- [ ] **Sitio web accesible** en `https://tu-dominio.com`
- [ ] **SSL funcionando** correctamente
- [ ] **Base de datos** conectando y funcionando
- [ ] **Archivos estáticos** cargando correctamente
- [ ] **Logs** funcionando sin errores críticos
- [ ] **Servicio** iniciando automáticamente
- [ ] **Backups** programados y funcionando
- [ ] **Monitoreo** configurado

### **9.2 Comandos de Verificación**
```bash
# Verificar estado general
sudo systemctl status arca-construccion nginx postgresql redis-server

# Verificar conectividad
curl -I https://tu-dominio.com

# Verificar logs
sudo journalctl -u arca-construccion --no-pager -n 50

# Verificar base de datos
sudo -u postgres psql -d arca_construccion -c "SELECT version();"
```

---

## **🚨 SOLUCIÓN DE PROBLEMAS COMUNES**

### **Problema: Error 502 Bad Gateway**
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status arca-construccion

# Verificar logs
sudo journalctl -u arca-construccion -f
```

### **Problema: Error de Base de Datos**
```bash
# Verificar conexión
sudo -u postgres psql -d arca_construccion

# Verificar logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### **Problema: Archivos Estáticos No Cargando**
```bash
# Verificar permisos
sudo chown -R www-data:www-data /opt/sistema-construccion-django/staticfiles

# Recolectar estáticos
cd /opt/sistema-construccion-django
source venv/bin/activate
python manage.py collectstatic --noinput
```

---

## **🎉 ¡DESPLIEGUE COMPLETADO!**

Tu sistema ARCA Construcción está ahora funcionando en producción con:
- ✅ **Seguridad avanzada** (HTTPS, headers de seguridad)
- ✅ **Base de datos robusta** (PostgreSQL)
- ✅ **Caché optimizado** (Redis)
- ✅ **Servidor web eficiente** (Nginx + Gunicorn)
- ✅ **Monitoreo y logs** configurados
- ✅ **Backups automáticos** programados
- ✅ **Actualizaciones** automatizadas

**¡El sistema está listo para uso en producción!** 🚀
