#!/usr/bin/env python3
"""
Script simple para probar finalizar planilla
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, TrabajadorDiario

def main():
    print("🔧 PROBANDO FINALIZAR PLANILLA - VERSIÓN SIMPLE")
    print("=" * 60)
    
    try:
        # Verificar proyectos
        proyectos = Proyecto.objects.all()
        print(f"📁 Proyectos encontrados: {proyectos.count()}")
        
        for proyecto in proyectos:
            print(f"   - {proyecto.nombre} (ID: {proyecto.id})")
            
            # Verificar trabajadores
            trabajadores = TrabajadorDiario.objects.filter(proyecto=proyecto)
            print(f"     👷 Trabajadores: {trabajadores.count()}")
            
            for trabajador in trabajadores:
                print(f"       - {trabajador.nombre}: Q{trabajador.pago_diario} {'✅' if trabajador.activo else '❌'}")
        
        print("\n✅ Script ejecutado correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
