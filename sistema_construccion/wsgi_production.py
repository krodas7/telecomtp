"""
WSGI config for sistema_construccion project in production.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configurar variables de entorno para producción
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.production_settings')

# Configurar variables de entorno adicionales si existen
env_file = BASE_DIR / '.env.production'
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("✅ WSGI de producción cargado correctamente")
    print(f"🔒 Configuración: {os.environ.get('DJANGO_SETTINGS_MODULE', 'No configurado')}")
    print(f"🌐 Ambiente: {os.environ.get('ENVIRONMENT', 'No configurado')}")
except Exception as e:
    print(f"❌ Error cargando WSGI de producción: {e}")
    # Fallback a configuración de desarrollo
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("⚠️ Fallback a configuración de desarrollo")
