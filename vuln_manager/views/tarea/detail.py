from django.views.generic import DetailView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.ejecucion_tarea import EjecucionTarea
from django.core.paginator import Paginator
from vuln_manager.repository.tarea.tarea_repository import TareaRepository
from vuln_manager.repository.tarea.ejecucion_tarea_repository import EjecucionTareaRepository

class TareaDetailView(RoleRequiredMixin, DetailView):
    model = Tarea
    template_name = 'vuln_manager/tarea/detail.html'
    context_object_name = 'tarea'
    allowed_roles = ['admin']

    def get_queryset(self):
        return TareaRepository().get_all().select_related('creada_por')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el historial de ejecuciones paginado
        page = self.request.GET.get('page', 1)
        ejecuciones = EjecucionTareaRepository().get_by_tarea(self.object).order_by('-fecha_inicio')
        paginator = Paginator(ejecuciones, 5)
        context['ejecuciones'] = paginator.get_page(page)
        return context 