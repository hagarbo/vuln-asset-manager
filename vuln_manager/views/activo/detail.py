from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.db.models import F, Case, When, Value, IntegerField
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class ActivoDetailView(RoleRequiredMixin, DetailView):
    model = Activo
    template_name = 'vuln_manager/activo/detail.html'
    context_object_name = 'activo'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        repository = ActivoRepository()
        if user.es_admin:
            return repository.get_all()
        elif user.es_analista:
            return repository.get_by_analista(user)
        elif user.es_cliente:
            return repository.get_by_cliente(user.cliente)
        return repository.get_none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.es_admin or user.es_analista or user.es_cliente:
            vulnerabilidades_queryset = ActivoVulnerabilidadRepository().get_by_activo(self.object)
        ordering = self.request.GET.get('ordering', '-fecha_deteccion')
        vulnerabilidades_queryset = vulnerabilidades_queryset.annotate(
            severidad_rank=Case(
                When(vulnerabilidad__severidad='critica', then=Value(5)),
                When(vulnerabilidad__severidad='alta', then=Value(4)),
                When(vulnerabilidad__severidad='media', then=Value(3)),
                When(vulnerabilidad__severidad='baja', then=Value(2)),
                When(vulnerabilidad__severidad='no_establecida', then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        )
        if ordering in ['severidad', '-severidad']:
            direction = '' if ordering == 'severidad' else '-'
            vulnerabilidades_queryset = vulnerabilidades_queryset.order_by(f'{direction}severidad_rank')
        else:
            vulnerabilidades_queryset = vulnerabilidades_queryset.order_by(ordering)
        paginator = Paginator(vulnerabilidades_queryset, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['vulnerabilidades'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1
        context['paginator'] = paginator
        context['ordering'] = ordering
        return context 