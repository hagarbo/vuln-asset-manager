from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from vuln_manager.forms.usuario.login import CustomAuthenticationForm

class CustomLoginView(LoginView):
    """
    Vista personalizada para el login.
    Redirige al dashboard correspondiente según el rol del usuario.
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        """
        Determina la URL de redirección después del login basado en el rol del usuario.
        Por defecto redirige al dashboard admin para evitar la landing page.
        """
        user = self.request.user
        if user.es_admin:
            return reverse_lazy('vuln_manager:dashboard_admin')
        elif user.es_analista:
            return reverse_lazy('vuln_manager:dashboard_analista')
        elif user.es_cliente:
            return reverse_lazy('vuln_manager:dashboard_cliente')
        # Si por algún motivo no tiene rol, redirigir al dashboard admin por defecto
        return reverse_lazy('vuln_manager:dashboard_admin') 