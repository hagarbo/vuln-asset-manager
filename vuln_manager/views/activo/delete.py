from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ActivoDeleteView(RoleRequiredMixin, DeleteView):
    model = Activo
    template_name = 'vuln_manager/activo/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:activo_list')
    allowed_roles = ['admin', 'analista']

    def delete(self, request, *args, **kwargs):
        try:
            activo = self.get_object()
            nombre = activo.nombre
            repository = ActivoRepository()
            if repository.delete(activo.id):
                messages.success(request, f'Activo "{nombre}" eliminado correctamente.')
                return super().delete(request, *args, **kwargs)
            else:
                messages.error(request, 'No se pudo eliminar el activo.')
                return self.get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error al eliminar el activo: {str(e)}')
            return self.get(request, *args, **kwargs) 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context