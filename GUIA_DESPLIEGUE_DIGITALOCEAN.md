# 🚀 Guía de Despliegue para DigitalOcean - Sistema ARCA Construcción

## 📋 Resumen de Archivos Disponibles

### 🆕 **Scripts de Actualización (Recomendados)**
- **`actualizar_digitalocean.sh`** - Actualización rápida del servidor existente
- **`desplegar_digitalocean_completo.sh`** - Despliegue completo desde cero
- **`sistema_construccion_deployment_20250905_171230.zip`** - Paquete con cambios más recientes

### 📦 **Paquete de Despliegue**
- **`sistema_construccion_deployment_20250905_171230.zip`** (8.4 MB)
  - Contiene el commit más reciente: `b143830`
  - Incluye todos los archivos necesarios para producción
  - Listo para subir al servidor

## 🎯 **Opciones de Despliegue**

### **Opción 1: Actualización Rápida (Si ya tienes el servidor configurado)**
```bash
# 1. Subir el archivo ZIP al servidor
scp sistema_construccion_deployment_20250905_171230.zip root@tu-servidor:/tmp/

# 2. Conectar al servidor
ssh root@tu-servidor

# 3. Extraer el ZIP en el directorio del proyecto
cd /var/www/sistema-arca
unzip /tmp/sistema_construccion_deployment_20250905_171230.zip

# 4. Ejecutar la actualización
chmod +x actualizar_digitalocean.sh
./actualizar_digitalocean.sh
```

### **Opción 2: Despliegue Completo (Servidor nuevo)**
```bash
# 1. Conectar al servidor
ssh root@tu-servidor

# 2. Subir el script de despliegue
scp desplegar_digitalocean_completo.sh root@tu-servidor:/tmp/

# 3. Ejecutar el despliegue completo
chmod +x /tmp/desplegar_digitalocean_completo.sh
/tmp/desplegar_digitalocean_completo.sh
```

## 🔧 **Configuración del Servidor**

### **Requisitos Mínimos**
- **Sistema**: Ubuntu 22.04 LTS
- **RAM**: 2 GB mínimo, 4 GB recomendado
- **Almacenamiento**: 20 GB mínimo
- **CPU**: 2 cores mínimo

### **Servicios Incluidos**
- ✅ **Python 3.8+** con entorno virtual
- ✅ **PostgreSQL** para base de datos
- ✅ **Redis** para caché
- ✅ **Nginx** como servidor web
- ✅ **Gunicorn** como servidor WSGI
- ✅ **Supervisor** para gestión de procesos
- ✅ **SSL** con Let's Encrypt
- ✅ **Firewall** configurado
- ✅ **Backups** automáticos

## 🌐 **Configuración de Dominio**

### **1. Configurar DNS en Hostinger**
```
Tipo: A
Nombre: @
Valor: IP_DEL_SERVIDOR

Tipo: A  
Nombre: www
Valor: IP_DEL_SERVIDOR
```

### **2. Obtener IP del servidor**
```bash
curl -s ifconfig.me
```

### **3. Configurar SSL (después de DNS)**
```bash
sudo certbot --nginx -d construccionesarca.net -d www.construccionesarca.net
```

## 🔑 **Credenciales por Defecto**

### **Aplicación**
- **Usuario**: admin
- **Contraseña**: Admin2025!
- **Email**: admin@arca.com

### **Base de Datos**
- **Usuario**: arca_user
- **Contraseña**: ARCA_2025_Super_Secure_Password_Change_This
- **Base de datos**: arca_construccion

⚠️ **IMPORTANTE**: Cambiar todas las contraseñas después del despliegue

## 📱 **Acceso a la Aplicación**

### **URLs**
- **Local**: http://localhost
- **Producción**: https://construccionesarca.net
- **Admin**: https://construccionesarca.net/admin

### **Funcionalidades**
- ✅ Dashboard principal
- ✅ Gestión de proyectos
- ✅ Control de gastos
- ✅ Inventario
- ✅ Colaboradores
- ✅ PWA (Progressive Web App)
- ✅ Modo offline

## 🔧 **Comandos de Mantenimiento**

### **Gestión de Servicios**
```bash
# Ver estado de la aplicación
sudo systemctl status sistema-arca

# Reiniciar aplicación
sudo systemctl restart sistema-arca

# Ver logs en tiempo real
sudo journalctl -u sistema-arca -f

# Ver logs de Gunicorn
tail -f /var/www/sistema-arca/logs/gunicorn_error.log
```

### **Gestión de Nginx**
```bash
# Verificar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

### **Gestión de Base de Datos**
```bash
# Conectar a PostgreSQL
sudo -u postgres psql -d arca_construccion

# Crear respaldo manual
sudo -u arca /var/www/sistema-arca/backup.sh

# Ver respaldos
ls -la /var/www/sistema-arca/backups/
```

## 🔄 **Actualizaciones Futuras**

### **Actualización Rápida**
```bash
# 1. Conectar al servidor
ssh root@tu-servidor

# 2. Ir al directorio del proyecto
cd /var/www/sistema-arca

# 3. Actualizar desde Git
sudo -u arca git pull origin main

# 4. Ejecutar actualización
./actualizar_digitalocean.sh
```

### **Verificar Actualización**
```bash
# Ver último commit
sudo -u arca git log -1 --oneline

# Verificar estado de servicios
sudo systemctl status sistema-arca nginx postgresql redis-server

# Verificar aplicación
curl -s http://localhost/health/
```

## 🚨 **Solución de Problemas**

### **Problemas Comunes**

#### **1. Aplicación no responde**
```bash
# Verificar estado
sudo systemctl status sistema-arca

# Ver logs
sudo journalctl -u sistema-arca -f

# Reiniciar
sudo systemctl restart sistema-arca
```

#### **2. Error 502 Bad Gateway**
```bash
# Verificar que Gunicorn esté funcionando
sudo systemctl status sistema-arca

# Verificar puerto 8000
sudo netstat -tlnp | grep :8000

# Verificar logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

#### **3. Problemas de permisos**
```bash
# Corregir permisos
sudo chown -R arca:arca /var/www/sistema-arca
sudo chmod -R 755 /var/www/sistema-arca
```

#### **4. Problemas de base de datos**
```bash
# Verificar estado de PostgreSQL
sudo systemctl status postgresql

# Verificar conexión
sudo -u postgres psql -d arca_construccion -c "SELECT 1;"
```

## 📊 **Monitoreo**

### **Métricas del Sistema**
```bash
# Uso de CPU y memoria
htop

# Uso de disco
df -h

# Espacio en base de datos
sudo -u postgres psql -d arca_construccion -c "SELECT pg_size_pretty(pg_database_size('arca_construccion'));"
```

### **Logs Importantes**
- **Aplicación**: `/var/www/sistema-arca/logs/gunicorn_error.log`
- **Nginx**: `/var/log/nginx/error.log`
- **Sistema**: `sudo journalctl -u sistema-arca -f`

## 🔒 **Seguridad**

### **Configuraciones Aplicadas**
- ✅ Firewall configurado (UFW)
- ✅ Fail2ban para protección SSH
- ✅ SSL/TLS con Let's Encrypt
- ✅ Headers de seguridad en Nginx
- ✅ Usuario no-root para la aplicación
- ✅ Permisos restrictivos

### **Recomendaciones Adicionales**
1. Cambiar contraseñas por defecto
2. Configurar backup externo
3. Monitorear logs regularmente
4. Mantener sistema actualizado
5. Configurar alertas de seguridad

## 📞 **Soporte**

### **Información del Sistema**
- **Versión**: 1.0.0
- **Última actualización**: 2025-09-05
- **Commit**: b143830
- **Soporte**: Django 5.2+, Python 3.8+

### **Archivos de Configuración**
- **Django**: `/var/www/sistema-arca/sistema_construccion/production_settings.py`
- **Nginx**: `/etc/nginx/sites-available/sistema-arca`
- **Gunicorn**: `/var/www/sistema-arca/gunicorn.conf.py`
- **Systemd**: `/etc/systemd/system/sistema-arca.service`

---

## 🎯 **Resumen de Pasos**

1. **Crear servidor DigitalOcean** (Ubuntu 22.04 LTS)
2. **Configurar DNS** en Hostinger
3. **Subir archivos** al servidor
4. **Ejecutar script** de despliegue
5. **Configurar SSL** con Let's Encrypt
6. **Verificar funcionamiento**
7. **Cambiar contraseñas** por defecto

**¡Tu Sistema ARCA Construcción estará listo para producción! 🚀**



