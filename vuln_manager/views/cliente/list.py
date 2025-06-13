from django.views.generic import ListView
from vuln_manager.models import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin

class ClienteListView(RoleRequiredMixin, ListView):
    model = Cliente
    template_name = 'vuln_manager/clientes/list.html'
    context_object_name = 'clientes'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        if user.es_admin():
            return Cliente.objects.all()
        elif user.es_analista():
            return Cliente.objects.filter(analistas=user)
        elif user.es_cliente():
            return Cliente.objects.filter(id=user.cliente.id)
        return Cliente.objects.none() 