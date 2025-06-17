from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.forms import ActivoCreationForm

class ActivoCreateView(RoleRequiredMixin, CreateView):
    model = Activo
    form_class = ActivoCreationForm
    template_name = 'vuln_manager/activo/create.html'
    success_url = reverse_lazy('vuln_manager:activo_list')
    allowed_roles = ['admin', 'analista']

    def form_valid(self, form):
        try:
            repository = ActivoRepository()
            instance = repository.create(**form.cleaned_data)
            if instance:
                messages.success(self.request, f'Activo "{instance.nombre}" creado exitosamente.')
                return super().form_valid(form)
            messages.error(self.request, 'No se pudo crear el activo.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear el activo: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crear Activo'
        context['form_subtitle'] = 'Crea un nuevo activo en el sistema'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Activos", "url": "/activo/"},
            {"label": "Crear"}
        ]
        context['card_title'] = 'Datos del Activo'
        return context