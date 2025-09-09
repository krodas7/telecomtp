#!/usr/bin/env python
"""
Script para sincronizar datos de usuarios, roles y permisos
"""
import os
import sys
import django
import json
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Rol, Permiso, RolPermiso, PerfilUsuario, Modulo

def exportar_datos_usuarios():
    """Exportar datos de usuarios, roles y permisos a JSON"""
    print("📤 EXPORTANDO DATOS DE USUARIOS...")
    
    datos = {
        'fecha_exportacion': datetime.now().isoformat(),
        'usuarios': [],
        'modulos': [],
        'roles': [],
        'permisos': [],
        'rol_permisos': [],
        'perfiles_usuario': []
    }
    
    # Exportar usuarios (sin contraseñas)
    for user in User.objects.all():
        datos['usuarios'].append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        })
    
    # Exportar módulos
    for modulo in Modulo.objects.all():
        datos['modulos'].append({
            'id': modulo.id,
            'nombre': modulo.nombre,
            'descripcion': modulo.descripcion,
            'icono': modulo.icono,
            'orden': modulo.orden,
            'activo': modulo.activo
        })
    
    # Exportar roles
    for rol in Rol.objects.all():
        datos['roles'].append({
            'id': rol.id,
            'nombre': rol.nombre,
            'descripcion': rol.descripcion,
            'creado_en': rol.creado_en.isoformat()
        })
    
    # Exportar permisos
    for permiso in Permiso.objects.all():
        datos['permisos'].append({
            'id': permiso.id,
            'nombre': permiso.nombre,
            'codigo': permiso.codigo,
            'tipo': permiso.tipo,
            'modulo_id': permiso.modulo.id,
            'descripcion': permiso.descripcion
        })
    
    # Exportar asignaciones rol-permiso
    for rp in RolPermiso.objects.all():
        datos['rol_permisos'].append({
            'id': rp.id,
            'rol_id': rp.rol.id,
            'permiso_id': rp.permiso.id,
            'activo': rp.activo,
            'creado_en': rp.creado_en.isoformat()
        })
    
    # Exportar perfiles de usuario
    for perfil in PerfilUsuario.objects.all():
        datos['perfiles_usuario'].append({
            'id': perfil.id,
            'usuario_id': perfil.usuario.id,
            'rol_id': perfil.rol.id if perfil.rol else None,
            'telefono': perfil.telefono,
            'direccion': perfil.direccion,
            'fecha_nacimiento': perfil.fecha_nacimiento.isoformat() if perfil.fecha_nacimiento else None,
            'creado_en': perfil.creado_en.isoformat()
        })
    
    # Guardar en archivo
    with open('datos_usuarios_export.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos exportados a 'datos_usuarios_export.json'")
    print(f"   - {len(datos['usuarios'])} usuarios")
    print(f"   - {len(datos['modulos'])} módulos")
    print(f"   - {len(datos['roles'])} roles")
    print(f"   - {len(datos['permisos'])} permisos")
    print(f"   - {len(datos['rol_permisos'])} asignaciones rol-permiso")
    print(f"   - {len(datos['perfiles_usuario'])} perfiles de usuario")
    
    return datos

def crear_datos_basicos():
    """Crear datos básicos de roles y permisos si no existen"""
    print("🔧 CREANDO DATOS BÁSICOS...")
    
    # Crear roles básicos si no existen
    roles_basicos = [
        {'nombre': 'Administrador', 'descripcion': 'Acceso completo al sistema'},
        {'nombre': 'Gerente', 'descripcion': 'Gestión de proyectos y reportes'},
        {'nombre': 'Supervisor', 'descripcion': 'Supervisión de proyectos'},
        {'nombre': 'Operador', 'descripcion': 'Operaciones básicas del sistema'},
        {'nombre': 'Consulta', 'descripcion': 'Solo consulta de información'}
    ]
    
    for rol_data in roles_basicos:
        rol, created = Rol.objects.get_or_create(
            nombre=rol_data['nombre'],
            defaults={'descripcion': rol_data['descripcion']}
        )
        if created:
            print(f"   ✅ Rol creado: {rol.nombre}")
        else:
            print(f"   ⚠️  Rol ya existe: {rol.nombre}")
    
    # Crear módulos básicos si no existen
    modulos_data = [
        {'nombre': 'proyectos', 'descripcion': 'Gestión de proyectos', 'icono': 'fas fa-project-diagram'},
        {'nombre': 'clientes', 'descripcion': 'Gestión de clientes', 'icono': 'fas fa-users'},
        {'nombre': 'colaboradores', 'descripcion': 'Gestión de colaboradores', 'icono': 'fas fa-user-tie'},
        {'nombre': 'facturas', 'descripcion': 'Gestión de facturas', 'icono': 'fas fa-file-invoice'},
        {'nombre': 'gastos', 'descripcion': 'Gestión de gastos', 'icono': 'fas fa-receipt'},
        {'nombre': 'inventario', 'descripcion': 'Gestión de inventario', 'icono': 'fas fa-boxes'},
        {'nombre': 'usuarios', 'descripcion': 'Gestión de usuarios', 'icono': 'fas fa-user-cog'},
        {'nombre': 'reportes', 'descripcion': 'Reportes del sistema', 'icono': 'fas fa-chart-bar'},
        {'nombre': 'dashboard', 'descripcion': 'Panel principal', 'icono': 'fas fa-tachometer-alt'}
    ]
    
    for modulo_data in modulos_data:
        modulo, created = Modulo.objects.get_or_create(
            nombre=modulo_data['nombre'],
            defaults={
                'descripcion': modulo_data['descripcion'],
                'icono': modulo_data['icono'],
                'orden': modulos_data.index(modulo_data)
            }
        )
        if created:
            print(f"   ✅ Módulo creado: {modulo.nombre}")
    
    # Crear permisos básicos si no existen
    modulos = Modulo.objects.all()
    tipos_permisos = ['ver', 'crear', 'editar', 'eliminar', 'exportar']
    
    for modulo in modulos:
        for tipo in tipos_permisos:
            try:
                permiso, created = Permiso.objects.get_or_create(
                    codigo=f"{tipo}_{modulo.nombre}",
                    defaults={
                        'nombre': f"{tipo.title()} {modulo.nombre.title()}",
                        'tipo': tipo,
                        'modulo': modulo,
                        'descripcion': f"Permiso para {tipo} en {modulo.nombre}"
                    }
                )
                if created:
                    print(f"   ✅ Permiso creado: {permiso.nombre}")
            except Exception as e:
                print(f"   ❌ Error creando permiso {tipo}_{modulo.nombre}: {e}")
    
    print("✅ Datos básicos creados/verificados")

def verificar_superusuario():
    """Verificar y crear superusuario si no existe"""
    print("👤 VERIFICANDO SUPERUSUARIO...")
    
    if not User.objects.filter(is_superuser=True).exists():
        print("   ⚠️  No hay superusuarios. Creando uno...")
        
        # Crear superusuario
        username = input("   Ingrese nombre de usuario para superusuario: ")
        email = input("   Ingrese email: ")
        password = input("   Ingrese contraseña: ")
        
        try:
            user = User.objects.create_superuser(username, email, password)
            print(f"   ✅ Superusuario creado: {username}")
        except Exception as e:
            print(f"   ❌ Error creando superusuario: {e}")
    else:
        superusuarios = User.objects.filter(is_superuser=True)
        print(f"   ✅ Superusuarios encontrados: {superusuarios.count()}")
        for user in superusuarios:
            print(f"      - {user.username} ({user.email})")

if __name__ == "__main__":
    print("🚀 SCRIPT DE SINCRONIZACIÓN DE USUARIOS")
    print("=" * 50)
    
    try:
        # 1. Crear datos básicos
        crear_datos_basicos()
        
        # 2. Verificar superusuario
        verificar_superusuario()
        
        # 3. Exportar datos
        exportar_datos_usuarios()
        
        print("\n" + "=" * 50)
        print("✅ SINCRONIZACIÓN COMPLETADA")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Copia 'datos_usuarios_export.json' al servidor")
        print("2. Ejecuta el script de importación en el servidor")
        print("3. Verifica que las migraciones estén aplicadas")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
