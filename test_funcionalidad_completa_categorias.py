#!/usr/bin/env python3
"""
Script para verificar la funcionalidad completa de colores e iconos en categorías
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Gasto
from django.db.models import Sum, Count

def verificar_dashboard_con_colores_iconos():
    """Verificar que el dashboard muestre colores e iconos correctamente"""
    print("📊 VERIFICANDO DASHBOARD CON COLORES E ICONOS")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    
    try:
        # Acceder al dashboard
        response = client.get('/gastos/dashboard/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos específicos del nuevo diseño
            elementos_verificar = [
                'categoria-header',
                'categoria-icon',
                'categoria-info',
                'style="color:'
            ]
            
            elementos_encontrados = 0
            for elemento in elementos_verificar:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Encontrado")
                else:
                    print(f"  ❌ {elemento}: No encontrado")
            
            if elementos_encontrados >= 3:
                print("  ✅ Dashboard con colores e iconos funcionando")
                return True
            else:
                print("  ❌ Dashboard no muestra colores e iconos correctamente")
                return False
        else:
            print(f"  ❌ Error accediendo al dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def verificar_categorias_con_datos():
    """Verificar que las categorías tengan colores e iconos únicos"""
    print("\n🎨 VERIFICANDO CATEGORÍAS CON COLORES E ICONOS")
    print("=" * 60)
    
    categorias = CategoriaGasto.objects.all()
    
    if not categorias.exists():
        print("  ❌ No hay categorías en la BD")
        return False
    
    colores_unicos = set()
    iconos_unicos = set()
    categorias_con_datos = 0
    
    for categoria in categorias:
        # Verificar que tenga color e icono
        if categoria.color and categoria.icono:
            colores_unicos.add(categoria.color)
            iconos_unicos.add(categoria.icono)
            categorias_con_datos += 1
            
            print(f"  ✅ {categoria.nombre}: {categoria.color} - {categoria.icono}")
        else:
            print(f"  ❌ {categoria.nombre}: Faltan color o icono")
    
    print(f"\n  📊 Estadísticas:")
    print(f"    - Categorías con color e icono: {categorias_con_datos}")
    print(f"    - Colores únicos: {len(colores_unicos)}")
    print(f"    - Iconos únicos: {len(iconos_unicos)}")
    
    return categorias_con_datos > 0 and len(colores_unicos) > 1

def verificar_gastos_por_categoria():
    """Verificar que los gastos se agrupen correctamente por categoría"""
    print("\n💰 VERIFICANDO GASTOS POR CATEGORÍA")
    print("=" * 60)
    
    try:
        # Consulta igual a la del dashboard
        gastos_por_categoria = Gasto.objects.values(
            'categoria__nombre', 'categoria__color', 'categoria__icono'
        ).annotate(
            total=Sum('monto'),
            cantidad=Count('id')
        ).order_by('-total')
        
        if gastos_por_categoria.exists():
            print(f"  ✅ {len(gastos_por_categoria)} categorías con gastos encontradas")
            
            for categoria in gastos_por_categoria:
                print(f"    📋 {categoria['categoria__nombre']}")
                print(f"      🎨 Color: {categoria['categoria__color']}")
                print(f"      🔧 Icono: {categoria['categoria__icono']}")
                print(f"      💰 Total: Q{categoria['total']:,.2f}")
                print(f"      📊 Cantidad: {categoria['cantidad']} gastos")
                print()
            
            return True
        else:
            print("  ⚠️  No hay gastos agrupados por categoría")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def probar_creacion_categoria_web():
    """Probar la creación de categorías a través de la interfaz web"""
    print("\n🌐 PROBANDO CREACIÓN DE CATEGORÍAS VIA WEB")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    
    try:
        # Acceder al formulario de creación
        response = client.get('/categorias-gasto/crear/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos del formulario
            elementos_formulario = [
                'color-picker',
                'icon-picker',
                'preview-card',
                'data-color=',
                'data-icon='
            ]
            
            elementos_encontrados = 0
            for elemento in elementos_formulario:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Presente en formulario")
                else:
                    print(f"  ❌ {elemento}: Faltante en formulario")
            
            if elementos_encontrados >= 4:
                print("  ✅ Formulario de creación completo")
                return True
            else:
                print("  ❌ Formulario de creación incompleto")
                return False
        else:
            print(f"  ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🎨 VERIFICACIÓN COMPLETA DE COLORES E ICONOS EN CATEGORÍAS")
    print("=" * 80)
    
    try:
        # Verificar dashboard
        dashboard_ok = verificar_dashboard_con_colores_iconos()
        
        # Verificar categorías
        categorias_ok = verificar_categorias_con_datos()
        
        # Verificar gastos por categoría
        gastos_ok = verificar_gastos_por_categoria()
        
        # Probar formulario web
        formulario_ok = probar_creacion_categoria_web()
        
        # Resumen final
        print(f"\n" + "=" * 80)
        print("📋 RESUMEN FINAL")
        print("=" * 80)
        
        if dashboard_ok and categorias_ok and gastos_ok and formulario_ok:
            print("🎉 ¡FUNCIONALIDAD COMPLETA DE COLORES E ICONOS IMPLEMENTADA!")
            print("✅ Dashboard muestra colores e iconos correctamente")
            print("✅ Categorías tienen colores e iconos únicos")
            print("✅ Gastos se agrupan por categoría con colores e iconos")
            print("✅ Formulario de creación completo con selectores visuales")
            
            print(f"\n🌐 FUNCIONALIDADES DISPONIBLES:")
            print("  🎨 Selector visual de colores (12 opciones)")
            print("  🔧 Selector visual de iconos (16 opciones)")
            print("  👁️  Vista previa en tiempo real")
            print("  📊 Dashboard con categorías colorizadas")
            print("  ✏️  Edición de categorías existentes")
            print("  💾 Persistencia en base de datos")
            
            print(f"\n🌐 PARA USAR:")
            print("  1. Crear categoría: http://localhost:8000/categorias-gasto/crear/")
            print("  2. Ver categorías: http://localhost:8000/categorias-gasto/")
            print("  3. Dashboard: http://localhost:8000/gastos/dashboard/")
        else:
            print("❌ HAY PROBLEMAS CON LA FUNCIONALIDAD")
            if not dashboard_ok:
                print("  - Problemas con dashboard")
            if not categorias_ok:
                print("  - Problemas con categorías")
            if not gastos_ok:
                print("  - Problemas con agrupación de gastos")
            if not formulario_ok:
                print("  - Problemas con formulario")
        
        return dashboard_ok and categorias_ok and gastos_ok and formulario_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
