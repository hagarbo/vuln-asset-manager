from django.views.generic import TemplateView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.alerta.alerta import Alerta

class ClienteDashboardView(RoleRequiredMixin, TemplateView):
    template_name = 'vuln_manager/dashboard/cliente/index.html'
    allowed_roles = ['cliente']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Obtener solo los activos del cliente
        activos = Activo.objects.filter(cliente=user.cliente)
        total_activos = activos.count()
        # Alertas abiertas (no resueltas ni ignoradas)
        alertas_abiertas = Alerta.objects.filter(activo__cliente=user.cliente).exclude(estado__in=['resuelta', 'ignorada'])
        total_alertas_abiertas = alertas_abiertas.count()
        # Alertas críticas
        total_alertas_criticas = alertas_abiertas.filter(vulnerabilidad__severidad='critica').count()
        # Última alerta recibida
        ultima_alerta = Alerta.objects.filter(activo__cliente=user.cliente).order_by('-fecha_creacion').first()
        context.update({
            'total_activos': total_activos,
            'total_alertas_abiertas': total_alertas_abiertas,
            'total_alertas_criticas': total_alertas_criticas,
            'ultima_alerta': ultima_alerta,
        })
        return context 