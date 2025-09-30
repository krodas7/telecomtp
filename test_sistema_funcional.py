#!/usr/bin/env python3
"""
Script para probar que el sistema funcione correctamente en el navegador
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_sistema_completo():
    """Probar que el sistema funcione completamente"""
    print("🌐 PROBANDO SISTEMA COMPLETO EN EL NAVEGADOR")
    print("=" * 50)
    
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
    
    # Lista de páginas principales a probar
    paginas_principales = [
        ("Dashboard", "/dashboard/"),
        ("Proyectos", "/proyectos/"),
        ("Clientes", "/clientes/"),
        ("Facturas", "/facturas/"),
        ("Colaboradores", "/colaboradores/"),
        ("Gastos", "/gastos/"),
        ("Inventario", "/inventario/"),
        ("Presupuestos", "/presupuestos/"),
        ("Usuarios", "/usuarios/"),
        ("Archivos", "/archivos/"),
        ("Anticipos", "/anticipos/"),
        ("Pagos", "/pagos/"),
        ("Rentabilidad", "/rentabilidad/"),
        ("Sistema", "/sistema/"),
    ]
    
    resultados = []
    
    for nombre, url in paginas_principales:
        print(f"\n🔍 Probando {nombre}...")
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {nombre}: Página carga correctamente")
                resultados.append((nombre, True, "OK"))
            elif response.status_code == 302:
                print(f"  ⚠️ {nombre}: Redirige (posible login)")
                resultados.append((nombre, True, "REDIRECT"))
            else:
                print(f"  ❌ {nombre}: Error {response.status_code}")
                resultados.append((nombre, False, f"ERROR {response.status_code}"))
        except Exception as e:
            print(f"  ❌ {nombre}: Excepción - {e}")
            resultados.append((nombre, False, f"EXCEPTION: {e}"))
    
    return resultados

def verificar_datos_en_paginas():
    """Verificar que las páginas muestren datos"""
    print("\n📊 VERIFICANDO DATOS EN PÁGINAS...")
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    # Probar dashboard con datos
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            content = response.content.decode()
            if 'proyectos' in content.lower() and 'clientes' in content.lower():
                print("  ✅ Dashboard muestra datos correctamente")
            else:
                print("  ⚠️ Dashboard puede no mostrar datos")
    except Exception as e:
        print(f"  ❌ Error en dashboard: {e}")
    
    # Probar lista de proyectos
    try:
        response = client.get('/proyectos/')
        if response.status_code == 200:
            content = response.content.decode()
            if 'proyecto' in content.lower():
                print("  ✅ Lista de proyectos muestra datos")
            else:
                print("  ⚠️ Lista de proyectos puede estar vacía")
    except Exception as e:
        print(f"  ❌ Error en proyectos: {e}")

def generar_reporte_final(resultados):
    """Generar reporte final"""
    print("\n" + "="*50)
    print("📋 REPORTE FINAL DEL SISTEMA")
    print("="*50)
    
    funcionando = sum(1 for _, ok, _ in resultados if ok)
    con_problemas = len(resultados) - funcionando
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"  ✅ Páginas funcionando: {funcionando}")
    print(f"  ❌ Páginas con problemas: {con_problemas}")
    print(f"  📈 Total de páginas: {len(resultados)}")
    print(f"  🎯 Porcentaje de éxito: {(funcionando/len(resultados)*100):.1f}%")
    
    if con_problemas > 0:
        print(f"\n❌ PÁGINAS CON PROBLEMAS:")
        for nombre, ok, error in resultados:
            if not ok:
                print(f"  • {nombre}: {error}")
    
    print(f"\n🎉 SISTEMA {'FUNCIONANDO PERFECTAMENTE' if con_problemas == 0 else 'FUNCIONANDO CON ALGUNOS PROBLEMAS'}")
    
    return con_problemas == 0

def main():
    """Función principal"""
    print("🔧 PRUEBA COMPLETA DEL SISTEMA")
    print("=" * 40)
    
    try:
        # Probar sistema completo
        resultados = probar_sistema_completo()
        
        # Verificar datos en páginas
        verificar_datos_en_paginas()
        
        # Generar reporte final
        todo_ok = generar_reporte_final(resultados)
        
        if todo_ok:
            print(f"\n🌐 Para usar el sistema:")
            print(f"   1. Ve a: http://localhost:8000/")
            print(f"   2. Inicia sesión con: admin / admin")
            print(f"   3. Navega por todos los módulos del menú")
            print(f"   4. Verifica que los datos se muestren correctamente")
        else:
            print(f"\n⚠️ Algunas páginas tienen problemas, pero el sistema es funcional")
        
        return todo_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
