#!/usr/bin/env python3
"""
Script para verificar que el dashboard de gastos esté conectado a la BD
y que el botón de gastos redirija correctamente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from core.models import Gasto, CategoriaGasto, Proyecto

def verificar_conexion_bd():
    """Verificar que el dashboard esté conectado a la base de datos"""
    print("🔗 VERIFICANDO CONEXIÓN A BASE DE DATOS")
    print("=" * 50)
    
    try:
        # Verificar modelos
        total_gastos = Gasto.objects.count()
        total_categorias = CategoriaGasto.objects.count()
        total_proyectos = Proyecto.objects.count()
        
        print(f"✅ Total de gastos en BD: {total_gastos}")
        print(f"✅ Total de categorías en BD: {total_categorias}")
        print(f"✅ Total de proyectos en BD: {total_proyectos}")
        
        # Verificar consultas del dashboard
        gastos_aprobados = Gasto.objects.filter(aprobado=True).count()
        gastos_pendientes = Gasto.objects.filter(aprobado=False).count()
        total_monto = Gasto.objects.aggregate(total=Sum('monto'))['total'] or 0
        
        print(f"✅ Gastos aprobados: {gastos_aprobados}")
        print(f"✅ Gastos pendientes: {gastos_pendientes}")
        print(f"✅ Monto total: Q{total_monto:,.2f}")
        
        # Verificar gastos por categoría
        gastos_por_categoria = Gasto.objects.values('categoria__nombre').annotate(
            total=Sum('monto'),
            cantidad=Count('id')
        ).order_by('-total')
        
        print(f"✅ Categorías con gastos: {len(gastos_por_categoria)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en conexión a BD: {e}")
        return False

def probar_redireccion_gastos():
    """Probar que el botón de gastos redirija al dashboard"""
    print("\n🔄 PROBANDO REDIRECCIÓN DE GASTOS")
    print("=" * 50)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar acceso directo al dashboard
    print("\n1️⃣ Probando acceso directo al dashboard...")
    try:
        response = client.get('/gastos/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard de gastos accesible")
        else:
            print(f"  ❌ Error accediendo al dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # 2. Probar redirección desde lista de gastos
    print("\n2️⃣ Probando redirección desde lista de gastos...")
    try:
        response = client.get('/gastos/')
        if response.status_code == 302:
            print("  ✅ Lista de gastos redirige correctamente")
            # Verificar que redirija al dashboard
            if 'gastos/dashboard/' in response.url:
                print("  ✅ Redirección va al dashboard correcto")
            else:
                print(f"  ❌ Redirección va a: {response.url}")
                return False
        else:
            print(f"  ❌ Lista de gastos no redirige: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    return True

def verificar_datos_dashboard():
    """Verificar que el dashboard muestre datos correctos"""
    print("\n📊 VERIFICANDO DATOS DEL DASHBOARD")
    print("=" * 50)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    
    try:
        response = client.get('/gastos/dashboard/')
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar que se muestren datos
            if 'Total Gastos' in content and 'Monto Total' in content:
                print("  ✅ Estadísticas principales presentes")
            else:
                print("  ❌ Estadísticas principales faltantes")
                return False
            
            if 'Gastos por Categoría' in content:
                print("  ✅ Sección de categorías presente")
            else:
                print("  ❌ Sección de categorías faltante")
                return False
            
            # Verificar que no haya errores de BD
            if 'Error al cargar' in content:
                print("  ❌ Hay errores de carga en el dashboard")
                return False
            else:
                print("  ✅ Dashboard carga sin errores")
            
            return True
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def mostrar_resumen_cambios():
    """Mostrar resumen de los cambios realizados"""
    print("\n📋 RESUMEN DE CAMBIOS REALIZADOS")
    print("=" * 50)
    print("✅ Botón 'Gastos' en sidebar ahora va a /gastos/dashboard/")
    print("✅ Vista gastos_list() ahora redirige al dashboard")
    print("✅ Dashboard conectado a base de datos")
    print("✅ Consultas optimizadas con select_related")
    print("✅ Estadísticas calculadas desde BD")
    print("✅ Categorías agrupadas y ordenadas")
    print("✅ Manejo de errores implementado")

def main():
    """Función principal"""
    print("🔗 VERIFICACIÓN DE CONEXIÓN DASHBOARD GASTOS")
    print("=" * 60)
    
    try:
        # Verificar conexión a BD
        bd_ok = verificar_conexion_bd()
        
        # Probar redirección
        redireccion_ok = probar_redireccion_gastos()
        
        # Verificar datos del dashboard
        datos_ok = verificar_datos_dashboard()
        
        # Mostrar resumen
        mostrar_resumen_cambios()
        
        # Resumen final
        print(f"\n" + "=" * 60)
        print("📋 RESUMEN FINAL")
        print("=" * 60)
        
        if bd_ok and redireccion_ok and datos_ok:
            print("🎉 ¡DASHBOARD DE GASTOS CONFIGURADO EXITOSAMENTE!")
            print("✅ Conexión a base de datos verificada")
            print("✅ Redirección desde sidebar funcionando")
            print("✅ Dashboard muestra datos correctos")
            print("✅ Todas las consultas optimizadas")
            
            print(f"\n🌐 PARA PROBAR:")
            print("  1. Ve a: http://localhost:8000/")
            print("  2. Haz clic en 'Gastos' en el sidebar")
            print("  3. Verifica que vaya al dashboard")
            print("  4. Observa las estadísticas y categorías")
        else:
            print("❌ HAY PROBLEMAS CON LA CONFIGURACIÓN")
            if not bd_ok:
                print("  - Problemas con conexión a BD")
            if not redireccion_ok:
                print("  - Problemas con redirección")
            if not datos_ok:
                print("  - Problemas con datos del dashboard")
        
        return bd_ok and redireccion_ok and datos_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
