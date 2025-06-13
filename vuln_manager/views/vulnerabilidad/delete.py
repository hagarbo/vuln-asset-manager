from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin

class VulnerabilidadDeleteView(RoleRequiredMixin, DeleteView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidades/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:vulnerabilidad_list')
    allowed_roles = ['admin', 'analista'] 