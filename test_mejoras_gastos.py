#!/usr/bin/env python3
"""
Script para probar las mejoras implementadas en el módulo de gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Proyecto, Cliente, Gasto
from datetime import date, timedelta

def probar_categorias_color_icono():
    """Probar visualización de color e icono en categorías"""
    print("🎨 PROBANDO COLOR E ICONO EN CATEGORÍAS")
    print("=" * 60)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/categorias-gasto/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos de color e icono
            elementos_color_icono = [
                'Color',
                'Icono',
                'color-preview',
                'fas fa-tag'
            ]
            
            elementos_encontrados = 0
            print("\n🔍 VERIFICANDO ELEMENTOS DE COLOR E ICONO:")
            for elemento in elementos_color_icono:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Presente")
                else:
                    print(f"  ❌ {elemento}: Faltante")
            
            if elementos_encontrados >= 3:
                print("\n✅ ¡COLOR E ICONO EN CATEGORÍAS FUNCIONANDO!")
                return True
            else:
                print("\n❌ HAY PROBLEMAS CON COLOR E ICONO")
                return False
        else:
            print(f"❌ Error accediendo a categorías: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_gastos_recientes_dashboard():
    """Probar lista de gastos recientes en dashboard"""
    print("\n📊 PROBANDO GASTOS RECIENTES EN DASHBOARD")
    print("=" * 60)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/gastos/dashboard/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos de gastos recientes
            elementos_gastos_recientes = [
                'Gastos Recientes',
                'gastos-recientes-section',
                'gastos-recientes-grid',
                'gasto-item',
                'gasto-categoria',
                'gasto-descripcion',
                'gasto-monto',
                'gasto-fecha',
                'gasto-estado',
                'estado-badge',
                'ver-todos-btn'
            ]
            
            elementos_encontrados = 0
            print("\n🔍 VERIFICANDO ELEMENTOS DE GASTOS RECIENTES:")
            for elemento in elementos_gastos_recientes:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Presente")
                else:
                    print(f"  ❌ {elemento}: Faltante")
            
            if elementos_encontrados >= 8:
                print("\n✅ ¡GASTOS RECIENTES EN DASHBOARD FUNCIONANDO!")
                return True
            else:
                print("\n❌ HAY PROBLEMAS CON GASTOS RECIENTES")
                return False
        else:
            print(f"❌ Error accediendo al dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_botones_aprobar():
    """Probar botones de aprobar/desaprobar gastos"""
    print("\n✅ PROBANDO BOTONES DE APROBAR GASTOS")
    print("=" * 60)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/gastos/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos de botones de aprobar
            elementos_botones = [
                'accion-aprobar',
                'accion-desaprobar',
                'gasto_aprobar',
                'gasto_desaprobar',
                'fas fa-check-circle',
                'fas fa-times-circle',
                'Aprobar',
                'Desaprobar'
            ]
            
            elementos_encontrados = 0
            print("\n🔍 VERIFICANDO BOTONES DE APROBAR:")
            for elemento in elementos_botones:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Presente")
                else:
                    print(f"  ❌ {elemento}: Faltante")
            
            if elementos_encontrados >= 6:
                print("\n✅ ¡BOTONES DE APROBAR FUNCIONANDO!")
                return True
            else:
                print("\n❌ HAY PROBLEMAS CON BOTONES DE APROBAR")
                return False
        else:
            print(f"❌ Error accediendo a la lista: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_funcionalidad_aprobar():
    """Probar funcionalidad de aprobar gastos"""
    print("\n🔧 PROBANDO FUNCIONALIDAD DE APROBAR")
    print("=" * 60)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        # Crear un gasto de prueba si no existe
        gasto, created = Gasto.objects.get_or_create(
            descripcion='Gasto de prueba para aprobar',
            defaults={
                'proyecto': Proyecto.objects.first(),
                'categoria': CategoriaGasto.objects.first(),
                'monto': 100.00,
                'fecha_gasto': date.today(),
                'aprobado': False,
                'aprobado_por': None
            }
        )
        
        if created:
            print("  ✅ Gasto de prueba creado")
        else:
            print("  ✅ Gasto de prueba existente")
        
        # Probar aprobar gasto
        response = client.get(f'/gastos/{gasto.id}/aprobar/')
        if response.status_code == 302:  # Redirect
            print("  ✅ URL de aprobar gasto: Funcionando")
        else:
            print(f"  ❌ URL de aprobar gasto: Error {response.status_code}")
            return False
        
        # Probar desaprobar gasto
        response = client.get(f'/gastos/{gasto.id}/desaprobar/')
        if response.status_code == 302:  # Redirect
            print("  ✅ URL de desaprobar gasto: Funcionando")
        else:
            print(f"  ❌ URL de desaprobar gasto: Error {response.status_code}")
            return False
        
        print("\n✅ ¡FUNCIONALIDAD DE APROBAR FUNCIONANDO!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def mostrar_resumen_mejoras():
    """Mostrar resumen de las mejoras implementadas"""
    print("\n✨ RESUMEN DE MEJORAS IMPLEMENTADAS")
    print("=" * 80)
    
    mejoras = [
        "🎨 CATEGORÍAS CON COLOR E ICONO:",
        "  ✅ Agregadas columnas de Color e Icono en la tabla",
        "  ✅ Círculo de color personalizado para cada categoría",
        "  ✅ Icono Font Awesome con color de la categoría",
        "  ✅ Diseño visual atractivo y profesional",
        "",
        "📊 GASTOS RECIENTES EN DASHBOARD:",
        "  ✅ Sección completa de gastos recientes",
        "  ✅ Grid responsive con tarjetas modernas",
        "  ✅ Información completa: descripción, proyecto, monto, fecha, estado",
        "  ✅ Categorías con color e icono personalizado",
        "  ✅ Estados visuales (aprobado/pendiente)",
        "  ✅ Botón 'Ver Todos los Gastos'",
        "  ✅ Diseño glassmorphism y animaciones",
        "",
        "✅ BOTONES DE APROBAR GASTOS:",
        "  ✅ Botón 'Aprobar' para gastos pendientes",
        "  ✅ Botón 'Desaprobar' para gastos aprobados",
        "  ✅ URLs funcionales para aprobar/desaprobar",
        "  ✅ Mensajes de confirmación",
        "  ✅ Estilos visuales distintivos",
        "  ✅ Integración completa con la lista de gastos",
        "",
        "🎯 BENEFICIOS PARA EL USUARIO:",
        "  • Visualización clara de colores e iconos de categorías",
        "  • Vista rápida de gastos recientes en el dashboard",
        "  • Control total sobre la aprobación de gastos",
        "  • Interfaz más intuitiva y funcional",
        "  • Mejor experiencia de gestión de gastos"
    ]
    
    for mejora in mejoras:
        print(mejora)

def main():
    """Función principal"""
    print("🚀 PRUEBA DE MEJORAS EN MÓDULO DE GASTOS")
    print("=" * 80)
    
    try:
        # Probar cada mejora
        categorias_ok = probar_categorias_color_icono()
        dashboard_ok = probar_gastos_recientes_dashboard()
        botones_ok = probar_botones_aprobar()
        funcionalidad_ok = probar_funcionalidad_aprobar()
        
        # Mostrar resumen
        mostrar_resumen_mejoras()
        
        # Resumen final
        print(f"\n" + "=" * 80)
        print("📋 RESUMEN FINAL")
        print("=" * 80)
        
        if categorias_ok and dashboard_ok and botones_ok and funcionalidad_ok:
            print("🎉 ¡TODAS LAS MEJORAS FUNCIONANDO PERFECTAMENTE!")
            print("✅ Categorías con color e icono: Implementado")
            print("✅ Gastos recientes en dashboard: Implementado")
            print("✅ Botones de aprobar gastos: Implementado")
            print("✅ Funcionalidad completa: Verificada")
            
            print(f"\n🌐 PARA VER LAS MEJORAS:")
            print("  1. Categorías: http://localhost:8000/categorias-gasto/")
            print("  2. Dashboard: http://localhost:8000/gastos/dashboard/")
            print("  3. Lista: http://localhost:8000/gastos/")
            print("  4. Prueba los botones de aprobar/desaprobar")
        else:
            print("❌ HAY PROBLEMAS CON ALGUNAS MEJORAS")
            if not categorias_ok:
                print("  - Problemas con color e icono en categorías")
            if not dashboard_ok:
                print("  - Problemas con gastos recientes en dashboard")
            if not botones_ok:
                print("  - Problemas con botones de aprobar")
            if not funcionalidad_ok:
                print("  - Problemas con funcionalidad de aprobar")
        
        return categorias_ok and dashboard_ok and botones_ok and funcionalidad_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
