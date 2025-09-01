from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import PerfilUsuario, Rol

class Command(BaseCommand):
    help = 'Lista todos los usuarios y sus roles asignados'

    def handle(self, *args, **options):
        self.stdout.write('📋 Lista de Usuarios y Roles')
        self.stdout.write('=' * 50)
        
        usuarios = User.objects.all().order_by('username')
        
        if not usuarios.exists():
            self.stdout.write('❌ No hay usuarios en el sistema')
            return
        
        for usuario in usuarios:
            try:
                perfil = PerfilUsuario.objects.get(usuario=usuario)
                rol = perfil.rol.nombre if perfil.rol else 'Sin rol'
                estado = '✅ Activo' if usuario.is_active else '❌ Inactivo'
                superuser = '👑 Superuser' if usuario.is_superuser else ''
            except PerfilUsuario.DoesNotExist:
                rol = 'Sin perfil'
                estado = '✅ Activo' if usuario.is_active else '❌ Inactivo'
                superuser = '👑 Superuser' if usuario.is_superuser else ''
            
            self.stdout.write(f'👤 {usuario.username}')
            self.stdout.write(f'   📧 Email: {usuario.email or "No especificado"}')
            self.stdout.write(f'   👤 Nombre: {usuario.get_full_name() or "No especificado"}')
            self.stdout.write(f'   🏷️ Rol: {rol}')
            self.stdout.write(f'   📊 Estado: {estado}')
            if superuser:
                self.stdout.write(f'   {superuser}')
            self.stdout.write('')
        
        # Estadísticas
        total_usuarios = usuarios.count()
        usuarios_activos = usuarios.filter(is_active=True).count()
        usuarios_superuser = usuarios.filter(is_superuser=True).count()
        
        self.stdout.write('📊 Estadísticas:')
        self.stdout.write(f'   Total usuarios: {total_usuarios}')
        self.stdout.write(f'   Usuarios activos: {usuarios_activos}')
        self.stdout.write(f'   Superusuarios: {usuarios_superuser}')
        
        # Roles disponibles
        roles = Rol.objects.all()
        if roles.exists():
            self.stdout.write('\n🏷️ Roles disponibles:')
            for rol in roles:
                usuarios_con_rol = PerfilUsuario.objects.filter(rol=rol).count()
                self.stdout.write(f'   • {rol.nombre}: {usuarios_con_rol} usuario(s)')
        
        self.stdout.write('\n💡 Comandos útiles:')
        self.stdout.write('   python manage.py asignar_rol_superusuario <username>')
        self.stdout.write('   python manage.py inicializar_roles')
