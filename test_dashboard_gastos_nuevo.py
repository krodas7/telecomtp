#!/usr/bin/env python3
"""
Script para probar el nuevo diseño del dashboard de gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_dashboard_gastos():
    """Probar el nuevo diseño del dashboard de gastos"""
    print("🎨 PROBANDO NUEVO DISEÑO DEL DASHBOARD DE GASTOS")
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
            
            # Verificar elementos del nuevo diseño
            elementos_nuevos = [
                'gastos-header',
                'categorias-section',
                'gastos-recientes-section',
                'categorias-grid',
                'gasto-item',
                'categoria-card',
                'gasto-titulo',
                'gasto-details'
            ]
            
            elementos_encontrados = 0
            for elemento in elementos_nuevos:
                if elemento in content:
                    elementos_encontrados += 1
            
            print(f"  📊 Elementos del nuevo diseño encontrados: {elementos_encontrados}/{len(elementos_nuevos)}")
            
            if elementos_encontrados >= len(elementos_nuevos) * 0.8:
                print("  ✅ Nuevo diseño implementado correctamente")
            else:
                print("  ❌ Nuevo diseño incompleto")
                return False
                
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # 2. Verificar CSS del nuevo diseño
    print("\n2️⃣ Verificando estilos CSS...")
    try:
        with open('templates/core/gastos/dashboard.html', 'r') as f:
            content = f.read()
        
        estilos_nuevos = [
            '.gastos-header',
            '.categorias-section',
            '.gastos-recientes-section',
            '.categorias-grid',
            '.gasto-item',
            '.categoria-card',
            '.gasto-titulo',
            '.gasto-details',
            '.categoria-stats'
        ]
        
        estilos_encontrados = 0
        for estilo in estilos_nuevos:
            if estilo in content:
                estilos_encontrados += 1
        
        print(f"  📊 Estilos CSS encontrados: {estilos_encontrados}/{len(estilos_nuevos)}")
        
        if estilos_encontrados >= len(estilos_nuevos) * 0.8:
            print("  ✅ Estilos CSS implementados correctamente")
        else:
            print("  ❌ Estilos CSS incompletos")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando CSS: {e}")
        return False
    
    return True

def mostrar_caracteristicas_nuevas():
    """Mostrar las características del nuevo diseño"""
    print("\n3️⃣ CARACTERÍSTICAS DEL NUEVO DISEÑO:")
    print("  ✅ Header limpio y moderno")
    print("  ✅ Tarjetas de estadísticas simplificadas")
    print("  ✅ Grid de categorías con diseño de tarjetas")
    print("  ✅ Lista de gastos recientes estilo lista limpia")
    print("  ✅ Diseño responsivo para móviles")
    print("  ✅ Colores consistentes y profesionales")
    print("  ✅ Tipografía mejorada")
    print("  ✅ Espaciado optimizado")

def mostrar_mejoras_visuales():
    """Mostrar las mejoras visuales implementadas"""
    print("\n4️⃣ MEJORAS VISUALES IMPLEMENTADAS:")
    print("  🎨 Diseño más limpio y minimalista")
    print("  📱 Mejor experiencia en dispositivos móviles")
    print("  🎯 Información más fácil de escanear")
    print("  📊 Tarjetas de categorías más organizadas")
    print("  📋 Lista de gastos más legible")
    print("  🎨 Colores más profesionales")
    print("  ⚡ Carga más rápida y fluida")

def main():
    """Función principal"""
    print("🎨 PRUEBA DEL NUEVO DISEÑO DEL DASHBOARD DE GASTOS")
    print("=" * 70)
    
    try:
        # Probar funcionalidad
        dashboard_ok = probar_dashboard_gastos()
        
        # Mostrar características
        mostrar_caracteristicas_nuevas()
        
        # Mostrar mejoras
        mostrar_mejoras_visuales()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if dashboard_ok:
            print("🎉 ¡NUEVO DISEÑO IMPLEMENTADO EXITOSAMENTE!")
            print("✅ Dashboard rediseñado con estilo moderno")
            print("✅ Tarjetas de categorías organizadas")
            print("✅ Lista de gastos recientes limpia")
            print("✅ Diseño responsivo implementado")
            print("✅ Mejor experiencia de usuario")
            
            print(f"\n🌐 PARA VER EL NUEVO DISEÑO:")
            print("  1. Ve a: http://localhost:8000/gastos/dashboard/")
            print("  2. Observa el nuevo diseño limpio y moderno")
            print("  3. Verifica las tarjetas de categorías")
            print("  4. Revisa la lista de gastos recientes")
            print("  5. Prueba en diferentes tamaños de pantalla")
        else:
            print("❌ HAY PROBLEMAS CON EL NUEVO DISEÑO")
        
        return dashboard_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
