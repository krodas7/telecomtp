#!/usr/bin/env python
"""
Script para cargar datos masivos en el Sistema de Construcción
Genera datos realistas para probar rendimiento y funcionalidad
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

from django.contrib.auth.models import User
from django.utils import timezone
from core.models import (
    Rol, PerfilUsuario, Cliente, Colaborador, Proyecto, 
    CategoriaGasto, Gasto, Factura, Anticipo, LogActividad
)

class GeneradorDatosMasivos:
    """Genera datos masivos y realistas para el sistema"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.fecha_base = timezone.now().date()
        
        # Datos de ejemplo para generar contenido realista
        self.empresas_constructoras = [
            "Constructora Maya S.A.", "Edificaciones del Valle", "Proyectos Urbanos GT",
            "Construcciones Modernas", "Inmobiliaria Central", "Desarrollo Residencial",
            "Constructora del Norte", "Edificaciones del Sur", "Proyectos Comerciales",
            "Construcciones Especializadas", "Inmobiliaria Premium", "Desarrollo Corporativo",
            "Constructora Internacional", "Edificaciones del Este", "Proyectos Industriales",
            "Construcciones Sostenibles", "Inmobiliaria del Lago", "Desarrollo Turístico",
            "Constructora del Pacífico", "Edificaciones del Atlántico"
        ]
        
        self.tipos_proyecto = [
            "Residencial", "Comercial", "Industrial", "Infraestructura", "Educativo",
            "Salud", "Hotelero", "Oficinas", "Logística", "Recreativo"
        ]
        
        self.ubicaciones = [
            "Zona 1 - Centro Histórico", "Zona 4 - Centro Comercial", "Zona 10 - Zona Viva",
            "Zona 14 - Zona Rosa", "Zona 15 - Vista Hermosa", "Zona 16 - Lomas de Pamplona",
            "Zona 17 - San Cristóbal", "Zona 18 - Villa Nueva", "Zona 19 - San José Pinula",
            "Zona 21 - Mixco", "Zona 22 - Villa Canales", "Zona 23 - San Miguel Petapa",
            "Zona 24 - Santa Catarina Pinula", "Zona 25 - Fraijanes", "Zona 26 - San Vicente Pacaya"
        ]
        
        self.categorias_gasto = [
            "Materiales de Construcción", "Mano de Obra", "Equipos y Maquinaria",
            "Permisos y Licencias", "Servicios Públicos", "Seguros y Garantías",
            "Transporte y Logística", "Supervisión Técnica", "Contingencias",
            "Gastos Administrativos", "Marketing y Ventas", "Mantenimiento",
            "Seguridad Industrial", "Capacitación", "Consultorías"
        ]
        
        self.nombres_colaboradores = [
            "Carlos Mendoza", "Ana López", "Miguel Torres", "Sofia Ramírez", "Roberto Jiménez",
            "Carmen Herrera", "Luis Morales", "Patricia Castro", "Jorge Silva", "María González",
            "Fernando Ruiz", "Isabel Vargas", "Ricardo Moreno", "Elena Santos", "Alberto Cruz",
            "Rosa Martínez", "Diego Ortega", "Lucía Fernández", "Héctor Rojas", "Natalia Vega",
            "Oscar Delgado", "Gabriela Peña", "Raúl Acosta", "Verónica Luna", "Francisco Méndez"
        ]
        
        self.estados_proyecto = ['pendiente', 'en_progreso', 'completado', 'cancelado']
        self.estados_factura = ['borrador', 'emitida', 'enviada', 'pagada', 'vencida']
        self.tipos_factura = ['progreso', 'final', 'adicional', 'retencion']
        
    def _setup_logger(self):
        """Configura logging básico"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def generar_roles(self):
        """Genera roles básicos del sistema"""
        self.logger.info("Generando roles del sistema...")
        
        roles_data = [
            {'nombre': 'Administrador', 'descripcion': 'Acceso completo al sistema'},
            {'nombre': 'Gerente', 'descripcion': 'Gestión de proyectos y reportes'},
            {'nombre': 'Supervisor', 'descripcion': 'Supervisión de obras y colaboradores'},
            {'nombre': 'Colaborador', 'descripcion': 'Acceso básico al sistema'},
            {'nombre': 'Contador', 'descripcion': 'Gestión financiera y facturación'},
            {'nombre': 'Cliente', 'descripcion': 'Acceso a información de proyectos'}
        ]
        
        roles_creados = []
        for rol_data in roles_data:
            rol, created = Rol.objects.get_or_create(
                nombre=rol_data['nombre'],
                defaults={'descripcion': rol_data['descripcion']}
            )
            if created:
                self.logger.info(f"Rol creado: {rol.nombre}")
            roles_creados.append(rol)
        
        return roles_creados
    
    def generar_usuarios_y_perfiles(self, roles):
        """Genera usuarios y perfiles del sistema"""
        self.logger.info("Generando usuarios y perfiles...")
        
        # Usuario administrador principal
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@construccion.com',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.logger.info("Usuario administrador creado: admin/admin123")
        
        # Crear perfil para admin
        admin_rol = next((r for r in roles if r.nombre == 'Administrador'), roles[0])
        admin_perfil, created = PerfilUsuario.objects.get_or_create(
            usuario=admin_user,
            defaults={'rol': admin_rol, 'telefono': '502-1234-5678'}
        )
        
        # Generar usuarios adicionales
        usuarios_creados = [admin_user]
        for i in range(1, 11):  # 10 usuarios adicionales
            username = f'usuario{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'usuario{i}@construccion.com',
                    'first_name': f'Usuario{i}',
                    'last_name': 'Sistema',
                    'is_staff': False
                }
            )
            if created:
                user.set_password('usuario123')
                user.save()
                
                # Asignar rol aleatorio
                rol = random.choice(roles[1:])  # Excluir admin
                perfil, created = PerfilUsuario.objects.get_or_create(
                    usuario=user,
                    defaults={'rol': rol, 'telefono': f'502-{random.randint(1000,9999)}-{random.randint(1000,9999)}'}
                )
                usuarios_creados.append(user)
                self.logger.info(f"Usuario creado: {username}/usuario123 con rol {rol.nombre}")
        
        return usuarios_creados
    
    def generar_clientes(self, cantidad=200):
        """Genera clientes del sistema"""
        self.logger.info(f"Generando {cantidad} clientes...")
        
        clientes_creados = []
        for i in range(cantidad):
            # Seleccionar empresa aleatoria
            empresa = random.choice(self.empresas_constructoras)
            
            # Generar datos únicos
            codigo_fiscal = f"CF-{random.randint(100000, 999999)}"
            email = f"contacto@{empresa.lower().replace(' ', '').replace('.', '').replace('s.a.', '')}.com"
            telefono = f"502-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            # Crear cliente
            cliente, created = Cliente.objects.get_or_create(
                codigo_fiscal=codigo_fiscal,
                defaults={
                    'razon_social': f"{empresa} - Cliente {i+1}",
                    'email': email,
                    'telefono': telefono,
                    'direccion': f"{random.choice(self.ubicaciones)}, Guatemala",
                    'activo': random.choice([True, True, True, False])  # 75% activos
                }
            )
            
            if created:
                clientes_creados.append(cliente)
                if i % 50 == 0:
                    self.logger.info(f"Clientes creados: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de clientes creados: {len(clientes_creados)}")
        return clientes_creados
    
    def generar_categorias_gasto(self):
        """Genera categorías de gasto"""
        self.logger.info("Generando categorías de gasto...")
        
        categorias_creadas = []
        for categoria_nombre in self.categorias_gasto:
            categoria, created = CategoriaGasto.objects.get_or_create(
                nombre=categoria_nombre,
                defaults={'descripcion': f'Categoría para {categoria_nombre.lower()}'}
            )
            if created:
                self.logger.info(f"Categoría creada: {categoria.nombre}")
            categorias_creadas.append(categoria)
        
        return categorias_creadas
    
    def generar_colaboradores(self, cantidad=30):
        """Genera colaboradores del sistema"""
        self.logger.info(f"Generando {cantidad} colaboradores...")
        
        colaboradores_creados = []
        for i in range(cantidad):
            nombre = random.choice(self.nombres_colaboradores)
            dpi = f"{random.randint(1000, 9999)}-{random.randint(10000, 99999)}-{random.randint(1000, 9999)}"
            email = f"{nombre.lower().replace(' ', '.')}@construccion.com"
            telefono = f"502-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            # Generar fechas de contratación realistas
            fecha_contratacion = self.fecha_base - timedelta(days=random.randint(30, 1000))
            fecha_vencimiento = fecha_contratacion + timedelta(days=random.randint(365, 1095))  # 1-3 años
            
            colaborador, created = Colaborador.objects.get_or_create(
                dpi=dpi,
                defaults={
                    'nombre': f"{nombre} {i+1}",
                    'direccion': f"{random.choice(self.ubicaciones)}, Guatemala",
                    'telefono': telefono,
                    'email': email,
                    'salario': Decimal(random.randint(3000, 15000)),
                    'fecha_contratacion': fecha_contratacion,
                    'fecha_vencimiento_contrato': fecha_vencimiento,
                    'activo': random.choice([True, True, True, False])  # 75% activos
                }
            )
            
            if created:
                colaboradores_creados.append(colaborador)
                if i % 10 == 0:
                    self.logger.info(f"Colaboradores creados: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de colaboradores creados: {len(colaboradores_creados)}")
        return colaboradores_creados
    
    def generar_proyectos(self, clientes, cantidad=80):
        """Genera proyectos del sistema"""
        self.logger.info(f"Generando {cantidad} proyectos...")
        
        proyectos_creados = []
        for i in range(cantidad):
            # Seleccionar cliente aleatorio
            cliente = random.choice(clientes)
            
            # Generar datos del proyecto
            tipo_proyecto = random.choice(self.tipos_proyecto)
            nombre = f"{tipo_proyecto} - {cliente.razon_social.split(' - ')[0]} - Proyecto {i+1}"
            
            # Generar fechas realistas
            fecha_inicio = self.fecha_base - timedelta(days=random.randint(0, 730))  # Últimos 2 años
            duracion_dias = random.randint(30, 365)  # 1 mes a 1 año
            fecha_fin = fecha_inicio + timedelta(days=duracion_dias)
            
            # Determinar estado basado en fechas
            if fecha_fin < self.fecha_base:
                estado = 'completado'
            elif fecha_inicio > self.fecha_base:
                estado = 'pendiente'
            else:
                estado = random.choice(['en_progreso', 'en_progreso', 'en_progreso', 'cancelado'])
            
            # Generar presupuesto realista
            area_m2 = random.randint(100, 10000)
            presupuesto_por_m2 = random.randint(800, 2500)
            presupuesto = Decimal(area_m2 * presupuesto_por_m2)
            
            proyecto, created = Proyecto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': f'Proyecto de {tipo_proyecto.lower()} para {cliente.razon_social}',
                    'cliente': cliente,
                    'presupuesto': presupuesto,
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'estado': estado,
                    'activo': estado != 'cancelado'
                }
            )
            
            if created:
                proyectos_creados.append(proyecto)
                if i % 20 == 0:
                    self.logger.info(f"Proyectos creados: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de proyectos creados: {len(proyectos_creados)}")
        return proyectos_creados
    
    def generar_gastos(self, proyectos, categorias, cantidad=300):
        """Genera gastos del sistema"""
        self.logger.info(f"Generando {cantidad} gastos...")
        
        gastos_creados = []
        for i in range(cantidad):
            proyecto = random.choice(proyectos)
            categoria = random.choice(categorias)
            
            # Generar monto realista basado en el presupuesto del proyecto
            presupuesto_proyecto = float(proyecto.presupuesto or 1000000)
            monto_maximo = min(presupuesto_proyecto * 0.1, 100000)  # Máximo 10% del presupuesto o 100k
            monto = Decimal(random.randint(1000, int(monto_maximo)))
            
            # Generar fecha de gasto
            if proyecto.fecha_inicio and proyecto.fecha_fin:
                fecha_gasto = proyecto.fecha_inicio + timedelta(
                    days=random.randint(0, (proyecto.fecha_fin - proyecto.fecha_inicio).days)
                )
            else:
                fecha_gasto = self.fecha_base - timedelta(days=random.randint(0, 365))
            
            gasto, created = Gasto.objects.get_or_create(
                proyecto=proyecto,
                categoria=categoria,
                descripcion=f"Gasto de {categoria.nombre.lower()} para {proyecto.nombre}",
                defaults={
                    'monto': monto,
                    'fecha_gasto': fecha_gasto,
                    'aprobado': random.choice([True, True, True, False]),  # 75% aprobados
                    'comprobante': None  # Por simplicidad
                }
            )
            
            if created:
                gastos_creados.append(gasto)
                if i % 100 == 0:
                    self.logger.info(f"Gastos creados: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de gastos creados: {len(gastos_creados)}")
        return gastos_creados
    
    def generar_facturas(self, proyectos, clientes, cantidad=50):
        """Genera facturas del sistema"""
        self.logger.info(f"Generando {cantidad} facturas...")
        
        facturas_creadas = []
        for i in range(cantidad):
            proyecto = random.choice(proyectos)
            cliente = proyecto.cliente
            
            # Generar datos de factura
            numero_factura = f"FAC-{random.randint(10000, 99999)}-{i+1}"
            tipo = random.choice(self.tipos_factura)
            
            # Generar fechas
            fecha_emision = self.fecha_base - timedelta(days=random.randint(0, 365))
            fecha_vencimiento = fecha_emision + timedelta(days=random.randint(15, 90))
            
            # Generar montos
            presupuesto_proyecto = float(proyecto.presupuesto or 1000000)
            monto_subtotal = Decimal(random.randint(int(presupuesto_proyecto * 0.05), int(presupuesto_proyecto * 0.3)))
            monto_iva = monto_subtotal * Decimal('0.12')  # IVA 12%
            monto_total = monto_subtotal + monto_iva
            
            # Determinar estado y montos pagados
            if fecha_vencimiento < self.fecha_base:
                estado = random.choice(['pagada', 'vencida'])
                monto_pagado = monto_total if estado == 'pagada' else Decimal('0')
            else:
                estado = random.choice(['borrador', 'emitida', 'enviada', 'pagada'])
                if estado == 'pagada':
                    monto_pagado = monto_total
                else:
                    monto_pagado = Decimal('0')
            
            factura, created = Factura.objects.get_or_create(
                numero_factura=numero_factura,
                defaults={
                    'proyecto': proyecto,
                    'cliente': cliente,
                    'tipo': tipo,
                    'estado': estado,
                    'fecha_emision': fecha_emision,
                    'fecha_vencimiento': fecha_vencimiento,
                    'monto_subtotal': monto_subtotal,
                    'monto_iva': monto_iva,
                    'monto_total': monto_total,
                    'monto_pagado': monto_pagado,
                    'monto_anticipos': Decimal('0'),
                    'monto_pendiente': monto_total - monto_pagado
                }
            )
            
            if created:
                facturas_creadas.append(factura)
                if i % 10 == 0:
                    self.logger.info(f"Facturas creadas: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de facturas creadas: {len(facturas_creadas)}")
        return facturas_creadas
    
    def generar_anticipos(self, proyectos, clientes, cantidad=20):
        """Genera anticipos del sistema"""
        self.logger.info(f"Generando {cantidad} anticipos...")
        
        anticipos_creados = []
        for i in range(cantidad):
            proyecto = random.choice(proyectos)
            cliente = proyecto.cliente
            
            # Generar datos del anticipo
            numero_anticipo = f"ANT-{random.randint(1000, 9999)}-{i+1}"
            tipo = random.choice(['anticipo', 'materiales', 'gastos', 'otros'])
            
            # Generar monto basado en presupuesto del proyecto
            presupuesto_proyecto = float(proyecto.presupuesto or 1000000)
            monto = Decimal(random.randint(int(presupuesto_proyecto * 0.05), int(presupuesto_proyecto * 0.2)))
            
            # Generar fechas
            fecha_recepcion = self.fecha_base - timedelta(days=random.randint(0, 180))
            fecha_vencimiento = fecha_recepcion + timedelta(days=random.randint(30, 365))
            
            # Determinar estado
            if fecha_vencimiento < self.fecha_base:
                estado = random.choice(['aplicado', 'devuelto'])
            else:
                estado = random.choice(['pendiente', 'aplicado'])
            
            anticipo, created = Anticipo.objects.get_or_create(
                numero_anticipo=numero_anticipo,
                defaults={
                    'cliente': cliente,
                    'proyecto': proyecto,
                    'monto': monto,
                    'monto_aplicado': monto if estado == 'aplicado' else Decimal('0'),
                    'monto_disponible': Decimal('0') if estado == 'aplicado' else monto,
                    'tipo': tipo,
                    'estado': estado,
                    'fecha_recepcion': fecha_recepcion,
                    'fecha_vencimiento': fecha_vencimiento,
                    'metodo_pago': random.choice(['transferencia', 'cheque', 'efectivo']),
                    'referencia_pago': f"REF-{random.randint(10000, 99999)}",
                    'banco_origen': f"Banco {random.choice(['Industrial', 'Agrario', 'G&T', 'Banrural'])}",
                    'descripcion': f'Anticipo de {tipo} para {proyecto.nombre}',
                    'observaciones': 'Anticipo generado automáticamente para pruebas'
                }
            )
            
            if created:
                anticipos_creados.append(anticipo)
                if i % 5 == 0:
                    self.logger.info(f"Anticipos creados: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de anticipos creados: {len(anticipos_creados)}")
        return anticipos_creados
    
    def generar_logs_actividad(self, usuarios, cantidad=100):
        """Genera logs de actividad del sistema"""
        self.logger.info(f"Generando {cantidad} logs de actividad...")
        
        acciones = [
            'LOGIN', 'LOGOUT', 'PROYECTO_CREADO', 'PROYECTO_ACTUALIZADO', 'FACTURA_EMITIDA',
            'GASTO_REGISTRADO', 'ANTICIPO_APLICADO', 'REPORTE_GENERADO', 'USUARIO_CREADO',
            'BACKUP_REALIZADO', 'SISTEMA_ACTUALIZADO', 'NOTIFICACION_ENVIADA'
        ]
        
        modulos = [
            'Autenticación', 'Proyectos', 'Facturación', 'Gastos', 'Anticipos',
            'Reportes', 'Usuarios', 'Sistema', 'Notificaciones', 'Dashboard'
        ]
        
        logs_creados = []
        for i in range(cantidad):
            usuario = random.choice(usuarios)
            accion = random.choice(acciones)
            modulo = random.choice(modulos)
            
            # Generar fecha de actividad
            fecha_actividad = self.fecha_base - timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            log, created = LogActividad.objects.get_or_create(
                usuario=usuario,
                accion=accion,
                modulo=modulo,
                fecha_actividad=fecha_actividad,
                defaults={
                    'descripcion': f'Actividad {accion.lower()} en módulo {modulo.lower()}',
                    'ip_address': f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            if created:
                logs_creados.append(log)
                if i % 50 == 0:
                    self.logger.info(f"Logs creados: {i+1}/{cantidad}")
        
        self.logger.info(f"Total de logs creados: {len(logs_creados)}")
        return logs_creados
    
    def generar_datos_completos(self):
        """Genera todos los datos del sistema"""
        self.logger.info("INICIANDO GENERACION DE DATOS MASIVOS")
        self.logger.info("=" * 60)
        
        try:
            # 1. Roles y usuarios
            self.logger.info("PASO 1: Generando roles y usuarios...")
            roles = self.generar_roles()
            usuarios = self.generar_usuarios_y_perfiles(roles)
            
            # 2. Categorías de gasto
            self.logger.info("PASO 2: Generando categorías de gasto...")
            categorias = self.generar_categorias_gasto()
            
            # 3. Clientes
            self.logger.info("PASO 3: Generando clientes...")
            clientes = self.generar_clientes(200)
            
            # 4. Colaboradores
            self.logger.info("PASO 4: Generando colaboradores...")
            colaboradores = self.generar_colaboradores(30)
            
            # 5. Proyectos
            self.logger.info("PASO 5: Generando proyectos...")
            proyectos = self.generar_proyectos(clientes, 80)
            
            # 6. Gastos
            self.logger.info("PASO 6: Generando gastos...")
            gastos = self.generar_gastos(proyectos, categorias, 300)
            
            # 7. Facturas
            self.logger.info("PASO 7: Generando facturas...")
            facturas = self.generar_facturas(proyectos, clientes, 50)
            
            # 8. Anticipos
            self.logger.info("PASO 8: Generando anticipos...")
            anticipos = self.generar_anticipos(proyectos, clientes, 20)
            
            # 9. Logs de actividad
            self.logger.info("PASO 9: Generando logs de actividad...")
            logs = self.generar_logs_actividad(usuarios, 100)
            
            # Resumen final
            self.logger.info("=" * 60)
            self.logger.info("GENERACION DE DATOS COMPLETADA EXITOSAMENTE")
            self.logger.info("=" * 60)
            self.logger.info(f"RESUMEN DE DATOS GENERADOS:")
            self.logger.info(f"   • Roles: {len(roles)}")
            self.logger.info(f"   • Usuarios: {len(usuarios)}")
            self.logger.info(f"   • Categorías de Gasto: {len(categorias)}")
            self.logger.info(f"   • Clientes: {len(clientes)}")
            self.logger.info(f"   • Colaboradores: {len(colaboradores)}")
            self.logger.info(f"   • Proyectos: {len(proyectos)}")
            self.logger.info(f"   • Gastos: {len(gastos)}")
            self.logger.info(f"   • Facturas: {len(facturas)}")
            self.logger.info(f"   • Anticipos: {len(anticipos)}")
            self.logger.info(f"   • Logs de Actividad: {len(logs)}")
            self.logger.info("=" * 60)
            self.logger.info("El sistema está listo para pruebas de rendimiento!")
            self.logger.info("Credenciales de acceso:")
            self.logger.info("   • Usuario: admin")
            self.logger.info("   • Contraseña: admin123")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error durante la generación de datos: {e}")
            return False

def main():
    """Función principal"""
    print("GENERADOR DE DATOS MASIVOS - SISTEMA DE CONSTRUCCION")
    print("=" * 70)
    print("Este script generará datos realistas para probar:")
    print("• Dashboard con gráficos")
    print("• Generación de reportes IA")
    print("• Módulos de inteligencia artificial")
    print("• Rendimiento del sistema con carga de datos")
    print("=" * 70)
    
    respuesta = input("¿Deseas continuar? (s/n): ").lower().strip()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("Operación cancelada por el usuario")
        return
    
    print("\nIniciando generación de datos...")
    
    generador = GeneradorDatosMasivos()
    exito = generador.generar_datos_completos()
    
    if exito:
        print("\n¡Datos generados exitosamente!")
        print("Ahora puedes:")
        print("1. Iniciar el servidor: python manage.py runserver")
        print("2. Acceder al dashboard: http://127.0.0.1:8000/")
        print("3. Probar la generación de reportes IA")
        print("4. Verificar el rendimiento del sistema")
    else:
        print("\nError durante la generación de datos")
        print("Revisa los logs para más detalles")

if __name__ == "__main__":
    main()
