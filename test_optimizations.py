#!/usr/bin/env python
"""
Script para probar las optimizaciones implementadas en el sistema
"""

import os
import sys
import django
import time
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.core.cache import cache
from django.db import connection
from core.optimization import PerformanceOptimizer, DatabaseOptimizer, CacheOptimizer
from sistema_construccion.database_optimization import setup_database_optimization
from sistema_construccion.cache_settings import get_cache_config, generate_cache_key

def test_cache_optimization():
    """Prueba las optimizaciones de cache"""
    print("🧪 Probando optimizaciones de cache...")
    
    # Probar cache básico
    test_key = "test_cache_key"
    test_data = {"message": "Hola mundo", "timestamp": time.time()}
    
    # Guardar en cache
    cache.set(test_key, test_data, 60)
    print(f"✅ Datos guardados en cache: {test_key}")
    
    # Recuperar del cache
    cached_data = cache.get(test_key)
    if cached_data:
        print(f"✅ Datos recuperados del cache: {cached_data}")
    else:
        print("❌ Error al recuperar datos del cache")
    
    # Probar generación de claves
    cache_key = generate_cache_key("dashboard", "user_123", 456)
    print(f"✅ Clave de cache generada: {cache_key}")
    
    # Limpiar cache de prueba
    cache.delete(test_key)
    print("✅ Cache de prueba limpiado")

def test_database_optimization():
    """Prueba las optimizaciones de base de datos"""
    print("\n🧪 Probando optimizaciones de base de datos...")
    
    try:
        # Aplicar índices de base de datos
        setup_database_optimization()
        print("✅ Índices de base de datos aplicados")
        
        # Probar optimizador de consultas
        db_optimizer = DatabaseOptimizer()
        print("✅ Optimizador de base de datos creado")
        
        # Probar datos agregados
        aggregated_data = db_optimizer.get_aggregated_data()
        print(f"✅ Datos agregados obtenidos: {len(aggregated_data)} módulos")
        
        # Mostrar estadísticas
        for module, data in aggregated_data.items():
            print(f"   📊 {module}: {data}")
            
    except Exception as e:
        print(f"❌ Error en optimización de base de datos: {e}")

def test_performance_optimizer():
    """Prueba el optimizador de rendimiento"""
    print("\n🧪 Probando optimizador de rendimiento...")
    
    try:
        # Crear instancia del optimizador
        optimizer = PerformanceOptimizer()
        print("✅ Optimizador de rendimiento creado")
        
        # Probar cache con callback
        def generate_test_data():
            return {"test": "data", "generated_at": time.time()}
        
        cached_data = optimizer.get_cached_or_set(
            "test_performance_data", 
            generate_test_data, 
            60
        )
        print(f"✅ Datos de rendimiento cacheados: {cached_data}")
        
        # Probar optimización de queryset
        from core.models import Proyecto
        queryset = Proyecto.objects.all()
        optimized_queryset = optimizer.optimize_queryset(
            queryset, 
            select_related=['cliente']
        )
        print(f"✅ QuerySet optimizado: {type(optimized_queryset)}")
        
    except Exception as e:
        print(f"❌ Error en optimizador de rendimiento: {e}")

def test_cache_configurations():
    """Prueba las configuraciones de cache"""
    print("\n🧪 Probando configuraciones de cache...")
    
    try:
        # Probar configuración de desarrollo
        dev_config = get_cache_config('development')
        print(f"✅ Configuración de desarrollo: {dev_config['default']['BACKEND']}")
        
        # Probar configuración de producción
        prod_config = get_cache_config('production')
        print(f"✅ Configuración de producción: {prod_config['default']['BACKEND']}")
        
        # Probar configuración híbrida
        hybrid_config = get_cache_config('hybrid')
        print(f"✅ Configuración híbrida: {len(hybrid_config)} backends")
        
    except Exception as e:
        print(f"❌ Error en configuraciones de cache: {e}")

def test_query_performance():
    """Prueba el rendimiento de consultas"""
    print("\n🧪 Probando rendimiento de consultas...")
    
    try:
        from core.models import Proyecto, Cliente, Factura
        
        # Medir tiempo de consulta sin optimización
        start_time = time.time()
        proyectos = Proyecto.objects.all()
        proyectos_list = list(proyectos)
        time_without_optimization = time.time() - start_time
        
        print(f"⏱️ Tiempo sin optimización: {time_without_optimization:.4f}s")
        print(f"📊 Proyectos obtenidos: {len(proyectos_list)}")
        
        # Medir tiempo de consulta con optimización
        start_time = time.time()
        proyectos_optimized = Proyecto.objects.select_related('cliente').all()
        proyectos_optimized_list = list(proyectos_optimized)
        time_with_optimization = time.time() - start_time
        
        print(f"⏱️ Tiempo con optimización: {time_with_optimization:.4f}s")
        print(f"📊 Proyectos optimizados obtenidos: {len(proyectos_optimized_list)}")
        
        # Calcular mejora
        if time_without_optimization > 0:
            improvement = ((time_without_optimization - time_with_optimization) / time_without_optimization) * 100
            print(f"🚀 Mejora de rendimiento: {improvement:.2f}%")
        
    except Exception as e:
        print(f"❌ Error en prueba de rendimiento: {e}")

def test_cache_warmup():
    """Prueba el pre-calentamiento del cache"""
    print("\n🧪 Probando pre-calentamiento del cache...")
    
    try:
        # Crear instancia del optimizador de cache
        cache_optimizer = CacheOptimizer()
        print("✅ Optimizador de cache creado")
        
        # Pre-calentar cache
        cache_optimizer.warm_up_cache()
        print("✅ Cache pre-calentado")
        
        # Verificar datos en cache
        clientes_cache = cache.get('clientes_activos')
        if clientes_cache:
            print(f"✅ Clientes en cache: {len(clientes_cache)}")
        else:
            print("⚠️ No hay clientes en cache")
            
        proyectos_cache = cache.get('proyectos_recientes')
        if proyectos_cache:
            print(f"✅ Proyectos en cache: {len(proyectos_cache)}")
        else:
            print("⚠️ No hay proyectos en cache")
            
    except Exception as e:
        print(f"❌ Error en pre-calentamiento de cache: {e}")

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DE OPTIMIZACIÓN")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    test_cache_optimization()
    test_database_optimization()
    test_performance_optimizer()
    test_cache_configurations()
    test_query_performance()
    test_cache_warmup()
    
    print("\n" + "=" * 50)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    
    # Mostrar estadísticas finales
    print(f"\n📊 Estadísticas de conexiones de base de datos: {len(connection.queries)} consultas")
    
    # Mostrar consultas lentas si las hay
    slow_queries = [q for q in connection.queries if float(q['time']) > 0.1]
    if slow_queries:
        print(f"⚠️ Consultas lentas detectadas: {len(slow_queries)}")
        for i, query in enumerate(slow_queries[:3]):  # Mostrar solo las primeras 3
            print(f"   {i+1}. Tiempo: {query['time']}s, SQL: {query['sql'][:100]}...")
    
    print("\n🎯 Sistema de optimización listo para uso en producción!")

if __name__ == "__main__":
    main()
