from django.views.generic import ListView
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin

class VulnerabilidadListView(RoleRequiredMixin, ListView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidades/list.html'
    context_object_name = 'vulnerabilidades'
    allowed_roles = ['admin', 'analista', 'gestor'] 