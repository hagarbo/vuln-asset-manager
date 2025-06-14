from django.views.generic import DeleteView
from django.urls import reverse_lazy
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin

class ClienteDeleteView(RoleRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'vuln_manager/cliente/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:cliente_list')
    allowed_roles = ['admin'] 