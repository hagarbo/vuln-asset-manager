from django.views.generic import ListView
from vuln_manager.models import Vulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin
from django.db.models import F, Case, When, Value, IntegerField
import json
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

class VulnerabilidadListView(RoleRequiredMixin, ListView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad/list.html'
    context_object_name = 'vulnerabilidades'
    paginate_by = 20
    ordering = ['-fecha_modificacion']
    allowed_roles = ['admin', 'analista', 'gestor']

    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get('sort')
        direction = self.request.GET.get('dir', 'desc')

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

        if sort == 'severidad':
            if direction == 'asc':
                queryset = queryset.order_by(F('severidad_rank').asc(nulls_last=True))
            else:
                queryset = queryset.order_by(F('severidad_rank').desc(nulls_last=True))
        elif sort in ['fecha_publicacion', 'fecha_modificacion']:
            if direction == 'asc':
                queryset = queryset.order_by(F(sort).asc(nulls_last=True))
            else:
                queryset = queryset.order_by(F(sort).desc(nulls_last=True))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', '')
        context['current_dir'] = self.request.GET.get('dir', 'desc')
        return context 