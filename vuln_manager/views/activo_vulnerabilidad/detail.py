from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from vuln_manager.models import ActivoVulnerabilidad

class ActivoVulnerabilidadDetailView(LoginRequiredMixin, DetailView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/detail.html'
    context_object_name = 'activo_vulnerabilidad' 