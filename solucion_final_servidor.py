#!/usr/bin/env python
"""
Script final para solucionar problemas de gestión de usuarios en el servidor
"""
import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Modulo, Rol, Permiso, RolPermiso, PerfilUsuario
from django.db import transaction

def solucion_final_servidor():
    print("=== SOLUCIÓN FINAL PARA GESTIÓN DE USUARIOS ===")
    
    with transaction.atomic():
        # 1. Limpiar datos duplicados
        print("\n1. LIMPIANDO DATOS DUPLICADOS...")
        
        # Limpiar módulos duplicados
        modulos_unicos = {}
        modulos_duplicados = []
        
        for modulo in Modulo.objects.all():
            nombre_lower = modulo.nombre.lower()
            if nombre_lower in modulos_unicos:
                modulos_duplicados.append(modulo)
            else:
                modulos_unicos[nombre_lower] = modulo
        
        for modulo in modulos_duplicados:
            modulo.delete()
        
        print(f"  ✅ Eliminados {len(modulos_duplicados)} módulos duplicados")
        
        # Limpiar permisos duplicados
        permisos_unicos = {}
        permisos_duplicados = []
        
        for permiso in Permiso.objects.all():
            clave = f"{permiso.nombre}_{permiso.modulo.id}"
            if clave in permisos_unicos:
                permisos_duplicados.append(permiso)
            else:
                permisos_unicos[clave] = permiso
        
        for permiso in permisos_duplicados:
            permiso.delete()
        
        print(f"  ✅ Eliminados {len(permisos_duplicados)} permisos duplicados")
        
        # 2. Crear módulos necesarios
        print("\n2. CREANDO MÓDULOS NECESARIOS...")
        modulos_necesarios = [
            {'nombre': 'Usuarios', 'descripcion': 'Gestión de usuarios del sistema'},
            {'nombre': 'Roles', 'descripcion': 'Gestión de roles y permisos'},
            {'nombre': 'Permisos', 'descripcion': 'Gestión de permisos del sistema'},
        ]
        
        for modulo_data in modulos_necesarios:
            modulo, created = Modulo.objects.get_or_create(
                nombre=modulo_data['nombre'],
                defaults={'descripcion': modulo_data['descripcion']}
            )
            if created:
                print(f"  ✅ Creado módulo: {modulo.nombre}")
        
        # 3. Crear permisos básicos
        print("\n3. CREANDO PERMISOS BÁSICOS...")
        modulo_usuarios = Modulo.objects.get(nombre='Usuarios')
        modulo_roles = Modulo.objects.get(nombre='Roles')
        modulo_permisos = Modulo.objects.get(nombre='Permisos')
        
        permisos_basicos = [
            # Permisos para usuarios
            {'nombre': 'Ver Usuarios', 'codigo': 'ver_usuarios', 'modulo': modulo_usuarios},
            {'nombre': 'Crear Usuarios', 'codigo': 'crear_usuarios', 'modulo': modulo_usuarios},
            {'nombre': 'Editar Usuarios', 'codigo': 'editar_usuarios', 'modulo': modulo_usuarios},
            {'nombre': 'Eliminar Usuarios', 'codigo': 'eliminar_usuarios', 'modulo': modulo_usuarios},
            {'nombre': 'Exportar Usuarios', 'codigo': 'exportar_usuarios', 'modulo': modulo_usuarios},
            
            # Permisos para roles
            {'nombre': 'Ver Roles', 'codigo': 'ver_roles', 'modulo': modulo_roles},
            {'nombre': 'Crear Roles', 'codigo': 'crear_roles', 'modulo': modulo_roles},
            {'nombre': 'Editar Roles', 'codigo': 'editar_roles', 'modulo': modulo_roles},
            {'nombre': 'Eliminar Roles', 'codigo': 'eliminar_roles', 'modulo': modulo_roles},
            {'nombre': 'Exportar Roles', 'codigo': 'exportar_roles', 'modulo': modulo_roles},
            
            # Permisos para permisos
            {'nombre': 'Ver Permisos', 'codigo': 'ver_permisos', 'modulo': modulo_permisos},
            {'nombre': 'Crear Permisos', 'codigo': 'crear_permisos', 'modulo': modulo_permisos},
            {'nombre': 'Editar Permisos', 'codigo': 'editar_permisos', 'modulo': modulo_permisos},
            {'nombre': 'Eliminar Permisos', 'codigo': 'eliminar_permisos', 'modulo': modulo_permisos},
            {'nombre': 'Exportar Permisos', 'codigo': 'exportar_permisos', 'modulo': modulo_permisos},
        ]
        
        for permiso_data in permisos_basicos:
            permiso, created = Permiso.objects.get_or_create(
                nombre=permiso_data['nombre'],
                defaults={
                    'codigo': permiso_data['codigo'],
                    'descripcion': f"Permiso para {permiso_data['nombre'].lower()}",
                    'modulo': permiso_data['modulo']
                }
            )
            if created:
                print(f"  ✅ Creado permiso: {permiso.nombre}")
        
        # 4. Asignar permisos al rol Superusuario
        print("\n4. ASIGNANDO PERMISOS AL ROL SUPERUSUARIO...")
        try:
            rol_superusuario = Rol.objects.get(nombre='Superusuario')
            permisos_gestion = Permiso.objects.filter(
                nombre__in=['Ver Usuarios', 'Crear Usuarios', 'Editar Usuarios', 'Eliminar Usuarios', 'Exportar Usuarios',
                           'Ver Roles', 'Crear Roles', 'Editar Roles', 'Eliminar Roles', 'Exportar Roles',
                           'Ver Permisos', 'Crear Permisos', 'Editar Permisos', 'Eliminar Permisos', 'Exportar Permisos']
            )
            
            for permiso in permisos_gestion:
                rp, created = RolPermiso.objects.get_or_create(
                    rol=rol_superusuario,
                    permiso=permiso
                )
                if created:
                    print(f"  ✅ Asignado permiso: {permiso.nombre}")
                    
        except Rol.DoesNotExist:
            print("  ❌ No se encontró el rol Superusuario")
        
        # 5. Verificar estado final
        print("\n5. ESTADO FINAL:")
        print(f"  - Usuarios: {User.objects.count()}")
        print(f"  - Módulos: {Modulo.objects.count()}")
        print(f"  - Roles: {Rol.objects.count()}")
        print(f"  - Permisos: {Permiso.objects.count()}")
        print(f"  - Relaciones Rol-Permiso: {RolPermiso.objects.count()}")
        print(f"  - Perfiles de Usuario: {PerfilUsuario.objects.count()}")
        
        # 6. Prueba de funcionalidad
        print("\n6. PRUEBA DE FUNCIONALIDAD:")
        try:
            # Crear un módulo de prueba
            modulo_test = Modulo.objects.create(
                nombre="Módulo de Prueba",
                descripcion="Módulo para probar funcionalidad"
            )
            print("  ✅ Creación de módulo: OK")
            modulo_test.delete()
            
            # Crear un permiso de prueba
            permiso_test = Permiso.objects.create(
                nombre="Permiso de Prueba",
                codigo="permiso_prueba",
                descripcion="Permiso para probar funcionalidad",
                modulo=Modulo.objects.first()
            )
            print("  ✅ Creación de permiso: OK")
            permiso_test.delete()
            
            # Crear un rol de prueba
            rol_test = Rol.objects.create(
                nombre="Rol de Prueba",
                descripcion="Rol para probar funcionalidad"
            )
            print("  ✅ Creación de rol: OK")
            rol_test.delete()
            
            print("  ✅ Todas las funcionalidades están operativas")
            
        except Exception as e:
            print(f"  ❌ Error en prueba de funcionalidad: {e}")
        
        print("\n✅ SOLUCIÓN APLICADA EXITOSAMENTE")
        print("\n📋 INSTRUCCIONES PARA EL SERVIDOR:")
        print("1. Subir este script al servidor")
        print("2. Ejecutar: python solucion_final_servidor.py")
        print("3. Reiniciar los servicios: sudo systemctl restart gunicorn")
        print("4. Verificar que la gestión de usuarios funcione correctamente")

if __name__ == "__main__":
    solucion_final_servidor()
