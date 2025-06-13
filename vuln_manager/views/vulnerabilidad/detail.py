from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from vuln_manager.models import Vulnerabilidad, ActivoVulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin

class VulnerabilidadDetailView(RoleRequiredMixin, DetailView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidades/detail.html'
    context_object_name = 'vulnerabilidad'
    allowed_roles = ['admin', 'analista', 'gestor']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activos'] = ActivoVulnerabilidad.objects.filter(vulnerabilidad=self.object)
        return context 