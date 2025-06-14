from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin

class VulnerabilidadUpdateView(RoleRequiredMixin, UpdateView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad/form.html'
    success_url = reverse_lazy('vuln_manager:vulnerabilidad_list')
    allowed_roles = ['admin', 'analista'] 