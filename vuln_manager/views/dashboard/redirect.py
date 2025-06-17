from django.views.generic import RedirectView
from vuln_manager.mixins.auth import CustomLoginRequiredMixin

class HomeView(CustomLoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.es_admin:
            return '/dashboard/admin/'
        elif user.es_analista:
            return '/dashboard/analista/'
        elif user.es_cliente:
            return '/dashboard/cliente/'
        return '/'