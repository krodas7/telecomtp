#!/usr/bin/env python3
"""
VERIFICACIÓN COMPLETA DEL SISTEMA ARCA
=====================================
"""

import os
import django
import requests
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import *
from django.contrib.auth.models import User
from decimal import Decimal

def verificar_base_datos():
    """Verificar estado de la base de datos"""
    print("🔍 VERIFICANDO BASE DE DATOS")
    print("=" * 40)
    
    try:
        # Verificar datos básicos
        datos = {
            'usuarios': User.objects.count(),
            'clientes': Cliente.objects.count(),
            'proyectos': Proyecto.objects.count(),
            'facturas': Factura.objects.count(),
            'gastos': Gasto.objects.count(),
            'anticipos': Anticipo.objects.count(),
            'colaboradores': Colaborador.objects.count(),
            'archivos': ArchivoProyecto.objects.count(),
            'trabajadores_diarios': TrabajadorDiario.objects.count(),
        }
        
        for nombre, cantidad in datos.items():
            print(f"  📊 {nombre.capitalize()}: {cantidad}")
        
        # Verificar si hay datos
        total_datos = sum(datos.values())
        if total_datos > 0:
            print(f"✅ Base de datos tiene {total_datos} registros")
            return True
        else:
            print("⚠️  Base de datos vacía")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando BD: {e}")
        return False

def verificar_dashboard():
    """Verificar funcionamiento del dashboard"""
    print("\n🔍 VERIFICANDO DASHBOARD")
    print("=" * 40)
    
    try:
        # Probar dashboard directamente
        from core.views import dashboard
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Crear usuario de prueba
        user, created = User.objects.get_or_create(
            username='test_dashboard',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Crear request
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = user
        
        # Ejecutar dashboard
        response = dashboard(request)
        
        if response.status_code == 200:
            print("✅ Dashboard ejecuta correctamente")
            
            # Verificar contexto
            if hasattr(response, 'context_data'):
                context = response.context_data
                print(f"📊 Contexto disponible: {len(context)} elementos")
                
                # Verificar datos específicos
                datos_importantes = [
                    'total_proyectos', 'total_clientes', 'total_facturado', 
                    'total_cobrado', 'proyectos_rentables'
                ]
                
                for dato in datos_importantes:
                    if dato in context:
                        valor = context[dato]
                        print(f"  📈 {dato}: {valor}")
                    else:
                        print(f"  ⚠️  {dato}: No disponible")
            
            return True
        else:
            print(f"❌ Dashboard error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en dashboard: {e}")
        import traceback
        traceback.print_exc()
        return False

def verificar_servidor():
    """Verificar si el servidor está funcionando"""
    print("\n🔍 VERIFICANDO SERVIDOR")
    print("=" * 40)
    
    try:
        # Intentar conectar al servidor
        response = requests.get('http://localhost:8000/', timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor funcionando")
            
            # Probar dashboard via HTTP
            dashboard_response = requests.get('http://localhost:8000/dashboard/', timeout=5)
            if dashboard_response.status_code == 200:
                print("✅ Dashboard accesible via HTTP")
                
                # Verificar si hay errores en el contenido
                contenido = dashboard_response.text
                if "contexto de emergencia" in contenido:
                    print("⚠️  Dashboard usando contexto de emergencia")
                    return False
                elif "Error" in contenido:
                    print("⚠️  Dashboard tiene errores")
                    return False
                else:
                    print("✅ Dashboard muestra datos correctamente")
                    return True
            else:
                print(f"❌ Dashboard no accesible: {dashboard_response.status_code}")
                return False
        else:
            print(f"❌ Servidor error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor no está corriendo")
        return False
    except Exception as e:
        print(f"❌ Error verificando servidor: {e}")
        return False

def crear_datos_prueba():
    """Crear datos de prueba si no existen"""
    print("\n🔍 CREANDO DATOS DE PRUEBA")
    print("=" * 40)
    
    try:
        # Verificar si ya hay datos
        if Cliente.objects.count() > 0:
            print("✅ Ya hay datos en el sistema")
            return True
        
        # Crear cliente
        cliente = Cliente.objects.create(
            razon_social='Cliente de Prueba',
            codigo_fiscal='12345678-9',
            telefono='1234-5678',
            email='cliente@prueba.com',
            direccion='Dirección de prueba',
            activo=True
        )
        print(f"✅ Cliente creado: {cliente.razon_social}")
        
        # Crear proyecto
        proyecto = Proyecto.objects.create(
            nombre='Proyecto de Prueba',
            cliente=cliente,
            descripcion='Proyecto de prueba para testing',
            presupuesto=100000.00,
            fecha_inicio='2025-01-01',
            fecha_fin='2025-12-31',
            estado='en_progreso',
            activo=True
        )
        print(f"✅ Proyecto creado: {proyecto.nombre}")
        
        # Crear categoría de gasto
        categoria = CategoriaGasto.objects.create(
            nombre='Materiales',
            descripcion='Gastos en materiales de construcción',
            color='#FF5733',
            icono='fas fa-hammer',
            activa=True
        )
        print(f"✅ Categoría creada: {categoria.nombre}")
        
        # Crear gasto
        gasto = Gasto.objects.create(
            proyecto=proyecto,
            categoria=categoria,
            descripcion='Compra de cemento',
            monto=5000.00,
            fecha_gasto='2025-09-30',
            aprobado=True
        )
        print(f"✅ Gasto creado: {gasto.descripcion}")
        
        print("✅ Datos de prueba creados exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        return False

def generar_reporte_final():
    """Generar reporte final del estado"""
    print("\n📋 REPORTE FINAL DEL SISTEMA")
    print("=" * 50)
    
    # Verificar componentes
    bd_ok = verificar_base_datos()
    dashboard_ok = verificar_dashboard()
    servidor_ok = verificar_servidor()
    
    # Crear datos si es necesario
    if not bd_ok:
        crear_datos_prueba()
        bd_ok = verificar_base_datos()
    
    # Estado general
    estado_general = "✅ FUNCIONANDO" if all([bd_ok, dashboard_ok, servidor_ok]) else "⚠️  CON PROBLEMAS"
    
    print(f"\n🎯 ESTADO GENERAL: {estado_general}")
    print(f"📊 Base de datos: {'✅' if bd_ok else '❌'}")
    print(f"📊 Dashboard: {'✅' if dashboard_ok else '❌'}")
    print(f"📊 Servidor: {'✅' if servidor_ok else '❌'}")
    
    if all([bd_ok, dashboard_ok, servidor_ok]):
        print("\n🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("🌐 Accede a: http://localhost:8000/")
        print("📊 Dashboard: http://localhost:8000/dashboard/")
    else:
        print("\n⚠️  SISTEMA REQUIERE ATENCIÓN")
        if not bd_ok:
            print("  - Verificar base de datos")
        if not dashboard_ok:
            print("  - Corregir errores en dashboard")
        if not servidor_ok:
            print("  - Verificar servidor")

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN COMPLETA DEL SISTEMA ARCA")
    print("=" * 60)
    
    generar_reporte_final()

if __name__ == "__main__":
    main()
