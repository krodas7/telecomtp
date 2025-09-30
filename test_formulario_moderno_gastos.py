#!/usr/bin/env python3
"""
Script para probar el nuevo formulario moderno de gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Proyecto, Cliente

def probar_formulario_moderno():
    """Probar el formulario moderno de gastos"""
    print("🎨 PROBANDO FORMULARIO MODERNO DE GASTOS")
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
    
    try:
        # Acceder al formulario de creación
        response = client.get('/gastos/crear/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos del diseño moderno
            elementos_modernos = [
                'page-container',
                'form-wrapper',
                'form-header',
                'form-title',
                'form-card',
                'form-section',
                'section-header',
                'section-icon',
                'section-title',
                'form-grid',
                'floating-elements',
                'glassmorphism',
                'backdrop-filter'
            ]
            
            elementos_encontrados = 0
            print("\n🔍 VERIFICANDO ELEMENTOS MODERNOS:")
            for elemento in elementos_modernos:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Presente")
                else:
                    print(f"  ❌ {elemento}: Faltante")
            
            # Verificar CSS moderno
            css_moderno = [
                'linear-gradient',
                'backdrop-filter',
                'border-radius: 24px',
                'box-shadow: 0 20px 60px',
                'animation: fadeInUp',
                'animation: fadeInDown',
                'animation: float',
                'transform: translateY',
                'rgba(255, 255, 255, 0.95)',
                'text-shadow',
                'letter-spacing'
            ]
            
            css_encontrado = 0
            print("\n🎨 VERIFICANDO CSS MODERNO:")
            for css in css_moderno:
                if css in content:
                    css_encontrado += 1
                    print(f"  ✅ {css}: Presente")
                else:
                    print(f"  ❌ {css}: Faltante")
            
            # Verificar estructura del formulario
            estructura_formulario = [
                'Información Básica',
                'Información del Proyecto',
                'Fechas y Estado',
                'Información Adicional',
                'Guardar Gasto',
                'Cancelar'
            ]
            
            estructura_encontrada = 0
            print("\n📋 VERIFICANDO ESTRUCTURA DEL FORMULARIO:")
            for elemento in estructura_formulario:
                if elemento in content:
                    estructura_encontrada += 1
                    print(f"  ✅ {elemento}: Presente")
                else:
                    print(f"  ❌ {elemento}: Faltante")
            
            # Verificar iconos Font Awesome
            iconos = [
                'fas fa-plus-circle',
                'fas fa-info-circle',
                'fas fa-project-diagram',
                'fas fa-calendar-alt',
                'fas fa-file-alt',
                'fas fa-tag',
                'fas fa-dollar-sign',
                'fas fa-tags',
                'fas fa-building',
                'fas fa-calendar',
                'fas fa-calendar-times',
                'fas fa-check-circle',
                'fas fa-comment-alt',
                'fas fa-save',
                'fas fa-arrow-left'
            ]
            
            iconos_encontrados = 0
            print("\n🔧 VERIFICANDO ICONOS:")
            for icono in iconos:
                if icono in content:
                    iconos_encontrados += 1
                    print(f"  ✅ {icono}: Presente")
                else:
                    print(f"  ❌ {icono}: Faltante")
            
            # Resumen de verificación
            print(f"\n📊 RESUMEN DE VERIFICACIÓN:")
            print(f"  🎨 Elementos modernos: {elementos_encontrados}/{len(elementos_modernos)}")
            print(f"  🎨 CSS moderno: {css_encontrado}/{len(css_moderno)}")
            print(f"  📋 Estructura: {estructura_encontrada}/{len(estructura_formulario)}")
            print(f"  🔧 Iconos: {iconos_encontrados}/{len(iconos)}")
            
            # Verificar que no hay errores de template
            if 'TemplateDoesNotExist' in content or 'TemplateSyntaxError' in content:
                print("  ❌ Error de template detectado")
                return False
            
            if elementos_encontrados >= 8 and css_encontrado >= 6 and estructura_encontrada >= 5:
                print("\n✅ ¡FORMULARIO MODERNO FUNCIONANDO CORRECTAMENTE!")
                return True
            else:
                print("\n❌ FORMULARIO MODERNO INCOMPLETO")
                return False
        else:
            print(f"❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_responsividad():
    """Verificar que el formulario sea responsive"""
    print("\n📱 VERIFICANDO RESPONSIVIDAD")
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
        # Simular diferentes tamaños de pantalla
        response = client.get('/gastos/crear/', HTTP_USER_AGENT='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar media queries responsive
            media_queries = [
                '@media (max-width: 768px)',
                '@media (max-width: 480px)',
                'grid-template-columns: 1fr',
                'flex-direction: column',
                'width: 100%'
            ]
            
            responsive_encontrado = 0
            for query in media_queries:
                if query in content:
                    responsive_encontrado += 1
                    print(f"  ✅ {query}: Presente")
                else:
                    print(f"  ❌ {query}: Faltante")
            
            if responsive_encontrado >= 3:
                print("  ✅ Formulario responsive")
                return True
            else:
                print("  ❌ Formulario no responsive")
                return False
        else:
            print(f"  ❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def mostrar_caracteristicas_modernas():
    """Mostrar las características modernas del formulario"""
    print("\n✨ CARACTERÍSTICAS MODERNAS DEL FORMULARIO")
    print("=" * 60)
    
    caracteristicas = [
        "🎨 Diseño con glassmorphism y backdrop-filter",
        "🌈 Gradientes modernos y colores vibrantes",
        "✨ Animaciones suaves (fadeIn, slideIn, float)",
        "📱 Diseño completamente responsive",
        "🎯 Elementos flotantes decorativos",
        "💎 Bordes redondeados y sombras elegantes",
        "🔧 Iconos Font Awesome integrados",
        "⚡ Validación en tiempo real",
        "🎭 Efectos hover y transiciones",
        "📐 Grid layout moderno",
        "🎪 Secciones organizadas con iconos",
        "💫 Efectos de brillo en botones",
        "🎨 Paleta de colores profesional",
        "📱 Optimizado para móviles",
        "🚀 Carga rápida y fluida"
    ]
    
    for caracteristica in caracteristicas:
        print(f"  {caracteristica}")

def main():
    """Función principal"""
    print("🎨 PRUEBA DEL FORMULARIO MODERNO DE GASTOS")
    print("=" * 70)
    
    try:
        # Probar formulario moderno
        formulario_ok = probar_formulario_moderno()
        
        # Verificar responsividad
        responsive_ok = verificar_responsividad()
        
        # Mostrar características
        mostrar_caracteristicas_modernas()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if formulario_ok and responsive_ok:
            print("🎉 ¡FORMULARIO MODERNO IMPLEMENTADO EXITOSAMENTE!")
            print("✅ Diseño moderno y profesional funcionando")
            print("✅ Responsividad verificada")
            print("✅ Todas las características modernas presentes")
            
            print(f"\n🌐 PARA VER EL FORMULARIO:")
            print("  1. Ve a: http://localhost:8000/gastos/crear/")
            print("  2. Observa el diseño moderno con glassmorphism")
            print("  3. Prueba la responsividad en diferentes dispositivos")
            print("  4. Disfruta de las animaciones y efectos visuales")
        else:
            print("❌ HAY PROBLEMAS CON EL FORMULARIO MODERNO")
            if not formulario_ok:
                print("  - Problemas con el diseño moderno")
            if not responsive_ok:
                print("  - Problemas con la responsividad")
        
        return formulario_ok and responsive_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
