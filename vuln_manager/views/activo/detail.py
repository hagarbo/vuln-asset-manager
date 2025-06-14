from django.views.generic import DetailView
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ActivoDetailView(RoleRequiredMixin, DetailView):
    model = Activo
    template_name = 'vuln_manager/activo/detail.html'
    context_object_name = 'activo'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        if user.es_admin():
            return ActivoRepository().get_all()
        elif user.es_analista():
            return ActivoRepository().get_by_analista(user)
        elif user.es_cliente():
            return ActivoRepository().get_by_cliente(user.cliente)
        return Activo.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activo = self.get_object()
        context['vulnerabilidades'] = ActivoVulnerabilidad.objects.filter(activo=activo).select_related('vulnerabilidad')
        return context 