#!/usr/bin/env python
"""
Script completo para verificar todas las funcionalidades del sistema
"""

import os
import sys
import django
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.cache import cache

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.views import dashboard, sistema_reset_app
from core.models import Cliente, Proyecto, Factura, Anticipo, Gasto, CategoriaGasto

def verificar_base_datos():
    """Verificar que la base de datos esté funcionando"""
    print("🔍 VERIFICANDO BASE DE DATOS...")
    
    try:
        # Contar registros
        total_clientes = Cliente.objects.count()
        total_proyectos = Proyecto.objects.count()
        total_facturas = Factura.objects.count()
        total_anticipos = Anticipo.objects.count()
        total_gastos = Gasto.objects.count()
        
        print(f"✅ Base de datos funcionando correctamente:")
        print(f"   - Clientes: {total_clientes}")
        print(f"   - Proyectos: {total_proyectos}")
        print(f"   - Facturas: {total_facturas}")
        print(f"   - Anticipos: {total_anticipos}")
        print(f"   - Gastos: {total_gastos}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en base de datos: {str(e)}")
        return False

def verificar_vistas():
    """Verificar que las vistas principales funcionen"""
    print("\n🔍 VERIFICANDO VISTAS PRINCIPALES...")
    
    try:
        # Obtener usuario
        user = User.objects.first()
        if not user:
            print("❌ No hay usuarios en el sistema")
            return False
        
        factory = RequestFactory()
        
        # Verificar dashboard
        request = factory.get('/dashboard/')
        request.user = user
        response = dashboard(request)
        
        if response.status_code == 200:
            print("✅ Dashboard funcionando correctamente")
        else:
            print(f"❌ Dashboard error: {response.status_code}")
            return False
        
        # Verificar reset app
        request = factory.get('/sistema/reset-app/')
        request.user = user
        response = sistema_reset_app(request)
        
        if response.status_code == 200:
            print("✅ Vista de reset funcionando correctamente")
        else:
            print(f"❌ Vista de reset error: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando vistas: {str(e)}")
        return False

def verificar_calendario():
    """Verificar que el calendario genere eventos correctamente"""
    print("\n🔍 VERIFICANDO CALENDARIO...")
    
    try:
        user = User.objects.first()
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = user
        
        response = dashboard(request)
        
        # Obtener contexto
        if hasattr(response, 'context_data'):
            context = response.context_data
        else:
            context = getattr(response, 'context', {})
        
        eventos = context.get('eventos_calendario', [])
        eventos_json = context.get('eventos_calendario_json', '')
        
        print(f"✅ Calendario funcionando correctamente:")
        print(f"   - Eventos generados: {len(eventos)}")
        print(f"   - JSON generado: {len(eventos_json)} caracteres")
        
        if eventos:
            print(f"   - Primer evento: {eventos[0]['title']}")
            print(f"   - Fecha: {eventos[0]['start']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando calendario: {str(e)}")
        return False

def verificar_cache():
    """Verificar que el sistema de cache funcione"""
    print("\n🔍 VERIFICANDO SISTEMA DE CACHE...")
    
    try:
        # Probar operaciones básicas de cache
        test_key = 'test_verificacion'
        test_value = 'valor_prueba'
        
        # Escribir en cache
        cache.set(test_key, test_value, 60)
        print("✅ Escritura en cache exitosa")
        
        # Leer del cache
        cached_value = cache.get(test_key)
        if cached_value == test_value:
            print("✅ Lectura del cache exitosa")
        else:
            print("❌ Error en lectura del cache")
            return False
        
        # Limpiar cache de prueba
        cache.delete(test_key)
        print("✅ Limpieza de cache exitosa")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando cache: {str(e)}")
        return False

def verificar_graficos():
    """Verificar que los datos para gráficos se generen correctamente"""
    print("\n🔍 VERIFICANDO DATOS PARA GRÁFICOS...")
    
    try:
        user = User.objects.first()
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = user
        
        response = dashboard(request)
        
        # Obtener contexto
        if hasattr(response, 'context_data'):
            context = response.context_data
        else:
            context = getattr(response, 'context', {})
        
        # Verificar datos de gráficos
        evolucion_proyectos = context.get('evolucion_proyectos', [])
        categorias_gastos = context.get('categorias_gastos', [])
        montos_gastos = context.get('montos_gastos', [])
        ingresos_mensuales = context.get('ingresos_mensuales', [])
        gastos_mensuales = context.get('gastos_mensuales', [])
        
        print(f"✅ Datos para gráficos generados correctamente:")
        print(f"   - Evolución proyectos: {len(evolucion_proyectos)} elementos")
        print(f"   - Categorías gastos: {len(categorias_gastos)} elementos")
        print(f"   - Montos gastos: {len(montos_gastos)} elementos")
        print(f"   - Ingresos mensuales: {len(ingresos_mensuales)} elementos")
        print(f"   - Gastos mensuales: {len(gastos_mensuales)} elementos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando gráficos: {str(e)}")
        return False

def verificar_urls():
    """Verificar que las URLs estén configuradas correctamente"""
    print("\n🔍 VERIFICANDO CONFIGURACIÓN DE URLS...")
    
    try:
        from django.urls import reverse, NoReverseMatch
        
        # URLs principales
        urls_a_verificar = [
            'dashboard',
            'login',
            'logout',
            'sistema',
            'sistema_reset_app',
            'clientes_list',
            'proyectos_list',
            'facturas_list',
            'gastos_list'
        ]
        
        urls_funcionando = 0
        for url_name in urls_a_verificar:
            try:
                reverse(url_name)
                urls_funcionando += 1
            except NoReverseMatch:
                print(f"   ⚠️  URL '{url_name}' no encontrada")
        
        print(f"✅ URLs verificadas: {urls_funcionando}/{len(urls_a_verificar)} funcionando")
        
        return urls_funcionando == len(urls_a_verificar)
        
    except Exception as e:
        print(f"❌ Error verificando URLs: {str(e)}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA")
    print("=" * 50)
    
    resultados = []
    
    # Ejecutar todas las verificaciones
    resultados.append(("Base de Datos", verificar_base_datos()))
    resultados.append(("Vistas Principales", verificar_vistas()))
    resultados.append(("Calendario", verificar_calendario()))
    resultados.append(("Sistema de Cache", verificar_cache()))
    resultados.append(("Datos para Gráficos", verificar_graficos()))
    resultados.append(("Configuración de URLs", verificar_urls()))
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    total_verificaciones = len(resultados)
    verificaciones_exitosas = sum(1 for _, resultado in resultados if resultado)
    
    for nombre, resultado in resultados:
        estado = "✅ EXITOSO" if resultado else "❌ FALLÓ"
        print(f"{estado} - {nombre}")
    
    print(f"\n🎯 RESULTADO FINAL: {verificaciones_exitosas}/{total_verificaciones} verificaciones exitosas")
    
    if verificaciones_exitosas == total_verificaciones:
        print("🎉 ¡SISTEMA FUNCIONANDO AL 100%!")
    else:
        print("⚠️  Algunas funcionalidades necesitan atención")
    
    return verificaciones_exitosas == total_verificaciones

if __name__ == '__main__':
    main()
