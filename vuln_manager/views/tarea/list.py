from django.views.generic import ListView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models import Tarea

class TareaListView(RoleRequiredMixin, ListView):
    model = Tarea
    template_name = 'vuln_manager/tarea/list.html'
    context_object_name = 'tareas'
    allowed_roles = ['admin']

    def get_queryset(self):
        return Tarea.objects.all().order_by('-created_at') 