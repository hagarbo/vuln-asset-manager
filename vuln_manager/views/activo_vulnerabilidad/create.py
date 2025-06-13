from django.views.generic import CreateView
from django.urls import reverse_lazy
from vuln_manager.models import ActivoVulnerabilidad

class ActivoVulnerabilidadCreateView(CreateView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad_form.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list') 