from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse


class WWWRedirectMiddleware:
    """
    Middleware para redirigir automáticamente entre www y no-www
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo aplicar en producción y si está habilitado
        if not settings.DEBUG and settings.USE_WWW_REDIRECT:
            host = request.get_host()
            
            # Si queremos redirigir www a no-www
            if settings.WWW_REDIRECT_TO_NON_WWW and host.startswith('www.'):
                new_host = host[4:]  # Remover 'www.'
                new_url = f"https://{new_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(new_url)
            
            # Si queremos redirigir no-www a www
            elif not settings.WWW_REDIRECT_TO_NON_WWW and not host.startswith('www.'):
                new_host = f"www.{host}"
                new_url = f"https://{new_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(new_url)
        
        response = self.get_response(request)
        return response


class SecurityHeadersMiddleware:
    """
    Middleware para agregar headers de seguridad
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Solo en producción
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
