from django.urls import reverse_lazy
from django.views.generic import CreateView
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.forms.activo.creation import ActivoCreationForm

class ActivoCreateView(RoleRequiredMixin, CreateView):
    model = Activo
    form_class = ActivoCreationForm
    template_name = 'vuln_manager/activo/form.html'
    success_url = reverse_lazy('vuln_manager:activo_list')
    allowed_roles = ['admin', 'analista']

    def form_valid(self, form):
        activo = form.save(commit=False)
        ActivoRepository().create(**form.cleaned_data)
        return super().form_valid(form) 