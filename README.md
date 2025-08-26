#  Sistema ARCA Construcción

Sistema integral de gestión para empresas de construcción con capacidades PWA (Progressive Web App) y acceso móvil.

##  Características Principales

###  Funcionalidades Core
- **Gestión de Proyectos** - Planificación, seguimiento y control de obras
- **Gestión de Clientes** - Base de datos completa de clientes
- **Facturación** - Sistema de facturas con estados y pagos
- **Gestión de Colaboradores** - Control de personal y anticipos
- **Inventario** - Control de materiales y herramientas
- **Presupuestos** - Elaboración y seguimiento de presupuestos

###  Características Móviles
- **PWA Completa** - Instalable como aplicación nativa
- **Responsive Design** - Optimizado para todos los dispositivos
- **Funcionamiento Offline** - Cache de datos importantes
- **Notificaciones Push** - Alertas en tiempo real

###  Seguridad
- **Atenticación de Usuarios** - Sistema de login seguro
- **Control de Permisos** - Roles y accesos diferenciados
- **Logs de Actividad** - Auditoría completa del sistema
- **Tokens CSRF** - Protección contra ataques

##  Tecnologías Utilizadas

- **Backend:** Django 5.2.5 (Python)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Framework CSS:** Bootstrap 5.3.0
- **Iconos:** Font Awesome 6.4.0
- **PWA:** Service Worker, Manifest, Cache API

## Requisitos del Sistema

### Desarrollo
- Python 3.11+
- Django 5.2.5
- SQLite3
- Navegador moderno con soporte PWA

### Producción
- Ubuntu 22.04 LTS
- PostgreSQL 15+
- Nginx
- Gunicorn
- SSL/HTTPS

##  Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd sistema-construccion-django
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

##  Acceso al Sistema

- **URL:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Dashboard:** http://localhost:8000/dashboard

##  Uso como PWA

### Instalación en Móvil
1. Abrir el sistema en Chrome/Safari
2. Aparecerá banner "Instalar App"
3. Seleccionar "Instalar"
4. La app aparecerá en la pantalla de inicio

### Funcionalidades PWA
- Instalación como app nativa
- Funcionamiento offline
-  Sincronización automática
-  Notificaciones push

##  Configuración de Producción

### Variables de Entorno
```bash
DEBUG=False
SECRET_KEY=tu-clave-secreta
DATABASE_URL=postgresql://user:pass@host:port/db
ALLOWED_HOSTS=tu-dominio.com
```

### Servidor Web
- **Nginx** como proxy reverso
- **Gunicorn** como servidor WSGI
- **SSL** con Let's Encrypt

##  Estructura del Proyecto

```
sistema-construccion-django/
├── core/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica
│   ├── urls.py             # URLs de la aplicación
│   └── admin.py            # Panel de administración
├── sistema_construccion/   # Configuración del proyecto
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs del proyecto
│   └── wsgi.py             # Configuración WSGI
├── templates/              # Plantillas HTML
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos
├── requirements.txt        # Dependencias Python
└── manage.py              # Script de gestión Django
```

## Despliegue

### DigitalOcean 
- **Droplet:** Ubuntu 22.04 LTS
- **RAM:** 2GB mínimo
- **Storage:** 50GB SSD
- **Costo:** $12 USD/mes


##  Control de Versiones

### Git Workflow
```bash
# Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commit
git add .
git commit -m "Agregar nueva funcionalidad"

# Push y merge
git push origin feature/nueva-funcionalidad
git checkout main
git merge feature/nueva-funcionalidad
```

### Tags de Versión
```bash
git tag -a v1.0.0 -m "Versión 1.0.0 estable"
git push origin v1.0.0
```

##  Solución de Problemas

### Problemas Comunes
1. **Error CSRF:** Verificar token en plantillas
2. **Error de permisos:** Verificar decoradores @login_required
3. **Error de base de datos:** Ejecutar migraciones
4. **PWA no funciona:** Verificar HTTPS en producción

### Logs
- **Django:** `logs/django.log`
- **Backup:** `logs/backup.log`
- **Sistema:** `/var/log/` (producción)

##  Soporte

### Documentación
- **README:** Este archivo
- **Comentarios:** En el código fuente
- **Tests:** Archivos de prueba incluidos

### Contacto
- **Desarrollador:** Kevin
- **Proyecto:** Sistema ARCA Construcción
- **Versión:** 1.0.0

##  Licencia

Este proyecto es de uso interno para ARCA Construcción.

##  Roadmap

### Versión 1.1
- [ ] Reportes avanzados
- [ ] Integración con WhatsApp
- [ ] App móvil nativa

### Versión 1.2
- [ ] Módulo de contabilidad
- [ ] Integración bancaria
- [ ] Dashboard ejecutivo

---


