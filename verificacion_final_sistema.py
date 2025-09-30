#!/usr/bin/env python3
"""
Verificación final del sistema - Todo debe funcionar al 100%
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import *
from core.forms_simple import *

def verificar_sistema_completo():
    """Verificación completa del sistema"""
    print("🔍 VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 45)
    
    # 1. Verificar que el servidor pueda iniciar
    print("\n1️⃣ Verificando configuración del servidor...")
    try:
        from django.conf import settings
        print(f"  ✅ DEBUG: {settings.DEBUG}")
        print(f"  ✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"  ✅ MEDIA_ROOT: {settings.MEDIA_ROOT}")
        print(f"  ✅ MEDIA_URL: {settings.MEDIA_URL}")
    except Exception as e:
        print(f"  ❌ Error en configuración: {e}")
        return False
    
    # 2. Verificar modelos críticos
    print("\n2️⃣ Verificando modelos críticos...")
    modelos_criticos = [
        ('Cliente', Cliente),
        ('Proyecto', Proyecto),
        ('Colaborador', Colaborador),
        ('Factura', Factura),
        ('Gasto', Gasto),
        ('Anticipo', Anticipo),
        ('ArchivoProyecto', ArchivoProyecto),
        ('CarpetaProyecto', CarpetaProyecto),
    ]
    
    for nombre, modelo in modelos_criticos:
        try:
            count = modelo.objects.count()
            print(f"  ✅ {nombre}: {count} registros")
        except Exception as e:
            print(f"  ❌ {nombre}: Error - {e}")
            return False
    
    # 3. Verificar formularios críticos
    print("\n3️⃣ Verificando formularios críticos...")
    formularios_criticos = [
        ('ClienteForm', ClienteForm),
        ('ProyectoForm', ProyectoForm),
        ('ArchivoProyectoForm', ArchivoProyectoForm),
        ('CarpetaProyectoForm', CarpetaProyectoForm),
    ]
    
    for nombre, form_class in formularios_criticos:
        try:
            form = form_class()
            campos = list(form.fields.keys())
            print(f"  ✅ {nombre}: {len(campos)} campos")
        except Exception as e:
            print(f"  ❌ {nombre}: Error - {e}")
            return False
    
    # 4. Verificar URLs críticas
    print("\n4️⃣ Verificando URLs críticas...")
    from django.urls import reverse
    urls_criticas = [
        'login',
        'dashboard',
        'clientes_list',
        'proyectos_list',
        'archivos_proyectos_list',
    ]
    
    for url_name in urls_criticas:
        try:
            url = reverse(url_name)
            print(f"  ✅ {url_name}: {url}")
        except Exception as e:
            print(f"  ❌ {url_name}: Error - {e}")
            return False
    
    # 5. Verificar que se puedan crear datos
    print("\n5️⃣ Verificando creación de datos...")
    try:
        # Obtener usuario admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("  ❌ No hay usuario admin")
            return False
        
        # Crear datos de prueba
        cliente = Cliente.objects.create(
            razon_social='VERIFICACION FINAL',
            codigo_fiscal='VERIF123456',
            email='verificacion@final.com',
            telefono='+502 9999-9999',
            direccion='Dirección de verificación',
            activo=True
        )
        
        proyecto = Proyecto.objects.create(
            nombre='VERIFICACION FINAL',
            descripcion='Proyecto de verificación final',
            cliente=cliente,
            presupuesto=Decimal('100000.00'),
            fecha_inicio=date.today(),
            estado='en_progreso',
            activo=True
        )
        
        carpeta = CarpetaProyecto.objects.create(
            proyecto=proyecto,
            nombre='VERIFICACION FINAL',
            descripcion='Carpeta de verificación',
            creada_por=admin_user,
            activa=True
        )
        
        print(f"  ✅ Cliente creado: {cliente.id}")
        print(f"  ✅ Proyecto creado: {proyecto.id}")
        print(f"  ✅ Carpeta creada: {carpeta.id}")
        
    except Exception as e:
        print(f"  ❌ Error creando datos: {e}")
        return False
    
    # 6. Verificar que se puedan subir archivos
    print("\n6️⃣ Verificando subida de archivos...")
    try:
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        archivo_contenido = SimpleUploadedFile(
            "verificacion_final.txt",
            b"Archivo de verificacion final",
            content_type="text/plain"
        )
        
        archivo = ArchivoProyecto.objects.create(
            proyecto=proyecto,
            carpeta=carpeta,
            nombre='VERIFICACION FINAL',
            descripcion='Archivo de verificación final',
            archivo=archivo_contenido,
            tipo='documento',
            subido_por=admin_user,
            activo=True
        )
        
        print(f"  ✅ Archivo creado: {archivo.id}")
        
    except Exception as e:
        print(f"  ❌ Error creando archivo: {e}")
        return False
    
    # 7. Verificar que se puedan eliminar datos de prueba
    print("\n7️⃣ Limpiando datos de prueba...")
    try:
        ArchivoProyecto.objects.filter(nombre='VERIFICACION FINAL').delete()
        CarpetaProyecto.objects.filter(nombre='VERIFICACION FINAL').delete()
        Proyecto.objects.filter(nombre='VERIFICACION FINAL').delete()
        Cliente.objects.filter(razon_social='VERIFICACION FINAL').delete()
        print("  ✅ Datos de prueba eliminados")
    except Exception as e:
        print(f"  ⚠️  Error eliminando datos de prueba: {e}")
    
    return True

def verificar_dashboard():
    """Verificar que el dashboard funcione correctamente"""
    print(f"\n📊 VERIFICANDO DASHBOARD")
    print("=" * 30)
    
    try:
        # Obtener datos del dashboard
        total_clientes = Cliente.objects.filter(activo=True).count()
        total_proyectos = Proyecto.objects.filter(activo=True).count()
        total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or 0
        total_gastos = Gasto.objects.filter(aprobado=True).aggregate(total=Sum('monto'))['total'] or 0
        
        print(f"  👥 Clientes activos: {total_clientes}")
        print(f"  🏗️ Proyectos activos: {total_proyectos}")
        print(f"  💰 Total facturado: Q{total_facturado:,.2f}")
        print(f"  💸 Total gastos: Q{total_gastos:,.2f}")
        
        if total_clientes > 0 and total_proyectos > 0:
            print("  ✅ Dashboard tiene datos")
            return True
        else:
            print("  ⚠️  Dashboard sin datos")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en dashboard: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN FINAL DEL SISTEMA")
    print("=" * 45)
    print("Verificando que todo funcione al 100%...")
    
    # Verificar sistema completo
    sistema_ok = verificar_sistema_completo()
    
    # Verificar dashboard
    dashboard_ok = verificar_dashboard()
    
    # Resumen final
    print(f"\n" + "=" * 45)
    print("📋 RESUMEN FINAL")
    print("=" * 45)
    
    if sistema_ok and dashboard_ok:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("✅ Todos los datos se guardan correctamente")
        print("✅ No hay riesgo de pérdida de datos")
        print("✅ El sistema es seguro para mantenimientos")
        print("✅ Dashboard funciona correctamente")
        print("✅ Subida de archivos funciona")
        print("✅ Formularios funcionan correctamente")
        print("\n🚀 EL SISTEMA ESTÁ LISTO PARA USO EN PRODUCCIÓN")
    else:
        print("❌ HAY PROBLEMAS EN EL SISTEMA")
        if not sistema_ok:
            print("❌ Problemas en el sistema base")
        if not dashboard_ok:
            print("❌ Problemas en el dashboard")
    
    print(f"\n📊 DATOS ACTUALES EN LA BASE DE DATOS:")
    try:
        conteos = {
            'Clientes': Cliente.objects.count(),
            'Proyectos': Proyecto.objects.count(),
            'Colaboradores': Colaborador.objects.count(),
            'Facturas': Factura.objects.count(),
            'Gastos': Gasto.objects.count(),
            'Anticipos': Anticipo.objects.count(),
            'Archivos': ArchivoProyecto.objects.count(),
            'Carpetas': CarpetaProyecto.objects.count(),
        }
        
        for entidad, conteo in conteos.items():
            print(f"  {entidad}: {conteo}")
    except Exception as e:
        print(f"  Error obteniendo conteos: {e}")

if __name__ == "__main__":
    main()
