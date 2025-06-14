from django.views.generic import CreateView
from django.urls import reverse_lazy
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin

class ClienteCreateView(RoleRequiredMixin, CreateView):
    model = Cliente
    # form_class = ClienteForm
    template_name = 'vuln_manager/cliente/form.html'
    success_url = reverse_lazy('vuln_manager:cliente_list')
    allowed_roles = ['admin'] 