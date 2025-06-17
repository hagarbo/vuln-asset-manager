from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
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

        if user.rol == 'admin':
            return repository.get_all()
        elif user.rol == 'analista':
            return repository.get_by_activos_analista(user.id)
        return repository.model.objects.none()

    def delete(self, request, *args, **kwargs):
        try:
            av = self.get_object()
            nombre = f"{av.activo.nombre} - {av.vulnerabilidad.cve_id}"
            repository = ActivoVulnerabilidadRepository()
            if repository.delete(av.id):
                messages.success(request, f'Relación activo-vulnerabilidad "{nombre}" eliminada correctamente.')
                return super().delete(request, *args, **kwargs)
            else:
                messages.error(request, 'No se pudo eliminar la relación activo-vulnerabilidad.')
                return self.get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error al eliminar la relación activo-vulnerabilidad: {str(e)}')
            return self.get(request, *args, **kwargs) 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Eliminar {self.model._meta.verbose_name.title()}"
        context['page_subtitle'] = f"¿Estás seguro de que deseas eliminar {self.object}?"
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Activo-Vulnerabilidad", "url": "/activo-vulnerabilidad/"},
            {"label": "Eliminar"}
        ]
        return context