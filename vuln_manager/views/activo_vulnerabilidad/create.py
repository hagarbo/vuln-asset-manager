from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadCreateView(RoleRequiredMixin, CreateView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/create.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list')
    allowed_roles = ['admin', 'analista']
    fields = ['activo', 'vulnerabilidad', 'estado', 'notas']

    def form_valid(self, form):
        try:
            repository = ActivoVulnerabilidadRepository()
            instance = repository.create(**form.cleaned_data)
            if instance:
                messages.success(
                    self.request, 
                    f'Relación activo-vulnerabilidad "{instance.activo.nombre} - {instance.vulnerabilidad.cve_id}" creada exitosamente.'
                )
                return super().form_valid(form)
            messages.error(self.request, 'No se pudo crear la relación activo-vulnerabilidad.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al crear la relación activo-vulnerabilidad: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Crear Relación Activo-Vulnerabilidad'
        context['form_subtitle'] = 'Crea una nueva relación entre un activo y una vulnerabilidad'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Relaciones", "url": "/activo_vulnerabilidad/"},
            {"label": "Crear"}
        ]
        context['card_title'] = 'Datos de la Relación Activo-Vulnerabilidad'
        return context