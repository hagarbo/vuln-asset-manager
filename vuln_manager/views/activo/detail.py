from django.views.generic import DetailView
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoDetailView(RoleRequiredMixin, DetailView):
    model = Activo
    template_name = 'vuln_manager/activo/detail.html'
    context_object_name = 'activo'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        repository = ActivoRepository()
        if user.es_admin:
            return repository.get_all()
        elif user.es_analista:
            return repository.get_by_analista(user)
        elif user.es_cliente:
            return repository.get_by_cliente(user.cliente)
        return repository.get_none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.es_admin:
            context['vulnerabilidades'] = self.object.vulnerabilidades.all()
        elif user.es_analista:
            context['vulnerabilidades'] = self.object.vulnerabilidades.all()
        elif user.es_cliente:
            context['vulnerabilidades'] = self.object.vulnerabilidades.all()
            
        return context 