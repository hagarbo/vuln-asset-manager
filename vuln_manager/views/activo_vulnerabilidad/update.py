from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadUpdateView(RoleRequiredMixin, UpdateView):
    model = ActivoVulnerabilidad
    fields = ['estado', 'notas']
    template_name = 'vuln_manager/activo_vulnerabilidad/form.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list')
    allowed_roles = ['admin', 'analista']

    def get_queryset(self):
        repository = ActivoVulnerabilidadRepository()
        user = self.request.user

        if user.rol == 'admin':
            return repository.get_all()
        elif user.rol == 'analista':
            return repository.get_by_activos_analista(user.id)
        return repository.model.objects.none()

    def form_valid(self, form):
        try:
            repository = ActivoVulnerabilidadRepository()
            instance = repository.update(self.object.id, **form.cleaned_data)
            if instance:
                messages.success(
                    self.request, 
                    f'Relación activo-vulnerabilidad "{instance.activo.nombre} - {instance.vulnerabilidad.cve_id}" actualizada correctamente.'
                )
                return super().form_valid(form)
            messages.error(self.request, 'No se pudo actualizar la relación activo-vulnerabilidad.')
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f'Error al actualizar la relación activo-vulnerabilidad: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form) 