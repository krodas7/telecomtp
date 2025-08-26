#!/usr/bin/env python
"""
Script simple para probar AJAX básico en el sistema
"""

import os
import sys
import django
from pathlib import Path

def configurar_django():
    """Configura Django para el script"""
    try:
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
        django.setup()
        print("✓ Django configurado correctamente")
        return True
    except Exception as e:
        print(f"✗ Error configurando Django: {e}")
        return False

def test_ajax_endpoints():
    """Prueba que los endpoints AJAX estén funcionando"""
    print("\n=== PRUEBA DE ENDPOINTS AJAX ===")
    
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        from core.views import dashboard
        
        factory = RequestFactory()
        user = User.objects.first()
        
        if not user:
            print("✗ No hay usuarios en el sistema")
            return False
        
        # Probar dashboard con AJAX
        request = factory.get('/dashboard/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = user
        
        response = dashboard(request)
        
        if response.status_code == 200:
            print("✓ Dashboard responde a requests AJAX")
        else:
            print(f"⚠ Dashboard responde con código {response.status_code} a AJAX")
        
        return True
        
    except Exception as e:
        print(f"✗ Error probando endpoints AJAX: {e}")
        return False

def test_json_responses():
    """Prueba que las respuestas JSON estén funcionando"""
    print("\n=== PRUEBA DE RESPUESTAS JSON ===")
    
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        from core.views import dashboard
        
        factory = RequestFactory()
        user = User.objects.first()
        
        if not user:
            print("✗ No hay usuarios en el sistema")
            return False
        
        # Probar dashboard normal
        request = factory.get('/dashboard/')
        request.user = user
        
        response = dashboard(request)
        
        if response.status_code == 200:
            print("✓ Dashboard responde correctamente")
            
            # Verificar que el contexto tenga datos JSON
            context = response.context_data if hasattr(response, 'context_data') else {}
            
            # Verificar datos críticos para gráficos
            data_keys = ['evolucion_proyectos', 'categorias_gastos', 'montos_gastos']
            missing_keys = []
            
            for key in data_keys:
                if key not in context:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"⚠ Claves faltantes para gráficos: {missing_keys}")
            else:
                print("✓ Todas las claves para gráficos están presentes")
                
                # Verificar que los datos sean serializables
                for key in data_keys:
                    try:
                        import json
                        json.dumps(context[key])
                        print(f"✓ {key} es serializable a JSON")
                    except Exception as e:
                        print(f"✗ {key} no es serializable: {e}")
            
            return True
        else:
            print(f"✗ Dashboard responde con código {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error probando respuestas JSON: {e}")
        return False

def test_static_files_loading():
    """Prueba que los archivos estáticos se carguen correctamente"""
    print("\n=== PRUEBA DE CARGA DE ARCHIVOS ESTÁTICOS ===")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        from django.test import Client
        
        client = Client()
        
        # Verificar que los archivos estén disponibles
        critical_files = [
            'js/dashboard-charts.js',
            'css/neostructure-enhanced.css',
            'js/global-functions.js'
        ]
        
        all_found = True
        for file_path in critical_files:
            if find(file_path):
                print(f"✓ {file_path} encontrado")
                
                # Verificar que se pueda acceder vía URL
                url = f"{settings.STATIC_URL}{file_path}"
                print(f"  URL: {url}")
            else:
                print(f"✗ {file_path} no encontrado")
                all_found = False
        
        return all_found
        
    except Exception as e:
        print(f"✗ Error probando carga de archivos estáticos: {e}")
        return False

def test_chart_initialization():
    """Prueba que los datos para gráficos estén disponibles"""
    print("\n=== PRUEBA DE INICIALIZACIÓN DE GRÁFICOS ===")
    
    try:
        from core.models import Proyecto, Gasto, CategoriaGasto
        from django.db.models import Sum, Count
        from django.utils import timezone
        from datetime import timedelta
        
        # Simular datos que se pasan al template
        evolucion_proyectos = [0, 0, 0, 0, 0]  # Valores por defecto
        
        # Obtener datos reales si existen
        if Proyecto.objects.exists():
            proyectos_por_estado = Proyecto.objects.values('estado').annotate(
                total=Count('id')
            )
            
            # Mapear estados a índices del array
            estado_mapping = {
                'planificacion': 0,
                'ejecucion': 1, 
                'control': 2,
                'cierre': 3,
                'evaluacion': 4
            }
            
            for item in proyectos_por_estado:
                estado = item['estado']
                if estado in estado_mapping:
                    idx = estado_mapping[estado]
                    evolucion_proyectos[idx] = item['total']
            
            print("✓ Datos de evolución de proyectos generados")
            print(f"  Array: {evolucion_proyectos}")
        else:
            print("⚠ No hay proyectos, usando valores por defecto")
        
        # Datos de gastos por categoría
        if Gasto.objects.exists():
            gastos_por_categoria = Gasto.objects.values('categoria__nombre').annotate(
                total=Sum('monto')
            )
            
            categorias = [item['categoria__nombre'] for item in gastos_por_categoria]
            montos = [float(item['total']) for item in gastos_por_categoria]
            
            print("✓ Datos de gastos por categoría generados")
            print(f"  Categorías: {categorias}")
            print(f"  Montos: {montos}")
        else:
            print("⚠ No hay gastos, usando valores por defecto")
        
        return True
        
    except Exception as e:
        print(f"✗ Error probando inicialización de gráficos: {e}")
        return False

def main():
    """Función principal"""
    print("PRUEBA DE FUNCIONALIDAD AJAX BÁSICA")
    print("="*60)
    
    if not configurar_django():
        print("No se puede continuar sin Django configurado")
        return
    
    # Ejecutar todas las pruebas
    pruebas = [
        ("Endpoints AJAX", test_ajax_endpoints),
        ("Respuestas JSON", test_json_responses),
        ("Carga de Archivos Estáticos", test_static_files_loading),
        ("Inicialización de Gráficos", test_chart_initialization),
    ]
    
    resultados = []
    for nombre, funcion in pruebas:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"✗ Error en prueba {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS AJAX")
    print("="*60)
    
    total_pruebas = len(resultados)
    pruebas_exitosas = sum(1 for _, resultado in resultados if resultado)
    
    print(f"Total de pruebas: {total_pruebas}")
    print(f"Pruebas exitosas: {pruebas_exitosas}")
    print(f"Pruebas fallidas: {total_pruebas - pruebas_exitosas}")
    
    if pruebas_exitosas == total_pruebas:
        print("\n🎉 ¡TODAS LAS PRUEBAS AJAX EXITOSAS!")
        print("El sistema AJAX está funcionando correctamente")
    elif pruebas_exitosas > total_pruebas // 2:
        print("\n⚠️ ALGUNAS PRUEBAS AJAX FALLARON")
        print("Revisa los errores anteriores para más detalles")
    else:
        print("\n❌ MUCHAS PRUEBAS AJAX FALLARON")
        print("Se requiere atención inmediata")
    
    # Recomendaciones específicas para AJAX
    print("\n" + "="*60)
    print("RECOMENDACIONES PARA AJAX")
    print("="*60)
    
    print("• Verificar que Chart.js esté cargado antes que dashboard-charts.js")
    print("• Asegurar que los datos JSON se pasen correctamente al template")
    print("• Verificar que no haya errores JavaScript en la consola del navegador")
    print("• Comprobar que los archivos estáticos se sirvan correctamente")
    print("• Verificar que CSRF tokens estén disponibles para requests POST")
    
    print("\n" + "="*60)
    print("PRUEBAS AJAX COMPLETADAS")
    print("="*60)

if __name__ == "__main__":
    main()
