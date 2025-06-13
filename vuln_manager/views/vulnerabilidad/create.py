from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin

class VulnerabilidadCreateView(RoleRequiredMixin, CreateView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidades/form.html'
    success_url = reverse_lazy('vuln_manager:vulnerabilidad_list')
    allowed_roles = ['admin', 'analista'] 