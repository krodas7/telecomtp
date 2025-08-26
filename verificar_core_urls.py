#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.urls import urlpatterns

print("=== VERIFICACIÓN DE URLs DE CORE ===")
print("=" * 50)

for pattern in urlpatterns:
    if hasattr(pattern, 'name') and pattern.name:
        print(f"✓ {pattern.name}: {pattern.pattern}")
    else:
        print(f"- {pattern.pattern}")

print("\n" + "=" * 50)
print(f"Total de URLs encontradas: {len(urlpatterns)}")
print("VERIFICACIÓN COMPLETADA")
