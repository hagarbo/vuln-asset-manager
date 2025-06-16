from django.views.generic import DetailView
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository

class ClienteDetailView(RoleRequiredMixin, DetailView):
    model = Cliente
    template_name = 'vuln_manager/cliente/detail.html'
    context_object_name = 'cliente'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_repo = UsuarioRepository()
        analistas = usuario_repo.get_analistas_by_cliente(self.object)
        print(f"Cliente: {self.object.nombre}")
        print(f"Analistas encontrados: {analistas.count()}")
        print(f"IDs de analistas: {list(analistas.values_list('id', flat=True))}")
        context['analistas'] = analistas
        return context 