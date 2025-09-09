#!/usr/bin/env python
"""
Script de diagnóstico para verificar la gestión de usuarios en el servidor desplegado
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Rol, Permiso, RolPermiso, PerfilUsuario

def diagnosticar_usuarios():
    print("🔍 DIAGNÓSTICO DE GESTIÓN DE USUARIOS")
    print("=" * 50)
    
    # 1. Verificar usuarios
    print("\n1. USUARIOS:")
    usuarios = User.objects.all()
    print(f"   Total de usuarios: {usuarios.count()}")
    
    superusuarios = User.objects.filter(is_superuser=True)
    print(f"   Superusuarios: {superusuarios.count()}")
    
    for user in superusuarios:
        print(f"   - {user.username} ({user.email}) - Activo: {user.is_active}")
    
    # 2. Verificar roles
    print("\n2. ROLES:")
    roles = Rol.objects.all()
    print(f"   Total de roles: {roles.count()}")
    
    for rol in roles:
        print(f"   - {rol.nombre}: {rol.descripcion}")
    
    # 3. Verificar permisos
    print("\n3. PERMISOS:")
    permisos = Permiso.objects.all()
    print(f"   Total de permisos: {permisos.count()}")
    
    for permiso in permisos[:10]:  # Mostrar solo los primeros 10
        print(f"   - {permiso.nombre} ({permiso.tipo})")
    
    if permisos.count() > 10:
        print(f"   ... y {permisos.count() - 10} más")
    
    # 4. Verificar asignaciones de permisos
    print("\n4. ASIGNACIONES DE PERMISOS:")
    rol_permisos = RolPermiso.objects.all()
    print(f"   Total de asignaciones: {rol_permisos.count()}")
    
    for rp in rol_permisos[:5]:  # Mostrar solo las primeras 5
        print(f"   - {rp.rol.nombre} -> {rp.permiso.nombre} (Activo: {rp.activo})")
    
    if rol_permisos.count() > 5:
        print(f"   ... y {rol_permisos.count() - 5} más")
    
    # 5. Verificar perfiles de usuario
    print("\n5. PERFILES DE USUARIO:")
    perfiles = PerfilUsuario.objects.all()
    print(f"   Total de perfiles: {perfiles.count()}")
    
    for perfil in perfiles:
        print(f"   - {perfil.usuario.username} -> {perfil.rol.nombre if perfil.rol else 'Sin rol'}")
    
    # 6. Verificar migraciones
    print("\n6. ESTADO DE MIGRACIONES:")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM django_migrations ORDER BY applied DESC LIMIT 5")
            migraciones = cursor.fetchall()
            print("   Últimas 5 migraciones:")
            for migracion in migraciones:
                print(f"   - {migracion[0]}")
    except Exception as e:
        print(f"   ⚠️  Error verificando migraciones: {e}")
    
    # 7. Verificar tablas en la base de datos
    print("\n7. TABLAS EN BASE DE DATOS:")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%rol%' OR table_name LIKE '%permiso%' OR table_name LIKE '%usuario%'
            ORDER BY table_name
        """)
        tablas = cursor.fetchall()
        print("   Tablas relacionadas con usuarios/roles:")
        for tabla in tablas:
            print(f"   - {tabla[0]}")
    
    print("\n" + "=" * 50)
    print("✅ DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    try:
        diagnosticar_usuarios()
    except Exception as e:
        print(f"❌ ERROR EN EL DIAGNÓSTICO: {e}")
        import traceback
        traceback.print_exc()
