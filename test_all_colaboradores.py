#!/usr/bin/env python
import os
import sys

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

try:
    import core.views
    print("📋 Todas las funciones en core.views:")
    
    # Obtener todas las funciones
    all_functions = [name for name in dir(core.views) if callable(getattr(core.views, name)) and not name.startswith('_')]
    
    # Filtrar funciones relacionadas con colaboradores
    colaborador_functions = [name for name in all_functions if 'colaborador' in name.lower()]
    
    print(f"\n🔍 Funciones relacionadas con colaboradores ({len(colaborador_functions)}):")
    for func in sorted(colaborador_functions):
        func_obj = getattr(core.views, func)
        print(f"   ✅ {func}: {func_obj}")
    
    print(f"\n📊 Total de funciones: {len(all_functions)}")
    
    # Verificar si colaborador_detail está disponible
    if hasattr(core.views, 'colaborador_detail'):
        print(f"\n✅ colaborador_detail está disponible")
        detail_func = getattr(core.views, 'colaborador_detail')
        print(f"   Tipo: {type(detail_func)}")
        print(f"   Nombre: {detail_func.__name__}")
        print(f"   Módulo: {detail_func.__module__}")
    else:
        print(f"\n❌ colaborador_detail NO está disponible")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
