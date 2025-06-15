from django.views.generic import DetailView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models import Tarea

class TareaDetailView(RoleRequiredMixin, DetailView):
    model = Tarea
    template_name = 'vuln_manager/tarea/detail.html'
    context_object_name = 'tarea'
    allowed_roles = ['admin'] 