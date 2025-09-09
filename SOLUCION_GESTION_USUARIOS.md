# 🔧 Solución para Gestión de Usuarios en Servidor Desplegado

## 📋 Problema Identificado

La gestión de usuarios, roles y permisos funciona correctamente en el entorno local pero no en el servidor desplegado. Esto suele ocurrir por:

1. **Migraciones no aplicadas** en el servidor
2. **Datos faltantes** (roles, permisos, superusuarios)
3. **Diferencias en la base de datos** entre local y servidor
4. **Permisos de superusuario** no configurados

## 🚀 Solución Paso a Paso

### **Opción 1: Solución Rápida (Recomendada)**

**En el servidor, ejecuta:**

```bash
python solucion_servidor.py
```

Este script:
- ✅ Crea módulos básicos necesarios
- ✅ Crea roles y permisos
- ✅ Verifica/crea superusuario
- ✅ Configura todo automáticamente

### **Opción 2: Solución Completa (Con Datos del Local)**

**Paso 1: Diagnóstico Local**

```bash
python diagnostico_usuarios.py
python sincronizar_usuarios.py
```

**Paso 2: Transferir al Servidor**

1. **Copia los archivos al servidor:**
   - `datos_usuarios_export.json`
   - `verificar_migraciones.py`
   - `importar_usuarios.py`

2. **Conecta al servidor** (SSH, panel de control, etc.)

**Paso 3: Verificar Migraciones en el Servidor**

```bash
# En el servidor
python verificar_migraciones.py
```

**Paso 4: Importar Datos en el Servidor**

```bash
# En el servidor
python importar_usuarios.py
```

### **Paso 5: Verificación Final**

1. **Accede al panel de administración** en el servidor
2. **Verifica que puedas:**
   - Ver la lista de usuarios
   - Crear nuevos usuarios
   - Gestionar roles
   - Asignar permisos

## 🔍 Diagnóstico Avanzado

Si el problema persiste, ejecuta:

```bash
python diagnostico_usuarios.py
```

Y revisa:
- ✅ Número de superusuarios
- ✅ Estado de las migraciones
- ✅ Tablas en la base de datos
- ✅ Asignaciones de permisos

## 🛠️ Soluciones Alternativas

### **Opción 1: Crear Superusuario Manualmente**

```bash
# En el servidor
python manage.py createsuperuser
```

### **Opción 2: Aplicar Migraciones Manualmente**

```bash
# En el servidor
python manage.py migrate core
python manage.py migrate
```

### **Opción 3: Resetear Base de Datos (⚠️ CUIDADO)**

```bash
# SOLO si no hay datos importantes
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

## 📊 Estructura de Datos

Los scripts manejan:

- **Usuarios**: Información básica (sin contraseñas)
- **Roles**: Administrador, Gerente, Supervisor, etc.
- **Permisos**: ver, crear, editar, eliminar por módulo
- **Asignaciones**: Qué permisos tiene cada rol
- **Perfiles**: Información adicional de usuarios

## ⚠️ Consideraciones Importantes

1. **Contraseñas**: Los usuarios importados NO tendrán contraseñas
2. **Superusuarios**: Se crean automáticamente si no existen
3. **Migraciones**: Siempre aplicar antes de importar datos
4. **Backup**: Hacer respaldo antes de cambios importantes

## 🎯 Resultado Esperado

Después de seguir estos pasos:

- ✅ Gestión de usuarios funcional en el servidor
- ✅ Roles y permisos sincronizados
- ✅ Superusuarios configurados
- ✅ Migraciones aplicadas correctamente

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs del servidor
2. Verifica permisos de archivos
3. Confirma que la base de datos esté accesible
4. Ejecuta el diagnóstico para más detalles

---

**¡La gestión de usuarios debería funcionar perfectamente en el servidor después de seguir estos pasos!** 🚀
