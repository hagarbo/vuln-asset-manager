from django.views.generic import UpdateView
from django.urls import reverse_lazy
from vuln_manager.models import ActivoVulnerabilidad

class ActivoVulnerabilidadUpdateView(UpdateView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad_form.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list') 