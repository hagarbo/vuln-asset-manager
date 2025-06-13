from django.urls import reverse_lazy
from django.views.generic import UpdateView
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.forms.activo.update import ActivoUpdateForm

class ActivoUpdateView(RoleRequiredMixin, UpdateView):
    model = Activo
    form_class = ActivoUpdateForm
    template_name = 'vuln_manager/activos/form.html'
    success_url = reverse_lazy('vuln_manager:activo_list')
    allowed_roles = ['admin', 'analista']

    def form_valid(self, form):
        activo = form.save(commit=False)
        ActivoRepository().update(activo.id, **form.cleaned_data)
        return super().form_valid(form) 