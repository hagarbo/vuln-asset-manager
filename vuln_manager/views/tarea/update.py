from django.urls import reverse_lazy
from django.views.generic import UpdateView
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models import Tarea
from vuln_manager.forms import TareaForm

class TareaUpdateView(RoleRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'vuln_manager/tarea/form.html'
    success_url = reverse_lazy('vuln_manager:tarea_list')
    allowed_roles = ['admin'] 