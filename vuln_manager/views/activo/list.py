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
        allowed_orderings = ['nombre', '-nombre', 'cliente__nombre', '-cliente__nombre', 'tipo', '-tipo']
        if ordering not in allowed_orderings:
            ordering = '-nombre'
        user = self.request.user
        repository = ActivoRepository()
        # Filtros
        nombre = self.request.GET.get('nombre', '')
        tipo = self.request.GET.get('tipo', '')
        cliente_id = self.request.GET.get('cliente', '')
        cliente = None
        if cliente_id:
            from vuln_manager.models.cliente.cliente import Cliente
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist:
                cliente = None
        # Filtrado según rol
        if user.es_admin or user.es_analista:
            queryset = repository.get_filtered(
                nombre=nombre if nombre else None,
                tipo=tipo if tipo else None,
                cliente=cliente if cliente else None
            )
        elif user.es_cliente:
            queryset = repository.get_filtered(
                nombre=nombre if nombre else None,
                tipo=tipo if tipo else None,
                cliente=user.cliente
            )
        else:
            queryset = repository.get_none()
        return queryset.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Opciones de tipo para el filtro
        context['tipos'] = self.model.TIPO_CHOICES
        # Opciones de cliente solo para admin y analista
        user = self.request.user
        if user.es_admin or user.es_analista:
            from vuln_manager.models.cliente.cliente import Cliente
            context['clientes'] = Cliente.objects.all().order_by('nombre')
        context['nombre_filter'] = self.request.GET.get('nombre', '')
        context['tipo_filter'] = self.request.GET.get('tipo', '')
        context['cliente_filter'] = self.request.GET.get('cliente', '')
        context['create_url'] = reverse('vuln_manager:activo_create')
        context['ordering'] = self.request.GET.get('ordering', '-nombre')
        return context 