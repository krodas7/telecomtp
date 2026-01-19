# 🏗️ Sistema TelecomTP

Sistema integral de gestión para empresas de construcción desarrollado en Django.

## ✨ Características Principales

- 📊 **Dashboard Inteligente** - Análisis financiero y de rentabilidad
- 🏢 **Gestión de Proyectos** - Control completo del ciclo de vida
- 👥 **Gestión de Clientes** - Base de datos de clientes y contactos
- 💰 **Facturación** - Sistema completo de facturas y pagos
- 📈 **Presupuestos** - Creación y seguimiento de presupuestos
- 🧾 **Gastos** - Control de gastos por proyecto
- 💳 **Anticipos** - Gestión de anticipos de clientes
- 👷 **Colaboradores** - Gestión del equipo de trabajo
- 📁 **Archivos** - Gestión documental
- 📊 **Reportes** - Análisis detallados y exportación

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.9+ (requerido)
- PostgreSQL 12+ (opcional para desarrollo, requerido para producción)
- Redis 6+ (opcional para desarrollo, requerido para producción)

### Desarrollo Local

#### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/krodas7/telecomtp.git
cd telecomtp
```

#### Paso 2: Crear Entorno Virtual
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Paso 3: Instalar Dependencias
```bash
pip install -r requirements_production_simple.txt
```

#### Paso 4: Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp env_example.txt .env

# Editar .env con tus configuraciones (opcional para desarrollo básico)
# Para desarrollo local, puedes usar los valores por defecto con SQLite
```

#### Paso 5: Configurar Base de Datos
```bash
# El sistema usa SQLite por defecto para desarrollo (no requiere configuración adicional)
# Si prefieres usar PostgreSQL, configura las variables DB_* en el archivo .env

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

#### Paso 6: Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

El sistema estará disponible en: `http://localhost:8000`

#### Notas para Desarrollo Local
- **SQLite**: Por defecto, el sistema usa SQLite para desarrollo local. No requiere configuración adicional.
- **PostgreSQL**: Si prefieres usar PostgreSQL, edita el archivo `.env` y configura las variables `DB_*`.
- **Redis**: Opcional para desarrollo. El sistema usa caché en memoria por defecto.

### Producción
```bash
# Usar script de despliegue
chmod +x deploy_digitalocean_final.sh
./deploy_digitalocean_final.sh
```

## 🛠️ Tecnologías

- **Backend**: Django 5.2.5
- **Base de Datos**: PostgreSQL
- **Cache**: Redis
- **Frontend**: Bootstrap 5, Chart.js
- **Servidor**: Gunicorn + Nginx

## 📁 Estructura del Proyecto

```
telecomtp/
├── core/                    # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas y lógica de negocio
│   ├── forms.py            # Formularios
│   └── templates/          # Plantillas HTML
├── static/                 # Archivos estáticos
├── media/                  # Archivos de usuario
├── requirements_production_simple.txt  # Dependencias
└── deploy_digitalocean_final.sh       # Script de despliegue
```

## 🔧 Configuración

### Variables de Entorno

El sistema usa variables de entorno para configuración. Para desarrollo local:

```bash
# Copiar archivo de ejemplo
cp env_example.txt .env

# Editar .env según tus necesidades
# Para desarrollo básico, los valores por defecto funcionan con SQLite
```

#### Variables Importantes

- `DEBUG`: `True` para desarrollo, `False` para producción
- `SECRET_KEY`: Clave secreta de Django (genera una nueva para cada entorno)
- `DB_ENGINE`: Motor de base de datos (`django.db.backends.sqlite3` o `django.db.backends.postgresql`)
- `DB_NAME`: Nombre de la base de datos
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Credenciales de PostgreSQL (solo si usas PostgreSQL)

#### Generar SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📊 Módulos del Sistema

### 🏠 Dashboard
- Resumen financiero general
- Gráficos de ingresos vs gastos
- Proyectos más rentables
- Estadísticas en tiempo real

### 🏢 Proyectos
- Creación y gestión de proyectos
- Seguimiento de progreso
- Dashboard específico por proyecto
- Control de fondos disponibles

### 💰 Facturación
- Emisión de facturas
- Control de pagos
- Estados de facturación
- Reportes detallados

### 📈 Presupuestos
- Creación de presupuestos
- Partidas detalladas
- Aprobación de presupuestos
- Seguimiento de costos

### 🧾 Gastos
- Registro de gastos
- Categorización automática
- Aprobación de gastos
- Control por proyecto

### 💳 Anticipos
- Gestión de anticipos de clientes
- Aplicación a facturas o proyectos
- Control de liquidación
- Seguimiento de disponibilidad

## 🔒 Seguridad

- ✅ Autenticación de usuarios
- ✅ Control de roles y permisos
- ✅ Validación de formularios
- ✅ Protección CSRF
- ✅ Sanitización de datos
- ✅ Logs de auditoría

## 🚀 Despliegue

### DigitalOcean + Hostinger
```bash
# Ejecutar script de despliegue
./deploy_digitalocean_final.sh
```

### Variables de Producción
- Dominio: `construccionesarca.net`
- Base de datos: PostgreSQL
- Cache: Redis
- Servidor web: Nginx
- SSL: Let's Encrypt

## 📈 Monitoreo

- Logs de aplicación
- Métricas de rendimiento
- Alertas de seguridad
- Backup automático

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Kevin Sierra** - [@krodas7](https://github.com/krodas7)

## 📞 Soporte

Para soporte técnico o consultas:
- 📧 Email: kevinsierra45@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/krodas7/telecomtp/issues)

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐