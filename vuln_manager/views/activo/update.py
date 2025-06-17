from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.forms.activo.update import ActivoUpdateForm

class ActivoUpdateView(RoleRequiredMixin, UpdateView):
    model = Activo
    form_class = ActivoUpdateForm
    template_name = 'vuln_manager/activo/create.html'
    success_url = reverse_lazy('vuln_manager:activo_list')
    allowed_roles = ['admin', 'analista']

    def form_valid(self, form):
        try:
            repository = ActivoRepository()
            instance = repository.update(self.object.id, **form.cleaned_data)
            if instance:
                messages.success(self.request, f'Activo "{instance.nombre}" actualizado correctamente.')
                return super().form_valid(form)
            messages.error(self.request, 'No se pudo actualizar el activo.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar el activo: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Activo'
        context['form_subtitle'] = 'Modifica los datos del activo'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Activos", "url": "/activo/"},
            {"label": "Editar"}
        ]
        context['card_title'] = 'Datos del Activo'
        return context