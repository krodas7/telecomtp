#!/usr/bin/env python3
"""
Script para probar la corrección del error de tipos Decimal/float
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Proyecto, Gasto, CategoriaGasto
from decimal import Decimal

def test_proyecto_dashboard():
    """Probar que el dashboard del proyecto funciona sin errores de tipo"""
    print("🔧 PROBANDO CORRECCIÓN DE ERROR DECIMAL/FLOAT")
    print("=" * 50)
    
    try:
        # Obtener un proyecto existente
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos en la base de datos")
            return False
        
        print(f"✅ Proyecto encontrado: {proyecto.nombre}")
        
        # Crear cliente de prueba
        client = Client()
        
        # Obtener usuario admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No hay usuario admin")
            return False
        
        # Autenticar
        client.force_login(admin_user)
        print(f"✅ Usuario autenticado: {admin_user.username}")
        
        # Probar acceso al dashboard del proyecto
        url = f'/proyectos/{proyecto.id}/'
        print(f"🌐 Probando URL: {url}")
        
        response = client.get(url)
        
        if response.status_code == 200:
            print("✅ Dashboard del proyecto carga correctamente")
            print("✅ Error de tipos Decimal/float corregido")
            return True
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                if 'TypeError' in content:
                    print("❌ Aún hay error de TypeError")
                    if 'unsupported operand type(s) for -' in content:
                        print("❌ Error de tipos Decimal/float persiste")
                print(f"Contenido del error: {content[:500]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def test_gastos_dashboard():
    """Probar que el dashboard de gastos funciona correctamente"""
    print("\n🔧 PROBANDO DASHBOARD DE GASTOS")
    print("=" * 50)
    
    try:
        client = Client()
        admin_user = User.objects.filter(is_superuser=True).first()
        client.force_login(admin_user)
        
        response = client.get('/gastos/dashboard/')
        
        if response.status_code == 200:
            print("✅ Dashboard de gastos carga correctamente")
            return True
        else:
            print(f"❌ Error en dashboard de gastos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def test_gastos_list():
    """Probar que la lista de gastos funciona correctamente"""
    print("\n🔧 PROBANDO LISTA DE GASTOS")
    print("=" * 50)
    
    try:
        client = Client()
        admin_user = User.objects.filter(is_superuser=True).first()
        client.force_login(admin_user)
        
        response = client.get('/gastos/')
        
        if response.status_code == 200:
            print("✅ Lista de gastos carga correctamente")
            return True
        else:
            print(f"❌ Error en lista de gastos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE CORRECCIÓN DECIMAL/FLOAT")
    print("=" * 60)
    
    # Ejecutar pruebas
    test1 = test_proyecto_dashboard()
    test2 = test_gastos_dashboard()
    test3 = test_gastos_list()
    
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 30)
    print(f"Dashboard Proyecto: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Dashboard Gastos: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Lista Gastos: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("✅ Error de tipos Decimal/float corregido exitosamente")
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar los errores mostrados arriba")

if __name__ == '__main__':
    main()
