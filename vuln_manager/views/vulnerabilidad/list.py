from django.views.generic import ListView
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin
from django.db.models import F, Case, When, Value, IntegerField
import json
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository
from django.urls import reverse
from django.core.paginator import Paginator

class VulnerabilidadListView(RoleRequiredMixin, ListView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad/list.html'
    context_object_name = 'vulnerabilidades'
    paginate_by = 20
    ordering = ['-fecha_modificacion']
    allowed_roles = ['admin', 'analista', 'gestor']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering', '-fecha_modificacion')

        # Anotación para ranking de severidad
        queryset = queryset.annotate(
            severidad_rank=Case(
                When(severidad='critica', then=Value(5)),
                When(severidad='alta', then=Value(4)),
                When(severidad='media', then=Value(3)),
                When(severidad='baja', then=Value(2)),
                When(severidad='no_establecida', then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        )

        # Mapeo especial para severidad
        if ordering in ['severidad', '-severidad']:
            direction = '' if ordering == 'severidad' else '-'
            queryset = queryset.order_by(f'{direction}severidad_rank')
        else:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Listado de Vulnerabilidades'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {'label': 'Vulnerabilidades', 'url': None}
        ]
        context['ordering'] = self.request.GET.get('ordering', '-fecha_modificacion')
        return context 