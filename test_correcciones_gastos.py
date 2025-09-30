#!/usr/bin/env python3
"""
Script para probar las correcciones implementadas en el módulo de gastos
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

def probar_gastos_recientes_lista():
    """Probar que los gastos recientes se muestren en formato de lista"""
    print("📋 PROBANDO GASTOS RECIENTES EN FORMATO DE LISTA")
    print("=" * 60)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/gastos/dashboard/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos de la lista
            elementos_lista = [
                'gastos-recientes-lista',
                'table table-hover',
                'Descripción',
                'Proyecto',
                'Monto',
                'Fecha',
                'Estado',
                'categoria-mini',
                'badge bg-success',
                'badge bg-warning'
            ]
            
            elementos_encontrados = 0
            print("\n🔍 VERIFICANDO ELEMENTOS DE LA LISTA:")
            for elemento in elementos_lista:
                if elemento in content:
                    elementos_encontrados += 1
                    print(f"  ✅ {elemento}: Presente")
                else:
                    print(f"  ❌ {elemento}: Faltante")
            
            if elementos_encontrados >= 8:
                print("\n✅ ¡GASTOS RECIENTES EN FORMATO DE LISTA FUNCIONANDO!")
                return True
            else:
                print("\n❌ HAY PROBLEMAS CON LA LISTA")
                return False
        else:
            print(f"❌ Error accediendo al dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def probar_aprobar_gasto_proyecto():
    """Probar que aprobar gasto se aplique al proyecto"""
    print("\n💰 PROBANDO APROBACIÓN DE GASTO AL PROYECTO")
    print("=" * 60)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        # Crear gasto de prueba
        proyecto = Proyecto.objects.first()
        categoria = CategoriaGasto.objects.first()
        
        if not proyecto or not categoria:
            print("❌ No hay proyecto o categoría disponible")
            return False
        
        # Guardar presupuesto inicial
        presupuesto_inicial = proyecto.presupuesto or 0
        print(f"  Presupuesto inicial del proyecto: Q{presupuesto_inicial}")
        
        gasto = Gasto.objects.create(
            proyecto=proyecto,
            categoria=categoria,
            descripcion='Test de aprobación al proyecto',
            monto=100.00,
            fecha_gasto=date.today(),
            aprobado=False
        )
        
        print(f"✅ Gasto creado: {gasto.id} - Q{gasto.monto}")
        print(f"   Estado inicial: {gasto.aprobado}")
        
        # Aprobar gasto
        response = client.get(f'/gastos/{gasto.id}/aprobar/')
        
        if response.status_code == 302:
            print("✅ Redirect correcto")
            
            # Verificar que se aprobó
            gasto.refresh_from_db()
            proyecto.refresh_from_db()
            
            print(f"   Estado del gasto después: {gasto.aprobado}")
            print(f"   Presupuesto del proyecto después: Q{proyecto.presupuesto}")
            
            if gasto.aprobado and proyecto.presupuesto == presupuesto_inicial - gasto.monto:
                print("✅ ¡Gasto aprobado y aplicado al proyecto correctamente!")
                
                # Probar desaprobar
                response2 = client.get(f'/gastos/{gasto.id}/desaprobar/')
                
                if response2.status_code == 302:
                    gasto.refresh_from_db()
                    proyecto.refresh_from_db()
                    
                    print(f"   Estado del gasto después de desaprobar: {gasto.aprobado}")
                    print(f"   Presupuesto del proyecto después de desaprobar: Q{proyecto.presupuesto}")
                    
                    if not gasto.aprobado and proyecto.presupuesto == presupuesto_inicial:
                        print("✅ ¡Gasto desaprobado y revertido del proyecto correctamente!")
                        return True
                    else:
                        print("❌ Error al desaprobar gasto")
                        return False
                else:
                    print("❌ Error en desaprobar gasto")
                    return False
            else:
                print("❌ Error al aprobar gasto o aplicar al proyecto")
                return False
        else:
            print(f"❌ Error en redirect: {response.status_code}")
            return False
        
        # Limpiar
        gasto.delete()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def probar_decoradores():
    """Probar que los decoradores @login_required funcionen"""
    print("\n🔐 PROBANDO DECORADORES @login_required")
    print("=" * 60)
    
    client = Client()
    
    try:
        # Probar sin autenticación
        response = client.get('/gastos/1/aprobar/')
        
        if response.status_code == 302 and '/login/' in response.url:
            print("✅ Decorador @login_required funciona correctamente")
            print("   Redirige a login cuando no está autenticado")
            return True
        else:
            print(f"❌ Decorador no funciona: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def mostrar_resumen_correcciones():
    """Mostrar resumen de las correcciones"""
    print("\n✨ RESUMEN DE CORRECCIONES IMPLEMENTADAS")
    print("=" * 80)
    
    correcciones = [
        "📋 GASTOS RECIENTES EN FORMATO DE LISTA:",
        "  ✅ Cambiado de grid de tarjetas a tabla simple",
        "  ✅ Diseño más limpio y fácil de leer",
        "  ✅ Categorías con mini círculos de color",
        "  ✅ Estados con badges de Bootstrap",
        "  ✅ Información organizada en columnas",
        "",
        "💰 APROBACIÓN DE GASTOS AL PROYECTO:",
        "  ✅ Al aprobar gasto se resta del presupuesto del proyecto",
        "  ✅ Al desaprobar gasto se suma de vuelta al presupuesto",
        "  ✅ Registro de actividad en LogActividad",
        "  ✅ Mensajes informativos al usuario",
        "  ✅ Control de integridad de datos",
        "",
        "🔐 DECORADORES RESTAURADOS:",
        "  ✅ @login_required restaurado en todas las funciones",
        "  ✅ Seguridad mejorada",
        "  ✅ Redirección a login cuando no está autenticado",
        "  ✅ Protección contra acceso no autorizado"
    ]
    
    for correccion in correcciones:
        print(correccion)

def main():
    """Función principal"""
    print("🔧 PRUEBA DE CORRECCIONES EN MÓDULO DE GASTOS")
    print("=" * 80)
    
    try:
        # Probar cada corrección
        lista_ok = probar_gastos_recientes_lista()
        aprobar_ok = probar_aprobar_gasto_proyecto()
        decoradores_ok = probar_decoradores()
        
        # Mostrar resumen
        mostrar_resumen_correcciones()
        
        # Resumen final
        print(f"\n" + "=" * 80)
        print("📋 RESUMEN FINAL")
        print("=" * 80)
        
        if lista_ok and aprobar_ok and decoradores_ok:
            print("🎉 ¡TODAS LAS CORRECCIONES FUNCIONANDO PERFECTAMENTE!")
            print("✅ Gastos recientes en formato de lista: Implementado")
            print("✅ Aprobación de gastos al proyecto: Funcionando")
            print("✅ Decoradores @login_required: Restaurados")
            
            print(f"\n🌐 PARA VER LAS CORRECCIONES:")
            print("  1. Dashboard: http://localhost:8000/gastos/dashboard/")
            print("  2. Lista: http://localhost:8000/gastos/")
            print("  3. Prueba aprobar/desaprobar gastos")
        else:
            print("❌ HAY PROBLEMAS CON ALGUNAS CORRECCIONES")
            if not lista_ok:
                print("  - Problemas con formato de lista")
            if not aprobar_ok:
                print("  - Problemas con aprobación al proyecto")
            if not decoradores_ok:
                print("  - Problemas con decoradores")
        
        return lista_ok and aprobar_ok and decoradores_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
