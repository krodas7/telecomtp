# 🚀 Guía de Despliegue para Producción - Sistema de Construcción

## 📋 Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Preparación del Servidor](#preparación-del-servidor)
3. [Instalación de Dependencias](#instalación-de-dependencias)
4. [Configuración del Proyecto](#configuración-del-proyecto)
5. [Despliegue Automático](#despliegue-automático)
6. [Configuración Manual](#configuración-manual)
7. [Verificación del Despliegue](#verificación-del-despliegue)
8. [Mantenimiento](#mantenimiento)
9. [Solución de Problemas](#solución-de-problemas)
10. [Seguridad](#seguridad)

## 🖥️ Requisitos del Sistema

### Requisitos Mínimos
- **Sistema Operativo**: Ubuntu 20.04 LTS o superior
- **RAM**: 2 GB mínimo, 4 GB recomendado
- **Almacenamiento**: 20 GB mínimo, 50 GB recomendado
- **CPU**: 2 cores mínimo, 4 cores recomendado

### Requisitos de Software
- **Python**: 3.8 o superior
- **PostgreSQL**: 12 o superior (recomendado para producción)
- **Redis**: 6.0 o superior (opcional para caché)
- **Nginx**: 1.18 o superior
- **Supervisor**: 4.0 o superior

## 🛠️ Preparación del Servidor

### 1. Actualizar el Sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt autoremove -y
```

### 2. Instalar Paquetes Básicos
```bash
sudo apt install -y \
    curl \
    wget \
    git \
    unzip \
    htop \
    vim \
    nano \
    ufw \
    fail2ban \
    logrotate \
    cron \
    rsyslog
```

### 3. Configurar Zona Horaria
```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
```

### 4. Crear Usuario del Sistema
```bash
sudo adduser --system --group --home /var/www/sistema_construccion www-data
sudo usermod -aG sudo www-data
```

## 📦 Instalación de Dependencias

### 1. Instalar Python y pip
```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y build-essential libssl-dev libffi-dev
```

### 2. Instalar PostgreSQL
```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos y usuario
sudo -u postgres psql -c "CREATE DATABASE sistema_construccion_prod;"
sudo -u postgres psql -c "CREATE USER sistema_user WITH PASSWORD 'tu_password_seguro';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE sistema_construccion_prod TO sistema_user;"
sudo -u postgres psql -c "ALTER USER sistema_user CREATEDB;"
```

### 3. Instalar Redis (Opcional)
```bash
sudo apt install -y redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 4. Instalar Nginx
```bash
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 5. Instalar Supervisor
```bash
sudo apt install -y supervisor
sudo systemctl start supervisor
sudo systemctl enable supervisor
```

### 6. Instalar Certbot (SSL)
```bash
sudo apt install -y certbot python3-certbot-nginx
```

## ⚙️ Configuración del Proyecto

### 1. Clonar el Proyecto
```bash
cd /var/www
sudo git clone https://github.com/tu-usuario/sistema-construccion-django.git sistema_construccion
sudo chown -R www-data:www-data sistema_construccion
```

### 2. Crear Entorno Virtual
```bash
cd sistema_construccion
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install --upgrade pip
sudo -u www-data venv/bin/pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno
```bash
sudo -u www-data cp env_example.txt .env
sudo -u www-data nano .env
```

**Configuración mínima del .env:**
```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=tu_clave_secreta_muy_larga_y_compleja
DATABASE_URL=postgresql://sistema_user:tu_password_seguro@localhost/sistema_construccion_prod
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
```

### 4. Aplicar Migraciones
```bash
sudo -u www-data venv/bin/python manage.py migrate --settings=sistema_construccion.production_settings
```

### 5. Crear Superusuario
```bash
sudo -u www-data venv/bin/python manage.py createsuperuser --settings=sistema_construccion.production_settings
```

### 6. Recolectar Archivos Estáticos
```bash
sudo -u www-data venv/bin/python manage.py collectstatic --settings=sistema_construccion.production_settings --noinput
```

## 🚀 Despliegue Automático

### 1. Ejecutar Script de Despliegue
```bash
cd /var/www/sistema_construccion/deploy
sudo chmod +x deploy_production.sh
sudo ./deploy_production.sh
```

### 2. El Script Automatiza:
- ✅ Verificación de dependencias
- ✅ Creación de directorios
- ✅ Configuración de permisos
- ✅ Configuración de Nginx
- ✅ Configuración de Supervisor
- ✅ Configuración de SSL (opcional)
- ✅ Configuración de firewall
- ✅ Configuración de respaldos automáticos
- ✅ Configuración de monitoreo
- ✅ Verificación del despliegue

## 🔧 Configuración Manual

### 1. Configurar Nginx
```bash
sudo cp /var/www/sistema_construccion/nginx/sistema_construccion.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/sistema_construccion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2. Configurar Supervisor
```bash
sudo cp /var/www/sistema_construccion/supervisor/sistema_construccion.conf /etc/supervisor/conf.d/
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start sistema_construccion_group:*
```

### 3. Configurar SSL con Let's Encrypt
```bash
sudo certbot --nginx -d tu-dominio.com
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## ✅ Verificación del Despliegue

### 1. Verificar Servicios
```bash
# Verificar Nginx
sudo systemctl status nginx

# Verificar Supervisor
sudo systemctl status supervisor

# Verificar PostgreSQL
sudo systemctl status postgresql

# Verificar Redis (si está instalado)
sudo systemctl status redis-server
```

### 2. Verificar Aplicación
```bash
# Verificar endpoint de salud
curl http://localhost/health/

# Verificar logs
sudo tail -f /var/log/supervisor/sistema_construccion_stdout.log
sudo tail -f /var/www/sistema_construccion/logs/django/django.log
```

### 3. Verificar Archivos Estáticos
```bash
# Verificar que los archivos estáticos estén disponibles
ls -la /var/www/sistema_construccion/staticfiles/
curl http://localhost/static/admin/css/base.css
```

## 🔄 Mantenimiento

### 1. Respaldos Automáticos
Los respaldos se ejecutan automáticamente cada 6 horas:
```bash
# Ver respaldos
ls -la /var/www/sistema_construccion/backups/auto/

# Crear respaldo manual
sudo -u www-data /var/www/sistema_construccion/backup_script.sh
```

### 2. Monitoreo del Sistema
El monitoreo se ejecuta cada 15 minutos:
```bash
# Ver script de monitoreo
cat /var/www/sistema_construccion/monitor_script.sh

# Ejecutar monitoreo manual
sudo -u www-data /var/www/sistema_construccion/monitor_script.sh
```

### 3. Actualizaciones
```bash
# Actualizar código
cd /var/www/sistema_construccion
sudo -u www-data git pull origin main

# Instalar nuevas dependencias
sudo -u www-data venv/bin/pip install -r requirements.txt

# Aplicar migraciones
sudo -u www-data venv/bin/python manage.py migrate --settings=sistema_construccion.production_settings

# Recolectar archivos estáticos
sudo -u www-data venv/bin/python manage.py collectstatic --settings=sistema_construccion.production_settings --noinput

# Reiniciar aplicación
sudo supervisorctl restart sistema_construccion
```

### 4. Logs del Sistema
```bash
# Logs de Django
sudo tail -f /var/www/sistema_construccion/logs/django/django.log

# Logs de Gunicorn
sudo tail -f /var/www/sistema_construccion/logs/gunicorn/gunicorn_error.log

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log

# Logs de Supervisor
sudo tail -f /var/log/supervisor/sistema_construccion_stdout.log
```

## 🚨 Solución de Problemas

### 1. Problemas Comunes

#### La aplicación no responde
```bash
# Verificar estado de Supervisor
sudo supervisorctl status

# Verificar logs de Gunicorn
sudo tail -f /var/www/sistema_construccion/logs/gunicorn/gunicorn_error.log

# Reiniciar aplicación
sudo supervisorctl restart sistema_construccion
```

#### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté funcionando
sudo supervisorctl status sistema_construccion

# Verificar puerto 8000
sudo netstat -tlnp | grep :8000

# Verificar logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

#### Problemas de permisos
```bash
# Corregir permisos
sudo chown -R www-data:www-data /var/www/sistema_construccion
sudo chmod -R 755 /var/www/sistema_construccion
sudo chmod -R 750 /var/www/sistema_construccion/logs
sudo chmod -R 750 /var/www/sistema_construccion/backups
```

### 2. Comandos de Diagnóstico
```bash
# Verificar estado de todos los servicios
sudo systemctl status nginx postgresql supervisor

# Verificar uso de recursos
htop
df -h
free -h

# Verificar conexiones de red
sudo netstat -tlnp
sudo ss -tlnp

# Verificar logs del sistema
sudo journalctl -u nginx -f
sudo journalctl -u supervisor -f
```

## 🔒 Seguridad

### 1. Firewall
```bash
# Verificar estado del firewall
sudo ufw status

# Configurar reglas adicionales si es necesario
sudo ufw allow from tu_ip_administrativa to any port 22
sudo ufw deny 22  # Bloquear SSH para todos excepto tu IP
```

### 2. Fail2ban
```bash
# Verificar estado de Fail2ban
sudo systemctl status fail2ban

# Ver logs de Fail2ban
sudo tail -f /var/log/fail2ban.log
```

### 3. Auditoría de Seguridad
```bash
# Verificar logs de seguridad
sudo tail -f /var/www/sistema_construccion/logs/django/django.log | grep -i "security\|auth\|login"

# Verificar intentos de acceso fallidos
sudo grep "Failed password" /var/log/auth.log
```

## 📊 Monitoreo y Métricas

### 1. Métricas del Sistema
- **CPU**: Monitoreado cada 15 minutos
- **Memoria**: Monitoreado cada 15 minutos
- **Disco**: Monitoreado cada 15 minutos
- **Logs de Error**: Monitoreado cada 15 minutos

### 2. Alertas Automáticas
- **Email**: Enviado cuando se superan los umbrales
- **Logs**: Registrados en `/var/www/sistema_construccion/logs/`
- **Supervisor**: Monitoreo automático de procesos

### 3. Dashboard de Monitoreo
Acceder a `/health/` para ver el estado del sistema:
```bash
curl http://localhost/health/
curl http://localhost/health/database/
```

## 🔧 Comandos Útiles

### Gestión de la Aplicación
```bash
# Reiniciar aplicación
sudo supervisorctl restart sistema_construccion

# Ver estado de todos los procesos
sudo supervisorctl status

# Ver logs en tiempo real
sudo supervisorctl tail sistema_construccion

# Parar aplicación
sudo supervisorctl stop sistema_construccion

# Iniciar aplicación
sudo supervisorctl start sistema_construccion
```

### Gestión de Nginx
```bash
# Verificar configuración
sudo nginx -t

# Recargar configuración
sudo nginx -s reload

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver logs en tiempo real
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Gestión de Base de Datos
```bash
# Conectar a PostgreSQL
sudo -u postgres psql -d sistema_construccion_prod

# Crear respaldo
sudo -u postgres pg_dump sistema_construccion_prod > backup.sql

# Restaurar respaldo
sudo -u postgres psql -d sistema_construccion_prod < backup.sql
```

## 📞 Soporte

### Información de Contacto
- **Email**: soporte@tu-empresa.com
- **Documentación**: [URL de la documentación]
- **Issues**: [URL del repositorio de issues]

### Información del Sistema
- **Versión**: 1.0.0
- **Última Actualización**: $(date)
- **Soporte**: Django 5.2+, Python 3.8+

---

## 🎯 Próximos Pasos

1. **Configurar dominio personalizado**
2. **Configurar certificado SSL**
3. **Configurar respaldos externos**
4. **Configurar monitoreo avanzado**
5. **Configurar CI/CD**
6. **Configurar balanceo de carga**

---

**¡El sistema está listo para producción! 🚀**

Para cualquier consulta o problema, revisa los logs y utiliza los comandos de diagnóstico proporcionados en esta guía.



