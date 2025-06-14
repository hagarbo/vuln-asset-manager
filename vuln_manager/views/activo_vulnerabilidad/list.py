from django.views.generic import ListView
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadListView(RoleRequiredMixin, ListView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/list.html'
    context_object_name = 'activo_vulnerabilidades'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        repository = ActivoVulnerabilidadRepository()
        user = self.request.user

        if user.role == 'admin':
            return repository.get_all()
        elif user.role == 'analista':
            return repository.get_by_activos_analista(user.id)
        else:  # cliente
            return repository.get_by_activos_cliente(user.id) 