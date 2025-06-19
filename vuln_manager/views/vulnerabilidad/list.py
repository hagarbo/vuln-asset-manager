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
        ordering = self.request.GET.get('ordering', '-fecha_modificacion')
        repository = VulnerabilidadRepository()
        # Filtros
        severidad = self.request.GET.get('severidad', '')
        cve_id = self.request.GET.get('cve_id', '')
        descripcion_en = self.request.GET.get('descripcion_en', '')
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        fecha_fin = self.request.GET.get('fecha_fin', '')
        queryset = repository.get_filtered(
            severidad=severidad if severidad else None,
            cve_id=cve_id if cve_id else None,
            descripcion_en=descripcion_en if descripcion_en else None,
            fecha_inicio=fecha_inicio if fecha_inicio else None,
            fecha_fin=fecha_fin if fecha_fin else None
        )
        # Anotación para ranking de severidad
        queryset = queryset.annotate(
            severidad_rank=Case(
                When(severidad='critica', then=Value(5)),
                When(severidad='alta', then=Value(4)),
                When(severidad='media', then=Value(3)),
                When(severidad='baja', then=Value(2)),
                When(severidad='no establecida', then=Value(1)),
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
        # Opciones de severidad para el filtro
        context['severidades'] = self.model.SEVERIDAD_CHOICES
        context['severidad_filter'] = self.request.GET.get('severidad', '')
        context['cve_id_filter'] = self.request.GET.get('cve_id', '')
        context['descripcion_en_filter'] = self.request.GET.get('descripcion_en', '')
        context['fecha_inicio_filter'] = self.request.GET.get('fecha_inicio', '')
        context['fecha_fin_filter'] = self.request.GET.get('fecha_fin', '')
        context['ordering'] = self.request.GET.get('ordering', '-fecha_modificacion')
        return context 