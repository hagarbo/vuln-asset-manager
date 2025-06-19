from django.views.generic import DetailView
from django.core.paginator import Paginator
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
        if user.es_admin:
            return repository.get_all()
        elif user.es_analista:
            return repository.get_by_analista(user)
        elif user.es_cliente:
            # Si Cliente tiene FK a Usuario, filtrar por ese campo
            return repository.get_by_usuario(user)
        return repository.get_none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.es_admin or user.es_analista or user.es_cliente:
            activos_queryset = self.object.activos.all()
        paginator = Paginator(activos_queryset, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['activos'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1
        context['paginator'] = paginator
        context['analistas'] = self.object.analistas.all()
        return context 