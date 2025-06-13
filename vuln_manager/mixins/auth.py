from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

class CustomLoginRequiredMixin(AccessMixin):
    """
    Mixin que asegura que un usuario esté autenticado.
    Si no está autenticado, redirige a la página de login.
    
    Attributes:
        login_url (str): URL a la que redirigir si el usuario no está autenticado.
    """
    login_url = reverse_lazy('vuln_manager:login')

    def dispatch(self, request, *args, **kwargs):
        """
        Verifica si el usuario está autenticado antes de procesar la vista.
        
        Args:
            request: La petición HTTP.
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos de palabra clave adicionales.
            
        Returns:
            La respuesta de la vista si el usuario está autenticado,
            o una redirección al login si no lo está.
        """
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs) 