from django.views.generic import DeleteView
from django.urls import reverse_lazy
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadDeleteView(RoleRequiredMixin, DeleteView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:activo_vulnerabilidad_list')
    allowed_roles = ['admin', 'analista']

    def get_queryset(self):
        repository = ActivoVulnerabilidadRepository()
        user = self.request.user

        if user.role == 'admin':
            return repository.get_all()
        else:  # analista
            return repository.get_by_activos_analista(user.id)

    def delete(self, request, *args, **kwargs):
        repository = ActivoVulnerabilidadRepository()
        success = repository.delete(self.get_object().id)
        if success:
            return super().delete(request, *args, **kwargs)
        return self.handle_no_permission() 