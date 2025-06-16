from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository
from vuln_manager.forms.vulnerabilidad_update import VulnerabilidadUpdateForm

class VulnerabilidadUpdateView(RoleRequiredMixin, UpdateView):
    model = Vulnerabilidad
    form_class = VulnerabilidadUpdateForm
    template_name = 'vuln_manager/vulnerabilidad/form.html'
    success_url = reverse_lazy('vuln_manager:vulnerabilidad_list')
    allowed_roles = ['admin']

    def form_valid(self, form):
        repository = VulnerabilidadRepository()
        instance = repository.update(self.object.id, **form.cleaned_data)
        if instance:
            return super().form_valid(form)
        return self.form_invalid(form) 