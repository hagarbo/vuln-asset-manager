from django.views.generic import ListView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea
from vuln_manager.repository.tarea.tarea_repository import TareaRepository

class TareaListView(RoleRequiredMixin, ListView):
    model = Tarea
    template_name = 'vuln_manager/tarea/list.html'
    context_object_name = 'tareas'
    allowed_roles = ['admin']

    def get_queryset(self):
        return TareaRepository().get_all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_tarea'] = TipoTarea.objects.filter(activo=True)
        return context 