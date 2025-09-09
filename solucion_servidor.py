#!/usr/bin/env python
"""
Script simplificado para solucionar la gestión de usuarios en el servidor
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Rol, Permiso, RolPermiso, PerfilUsuario, Modulo

def crear_datos_basicos_servidor():
    """Crear datos básicos necesarios en el servidor"""
    print("🔧 CREANDO DATOS BÁSICOS EN EL SERVIDOR...")
    
    # 1. Crear módulos básicos
    print("\n1. CREANDO MÓDULOS...")
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
    
    modulos_creados = 0
    for modulo_data in modulos_data:
        modulo, created = Modulo.objects.get_or_create(
            nombre=modulo_data['nombre'],
            defaults={
                'descripcion': modulo_data['descripcion'],
                'icono': modulo_data['icono'],
                'orden': modulos_data.index(modulo_data),
                'activo': True
            }
        )
        if created:
            print(f"   ✅ Módulo creado: {modulo.nombre}")
            modulos_creados += 1
        else:
            print(f"   ⚠️  Módulo ya existe: {modulo.nombre}")
    
    # 2. Crear roles básicos
    print("\n2. CREANDO ROLES...")
    roles_data = [
        {'nombre': 'Administrador', 'descripcion': 'Acceso completo al sistema'},
        {'nombre': 'Gerente', 'descripcion': 'Gestión de proyectos y reportes'},
        {'nombre': 'Supervisor', 'descripcion': 'Supervisión de proyectos'},
        {'nombre': 'Operador', 'descripcion': 'Operaciones básicas del sistema'},
        {'nombre': 'Consulta', 'descripcion': 'Solo consulta de información'}
    ]
    
    roles_creados = 0
    for rol_data in roles_data:
        rol, created = Rol.objects.get_or_create(
            nombre=rol_data['nombre'],
            defaults={'descripcion': rol_data['descripcion']}
        )
        if created:
            print(f"   ✅ Rol creado: {rol.nombre}")
            roles_creados += 1
        else:
            print(f"   ⚠️  Rol ya existe: {rol.nombre}")
    
    # 3. Crear permisos básicos
    print("\n3. CREANDO PERMISOS...")
    modulos = Modulo.objects.all()
    tipos_permisos = ['ver', 'crear', 'editar', 'eliminar', 'exportar']
    
    permisos_creados = 0
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
                    permisos_creados += 1
            except Exception as e:
                print(f"   ❌ Error creando permiso {tipo}_{modulo.nombre}: {e}")
    
    print(f"   ✅ {permisos_creados} permisos creados")
    
    # 4. Verificar superusuario
    print("\n4. VERIFICANDO SUPERUSUARIO...")
    if not User.objects.filter(is_superuser=True).exists():
        print("   ⚠️  No hay superusuarios. Creando uno...")
        try:
            user = User.objects.create_superuser(
                username='admin',
                email='admin@sistema.com',
                password='admin123'
            )
            print(f"   ✅ Superusuario creado: {user.username}")
        except Exception as e:
            print(f"   ❌ Error creando superusuario: {e}")
    else:
        superusuarios = User.objects.filter(is_superuser=True)
        print(f"   ✅ Superusuarios encontrados: {superusuarios.count()}")
        for user in superusuarios:
            print(f"      - {user.username} ({user.email})")
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print(f"   - {modulos_creados} módulos creados")
    print(f"   - {roles_creados} roles creados")
    print(f"   - {permisos_creados} permisos creados")
    
    return True

def verificar_sistema():
    """Verificar que el sistema esté funcionando correctamente"""
    print("\n🔍 VERIFICANDO SISTEMA...")
    
    print(f"   Módulos: {Modulo.objects.count()}")
    print(f"   Usuarios: {User.objects.count()}")
    print(f"   Roles: {Rol.objects.count()}")
    print(f"   Permisos: {Permiso.objects.count()}")
    print(f"   Asignaciones: {RolPermiso.objects.count()}")
    print(f"   Perfiles: {PerfilUsuario.objects.count()}")
    
    # Verificar superusuarios
    superusuarios = User.objects.filter(is_superuser=True)
    print(f"   Superusuarios: {superusuarios.count()}")
    
    if superusuarios.exists():
        print("\n✅ SISTEMA CONFIGURADO CORRECTAMENTE")
        print("   Puedes acceder a la gestión de usuarios en:")
        print("   - /usuarios/ (Lista de usuarios)")
        print("   - /roles/ (Gestión de roles)")
        print("   - /admin/ (Panel de administración de Django)")
        return True
    else:
        print("\n❌ SISTEMA NO CONFIGURADO")
        print("   No hay superusuarios. Ejecuta el script nuevamente.")
        return False

if __name__ == "__main__":
    print("🚀 SOLUCIÓN PARA GESTIÓN DE USUARIOS EN SERVIDOR")
    print("=" * 60)
    
    try:
        # Crear datos básicos
        if crear_datos_basicos_servidor():
            # Verificar sistema
            if verificar_sistema():
                print("\n🎉 ¡PROBLEMA RESUELTO!")
                print("\n📋 INSTRUCCIONES:")
                print("1. Accede a /usuarios/ para gestionar usuarios")
                print("2. Accede a /roles/ para gestionar roles y permisos")
                print("3. Usa el superusuario 'admin' con contraseña 'admin123'")
                print("4. Cambia la contraseña del superusuario por seguridad")
            else:
                print("\n❌ CONFIGURACIÓN INCOMPLETA")
        else:
            print("\n❌ ERROR EN LA CONFIGURACIÓN")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
