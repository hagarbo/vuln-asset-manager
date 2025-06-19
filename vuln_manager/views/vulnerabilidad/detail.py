from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from vuln_manager.models import Vulnerabilidad, ActivoVulnerabilidad
from vuln_manager.mixins import RoleRequiredMixin
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository

class VulnerabilidadDetailView(RoleRequiredMixin, DetailView):
    model = Vulnerabilidad
    template_name = 'vuln_manager/vulnerabilidad/detail.html'
    context_object_name = 'vulnerabilidad'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener activos afectados por la vulnerabilidad
        activos_queryset = ActivoVulnerabilidadRepository().get_by_vulnerabilidad(self.object.id)
        
        # Configurar paginación
        paginator = Paginator(activos_queryset, 10)  # 10 activos por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['activos'] = page_obj.object_list  # Lista de objetos para el template
        context['page_obj'] = page_obj  # Objeto de página para la paginación
        context['is_paginated'] = paginator.num_pages > 1
        context['paginator'] = paginator
        
        context['page_title'] = 'Detalle de Vulnerabilidad'
        context['breadcrumbs'] = [
            {"label": "Dashboard", "url": "/dashboard/"},
            {"label": "Vulnerabilidades", "url": "/vulnerabilidades/"},
            {"label": "Detalle"}
        ]
        return context 