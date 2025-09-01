from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Rol, PerfilUsuario

class Command(BaseCommand):
    help = 'Asigna el rol de Superusuario al usuario especificado'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            # Obtener el usuario
            usuario = User.objects.get(username=username)
            
            # Obtener el rol de Superusuario
            rol_superusuario = Rol.objects.get(nombre='Superusuario')
            
            # Crear o actualizar el perfil de usuario
            perfil, created = PerfilUsuario.objects.get_or_create(
                usuario=usuario,
                defaults={'rol': rol_superusuario}
            )
            
            if not created:
                perfil.rol = rol_superusuario
                perfil.save()
                self.stdout.write(f'  ✅ Rol actualizado para: {usuario.username}')
            else:
                self.stdout.write(f'  ✅ Rol asignado a: {usuario.username}')
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Usuario "{usuario.username}" ahora tiene el rol de Superusuario')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: No se encontró el usuario "{username}"')
            )
        except Rol.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Error: No se encontró el rol "Superusuario". Ejecuta primero: python manage.py inicializar_roles')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
