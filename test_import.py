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
    from core.views import colaborador_detail, factura_detail
    print("✅ Vistas importadas correctamente:")
    print(f"   - colaborador_detail: {colaborador_detail}")
    print(f"   - factura_detail: {factura_detail}")
except Exception as e:
    print(f"❌ Error al importar vistas: {e}")
    import traceback
    traceback.print_exc()
