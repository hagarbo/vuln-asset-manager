from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from vuln_manager.models import ActivoVulnerabilidad

class ActivoVulnerabilidadDeleteView(LoginRequiredMixin, DeleteView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list') 