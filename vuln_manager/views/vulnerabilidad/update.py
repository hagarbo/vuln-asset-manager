from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
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
        try:
            repository = VulnerabilidadRepository()
            instance = repository.update(self.object.id, **form.cleaned_data)
            if instance:
                messages.success(self.request, f'Vulnerabilidad "{instance.cve_id}" actualizada correctamente.')
                return super().form_valid(form)
            messages.error(self.request, 'No se pudo actualizar la vulnerabilidad.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar la vulnerabilidad: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Editar Vulnerabilidad'
        context['form_subtitle'] = 'Modifica los datos de la vulnerabilidad'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Vulnerabilidades", "url": "/vulnerabilidades/"},
            {"label": "Editar"}
        ]
        context['card_title'] = 'Datos de la Vulnerabilidad'
        return context