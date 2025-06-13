from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from vuln_manager.models import ActivoVulnerabilidad

class ActivoVulnerabilidadListView(LoginRequiredMixin, ListView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/list.html'
    context_object_name = 'activo_vulnerabilidades' 