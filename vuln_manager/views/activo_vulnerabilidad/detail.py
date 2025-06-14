from django.views.generic import DetailView
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo_vulnerabilidad import ActivoVulnerabilidadRepository

class ActivoVulnerabilidadDetailView(RoleRequiredMixin, DetailView):
    model = ActivoVulnerabilidad
    template_name = 'vuln_manager/activo_vulnerabilidad/detail.html'
    context_object_name = 'activo_vulnerabilidad'
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