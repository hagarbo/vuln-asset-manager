from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from vuln_manager.models import Vulnerabilidad, ActivoVulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class VulnerabilidadDetailView(RoleRequiredMixin, DetailView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad/detail.html'
    context_object_name = 'vulnerabilidad'
    allowed_roles = ['admin', 'analista', 'gestor']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activos'] = ActivoVulnerabilidadRepository().get_by_vulnerabilidad(self.object.id)
        context['page_title'] = 'Detalle de Vulnerabilidad'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Vulnerabilidades", "url": "/vulnerabilidades/"},
            {"label": "Detalle"}
        ]
        return context 