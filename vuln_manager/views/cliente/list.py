from django.views.generic import ListView
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository

class ClienteListView(RoleRequiredMixin, ListView):
    model = Cliente
    template_name = 'vuln_manager/cliente/list.html'
    context_object_name = 'clientes'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        repository = ClienteRepository()
        if user.es_admin():
            return repository.get_all()
        elif user.es_analista():
            return repository.get_by_analista(user)
        elif user.es_cliente():
            # Si Cliente tiene FK a Usuario, filtrar por ese campo
            return repository.get_by_usuario(user)
        return repository.get_none() 