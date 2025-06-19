from django.views.generic import DetailView
from django.utils import timezone
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.alerta.alerta_repository import AlertaRepository

class AlertaDetailView(RoleRequiredMixin, DetailView):
    model = Alerta
    template_name = 'vuln_manager/alerta/detail.html'
    context_object_name = 'alerta'
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        user = self.request.user
        repository = AlertaRepository()
        if user.es_admin:
            return repository.get_all().select_related('vulnerabilidad', 'activo', 'activo__cliente', 'analista_asignado', 'resuelta_por')
        elif user.es_analista:
            return repository.get_by_analista(user)
        elif hasattr(user, 'cliente') and user.es_cliente:
            return repository.get_by_cliente(user.cliente)
        return repository.get_none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener alertas relacionadas del mismo activo
        alertas_relacionadas = Alerta.objects.filter(
            activo=self.object.activo
        ).exclude(
            id=self.object.id
        ).select_related('vulnerabilidad').order_by('-fecha_creacion')[:5]
        
        # Obtener alertas relacionadas de la misma vulnerabilidad
        alertas_misma_vulnerabilidad = Alerta.objects.filter(
            vulnerabilidad=self.object.vulnerabilidad
        ).exclude(
            id=self.object.id
        ).select_related('activo', 'activo__cliente').order_by('-fecha_creacion')[:5]
        
        context.update({
            'page_title': 'Detalle de Alerta',
            'breadcrumbs': [
                {'label': 'Dashboard', 'url': '/dashboard/'},
                {'label': 'Alertas', 'url': '/alertas/'},
                {'label': f'Alerta {self.object.vulnerabilidad.cve_id}', 'url': None}
            ],
            'alertas_relacionadas': alertas_relacionadas,
            'alertas_misma_vulnerabilidad': alertas_misma_vulnerabilidad,
            'estado_choices': dict(Alerta.ESTADO_CHOICES),
            'puede_editar': self.request.user.es_admin or (
                self.request.user.es_analista and 
                self.object.activo.cliente in self.request.user.clientes_asignados.all()
            ),
        })
        
        return context 