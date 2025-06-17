from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.cliente.cliente_repository import ClienteRepository

class ClienteDeleteView(RoleRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'vuln_manager/cliente/confirm_delete.html'
    success_url = reverse_lazy('vuln_manager:cliente_list')
    allowed_roles = ['admin']

    def get_queryset(self):
        user = self.request.user
        repository = ClienteRepository()
        if user.es_admin:
            return repository.get_all()
        return repository.get_none()

    def delete(self, request, *args, **kwargs):
        try:
            cliente = self.get_object()
            nombre = cliente.nombre
            repository = ClienteRepository()
            if repository.delete(cliente.id):
                messages.success(request, f'Cliente "{nombre}" eliminado correctamente.')
                return super().delete(request, *args, **kwargs)
            else:
                messages.error(request, 'No se pudo eliminar el cliente.')
                return self.get(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, f'Error al eliminar el cliente: {str(e)}')
            return self.get(request, *args, **kwargs) 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Eliminar {self.model._meta.verbose_name.title()}"
        context['page_subtitle'] = f"¿Estás seguro de que deseas eliminar {self.object}?"
        context['breadcrumbs'] = [
             {"label": "Dashboard", "url": "/dashboard/"},
             {"label": "Clientes", "url": "/clientes/"},
             {"label": "Eliminar"}
         ]
        return context