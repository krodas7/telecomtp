from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PermisosMiddleware:
    """
    Middleware para verificar permisos de usuario de forma automática
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que requieren permisos específicos
        self.permisos_requeridos = {
            # Gestión de usuarios
            'usuarios_lista_mejorada': 'usuarios.ver',
            'usuario_crear_mejorado': 'usuarios.crear',
            'usuario_editar_mejorado': 'usuarios.editar',
            
            # Gestión de roles
            'roles_lista_mejorada': 'roles.ver',
            'rol_crear_mejorado': 'roles.crear',
            'rol_editar_mejorado': 'roles.editar',
            'rol_eliminar_mejorado': 'roles.eliminar',
            
            # Gestor de permisos
            'permisos_gestor': 'permisos.ver',
            'permisos_actualizar_masivo': 'permisos.editar',
            
            # Dashboard de usuarios
            'usuarios_dashboard': 'usuarios.ver',
            
            # Gestión de clientes
            'clientes_list': 'clientes.ver',
            'cliente_create': 'clientes.crear',
            'cliente_edit': 'clientes.editar',
            'cliente_delete': 'clientes.eliminar',
            
            # Gestión de proyectos
            'proyectos_list': 'proyectos.ver',
            'proyecto_create': 'proyectos.crear',
            'proyecto_edit': 'proyectos.editar',
            'proyecto_delete': 'proyectos.eliminar',
            
            # Gestión de facturas
            'facturas_list': 'facturas.ver',
            'factura_create': 'facturas.crear',
            'factura_edit': 'facturas.editar',
            'factura_delete': 'facturas.eliminar',
            
            # Gestión de gastos
            'gastos_list': 'gastos.ver',
            'gasto_create': 'gastos.crear',
            'gasto_edit': 'gastos.editar',
            'gasto_delete': 'gastos.eliminar',
            
            # Gestión de colaboradores
            'colaboradores_list': 'colaboradores.ver',
            'colaborador_create': 'colaboradores.crear',
            'colaborador_edit': 'colaboradores.editar',
            'colaborador_delete': 'colaboradores.eliminar',
        }
        
        # URLs que solo requieren estar autenticado
        self.solo_autenticado = {
            'dashboard',
            'perfil',
            'logout',
        }
        
        # URLs públicas (no requieren autenticación)
        self.urls_publicas = {
            'login',
            'offline',
            'offline_page',
        }

    def __call__(self, request):
        # Obtener el nombre de la vista actual
        view_name = request.resolver_match.url_name if request.resolver_match else None
        
        # Si no hay nombre de vista, continuar
        if not view_name:
            return self.get_response(request)
        
        # Si es una URL pública, continuar
        if view_name in self.urls_publicas:
            return self.get_response(request)
        
        # Si el usuario no está autenticado
        if not request.user.is_authenticated:
            # Redirigir a login si no es una URL pública
            if view_name not in self.urls_publicas:
                messages.warning(request, 'Debes iniciar sesión para acceder a esta página')
                return redirect('login')
            return self.get_response(request)
        
        # Si es superusuario, permitir todo
        if request.user.is_superuser:
            return self.get_response(request)
        
        # Verificar si solo requiere autenticación
        if view_name in self.solo_autenticado:
            return self.get_response(request)
        
        # Verificar permisos específicos
        if view_name in self.permisos_requeridos:
            permiso_requerido = self.permisos_requeridos[view_name]
            
            # Verificar si el usuario tiene el permiso
            if not self.tiene_permiso(request.user, permiso_requerido):
                logger.warning(f"Usuario {request.user.username} intentó acceder a {view_name} sin permiso {permiso_requerido}")
                messages.error(request, f'No tienes permisos para acceder a esta sección. Se requiere: {permiso_requerido}')
                return redirect('dashboard')
        
        return self.get_response(request)
    
    def tiene_permiso(self, user, codigo_permiso):
        """
        Verifica si el usuario tiene un permiso específico
        """
        try:
            # Obtener el perfil del usuario
            if hasattr(user, 'perfilusuario'):
                perfil = user.perfilusuario
                return perfil.tiene_permiso(codigo_permiso)
            return False
        except Exception as e:
            logger.error(f"Error verificando permiso {codigo_permiso} para usuario {user.username}: {e}")
            return False


class LogActividadMiddleware:
    """
    Middleware para registrar actividad de usuarios
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Solo registrar si el usuario está autenticado y no es una petición AJAX
        if (request.user.is_authenticated and 
            not request.headers.get('X-Requested-With') == 'XMLHttpRequest' and
            request.method in ['POST', 'PUT', 'DELETE']):
            
            try:
                from .models import LogActividad
                
                # Obtener información de la vista
                view_name = request.resolver_match.url_name if request.resolver_match else 'unknown'
                
                # Determinar la acción basada en el método HTTP
                accion_map = {
                    'POST': 'Crear/Actualizar',
                    'PUT': 'Actualizar',
                    'DELETE': 'Eliminar',
                }
                accion = accion_map.get(request.method, 'Acción')
                
                # Determinar el módulo basado en la URL
                modulo = self.determinar_modulo(request.path)
                
                # Crear log de actividad
                LogActividad.objects.create(
                    usuario=request.user,
                    accion=accion,
                    modulo=modulo,
                    descripcion=f'{accion} en {view_name}',
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                
            except Exception as e:
                logger.error(f"Error creando log de actividad: {e}")
        
        return response
    
    def determinar_modulo(self, path):
        """
        Determina el módulo basado en la ruta
        """
        if '/usuarios' in path:
            return 'Usuarios'
        elif '/roles' in path:
            return 'Roles'
        elif '/clientes' in path:
            return 'Clientes'
        elif '/proyectos' in path:
            return 'Proyectos'
        elif '/facturas' in path:
            return 'Facturas'
        elif '/gastos' in path:
            return 'Gastos'
        elif '/colaboradores' in path:
            return 'Colaboradores'
        elif '/inventario' in path:
            return 'Inventario'
        else:
            return 'Sistema'
    
    def get_client_ip(self, request):
        """
        Obtiene la IP real del cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
