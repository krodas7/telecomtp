#!/usr/bin/env python
"""
Script para generar datos específicos para pruebas de IA
Incluye datos de entrenamiento y casos de prueba
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.utils import timezone
from core.models import Proyecto, Gasto, Factura, Cliente

class GeneradorDatosIA:
    """Genera datos específicos para pruebas de IA"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.fecha_base = timezone.now().date()
        
    def _setup_logger(self):
        """Configura logging básico"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def generar_datos_entrenamiento_ia(self):
        """Genera datos específicos para entrenar modelos de IA"""
        self.logger.info("Generando datos para entrenamiento de IA...")
        
        try:
            # Obtener proyectos existentes
            proyectos = list(Proyecto.objects.all())
            if not proyectos:
                self.logger.error("No hay proyectos en el sistema. Ejecuta primero cargar_datos_masivos.py")
                return False
            
            # Generar datos de costos históricos para IA
            self._generar_historial_costos(proyectos)
            
            # Generar datos de riesgos históricos
            self._generar_historial_riesgos(proyectos)
            
            # Generar métricas de rendimiento
            self._generar_metricas_rendimiento(proyectos)
            
            # Generar patrones de gastos
            self._generar_patrones_gastos(proyectos)
            
            self.logger.info("Datos de entrenamiento IA generados exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generando datos de IA: {e}")
            return False
    
    def _generar_historial_costos(self, proyectos):
        """Genera historial de costos para análisis de IA"""
        self.logger.info("💰 Generando historial de costos...")
        
        # Simular variaciones de costos a lo largo del tiempo
        for proyecto in proyectos:
            if proyecto.presupuesto and proyecto.fecha_inicio and proyecto.fecha_fin:
                presupuesto_inicial = float(proyecto.presupuesto)
                
                # Generar variaciones mensuales
                fecha_actual = proyecto.fecha_inicio
                while fecha_actual <= proyecto.fecha_fin:
                    # Simular variación de costos (inflación, cambios de mercado, etc.)
                    variacion = random.uniform(-0.15, 0.25)  # -15% a +25%
                    nuevo_presupuesto = presupuesto_inicial * (1 + variacion)
                    
                    # Crear registro de variación (simulado como gasto adicional)
                    if abs(variacion) > 0.05:  # Solo registrar variaciones significativas
                        from core.models import CategoriaGasto
                        categoria, _ = CategoriaGasto.objects.get_or_create(
                            nombre='Contingencias',
                            defaults={'descripcion': 'Gastos por contingencias y variaciones'}
                        )
                        
                        # Crear gasto que represente la variación
                        monto_variacion = abs(nuevo_presupuesto - presupuesto_inicial)
                        if monto_variacion > 1000:  # Solo gastos significativos
                            Gasto.objects.get_or_create(
                                proyecto=proyecto,
                                categoria=categoria,
                                descripcion=f'Variación de costos en {fecha_actual.strftime("%B %Y")}',
                                defaults={
                                    'monto': Decimal(monto_variacion),
                                    'fecha_gasto': fecha_actual,
                                    'aprobado': True
                                }
                            )
                    
                    # Avanzar al siguiente mes
                    fecha_actual = fecha_actual.replace(day=1) + timedelta(days=32)
                    fecha_actual = fecha_actual.replace(day=1)
                    
                    # Actualizar presupuesto para el siguiente mes
                    presupuesto_inicial = nuevo_presupuesto
    
    def _generar_historial_riesgos(self, proyectos):
        """Genera historial de riesgos para análisis de IA"""
        self.logger.info("⚠️ Generando historial de riesgos...")
        
        factores_riesgo = [
            'retraso_cronograma', 'sobrecostos', 'problemas_calidad',
            'incidentes_seguridad', 'problemas_suministros', 'cambios_alcance'
        ]
        
        for proyecto in proyectos:
            if proyecto.fecha_inicio and proyecto.fecha_fin:
                # Generar eventos de riesgo a lo largo del proyecto
                fecha_actual = proyecto.fecha_inicio
                while fecha_actual <= proyecto.fecha_fin:
                    # Probabilidad de evento de riesgo (20%)
                    if random.random() < 0.2:
                        factor_riesgo = random.choice(factores_riesgo)
                        
                        # Crear gasto que represente el impacto del riesgo
                        from core.models import CategoriaGasto
                        categoria, _ = CategoriaGasto.objects.get_or_create(
                            nombre='Contingencias',
                            defaults={'descripcion': 'Gastos por contingencias y variaciones'}
                        )
                        
                        # Calcular impacto del riesgo
                        presupuesto_proyecto = float(proyecto.presupuesto or 1000000)
                        impacto_riesgo = presupuesto_proyecto * random.uniform(0.02, 0.08)  # 2-8% del presupuesto
                        
                        Gasto.objects.get_or_create(
                            proyecto=proyecto,
                            categoria=categoria,
                            descripcion=f'Impacto de riesgo: {factor_riesgo} en {fecha_actual.strftime("%B %Y")}',
                            defaults={
                                'monto': Decimal(impacto_riesgo),
                                'fecha_gasto': fecha_actual,
                                'aprobado': True
                            }
                        )
                    
                    # Avanzar al siguiente mes
                    fecha_actual = fecha_actual.replace(day=1) + timedelta(days=32)
                    fecha_actual = fecha_actual.replace(day=1)
    
    def _generar_metricas_rendimiento(self, proyectos):
        """Genera métricas de rendimiento para análisis de IA"""
        self.logger.info("📊 Generando métricas de rendimiento...")
        
        for proyecto in proyectos:
            if proyecto.fecha_inicio and proyecto.fecha_fin:
                # Calcular eficiencia del proyecto
                duracion_planificada = (proyecto.fecha_fin - proyecto.fecha_inicio).days
                duracion_real = random.randint(
                    int(duracion_planificada * 0.8),  # 20% más rápido
                    int(duracion_planificada * 1.5)   # 50% más lento
                )
                
                # Simular variaciones en el cronograma
                if duracion_real > duracion_planificada:
                    # Proyecto retrasado - crear gastos por retrasos
                    from core.models import CategoriaGasto
                    categoria, _ = CategoriaGasto.objects.get_or_create(
                        nombre='Gastos Administrativos',
                        defaults={'descripcion': 'Gastos administrativos del proyecto'}
                    )
                    
                    costo_retraso = float(proyecto.presupuesto or 1000000) * 0.01  # 1% del presupuesto
                    Gasto.objects.get_or_create(
                        proyecto=proyecto,
                        categoria=categoria,
                        descripcion=f'Costo por retraso en cronograma',
                        defaults={
                            'monto': Decimal(costo_retraso),
                            'fecha_gasto': proyecto.fecha_fin,
                            'aprobado': True
                        }
                    )
    
    def _generar_patrones_gastos(self, proyectos):
        """Genera patrones de gastos para análisis de IA"""
        self.logger.info("💸 Generando patrones de gastos...")
        
        # Simular estacionalidad en gastos
        meses_altos_gastos = [1, 2, 6, 7, 8, 12]  # Enero, Febrero, Junio-Julio-Agosto, Diciembre
        
        for proyecto in proyectos:
            if proyecto.fecha_inicio and proyecto.fecha_fin:
                fecha_actual = proyecto.fecha_inicio
                while fecha_actual <= proyecto.fecha_fin:
                    # Verificar si es mes de altos gastos
                    if fecha_actual.month in meses_altos_gastos:
                        # Generar gastos adicionales por estacionalidad
                        from core.models import CategoriaGasto
                        categoria, _ = CategoriaGasto.objects.get_or_create(
                            nombre='Gastos Administrativos',
                            defaults={'descripcion': 'Gastos administrativos del proyecto'}
                        )
                        
                        presupuesto_proyecto = float(proyecto.presupuesto or 1000000)
                        gasto_estacional = presupuesto_proyecto * random.uniform(0.01, 0.03)  # 1-3% del presupuesto
                        
                        Gasto.objects.get_or_create(
                            proyecto=proyecto,
                            categoria=categoria,
                            descripcion=f'Gasto estacional en {fecha_actual.strftime("%B %Y")}',
                            defaults={
                                'monto': Decimal(gasto_estacional),
                                'fecha_gasto': fecha_actual,
                                'aprobado': True
                            }
                        )
                    
                    # Avanzar al siguiente mes
                    fecha_actual = fecha_actual.replace(day=1) + timedelta(days=32)
                    fecha_actual = fecha_actual.replace(day=1)
    
    def generar_casos_prueba_ia(self):
        """Genera casos de prueba específicos para IA"""
        self.logger.info("Generando casos de prueba para IA...")
        
        try:
            # Caso 1: Proyecto con alto riesgo
            self._crear_proyecto_alto_riesgo()
            
            # Caso 2: Proyecto con sobrecostos
            self._crear_proyecto_sobrecostos()
            
            # Caso 3: Proyecto exitoso
            self._crear_proyecto_exitoso()
            
            # Caso 4: Proyecto con retrasos
            self._crear_proyecto_retrasos()
            
            self.logger.info("Casos de prueba IA generados exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generando casos de prueba: {e}")
            return False
    
    def _crear_proyecto_alto_riesgo(self):
        """Crea un proyecto con alto riesgo para pruebas de IA"""
        from core.models import Cliente, CategoriaGasto
        
        # Obtener o crear cliente
        cliente, _ = Cliente.objects.get_or_create(
            razon_social="Cliente de Alto Riesgo - Pruebas IA",
            defaults={
                'codigo_fiscal': 'CF-999999',
                'email': 'alto.riesgo@pruebas.com',
                'telefono': '502-9999-9999',
                'direccion': 'Zona de Alto Riesgo, Guatemala'
            }
        )
        
        # Crear proyecto de alto riesgo
        proyecto, _ = Proyecto.objects.get_or_create(
            nombre="Proyecto de Alto Riesgo - Pruebas IA",
            defaults={
                'descripcion': 'Proyecto diseñado para probar detección de riesgos de IA',
                'cliente': cliente,
                'presupuesto': Decimal('5000000'),  # 5M
                'fecha_inicio': self.fecha_base - timedelta(days=30),
                'fecha_fin': self.fecha_base + timedelta(days=60),
                'estado': 'en_progreso',
                'activo': True
            }
        )
        
        # Crear gastos que indiquen alto riesgo
        categoria_riesgo, _ = CategoriaGasto.objects.get_or_create(
            nombre='Contingencias',
            defaults={'descripcion': 'Gastos por contingencias y variaciones'}
        )
        
        # Gastos por incidentes de seguridad
        Gasto.objects.get_or_create(
            proyecto=proyecto,
            categoria=categoria_riesgo,
            descripcion='Incidente de seguridad - Evacuación de obra',
            defaults={
                'monto': Decimal('150000'),
                'fecha_gasto': self.fecha_base - timedelta(days=15),
                'aprobado': True
            }
        )
        
        # Gastos por problemas de calidad
        Gasto.objects.get_or_create(
            proyecto=proyecto,
            categoria=categoria_riesgo,
            descripcion='Reparación por problemas de calidad',
            defaults={
                'monto': Decimal('250000'),
                'fecha_gasto': self.fecha_base - timedelta(days=10),
                'aprobado': True
            }
        )
        
        self.logger.info("✅ Proyecto de alto riesgo creado para pruebas IA")
    
    def _crear_proyecto_sobrecostos(self):
        """Crea un proyecto con sobrecostos para pruebas de IA"""
        from core.models import Cliente, CategoriaGasto
        
        cliente, _ = Cliente.objects.get_or_create(
            razon_social="Cliente Sobrecostos - Pruebas IA",
            defaults={
                'codigo_fiscal': 'CF-888888',
                'email': 'sobrecostos@pruebas.com',
                'telefono': '502-8888-8888',
                'direccion': 'Zona de Sobrecostos, Guatemala'
            }
        )
        
        proyecto, _ = Proyecto.objects.get_or_create(
            nombre="Proyecto con Sobrecostos - Pruebas IA",
            defaults={
                'descripcion': 'Proyecto diseñado para probar detección de sobrecostos de IA',
                'cliente': cliente,
                'presupuesto': Decimal('3000000'),  # 3M
                'fecha_inicio': self.fecha_base - timedelta(days=45),
                'fecha_fin': self.fecha_base + timedelta(days=30),
                'estado': 'en_progreso',
                'activo': True
            }
        )
        
        # Crear gastos que excedan el presupuesto
        categoria_materiales, _ = CategoriaGasto.objects.get_or_create(
            nombre='Materiales de Construcción',
            defaults={'descripcion': 'Materiales de construcción'}
        )
        
        # Gastos excesivos por materiales
        Gasto.objects.get_or_create(
            proyecto=proyecto,
            categoria=categoria_materiales,
            descripcion='Materiales premium - sobrecostos',
            defaults={
                'monto': Decimal('800000'),
                'fecha_gasto': self.fecha_base - timedelta(days=20),
                'aprobado': True
            }
        )
        
        self.logger.info("✅ Proyecto con sobrecostos creado para pruebas IA")
    
    def _crear_proyecto_exitoso(self):
        """Crea un proyecto exitoso para pruebas de IA"""
        from core.models import Cliente, CategoriaGasto
        
        cliente, _ = Cliente.objects.get_or_create(
            razon_social="Cliente Exitoso - Pruebas IA",
            defaults={
                'codigo_fiscal': 'CF-777777',
                'email': 'exitoso@pruebas.com',
                'telefono': '502-7777-7777',
                'direccion': 'Zona de Éxito, Guatemala'
            }
        )
        
        proyecto, _ = Proyecto.objects.get_or_create(
            nombre="Proyecto Exitoso - Pruebas IA",
            defaults={
                'descripcion': 'Proyecto diseñado para probar análisis de éxito de IA',
                'cliente': cliente,
                'presupuesto': Decimal('2000000'),  # 2M
                'fecha_inicio': self.fecha_base - timedelta(days=90),
                'fecha_fin': self.fecha_base - timedelta(days=10),  # Completado
                'estado': 'completado',
                'activo': True
            }
        )
        
        # Crear gastos que muestren eficiencia
        categoria_mano_obra, _ = CategoriaGasto.objects.get_or_create(
            nombre='Mano de Obra',
            defaults={'descripcion': 'Costos de mano de obra'}
        )
        
        # Gastos eficientes
        Gasto.objects.get_or_create(
            proyecto=proyecto,
            categoria=categoria_mano_obra,
            descripcion='Mano de obra eficiente - proyecto exitoso',
            defaults={
                'monto': Decimal('1200000'),
                'fecha_gasto': self.fecha_base - timedelta(days=30),
                'aprobado': True
            }
        )
        
        self.logger.info("✅ Proyecto exitoso creado para pruebas IA")
    
    def _crear_proyecto_retrasos(self):
        """Crea un proyecto con retrasos para pruebas de IA"""
        from core.models import Cliente, CategoriaGasto
        
        cliente, _ = Cliente.objects.get_or_create(
            razon_social="Cliente Retrasos - Pruebas IA",
            defaults={
                'codigo_fiscal': 'CF-666666',
                'email': 'retrasos@pruebas.com',
                'telefono': '502-6666-6666',
                'direccion': 'Zona de Retrasos, Guatemala'
            }
        )
        
        proyecto, _ = Proyecto.objects.get_or_create(
            nombre="Proyecto con Retrasos - Pruebas IA",
            defaults={
                'descripcion': 'Proyecto diseñado para probar detección de retrasos de IA',
                'cliente': cliente,
                'presupuesto': Decimal('4000000'),  # 4M
                'fecha_inicio': self.fecha_base - timedelta(days=120),
                'fecha_fin': self.fecha_base - timedelta(days=30),  # Ya debería estar terminado
                'estado': 'en_progreso',  # Pero sigue en progreso
                'activo': True
            }
        )
        
        # Crear gastos por retrasos
        categoria_equipos, _ = CategoriaGasto.objects.get_or_create(
            nombre='Equipos y Maquinaria',
            defaults={'descripcion': 'Costos de equipos y maquinaria'}
        )
        
        # Gastos por alquiler extendido de equipos
        Gasto.objects.get_or_create(
            proyecto=proyecto,
            categoria=categoria_equipos,
            descripcion='Alquiler extendido de equipos por retrasos',
            defaults={
                'monto': Decimal('300000'),
                'fecha_gasto': self.fecha_base - timedelta(days=15),
                'aprobado': True
            }
        )
        
        self.logger.info("✅ Proyecto con retrasos creado para pruebas IA")

def main():
    """Función principal"""
    print("GENERADOR DE DATOS PARA IA - SISTEMA DE CONSTRUCCION")
    print("=" * 70)
    print("Este script generará datos específicos para:")
    print("• Entrenamiento de modelos de IA")
    print("• Casos de prueba para análisis de riesgos")
    print("• Datos para predicción de costos")
    print("• Análisis de patrones y tendencias")
    print("=" * 70)
    
    respuesta = input("¿Deseas continuar? (s/n): ").lower().strip()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("Operación cancelada por el usuario")
        return
    
    print("\nIniciando generación de datos para IA...")
    
    generador = GeneradorDatosIA()
    
    # Generar datos de entrenamiento
    print("\nGenerando datos de entrenamiento...")
    exito_entrenamiento = generador.generar_datos_entrenamiento_ia()
    
    # Generar casos de prueba
    print("\nGenerando casos de prueba...")
    exito_pruebas = generador.generar_casos_prueba_ia()
    
    if exito_entrenamiento and exito_pruebas:
        print("\n¡Datos para IA generados exitosamente!")
        print("Ahora puedes:")
        print("1. Probar la generación de reportes IA")
        print("2. Verificar la detección de riesgos")
        print("3. Probar predicciones de costos")
        print("4. Analizar patrones y tendencias")
    else:
        print("\nError durante la generación de datos para IA")
        print("Revisa los logs para más detalles")

if __name__ == "__main__":
    main()
