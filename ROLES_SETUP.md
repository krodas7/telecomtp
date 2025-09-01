# 🏷️ Sistema de Gestión de Roles - ARCA Construcción

## 📋 Descripción

El sistema de gestión de roles permite controlar el acceso de los usuarios a diferentes módulos y funcionalidades del sistema de construcción ARCA.

## 🚀 Configuración Inicial

### 1. Inicializar Roles Predefinidos

```bash
python manage.py inicializar_roles
```

Este comando crea:
- **5 roles predefinidos** con permisos específicos
- **10 módulos del sistema** con sus respectivos permisos
- **50 permisos básicos** (5 tipos × 10 módulos)
- **Asignación automática** de permisos a cada rol

### 2. Asignar Rol a Usuario

```bash
python manage.py asignar_rol_superusuario <username>
```

Ejemplo:
```bash
python manage.py asignar_rol_superusuario kevin
```

### 3. Verificar Usuarios y Roles

```bash
python manage.py listar_usuarios_roles
```

## 🏷️ Roles Predefinidos

### 👑 Superusuario
- **Acceso completo** a todo el sistema
- **Gestión de usuarios** y roles
- **Configuraciones del sistema**
- **Todos los permisos** habilitados

### 👨‍💼 Administrador
- **Permisos amplios** excepto gestión de usuarios
- **Gestión de proyectos**, clientes, facturas
- **Reportes completos**
- **No puede gestionar usuarios**

### 👷 Encargado de Proyecto
- **Gestión de proyectos** y clientes
- **Gestión de colaboradores**
- **Anticipos**
- **No puede eliminar registros**

### 👥 Colaborador
- **Acceso de solo lectura**
- **Ver proyectos asignados**
- **Reportes básicos**
- **Permisos limitados**

### 💰 Contador
- **Módulos financieros** completos
- **Facturas**, gastos, pagos
- **Reportes financieros**
- **Gestión de anticipos**

## 🔧 Gestión de Roles desde la Interfaz

### Acceso a Gestión de Roles
1. Ir a **Usuarios** en el menú principal
2. Hacer clic en **"Gestión de Roles"**
3. Solo usuarios con rol **Superusuario** pueden acceder

### Funcionalidades Disponibles

#### ✅ Crear Nuevo Rol
- Botón **"Crear Rol"** en la página de roles
- Formulario con nombre y descripción
- Validación de nombres únicos

#### ✏️ Editar Rol Existente
- Botón **"Editar"** en cada tarjeta de rol
- Modificar nombre y descripción
- Acceso directo a gestión de permisos

#### 🗑️ Eliminar Rol
- Botón **"Eliminar"** en cada tarjeta de rol
- **Validación de seguridad**: No se puede eliminar si tiene usuarios asignados
- **Confirmación** requerida

#### ⚙️ Gestionar Permisos
- Botón **"Permisos"** en cada tarjeta de rol
- **Interfaz visual** para asignar/desasignar permisos
- **Organización por módulos**
- **Guardado automático** de cambios

## 📊 Tipos de Permisos

### 🔍 Ver
- **Acceso de solo lectura**
- Ver listas y detalles
- No puede modificar datos

### ➕ Crear
- **Crear nuevos registros**
- Formularios de creación
- Validación de datos

### ✏️ Editar
- **Modificar registros existentes**
- Formularios de edición
- Actualización de datos

### 🗑️ Eliminar
- **Eliminar registros**
- Confirmación requerida
- Acción irreversible

### 📤 Exportar
- **Exportar datos** a PDF/Excel
- Generar reportes
- Descarga de archivos

## 🛡️ Seguridad

### Validaciones Implementadas
- ✅ **Nombres únicos** para roles
- ✅ **Verificación de usuarios** antes de eliminar
- ✅ **Permisos específicos** por módulo
- ✅ **Acceso restringido** solo a superusuarios
- ✅ **Confirmaciones** para acciones críticas

### Buenas Prácticas
1. **Principio de menor privilegio**: Solo permisos necesarios
2. **Nombres descriptivos**: "Supervisor de Obra" en lugar de "Rol 1"
3. **Documentación**: Describir responsabilidades claramente
4. **Revisión periódica**: Verificar permisos asignados
5. **Backup**: Respaldo antes de cambios importantes

## 🔄 Comandos de Mantenimiento

### Verificar Estado del Sistema
```bash
python manage.py check
```

### Listar Usuarios y Roles
```bash
python manage.py listar_usuarios_roles
```

### Asignar Rol Específico
```bash
python manage.py asignar_rol_superusuario <username>
```

### Reinicializar Roles (Cuidado)
```bash
python manage.py inicializar_roles
```

## 🆘 Solución de Problemas

### Error: "No tienes permisos para acceder a esta sección"
**Solución**: Asignar rol de Superusuario al usuario
```bash
python manage.py asignar_rol_superusuario <username>
```

### Error: "No hay roles configurados"
**Solución**: Ejecutar inicialización de roles
```bash
python manage.py inicializar_roles
```

### Error: "No se puede eliminar el rol"
**Solución**: Cambiar rol de usuarios asignados o eliminar usuarios

### Error: "Ya existe un rol con ese nombre"
**Solución**: Usar un nombre diferente para el nuevo rol

## 📞 Soporte

Para problemas técnicos o consultas sobre el sistema de roles:

1. **Verificar logs** del sistema
2. **Ejecutar comandos** de diagnóstico
3. **Revisar documentación** de Django
4. **Contactar al administrador** del sistema

---

**🎯 Objetivo**: Mantener un sistema de permisos robusto y fácil de gestionar para garantizar la seguridad y eficiencia del sistema ARCA Construcción.
