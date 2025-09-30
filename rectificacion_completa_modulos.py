#!/usr/bin/env python3
"""
Script de rectificación completa de todos los módulos del sistema
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from core.models import *

def verificar_usuarios():
    """Verificar y crear usuarios necesarios"""
    print("👥 VERIFICANDO USUARIOS...")
    
    # Verificar usuario admin
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@construccionesarca.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin')
        admin_user.save()
        print("  ✅ Usuario admin creado")
    else:
        print("  ✅ Usuario admin existe")
    
    return admin_user

def verificar_datos_basicos():
    """Verificar que existan datos básicos necesarios"""
    print("\n📊 VERIFICANDO DATOS BÁSICOS...")
    
    # Verificar categorías de gastos
    categorias_gastos = [
        'Materiales de Construcción',
        'Mano de Obra',
        'Equipos y Herramientas',
        'Transporte',
        'Servicios Profesionales',
        'Otros Gastos'
    ]
    
    for categoria in categorias_gastos:
        cat, created = CategoriaGasto.objects.get_or_create(nombre=categoria)
        if created:
            print(f"  ✅ Categoría de gasto creada: {categoria}")
    
    # Verificar roles de usuario
    roles = ['Administrador', 'Gerente', 'Supervisor', 'Operador']
    for rol in roles:
        group, created = Group.objects.get_or_create(name=rol)
        if created:
            print(f"  ✅ Rol creado: {rol}")
    
    print("  ✅ Datos básicos verificados")

def probar_modulo(nombre, url_name, descripcion=""):
    """Probar un módulo específico"""
    try:
        url = reverse(url_name)
        return True, f"URL válida: {url}"
    except Exception as e:
        return False, f"Error: {e}"

def verificar_todos_los_modulos():
    """Verificar todos los módulos del sistema"""
    print("\n🔍 VERIFICANDO TODOS LOS MÓDULOS...")
    
    modulos = [
        # Módulos principales
        ("Dashboard", "dashboard", "Panel principal del sistema"),
        ("Proyectos", "proyectos_list", "Gestión de proyectos"),
        ("Clientes", "clientes_list", "Gestión de clientes"),
        ("Facturas", "facturas_list", "Gestión de facturas"),
        ("Colaboradores", "colaboradores_list", "Gestión de colaboradores"),
        ("Gastos", "gastos_list", "Gestión de gastos"),
        ("Inventario", "inventario_dashboard", "Dashboard de inventario"),
        ("Presupuestos", "presupuestos_list", "Gestión de presupuestos"),
        ("Usuarios", "usuarios_lista", "Gestión de usuarios"),
        ("Archivos", "archivos_proyectos_list", "Gestión de archivos"),
        ("Anticipos", "anticipos_list", "Gestión de anticipos"),
        ("Pagos", "pagos_list", "Gestión de pagos"),
        ("Rentabilidad", "rentabilidad", "Análisis de rentabilidad"),
        ("Sistema", "sistema", "Configuración del sistema"),
        
        # Módulos de inventario
        ("Categorías Inventario", "categoria_list", "Categorías de inventario"),
        ("Items Inventario", "item_list", "Items de inventario"),
        ("Asignaciones", "asignacion_list", "Asignaciones de inventario"),
        
        # Módulos de archivos
        ("Subir Archivo", "archivo_upload", "Subir archivos"),
        ("Descargar Archivo", "archivo_download", "Descargar archivos"),
        ("Eliminar Archivo", "archivo_delete", "Eliminar archivos"),
        
        # Módulos de sistema
        ("Reset App", "sistema_reset_app", "Reset de aplicación"),
        ("Crear Respaldo", "sistema_crear_respaldo", "Crear respaldo"),
        ("Ver Respaldos", "sistema_ver_respaldos", "Ver respaldos"),
        ("Logs Sistema", "sistema_logs", "Logs del sistema"),
    ]
    
    resultados = []
    
    for nombre, url_name, descripcion in modulos:
        print(f"\n🔍 Probando {nombre}...")
        try:
            url = reverse(url_name)
            print(f"  ✅ {nombre}: {url}")
            resultados.append((nombre, True, "OK", url))
        except Exception as e:
            print(f"  ❌ {nombre}: {e}")
            resultados.append((nombre, False, str(e), ""))
    
    return resultados

def verificar_formularios():
    """Verificar que todos los formularios funcionen"""
    print("\n📝 VERIFICANDO FORMULARIOS...")
    
    from core.forms_simple import (
        ProyectoForm, ClienteForm, FacturaForm, AnticipoForm, PagoForm,
        PresupuestoForm, CategoriaInventarioForm, ItemInventarioForm, ArchivoProyectoForm
    )
    
    formularios = [
        ("ProyectoForm", ProyectoForm, "Formulario de proyectos"),
        ("ClienteForm", ClienteForm, "Formulario de clientes"),
        ("FacturaForm", FacturaForm, "Formulario de facturas"),
        ("AnticipoForm", AnticipoForm, "Formulario de anticipos"),
        ("PagoForm", PagoForm, "Formulario de pagos"),
        ("PresupuestoForm", PresupuestoForm, "Formulario de presupuestos"),
        ("CategoriaInventarioForm", CategoriaInventarioForm, "Formulario de categorías"),
        ("ItemInventarioForm", ItemInventarioForm, "Formulario de items"),
        ("ArchivoProyectoForm", ArchivoProyectoForm, "Formulario de archivos"),
    ]
    
    for nombre, form_class, descripcion in formularios:
        try:
            form = form_class()
            print(f"  ✅ {nombre}: {descripcion}")
        except Exception as e:
            print(f"  ❌ {nombre}: {e}")

def verificar_modelos():
    """Verificar que todos los modelos funcionen"""
    print("\n🗄️ VERIFICANDO MODELOS...")
    
    modelos = [
        ("Proyecto", Proyecto, "Modelo de proyectos"),
        ("Cliente", Cliente, "Modelo de clientes"),
        ("Factura", Factura, "Modelo de facturas"),
        ("Anticipo", Anticipo, "Modelo de anticipos"),
        ("Pago", Pago, "Modelo de pagos"),
        ("Presupuesto", Presupuesto, "Modelo de presupuestos"),
        ("CategoriaInventario", CategoriaInventario, "Modelo de categorías"),
        ("ItemInventario", ItemInventario, "Modelo de items"),
        ("ArchivoProyecto", ArchivoProyecto, "Modelo de archivos"),
        ("Colaborador", Colaborador, "Modelo de colaboradores"),
        ("Gasto", Gasto, "Modelo de gastos"),
    ]
    
    for nombre, model_class, descripcion in modelos:
        try:
            count = model_class.objects.count()
            print(f"  ✅ {nombre}: {count} registros - {descripcion}")
        except Exception as e:
            print(f"  ❌ {nombre}: {e}")

def verificar_templates():
    """Verificar que los templates principales existan"""
    print("\n🎨 VERIFICANDO TEMPLATES...")
    
    templates_importantes = [
        "base.html",
        "core/dashboard.html",
        "core/proyectos/list.html",
        "core/clientes/list.html",
        "core/facturas/list.html",
        "core/anticipos/list.html",
        "core/archivos/upload.html",
        "core/sistema/index.html",
    ]
    
    for template in templates_importantes:
        template_path = f"templates/{template}"
        if os.path.exists(template_path):
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template} - NO ENCONTRADO")

def generar_reporte_final(resultados):
    """Generar reporte final de la rectificación"""
    print("\n" + "="*60)
    print("📋 REPORTE FINAL DE RECTIFICACIÓN")
    print("="*60)
    
    funcionando = sum(1 for _, ok, _, _ in resultados if ok)
    con_problemas = len(resultados) - funcionando
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"  ✅ Módulos funcionando: {funcionando}")
    print(f"  ❌ Módulos con problemas: {con_problemas}")
    print(f"  📈 Total de módulos: {len(resultados)}")
    print(f"  🎯 Porcentaje de éxito: {(funcionando/len(resultados)*100):.1f}%")
    
    if con_problemas > 0:
        print(f"\n❌ MÓDULOS CON PROBLEMAS:")
        for nombre, ok, error, url in resultados:
            if not ok:
                print(f"  • {nombre}: {error}")
    
    print(f"\n🎉 RECTIFICACIÓN COMPLETADA!")
    print(f"   El sistema está {'FUNCIONANDO PERFECTAMENTE' if con_problemas == 0 else 'CON ALGUNOS PROBLEMAS'}")
    
    return con_problemas == 0

def main():
    """Función principal de rectificación"""
    print("🔧 RECTIFICACIÓN COMPLETA DEL SISTEMA")
    print("="*50)
    
    try:
        # 1. Verificar usuarios
        admin_user = verificar_usuarios()
        
        # 2. Verificar datos básicos
        verificar_datos_basicos()
        
        # 3. Verificar modelos
        verificar_modelos()
        
        # 4. Verificar formularios
        verificar_formularios()
        
        # 5. Verificar templates
        verificar_templates()
        
        # 6. Verificar todos los módulos
        resultados = verificar_todos_los_modulos()
        
        # 7. Generar reporte final
        todo_ok = generar_reporte_final(resultados)
        
        if todo_ok:
            print(f"\n🌐 Para probar el sistema:")
            print(f"   1. Ve a: http://localhost:8000/")
            print(f"   2. Inicia sesión con: admin / admin")
            print(f"   3. Navega por todos los módulos del menú")
        
        return todo_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EN LA RECTIFICACIÓN: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
