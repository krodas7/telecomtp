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
    # Intentar importar solo colaborador_detail
    from core.views import colaborador_detail
    print("✅ colaborador_detail importada correctamente")
    print(f"   Función: {colaborador_detail}")
    print(f"   Nombre: {colaborador_detail.__name__}")
    print(f"   Módulo: {colaborador_detail.__module__}")
except Exception as e:
    print(f"❌ Error al importar colaborador_detail: {e}")
    import traceback
    traceback.print_exc()

try:
    # Verificar si está en el módulo
    import core.views
    print(f"\n📋 Funciones disponibles en core.views:")
    functions = [name for name in dir(core.views) if callable(getattr(core.views, name)) and not name.startswith('_')]
    for func in sorted(functions):
        if 'colaborador' in func.lower():
            print(f"   - {func}")
except Exception as e:
    print(f"❌ Error al listar funciones: {e}")
