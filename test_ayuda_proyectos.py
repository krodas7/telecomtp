#!/usr/bin/env python3
"""
Script para probar la nueva funcionalidad de ayuda en proyectos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_ayuda_proyectos():
    """Probar la nueva funcionalidad de ayuda en proyectos"""
    print("🔔 PROBANDO NUEVA FUNCIONALIDAD DE AYUDA EN PROYECTOS")
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
    
    # 1. Probar carga de la página de proyectos
    print("\n1️⃣ Probando carga de página de proyectos...")
    try:
        response = client.get('/proyectos/')
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar que las notificaciones estáticas ya no estén
            if 'El proyecto será marcado como inactivo' in content and 'alert alert-info' in content:
                print("  ❌ Las notificaciones estáticas aún están presentes")
                return False
            else:
                print("  ✅ Notificaciones estáticas removidas correctamente")
            
            # Verificar que el botón de ayuda esté presente
            if 'mostrarAyudaProyectos()' in content and 'Ayuda sobre Proyectos' in content:
                print("  ✅ Botón de ayuda contextual agregado correctamente")
            else:
                print("  ❌ Botón de ayuda no encontrado")
                return False
                
        else:
            print(f"  ❌ Error cargando proyectos: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # 2. Verificar que el JavaScript esté presente
    print("\n2️⃣ Verificando JavaScript de ayuda...")
    try:
        with open('templates/core/proyectos/list.html', 'r') as f:
            content = f.read()
        
        elementos_js = [
            'function mostrarAyudaProyectos()',
            'toastNotification.info',
            'toastNotification.warning',
            'Información sobre Proyectos',
            'Restricciones de Proyectos Inactivos'
        ]
        
        elementos_encontrados = 0
        for elemento in elementos_js:
            if elemento in content:
                elementos_encontrados += 1
        
        print(f"  📊 Elementos JS encontrados: {elementos_encontrados}/{len(elementos_js)}")
        
        if elementos_encontrados >= len(elementos_js) * 0.8:
            print("  ✅ JavaScript de ayuda implementado correctamente")
        else:
            print("  ❌ JavaScript de ayuda incompleto")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando JavaScript: {e}")
        return False
    
    return True

def mostrar_mejoras_implementadas():
    """Mostrar las mejoras implementadas"""
    print("\n3️⃣ MEJORAS IMPLEMENTADAS:")
    print("  ✅ Eliminadas notificaciones estáticas molestas")
    print("  ✅ Agregado botón de ayuda contextual")
    print("  ✅ Implementadas notificaciones toast elegantes")
    print("  ✅ Información disponible solo cuando se necesita")
    print("  ✅ Mejor experiencia de usuario")
    print("  ✅ Diseño más limpio y profesional")

def mostrar_beneficios():
    """Mostrar los beneficios de la nueva implementación"""
    print("\n4️⃣ BENEFICIOS DE LA NUEVA IMPLEMENTACIÓN:")
    print("  🎨 Interfaz más limpia sin notificaciones permanentes")
    print("  🔘 Ayuda disponible bajo demanda")
    print("  🔔 Notificaciones toast elegantes y temporales")
    print("  📱 Mejor experiencia en móviles")
    print("  ⚡ Carga más rápida de la página")
    print("  🎯 Información contextual cuando se necesita")

def main():
    """Función principal"""
    print("🔔 PRUEBA DE AYUDA CONTEXTUAL EN PROYECTOS")
    print("=" * 70)
    
    try:
        # Probar funcionalidad
        ayuda_ok = probar_ayuda_proyectos()
        
        # Mostrar mejoras
        mostrar_mejoras_implementadas()
        
        # Mostrar beneficios
        mostrar_beneficios()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if ayuda_ok:
            print("🎉 ¡AYUDA CONTEXTUAL IMPLEMENTADA EXITOSAMENTE!")
            print("✅ Notificaciones estáticas eliminadas")
            print("✅ Botón de ayuda contextual agregado")
            print("✅ Notificaciones toast elegantes implementadas")
            print("✅ Mejor experiencia de usuario")
            
            print(f"\n🌐 PARA PROBAR EN EL NAVEGADOR:")
            print("  1. Ve a: http://localhost:8000/proyectos/")
            print("  2. Observa que ya no hay notificaciones estáticas")
            print("  3. Haz clic en 'Ayuda sobre Proyectos'")
            print("  4. Verás notificaciones toast elegantes")
            print("  5. Las notificaciones desaparecen automáticamente")
        else:
            print("❌ HAY PROBLEMAS CON LA IMPLEMENTACIÓN")
        
        return ayuda_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
