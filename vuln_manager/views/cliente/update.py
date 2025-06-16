from django.views.generic import UpdateView
from django.urls import reverse_lazy
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository
from vuln_manager.forms.cliente.update import ClienteUpdateForm

class ClienteUpdateView(RoleRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteUpdateForm
    template_name = 'vuln_manager/cliente/form.html'
    success_url = reverse_lazy('vuln_manager:cliente_list')
    allowed_roles = ['admin']

    def get_queryset(self):
        user = self.request.user
        repository = ClienteRepository()
        if user.es_admin():
            return repository.get_all()
        return repository.get_none() 