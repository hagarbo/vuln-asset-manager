from django.urls import reverse_lazy
from django.views.generic import DeleteView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models import Tarea

class TareaDeleteView(RoleRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'vuln_manager/tarea/delete.html'
    success_url = reverse_lazy('vuln_manager:tarea_list')
    allowed_roles = ['admin'] 