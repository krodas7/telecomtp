# 🚀 Guía de Despliegue para SmartASP

## 📋 Pasos para Desplegar en SmartASP

### 1. Preparación del Proyecto
- ✅ Dependencias instaladas
- ✅ Migraciones ejecutadas
- ✅ Archivos estáticos recolectados
- ✅ Superusuario creado
- ✅ Datos iniciales cargados

### 2. Subir a SmartASP
1. Comprimir el proyecto (excluir venv, __pycache__, .git)
2. Subir via FTP o Panel de Control
3. Extraer en la carpeta raíz del hosting

### 3. Configuración en SmartASP
1. Crear base de datos SQL Server
2. Configurar variables de entorno
3. Actualizar archivo .env con credenciales reales
4. Configurar dominio en Panel de Control

### 4. Verificación
1. Acceder a tu-dominio.com
2. Verificar que el dashboard funcione
3. Probar funcionalidades principales

### 5. Soporte
- Documentación: README.md
- Logs: carpeta logs/
- Backup: carpeta backups/

## 🔧 Configuración de Base de Datos
- Motor: SQL Server
- Puerto: 1433
- Driver: ODBC Driver 17 for SQL Server

## 📧 Configuración de Email
- Host: smtp.hostinger.com
- Puerto: 587
- TLS: Habilitado

## 🌐 Dominio
- Configurar en Panel de Control de Hostinger
- Apuntar a la carpeta del proyecto en SmartASP
