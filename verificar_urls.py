#!/usr/bin/env python
"""
Script para verificar que todas las URLs y vistas del sistema estén funcionando correctamente.
Este script revisa la consistencia entre core/urls.py y core/views.py
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from core import views
import inspect

def verificar_vistas():
    """Verifica que todas las vistas referenciadas en URLs existan en views.py"""
    print("🔍 Verificando vistas del sistema...")
    print("=" * 60)
    
    # Obtener todas las funciones definidas en views.py
    vistas_disponibles = []
    for name, obj in inspect.getmembers(views):
        if inspect.isfunction(obj) and obj.__module__ == 'core.views':
            vistas_disponibles.append(name)
    
    print(f"✅ Vistas disponibles en core/views.py: {len(vistas_disponibles)}")
    print(f"📋 Lista de vistas: {', '.join(sorted(vistas_disponibles))}")
    print()
    
    # Verificar que las vistas principales estén presentes
    vistas_requeridas = [
        'dashboard', 'login_view', 'logout_view',
        'clientes_list', 'cliente_create', 'cliente_edit', 'cliente_delete',
        'proyectos_list', 'proyecto_create', 'proyecto_edit', 'proyecto_delete',
        'colaboradores_list', 'colaborador_create', 'colaborador_detail', 'colaborador_edit', 'colaborador_delete',
        'facturas_list', 'factura_create', 'factura_detail', 'factura_edit', 'factura_delete',
        'gastos_list', 'gasto_create', 'gasto_edit', 'gasto_delete',
        'pagos_list', 'pago_create', 'pago_edit', 'pago_delete',
        'categorias_gasto_list', 'categoria_gasto_create', 'categoria_gasto_edit', 'categoria_gasto_delete',
        'anticipos_list', 'anticipo_create', 'anticipo_detail', 'anticipo_edit', 'anticipo_delete', 'aplicar_anticipo',
        'archivos_proyectos_list', 'proyecto_dashboard', 'archivos_proyecto_list', 'archivo_upload', 'archivo_download', 'archivo_delete', 'archivo_preview',
        'presupuestos_list', 'presupuesto_create', 'presupuesto_detail', 'presupuesto_edit', 'partida_create', 'presupuesto_aprobar',
        'rentabilidad_view', 'usuarios_list', 'usuario_create', 'usuario_edit',
        'sistema_view', 'sistema_configurar', 'sistema_logs',
        'notificaciones_list', 'notificaciones_configurar', 'notificaciones_historial',
        'notificacion_marcar_leida', 'notificacion_marcar_todas_leidas',
        'api_notificaciones_no_leidas', 'api_marcar_leida',
        'admin_notificaciones_sistema', 'admin_ejecutar_verificaciones',
        'test_notification_email', 'push_notifications_setup', 'api_push_subscription',
        'perfil'
    ]
    
    vistas_faltantes = []
    for vista in vistas_requeridas:
        if vista not in vistas_disponibles:
            vistas_faltantes.append(vista)
    
    if vistas_faltantes:
        print("❌ Vistas faltantes:")
        for vista in vistas_faltantes:
            print(f"   - {vista}")
        print()
    else:
        print("✅ Todas las vistas requeridas están presentes")
        print()
    
    return vistas_disponibles, vistas_faltantes

def verificar_urls():
    """Verifica que todas las URLs puedan ser resueltas correctamente"""
    print("🔗 Verificando URLs del sistema...")
    print("=" * 60)
    
    # Lista de URLs a verificar
    urls_a_verificar = [
        'dashboard', 'login', 'logout', 'perfil',
        'clientes_list', 'cliente_create', 'cliente_edit', 'cliente_delete',
        'proyectos_list', 'proyecto_create', 'proyecto_edit', 'proyecto_delete',
        'colaboradores_list', 'colaborador_create', 'colaborador_detail', 'colaborador_edit', 'colaborador_delete',
        'facturas_list', 'factura_create', 'factura_detail', 'factura_edit', 'factura_delete',
        'gastos_list', 'gasto_create', 'gasto_edit', 'gasto_delete',
        'pagos_list', 'pago_create', 'pago_edit', 'pago_delete',
        'categorias_gasto_list', 'categoria_gasto_create', 'categoria_gasto_edit', 'categoria_gasto_delete',
        'anticipos_list', 'anticipo_create', 'anticipo_detail', 'anticipo_edit', 'anticipo_delete', 'aplicar_anticipo',
        'archivos_proyectos_list', 'proyecto_dashboard', 'archivos_proyecto_list', 'archivo_upload', 'archivo_download', 'archivo_delete', 'archivo_preview',
        'presupuestos_list', 'presupuesto_create', 'presupuesto_detail', 'presupuesto_edit', 'partida_create', 'presupuesto_aprobar',
        'rentabilidad', 'usuarios_list', 'usuario_create', 'usuario_edit',
        'sistema', 'sistema_configurar', 'sistema_logs',
        'notificaciones_list', 'notificaciones_configurar', 'notificaciones_historial',
        'notificacion_marcar_leida', 'notificacion_marcar_todas_leidas',
        'api_notificaciones_no_leidas', 'api_marcar_leida',
        'admin_notificaciones_sistema', 'admin_ejecutar_verificaciones',
        'test_notification_email', 'push_notifications_setup', 'api_push_subscription'
    ]
    
    urls_exitosas = []
    urls_fallidas = []
    
    for url_name in urls_a_verificar:
        try:
            reverse(url_name)
            urls_exitosas.append(url_name)
        except NoReverseMatch as e:
            urls_fallidas.append((url_name, str(e)))
    
    print(f"✅ URLs exitosas: {len(urls_exitosas)}")
    print(f"❌ URLs fallidas: {len(urls_fallidas)}")
    
    if urls_fallidas:
        print("\n❌ URLs que fallaron:")
        for url_name, error in urls_fallidas:
            print(f"   - {url_name}: {error}")
    
    print()
    return urls_exitosas, urls_fallidas

def verificar_templates():
    """Verifica que los templates principales existan"""
    print("📁 Verificando templates del sistema...")
    print("=" * 60)
    
    templates_requeridos = [
        'core/dashboard.html',
        'core/gastos/list.html',
        'core/gastos/create.html',
        'core/gastos/edit.html',
        'core/gastos/delete.html',
        'core/clientes/list.html',
        'core/proyectos/list.html',
        'core/facturas/list.html',
        'core/colaboradores/list.html',
        'core/base.html'
    ]
    
    templates_existentes = []
    templates_faltantes = []
    
    for template in templates_requeridos:
        template_path = BASE_DIR / 'templates' / template
        if template_path.exists():
            templates_existentes.append(template)
        else:
            templates_faltantes.append(template)
    
    print(f"✅ Templates existentes: {len(templates_existentes)}")
    print(f"❌ Templates faltantes: {len(templates_faltantes)}")
    
    if templates_faltantes:
        print("\n❌ Templates que faltan:")
        for template in templates_faltantes:
            print(f"   - {template}")
    
    print()
    return templates_existentes, templates_faltantes

def main():
    """Función principal del script"""
    print("🚀 INICIANDO VERIFICACIÓN DEL SISTEMA DE CONSTRUCCIÓN")
    print("=" * 60)
    print()
    
    # Verificar vistas
    vistas_disponibles, vistas_faltantes = verificar_vistas()
    
    # Verificar URLs
    urls_exitosas, urls_fallidas = verificar_urls()
    
    # Verificar templates
    templates_existentes, templates_faltantes = verificar_templates()
    
    # Resumen final
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    total_vistas = len(vistas_disponibles)
    total_urls = len(urls_exitosas)
    total_templates = len(templates_existentes)
    
    print(f"✅ Vistas funcionando: {total_vistas}")
    print(f"✅ URLs funcionando: {total_urls}")
    print(f"✅ Templates disponibles: {total_templates}")
    
    if not vistas_faltantes and not urls_fallidas and not templates_faltantes:
        print("\n🎉 ¡SISTEMA VERIFICADO EXITOSAMENTE!")
        print("   Todas las vistas, URLs y templates están funcionando correctamente.")
    else:
        print("\n⚠️  PROBLEMAS DETECTADOS:")
        if vistas_faltantes:
            print(f"   - Faltan {len(vistas_faltantes)} vistas")
        if urls_fallidas:
            print(f"   - Faltan {len(urls_fallidas)} URLs")
        if templates_faltantes:
            print(f"   - Faltan {len(templates_faltantes)} templates")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
