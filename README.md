# 🏗️ Sistema ARCA Construcción

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
- Python 3.9+
- PostgreSQL 12+
- Redis 6+

### Desarrollo Local
```bash
# Clonar repositorio
git clone https://github.com/krodas7/arca-sistema.git
cd arca-sistema

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements_production_simple.txt

# Configurar base de datos
python manage.py migrate
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

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
arca-sistema/
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
```bash
# Copiar archivo de ejemplo
cp production.env .env

# Configurar variables
DEBUG=False
SECRET_KEY=tu-clave-secreta
DB_NAME=arca_construccion
DB_USER=arca_user
DB_PASSWORD=tu-password
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
- 🐛 Issues: [GitHub Issues](https://github.com/krodas7/arca-sistema/issues)

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐