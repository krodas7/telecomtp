# 🌐 CONFIGURACIÓN DE DOMINIO HOSTINGER PARA DIGITALOCEAN

## **Sistema ARCA Construcción - Configuración DNS**

---

## **📋 INFORMACIÓN NECESARIA:**

### **1. Tu Dominio en Hostinger:**
- **Dominio:** [TU-DOMINIO.com]
- **Panel de Control:** https://hpanel.hostinger.com

### **2. Servidor DigitalOcean:**
- **IP del Servidor:** [IP-DE-TU-DROPLET]
- **Ubicación:** [Región del Droplet]

---

## **🔧 PASO 1: CONFIGURAR DNS EN HOSTINGER**

### **1.1 Acceder al Panel de Hostinger:**
1. Ve a: https://hpanel.hostinger.com
2. Inicia sesión con tu cuenta
3. Selecciona tu dominio

### **1.2 Configurar Registros DNS:**
En la sección **"DNS / Nameservers"**, agrega estos registros:

#### **Registro A (Principal):**
```
Tipo: A
Nombre: @
Valor: [IP-DE-TU-DROPLET-DIGITALOCEAN]
TTL: 300
```

#### **Registro A (www):**
```
Tipo: A
Nombre: www
Valor: [IP-DE-TU-DROPLET-DIGITALOCEAN]
TTL: 300
```

#### **Registro CNAME (opcional):**
```
Tipo: CNAME
Nombre: *
Valor: [TU-DOMINIO.com]
TTL: 300
```

---

## **🔒 PASO 2: CONFIGURAR SSL/HTTPS**

### **2.1 En DigitalOcean (Let's Encrypt):**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d [TU-DOMINIO.com] -d www.[TU-DOMINIO.com]
```

### **2.2 Verificar Renovación Automática:**
```bash
# Probar renovación
sudo certbot renew --dry-run

# Agregar a crontab
sudo crontab -e
# Agregar esta línea:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## **⚙️ PASO 3: CONFIGURAR NGINX**

### **3.1 Archivo de Configuración:**
```nginx
server {
    listen 80;
    server_name [TU-DOMINIO.com] www.[TU-DOMINIO.com];
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name [TU-DOMINIO.com] www.[TU-DOMINIO.com];

    ssl_certificate /etc/letsencrypt/live/[TU-DOMINIO.com]/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/[TU-DOMINIO.com]/privkey.pem;

    # Configuración SSL moderna
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Archivos estáticos
    location /static/ {
        alias /var/www/sistema-arca/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Archivos media
    location /media/ {
        alias /var/www/sistema-arca/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy a Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## **🚀 PASO 4: VERIFICAR CONFIGURACIÓN**

### **4.1 Verificar DNS:**
```bash
# Verificar resolución DNS
nslookup [TU-DOMINIO.com]
dig [TU-DOMINIO.com]

# Verificar desde diferentes ubicaciones
# https://www.whatsmydns.net/
```

### **4.2 Verificar SSL:**
```bash
# Verificar certificado SSL
openssl s_client -connect [TU-DOMINIO.com]:443 -servername [TU-DOMINIO.com]

# Verificar en navegador
# https://[TU-DOMINIO.com]
```

### **4.3 Verificar Nginx:**
```bash
# Verificar sintaxis
sudo nginx -t

# Verificar estado
sudo systemctl status nginx

# Reiniciar si es necesario
sudo systemctl restart nginx
```

---

## **📱 PASO 5: CONFIGURACIÓN MÓVIL**

### **5.1 Verificar PWA:**
- Asegurar que `manifest.json` esté en `/static/`
- Verificar que `service-worker.js` funcione
- Probar instalación en dispositivos móviles

### **5.2 Optimizaciones Móviles:**
- Verificar responsive design
- Optimizar imágenes para móviles
- Verificar tiempos de carga

---

## **🔍 PASO 6: MONITOREO Y MANTENIMIENTO**

### **6.1 Logs del Sistema:**
```bash
# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs de Django
tail -f /var/www/sistema-arca/logs/django.log

# Logs del sistema
sudo journalctl -u sistema-arca -f
```

### **6.2 Monitoreo de Recursos:**
```bash
# Uso de CPU y memoria
htop

# Uso de disco
df -h

# Uso de red
iftop
```

---

## **⚠️ NOTAS IMPORTANTES:**

1. **Cambios DNS:** Pueden tardar hasta 48 horas en propagarse
2. **SSL:** Let's Encrypt renueva automáticamente cada 90 días
3. **Backups:** Configurar backups automáticos de la base de datos
4. **Monitoreo:** Configurar alertas para caídas del servicio
5. **Seguridad:** Mantener el sistema actualizado regularmente

---

## **📞 SOPORTE:**

- **Hostinger:** Soporte DNS y dominio
- **DigitalOcean:** Soporte del servidor
- **Documentación:** Esta guía y archivos del proyecto
