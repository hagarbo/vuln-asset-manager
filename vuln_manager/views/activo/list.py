from django.views.generic import ListView
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ActivoListView(RoleRequiredMixin, ListView):
    model = Activo
    template_name = 'vuln_manager/activos/list.html'
    context_object_name = 'activos'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        if user.es_admin():
            return ActivoRepository().get_all()
        elif user.es_analista():
            return ActivoRepository().get_by_analista(user)
        elif user.es_cliente():
            return ActivoRepository().get_by_cliente(user.cliente)
        return Activo.objects.none() 