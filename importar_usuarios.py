#!/usr/bin/env python
"""
Script para importar datos de usuarios, roles y permisos en el servidor
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

def importar_datos_usuarios(archivo_json='datos_usuarios_export.json'):
    """Importar datos de usuarios, roles y permisos desde JSON"""
    print("📥 IMPORTANDO DATOS DE USUARIOS...")
    
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except FileNotFoundError:
        print(f"❌ Archivo {archivo_json} no encontrado")
        return False
    
    print(f"   📅 Fecha de exportación: {datos.get('fecha_exportacion', 'Desconocida')}")
    
    # 1. Importar módulos
    print("\n1. IMPORTANDO MÓDULOS...")
    modulos_importados = 0
    for modulo_data in datos.get('modulos', []):
        modulo, created = Modulo.objects.get_or_create(
            nombre=modulo_data['nombre'],
            defaults={
                'descripcion': modulo_data['descripcion'],
                'icono': modulo_data.get('icono', ''),
                'orden': modulo_data.get('orden', 0),
                'activo': modulo_data.get('activo', True)
            }
        )
        if created:
            print(f"   ✅ Módulo creado: {modulo.nombre}")
            modulos_importados += 1
        else:
            print(f"   ⚠️  Módulo ya existe: {modulo.nombre}")
    
    # 2. Importar roles
    print("\n2. IMPORTANDO ROLES...")
    roles_importados = 0
    for rol_data in datos.get('roles', []):
        rol, created = Rol.objects.get_or_create(
            nombre=rol_data['nombre'],
            defaults={
                'descripcion': rol_data['descripcion'],
                'creado_en': datetime.fromisoformat(rol_data['creado_en'])
            }
        )
        if created:
            print(f"   ✅ Rol creado: {rol.nombre}")
            roles_importados += 1
        else:
            print(f"   ⚠️  Rol ya existe: {rol.nombre}")
    
    # 3. Importar permisos
    print("\n3. IMPORTANDO PERMISOS...")
    permisos_importados = 0
    for permiso_data in datos.get('permisos', []):
        try:
            modulo = Modulo.objects.get(id=permiso_data['modulo_id'])
            permiso, created = Permiso.objects.get_or_create(
                codigo=permiso_data['codigo'],
                defaults={
                    'nombre': permiso_data['nombre'],
                    'tipo': permiso_data['tipo'],
                    'modulo': modulo,
                    'descripcion': permiso_data['descripcion']
                }
            )
            if created:
                print(f"   ✅ Permiso creado: {permiso.nombre}")
                permisos_importados += 1
            else:
                print(f"   ⚠️  Permiso ya existe: {permiso.nombre}")
        except Modulo.DoesNotExist:
            print(f"   ❌ Módulo no encontrado para permiso: {permiso_data['nombre']}")
    
    # 4. Importar usuarios (solo si no existen)
    print("\n4. IMPORTANDO USUARIOS...")
    usuarios_importados = 0
    for user_data in datos.get('usuarios', []):
        if not User.objects.filter(username=user_data['username']).exists():
            try:
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_active=user_data['is_active'],
                    is_staff=user_data['is_staff'],
                    is_superuser=user_data['is_superuser']
                )
                print(f"   ✅ Usuario creado: {user.username}")
                usuarios_importados += 1
            except Exception as e:
                print(f"   ❌ Error creando usuario {user_data['username']}: {e}")
        else:
            print(f"   ⚠️  Usuario ya existe: {user_data['username']}")
    
    # 5. Importar asignaciones rol-permiso
    print("\n5. IMPORTANDO ASIGNACIONES ROL-PERMISO...")
    asignaciones_importadas = 0
    for rp_data in datos.get('rol_permisos', []):
        try:
            rol = Rol.objects.get(id=rp_data['rol_id'])
            permiso = Permiso.objects.get(id=rp_data['permiso_id'])
            
            rp, created = RolPermiso.objects.get_or_create(
                rol=rol,
                permiso=permiso,
                defaults={
                    'activo': rp_data['activo'],
                    'creado_en': datetime.fromisoformat(rp_data['creado_en'])
                }
            )
            if created:
                print(f"   ✅ Asignación creada: {rol.nombre} -> {permiso.nombre}")
                asignaciones_importadas += 1
        except (Rol.DoesNotExist, Permiso.DoesNotExist) as e:
            print(f"   ❌ Error en asignación: {e}")
    
    # 6. Importar perfiles de usuario
    print("\n6. IMPORTANDO PERFILES DE USUARIO...")
    perfiles_importados = 0
    for perfil_data in datos.get('perfiles_usuario', []):
        try:
            usuario = User.objects.get(id=perfil_data['usuario_id'])
            rol = Rol.objects.get(id=perfil_data['rol_id']) if perfil_data['rol_id'] else None
            
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                defaults={
                    'rol': rol,
                    'telefono': perfil_data.get('telefono', ''),
                    'direccion': perfil_data.get('direccion', ''),
                    'fecha_nacimiento': datetime.fromisoformat(perfil_data['fecha_nacimiento']).date() if perfil_data.get('fecha_nacimiento') else None,
                    'creado_en': datetime.fromisoformat(perfil_data['creado_en'])
                }
            )
            if created:
                print(f"   ✅ Perfil creado: {usuario.username}")
                perfiles_importados += 1
        except (User.DoesNotExist, Rol.DoesNotExist) as e:
            print(f"   ❌ Error en perfil: {e}")
    
    print("\n" + "=" * 50)
    print("✅ IMPORTACIÓN COMPLETADA")
    print(f"   - {modulos_importados} módulos importados")
    print(f"   - {roles_importados} roles importados")
    print(f"   - {permisos_importados} permisos importados")
    print(f"   - {usuarios_importados} usuarios importados")
    print(f"   - {asignaciones_importadas} asignaciones importadas")
    print(f"   - {perfiles_importados} perfiles importados")
    
    return True

def verificar_importacion():
    """Verificar que la importación fue exitosa"""
    print("\n🔍 VERIFICANDO IMPORTACIÓN...")
    
    print(f"   Módulos: {Modulo.objects.count()}")
    print(f"   Usuarios: {User.objects.count()}")
    print(f"   Roles: {Rol.objects.count()}")
    print(f"   Permisos: {Permiso.objects.count()}")
    print(f"   Asignaciones: {RolPermiso.objects.count()}")
    print(f"   Perfiles: {PerfilUsuario.objects.count()}")
    
    # Verificar superusuarios
    superusuarios = User.objects.filter(is_superuser=True)
    print(f"   Superusuarios: {superusuarios.count()}")
    for user in superusuarios:
        print(f"      - {user.username} ({user.email})")

if __name__ == "__main__":
    print("🚀 SCRIPT DE IMPORTACIÓN DE USUARIOS")
    print("=" * 50)
    
    try:
        # Importar datos
        if importar_datos_usuarios():
            # Verificar importación
            verificar_importacion()
            
            print("\n✅ IMPORTACIÓN EXITOSA")
            print("\n📋 PRÓXIMOS PASOS:")
            print("1. Verifica que puedas acceder a la gestión de usuarios")
            print("2. Crea un superusuario si es necesario")
            print("3. Asigna roles a los usuarios según sea necesario")
        else:
            print("\n❌ IMPORTACIÓN FALLIDA")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
