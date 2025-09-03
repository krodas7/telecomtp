from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Rol, Modulo, Permiso, RolPermiso

class Command(BaseCommand):
    help = 'Inicializa los roles predefinidos del sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando inicialización de roles...'))
        
        with transaction.atomic():
            # Crear roles predefinidos
            roles_data = [
                {
                    'nombre': 'Superusuario',
                    'descripcion': 'Acceso completo a todo el sistema. Puede gestionar usuarios, roles y configuraciones del sistema.'
                },
                {
                    'nombre': 'Administrador',
                    'descripcion': 'Administrador con permisos amplios. Puede gestionar proyectos, clientes, facturas y reportes.'
                },
                {
                    'nombre': 'Encargado de Proyecto',
                    'descripcion': 'Gestión de proyectos y clientes. Puede crear y editar proyectos, gestionar colaboradores y ver reportes.'
                },
                {
                    'nombre': 'Colaborador',
                    'descripcion': 'Acceso limitado de solo lectura. Puede ver proyectos asignados y reportes básicos.'
                },
                {
                    'nombre': 'Contador',
                    'descripcion': 'Gestión de facturas, pagos y reportes financieros. Acceso completo a módulos financieros.'
                }
            ]
            
            roles_creados = []
            for rol_data in roles_data:
                rol, created = Rol.objects.get_or_create(
                    nombre=rol_data['nombre'],
                    defaults={'descripcion': rol_data['descripcion']}
                )
                if created:
                    roles_creados.append(rol)
                    self.stdout.write(f'  ✅ Rol creado: {rol.nombre}')
                else:
                    self.stdout.write(f'  ⚠️ Rol ya existe: {rol.nombre}')
            
            # Crear módulos del sistema
            modulos_data = [
                {
                    'nombre': 'Dashboard',
                    'descripcion': 'Panel principal del sistema',
                    'icono': 'fas fa-tachometer-alt',
                    'orden': 1
                },
                {
                    'nombre': 'Clientes',
                    'descripcion': 'Gestión de clientes',
                    'icono': 'fas fa-users',
                    'orden': 2
                },
                {
                    'nombre': 'Proyectos',
                    'descripcion': 'Gestión de proyectos',
                    'icono': 'fas fa-project-diagram',
                    'orden': 3
                },
                {
                    'nombre': 'Colaboradores',
                    'descripcion': 'Gestión de colaboradores',
                    'icono': 'fas fa-user-friends',
                    'orden': 4
                },
                {
                    'nombre': 'Facturas',
                    'descripcion': 'Gestión de facturas',
                    'icono': 'fas fa-file-invoice-dollar',
                    'orden': 5
                },
                {
                    'nombre': 'Gastos',
                    'descripcion': 'Gestión de gastos',
                    'icono': 'fas fa-money-bill-wave',
                    'orden': 6
                },
                {
                    'nombre': 'Pagos',
                    'descripcion': 'Gestión de pagos',
                    'icono': 'fas fa-credit-card',
                    'orden': 7
                },
                {
                    'nombre': 'Anticipos',
                    'descripcion': 'Gestión de anticipos',
                    'icono': 'fas fa-hand-holding-usd',
                    'orden': 8
                },
                {
                    'nombre': 'Reportes',
                    'descripcion': 'Reportes del sistema',
                    'icono': 'fas fa-chart-bar',
                    'orden': 9
                },
                {
                    'nombre': 'Usuarios',
                    'descripcion': 'Gestión de usuarios',
                    'icono': 'fas fa-user-cog',
                    'orden': 10
                },
                {
                    'nombre': 'Archivos',
                    'descripcion': 'Gestión de archivos y documentos',
                    'icono': 'fas fa-folder-open',
                    'orden': 11
                },
                {
                    'nombre': 'Inventario',
                    'descripcion': 'Gestión de inventario y materiales',
                    'icono': 'fas fa-boxes',
                    'orden': 12
                },
                {
                    'nombre': 'Rentabilidad',
                    'descripcion': 'Análisis de rentabilidad y reportes financieros',
                    'icono': 'fas fa-chart-line',
                    'orden': 13
                }
            ]
            
            modulos_creados = []
            for modulo_data in modulos_data:
                modulo, created = Modulo.objects.get_or_create(
                    nombre=modulo_data['nombre'],
                    defaults={
                        'descripcion': modulo_data['descripcion'],
                        'icono': modulo_data['icono'],
                        'orden': modulo_data['orden']
                    }
                )
                if created:
                    modulos_creados.append(modulo)
                    self.stdout.write(f'  ✅ Módulo creado: {modulo.nombre}')
                else:
                    self.stdout.write(f'  ⚠️ Módulo ya existe: {modulo.nombre}')
            
            # Crear permisos básicos
            tipos_permisos = ['ver', 'crear', 'editar', 'eliminar', 'exportar']
            
            for modulo in Modulo.objects.all():
                for tipo in tipos_permisos:
                    codigo = f'{tipo}_{modulo.nombre.lower()}'
                    permiso, created = Permiso.objects.get_or_create(
                        codigo=codigo,
                        defaults={
                            'nombre': f'{tipo.title()} {modulo.nombre}',
                            'modulo': modulo,
                            'descripcion': f'Permiso para {tipo} en {modulo.nombre}',
                            'tipo': tipo
                        }
                    )
                    if created:
                        self.stdout.write(f'  ✅ Permiso creado: {permiso.nombre}')
                    else:
                        self.stdout.write(f'  ⚠️ Permiso ya existe: {permiso.nombre}')
            
            # Asignar permisos a roles
            self.asignar_permisos_roles()
            
        self.stdout.write(self.style.SUCCESS('✅ Inicialización de roles completada exitosamente!'))
    
    def asignar_permisos_roles(self):
        """Asigna permisos específicos a cada rol"""
        
        # Superusuario - Todos los permisos
        rol_superusuario = Rol.objects.get(nombre='Superusuario')
        permisos_superusuario = Permiso.objects.all()
        for permiso in permisos_superusuario:
            RolPermiso.objects.get_or_create(rol=rol_superusuario, permiso=permiso)
        self.stdout.write(f'  ✅ Permisos asignados a: {rol_superusuario.nombre}')
        
        # Administrador - Permisos amplios excepto gestión de usuarios
        rol_admin = Rol.objects.get(nombre='Administrador')
        permisos_admin = Permiso.objects.exclude(
            modulo__nombre='Usuarios'
        ).exclude(
            nombre__startswith='eliminar_usuarios'
        )
        for permiso in permisos_admin:
            RolPermiso.objects.get_or_create(rol=rol_admin, permiso=permiso)
        self.stdout.write(f'  ✅ Permisos asignados a: {rol_admin.nombre}')
        
        # Encargado de Proyecto - Gestión de proyectos y clientes
        rol_encargado = Rol.objects.get(nombre='Encargado de Proyecto')
        modulos_encargado = ['Dashboard', 'Clientes', 'Proyectos', 'Colaboradores', 'Anticipos', 'Archivos', 'Inventario']
        permisos_encargado = Permiso.objects.filter(
            modulo__nombre__in=modulos_encargado
        ).exclude(
            nombre__startswith='eliminar_'
        )
        for permiso in permisos_encargado:
            RolPermiso.objects.get_or_create(rol=rol_encargado, permiso=permiso)
        self.stdout.write(f'  ✅ Permisos asignados a: {rol_encargado.nombre}')
        
        # Colaborador - Solo lectura
        rol_colaborador = Rol.objects.get(nombre='Colaborador')
        permisos_colaborador = Permiso.objects.filter(
            nombre__startswith='ver_'
        )
        for permiso in permisos_colaborador:
            RolPermiso.objects.get_or_create(rol=rol_colaborador, permiso=permiso)
        self.stdout.write(f'  ✅ Permisos asignados a: {rol_colaborador.nombre}')
        
        # Contador - Módulos financieros
        rol_contador = Rol.objects.get(nombre='Contador')
        modulos_contador = ['Dashboard', 'Facturas', 'Gastos', 'Pagos', 'Reportes', 'Rentabilidad']
        permisos_contador = Permiso.objects.filter(
            modulo__nombre__in=modulos_contador
        )
        for permiso in permisos_contador:
            RolPermiso.objects.get_or_create(rol=rol_contador, permiso=permiso)
        self.stdout.write(f'  ✅ Permisos asignados a: {rol_contador.nombre}')
