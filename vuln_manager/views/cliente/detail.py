from django.views.generic import DetailView
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository

class ClienteDetailView(RoleRequiredMixin, DetailView):
    model = Cliente
    template_name = 'vuln_manager/cliente/detail.html'
    context_object_name = 'cliente'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        if user.es_admin():
            return ClienteRepository.get_all()
        elif user.es_analista():
            return ClienteRepository.get_by_analista(user)
        elif user.es_cliente():
            # Si Cliente tiene FK a Usuario, filtrar por ese campo
            return ClienteRepository.get_by_usuario(user)
        return ClienteRepository.get_none() 