from django.urls import reverse_lazy
from django.views.generic import DeleteView
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ActivoDeleteView(RoleRequiredMixin, DeleteView):
    model = Activo
    template_name = 'vuln_manager/activos/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:activo_list')
    allowed_roles = ['admin', 'analista']

    def delete(self, request, *args, **kwargs):
        activo = self.get_object()
        ActivoRepository().delete(activo.id)
        return super().delete(request, *args, **kwargs) 