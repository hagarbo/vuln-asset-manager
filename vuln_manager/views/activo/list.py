from django.views.generic import ListView
from django.urls import reverse
from django.core.paginator import Paginator
from vuln_manager.models import Activo
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ActivoListView(RoleRequiredMixin, ListView):
    model = Activo
    template_name = 'vuln_manager/activo/list.html'
    context_object_name = 'activos'
    paginate_by = 10
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        ordering = self.request.GET.get('ordering', '-nombre')
        # Permitimos ordenar por nombre, cliente__nombre y tipo
        allowed_orderings = ['nombre', '-nombre', 'cliente__nombre', '-cliente__nombre', 'tipo', '-tipo']
        if ordering not in allowed_orderings:
            ordering = '-nombre'
        user = self.request.user
        repository = ActivoRepository()
        
        if user.es_admin:
            return repository.get_all().order_by(ordering)
        elif user.es_analista:
            return repository.get_by_analista(user).order_by(ordering)
        elif user.es_cliente:
            return repository.get_by_cliente(user.cliente).order_by(ordering)
            
        return repository.get_none().order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Listado de Activos'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {'label': 'Activos', 'url': None}
        ]
        context['create_url'] = reverse('vuln_manager:activo_create')
        context['ordering'] = self.request.GET.get('ordering', '-nombre')
        return context 