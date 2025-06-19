from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models import Tarea

class TareaDeleteView(RoleRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'vuln_manager/tarea/delete.html'
    success_url = reverse_lazy('vuln_manager:tarea_list')
    allowed_roles = ['admin']

    def delete(self, request, *args, **kwargs):
        try:
            tarea = self.get_object()
            nombre = str(tarea)
            response = super().delete(request, *args, **kwargs)
            messages.success(request, f'Tarea "{nombre}" eliminada correctamente.')
            return response
        except Exception as e:
            messages.error(request, f'Error al eliminar la tarea: {str(e)}')
            return self.get(request, *args, **kwargs) 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context