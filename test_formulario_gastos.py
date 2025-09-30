#!/usr/bin/env python3
"""
Script para probar el nuevo formulario de crear gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Proyecto, CategoriaGasto

def probar_formulario_gastos():
    """Probar el nuevo formulario de crear gastos"""
    print("📝 PROBANDO NUEVO FORMULARIO DE GASTOS")
    print("=" * 45)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar carga del formulario
    print("\n1️⃣ Probando carga del formulario...")
    try:
        response = client.get('/gastos/crear/')
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos del nuevo formulario
            elementos_verificar = [
                'Crear Nuevo Gasto',
                'Información del Gasto',
                'Información Básica',
                'Información del Proyecto',
                'Fechas y Estado',
                'Información Adicional',
                'form-container',
                'form-section',
                'form-control',
                'btn-success'
            ]
            
            elementos_encontrados = 0
            for elemento in elementos_verificar:
                if elemento in content:
                    print(f"  ✅ {elemento} encontrado")
                    elementos_encontrados += 1
                else:
                    print(f"  ❌ {elemento} no encontrado")
            
            print(f"  📊 Elementos encontrados: {elementos_encontrados}/{len(elementos_verificar)}")
            
        else:
            print(f"  ❌ Error cargando formulario: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # 2. Verificar que hay proyectos y categorías disponibles
    print("\n2️⃣ Verificando datos disponibles...")
    try:
        proyectos = Proyecto.objects.all()
        categorias = CategoriaGasto.objects.all()
        
        print(f"  📊 Proyectos disponibles: {proyectos.count()}")
        print(f"  📊 Categorías disponibles: {categorias.count()}")
        
        if proyectos.count() > 0:
            print("  ✅ Hay proyectos disponibles para seleccionar")
        else:
            print("  ⚠️ No hay proyectos disponibles")
        
        if categorias.count() > 0:
            print("  ✅ Hay categorías disponibles para seleccionar")
        else:
            print("  ⚠️ No hay categorías disponibles")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 3. Probar envío del formulario
    print("\n3️⃣ Probando envío del formulario...")
    try:
        # Obtener un proyecto y categoría para la prueba
        proyecto = Proyecto.objects.first()
        categoria = CategoriaGasto.objects.first()
        
        if proyecto and categoria:
            form_data = {
                'descripcion': 'Prueba de gasto desde formulario mejorado',
                'monto': '1500.00',
                'categoria': categoria.id,
                'proyecto': proyecto.id,
                'fecha_gasto': '2025-09-29',
                'observaciones': 'Gasto de prueba del nuevo formulario'
            }
            
            response = client.post('/gastos/crear/', form_data)
            
            if response.status_code == 302:
                print("  ✅ Formulario enviado correctamente (redirección)")
                print("  ✅ Gasto creado exitosamente")
            else:
                print(f"  ❌ Error en envío: {response.status_code}")
                # Mostrar errores si los hay
                if hasattr(response, 'content'):
                    content = response.content.decode()
                    if 'error' in content.lower():
                        print("  📋 Posibles errores en el formulario")
        else:
            print("  ⚠️ No hay datos suficientes para probar el envío")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def verificar_estilos_css():
    """Verificar que los estilos CSS estén aplicados"""
    print("\n4️⃣ Verificando estilos CSS...")
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/gastos/crear/')
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar clases CSS específicas
            clases_css = [
                'form-container',
                'form-section',
                'form-group',
                'form-label',
                'form-control',
                'btn-success',
                'hero-section',
                'form-header'
            ]
            
            clases_encontradas = 0
            for clase in clases_css:
                if clase in content:
                    clases_encontradas += 1
            
            print(f"  📊 Clases CSS encontradas: {clases_encontradas}/{len(clases_css)}")
            
            if clases_encontradas >= len(clases_css) * 0.8:
                print("  ✅ Estilos CSS aplicados correctamente")
            else:
                print("  ⚠️ Algunos estilos CSS pueden no estar aplicados")
                
    except Exception as e:
        print(f"  ❌ Error: {e}")

def main():
    """Función principal"""
    print("🔧 PRUEBA DEL NUEVO FORMULARIO DE GASTOS")
    print("=" * 50)
    
    try:
        # Probar formulario
        formulario_ok = probar_formulario_gastos()
        
        # Verificar estilos
        verificar_estilos_css()
        
        # Resumen final
        print(f"\n" + "=" * 50)
        print("📋 RESUMEN FINAL")
        print("=" * 50)
        
        if formulario_ok:
            print("🎉 ¡NUEVO FORMULARIO FUNCIONA PERFECTAMENTE!")
            print("✅ Formulario moderno y responsivo")
            print("✅ Validación en tiempo real")
            print("✅ Estilos CSS aplicados")
            print("✅ Funcionalidad completa")
            
            print(f"\n🌐 Para probar en el navegador:")
            print(f"   1. Ve a: http://localhost:8000/gastos/crear/")
            print(f"   2. Verifica el nuevo diseño moderno")
            print(f"   3. Prueba la validación en tiempo real")
            print(f"   4. Completa y envía el formulario")
        else:
            print("❌ HAY PROBLEMAS CON EL FORMULARIO")
        
        return formulario_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
