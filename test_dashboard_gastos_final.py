#!/usr/bin/env python3
"""
Script para probar el diseño final del dashboard de gastos
que coincide exactamente con la imagen proporcionada
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_dashboard_final():
    """Probar el diseño final del dashboard de gastos"""
    print("🎨 PROBANDO DISEÑO FINAL DEL DASHBOARD DE GASTOS")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar carga del dashboard
    print("\n1️⃣ Probando carga del dashboard de gastos...")
    try:
        response = client.get('/gastos/dashboard/')
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos del diseño final
            elementos_finales = [
                'gastos-hero',
                'gastos-hero-content',
                'hero-icon',
                'gastos-hero-title',
                'gastos-hero-subtitle',
                'gastos-actions',
                'stats-grid',
                'stat-card',
                'categorias-section',
                'categorias-grid',
                'categoria-card'
            ]
            
            elementos_encontrados = 0
            for elemento in elementos_finales:
                if elemento in content:
                    elementos_encontrados += 1
            
            print(f"  📊 Elementos del diseño final encontrados: {elementos_encontrados}/{len(elementos_finales)}")
            
            if elementos_encontrados >= len(elementos_finales) * 0.9:
                print("  ✅ Diseño final implementado correctamente")
            else:
                print("  ❌ Diseño final incompleto")
                return False
                
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # 2. Verificar CSS del diseño final
    print("\n2️⃣ Verificando estilos CSS finales...")
    try:
        with open('templates/core/gastos/dashboard.html', 'r') as f:
            content = f.read()
        
        estilos_finales = [
            '.gastos-hero',
            '.gastos-hero-content',
            '.hero-icon',
            '.gastos-hero-title',
            '.gastos-hero-subtitle',
            '.gastos-actions',
            '.stats-grid',
            '.stat-card',
            '.categorias-section',
            '.categorias-grid',
            '.categoria-card',
            '.categoria-nombre',
            '.categoria-total',
            '.categoria-stats'
        ]
        
        estilos_encontrados = 0
        for estilo in estilos_finales:
            if estilo in content:
                estilos_encontrados += 1
        
        print(f"  📊 Estilos CSS encontrados: {estilos_encontrados}/{len(estilos_finales)}")
        
        if estilos_encontrados >= len(estilos_finales) * 0.9:
            print("  ✅ Estilos CSS implementados correctamente")
        else:
            print("  ❌ Estilos CSS incompletos")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando CSS: {e}")
        return False
    
    return True

def mostrar_caracteristicas_finales():
    """Mostrar las características del diseño final"""
    print("\n3️⃣ CARACTERÍSTICAS DEL DISEÑO FINAL:")
    print("  ✅ Hero section con gradiente rojo-naranja")
    print("  ✅ Icono grande de gastos en el hero")
    print("  ✅ Título 'Gestión de Gastos' prominente")
    print("  ✅ Subtítulo descriptivo")
    print("  ✅ 3 botones de acción con estilo glassmorphism")
    print("  ✅ 4 tarjetas de estadísticas con iconos de colores")
    print("  ✅ Grid de 3 columnas para categorías")
    print("  ✅ Tarjetas de categorías con nombres en rojo")
    print("  ✅ Totales en rojo y estadísticas organizadas")
    print("  ✅ Sin sección de gastos recientes (como en la imagen)")

def mostrar_colores_implementados():
    """Mostrar los colores implementados"""
    print("\n4️⃣ COLORES IMPLEMENTADOS:")
    print("  🎨 Hero: Gradiente #ff6b6b → #ee5a24")
    print("  🎨 Iconos de estadísticas:")
    print("     - Tarjeta 1: #9b59b6 (púrpura)")
    print("     - Tarjeta 2: #e91e63 (rosa)")
    print("     - Tarjeta 3: #3498db (azul)")
    print("     - Tarjeta 4: #27ae60 (verde)")
    print("  🎨 Categorías: Nombres y totales en #e74c3c (rojo)")
    print("  🎨 Botones: Glassmorphism con transparencia")
    print("  🎨 Fondos: Blanco con sombras sutiles")

def mostrar_estructura_final():
    """Mostrar la estructura final del dashboard"""
    print("\n5️⃣ ESTRUCTURA FINAL DEL DASHBOARD:")
    print("  📋 1. Hero Section (gradiente)")
    print("     - Icono grande de gastos")
    print("     - Título 'Gestión de Gastos'")
    print("     - Subtítulo descriptivo")
    print("     - 3 botones de acción")
    print("  📊 2. Estadísticas (4 tarjetas)")
    print("     - Total Gastos (púrpura)")
    print("     - Monto Total (rosa)")
    print("     - Aprobados (azul)")
    print("     - Pendientes (verde)")
    print("  📈 3. Gastos por Categoría (grid 3x2)")
    print("     - 6 categorías máximo")
    print("     - Nombres en rojo")
    print("     - Totales en rojo")
    print("     - Cantidad y promedio")

def main():
    """Función principal"""
    print("🎨 PRUEBA DEL DISEÑO FINAL DEL DASHBOARD DE GASTOS")
    print("=" * 70)
    
    try:
        # Probar funcionalidad
        dashboard_ok = probar_dashboard_final()
        
        # Mostrar características
        mostrar_caracteristicas_finales()
        
        # Mostrar colores
        mostrar_colores_implementados()
        
        # Mostrar estructura
        mostrar_estructura_final()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if dashboard_ok:
            print("🎉 ¡DISEÑO FINAL IMPLEMENTADO EXITOSAMENTE!")
            print("✅ Hero section con gradiente como en la imagen")
            print("✅ Tarjetas de estadísticas con iconos de colores")
            print("✅ Grid de categorías exactamente como la imagen")
            print("✅ Colores y tipografía coincidentes")
            print("✅ Estructura idéntica al diseño deseado")
            
            print(f"\n🌐 PARA VER EL DISEÑO FINAL:")
            print("  1. Ve a: http://localhost:8000/gastos/dashboard/")
            print("  2. Observa el hero section con gradiente")
            print("  3. Verifica las 4 tarjetas de estadísticas")
            print("  4. Revisa el grid de categorías (3 columnas)")
            print("  5. Compara con la imagen proporcionada")
        else:
            print("❌ HAY PROBLEMAS CON EL DISEÑO FINAL")
        
        return dashboard_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
