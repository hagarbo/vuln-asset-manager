from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from vuln_manager.models import AnalistaCliente
from .auth import CustomLoginRequiredMixin

class RoleRequiredMixin(CustomLoginRequiredMixin):
    """
    Mixin que asegura que un usuario tenga uno de los roles requeridos.
    Redirige a la página de inicio si el rol no es válido.
    
    Attributes:
        allowed_roles (list): Lista de roles permitidos para acceder a la vista.
        login_url (str): URL a la que redirigir si el usuario no tiene permisos.
    """
    allowed_roles = []  # Se debe sobrescribir en la vista
    login_url = reverse_lazy('vuln_manager:login')

    def dispatch(self, request, *args, **kwargs):
        """
        Verifica si el usuario tiene uno de los roles permitidos.
        
        Args:
            request: La petición HTTP.
            *args: Argumentos posicionales adicionales.
            **kwargs: Argumentos de palabra clave adicionales.
            
        Returns:
            La respuesta de la vista si el usuario tiene el rol adecuado,
            o una redirección al login si no lo tiene.
        """
        if not request.user.is_authenticated or request.user.rol not in self.allowed_roles:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin para verificar que el usuario es administrador.
    """
    allowed_roles = ['admin']

class AnalistaRequiredMixin(RoleRequiredMixin):
    """
    Mixin para verificar que el usuario es analista.
    """
    allowed_roles = ['analista']

class ClienteRequiredMixin(RoleRequiredMixin):
    """
    Mixin para verificar que el usuario es cliente.
    """
    allowed_roles = ['cliente']

class ClientePropioMixin(UserPassesTestMixin):
    """
    Mixin para verificar que el usuario está accediendo a sus propios datos.
    Solo aplicable para usuarios con rol 'cliente'.
    
    Attributes:
        login_url (str): URL a la que redirigir si el usuario no tiene permisos.
    """
    login_url = reverse_lazy('vuln_manager:login')

    def test_func(self):
        """
        Verifica si el usuario está accediendo a sus propios datos.
        
        Returns:
            bool: True si el usuario está accediendo a sus propios datos,
                  False en caso contrario.
        """
        if not self.request.user.is_authenticated:
            return False
        if not self.request.user.es_cliente:
            return False
        cliente_id = self.kwargs.get('pk') or self.kwargs.get('cliente_id')
        return str(self.request.user.id) == str(cliente_id)

class AnalistaClienteMixin(UserPassesTestMixin):
    """
    Mixin para verificar que el analista está accediendo a datos de sus clientes asignados.
    
    Attributes:
        login_url (str): URL a la que redirigir si el usuario no tiene permisos.
    """
    login_url = reverse_lazy('vuln_manager:login')

    def test_func(self):
        """
        Verifica si el analista está asignado al cliente especificado.
        
        Returns:
            bool: True si el analista está asignado al cliente,
                  False en caso contrario.
        """
        cliente_id = self.kwargs.get('cliente_id')
        if not cliente_id:
            return False
        return AnalistaCliente.objects.filter(
            analista=self.request.user,
            cliente_id=cliente_id
        ).exists() 