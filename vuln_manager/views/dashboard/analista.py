from django.views.generic import TemplateView
from django.db.models import Count, Q, Subquery, OuterRef
from django.utils import timezone
from datetime import timedelta
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad

class AnalistaDashboardView(RoleRequiredMixin, TemplateView):
    template_name = 'vuln_manager/dashboard/analista/index.html'
    allowed_roles = ['analista']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener clientes asignados al analista
        clientes_asignados = user.clientes_asignados.all()
        
        # Alertas nuevas (estado 'nueva')
        alertas_nuevas = Alerta.objects.filter(
            estado='nueva',
            activo__cliente__in=clientes_asignados
        ).select_related('vulnerabilidad', 'activo', 'activo__cliente').order_by('-fecha_creacion')[:5]
        
        # Resumen por cliente (expandible)
        resumen_clientes = []
        for cliente in clientes_asignados:
            alertas_cliente = Alerta.objects.filter(activo__cliente=cliente)
            resumen = {
                'cliente': cliente,
                'total_alertas': alertas_cliente.count(),
                'criticas': alertas_cliente.filter(vulnerabilidad__severidad='critica').count(),
                'altas': alertas_cliente.filter(vulnerabilidad__severidad='alta').count(),
                'medias': alertas_cliente.filter(vulnerabilidad__severidad='media').count(),
                'bajas': alertas_cliente.filter(vulnerabilidad__severidad='baja').count(),
                'nuevas': alertas_cliente.filter(estado='nueva').count(),
                'en_proceso': alertas_cliente.filter(estado='en_proceso').count(),
            }
            resumen_clientes.append(resumen)
        
        # Activos más vulnerables (top 5)
        # Subconsulta para obtener la fecha de la última alerta
        ultima_alerta_subquery = Alerta.objects.filter(
            activo=OuterRef('pk')
        ).order_by('-fecha_creacion').values('fecha_creacion')[:1]
        
        activos_vulnerables = Activo.objects.filter(
            cliente__in=clientes_asignados
        ).annotate(
            num_alertas=Count('alerta'),
            ultima_alerta_fecha=Subquery(ultima_alerta_subquery)
        ).filter(
            num_alertas__gt=0
        ).order_by('-num_alertas')[:5]
        
        # Resumen de trabajo (alertas resueltas hoy y esta semana)
        hoy = timezone.now().date()
        inicio_semana = hoy - timedelta(days=7)
        
        alertas_resueltas_hoy = Alerta.objects.filter(
            estado='resuelta',
            activo__cliente__in=clientes_asignados,
            fecha_resolucion__date=hoy
        ).count()
        
        alertas_resueltas_semana = Alerta.objects.filter(
            estado='resuelta',
            activo__cliente__in=clientes_asignados,
            fecha_resolucion__date__gte=inicio_semana
        ).count()
        
        # Estadísticas generales
        total_alertas_nuevas = Alerta.objects.filter(
            estado='nueva',
            activo__cliente__in=clientes_asignados
        ).count()
        
        total_alertas_en_proceso = Alerta.objects.filter(
            estado='en_proceso',
            activo__cliente__in=clientes_asignados
        ).count()
        
        context.update({
            'page_title': 'Dashboard del Analista',
            'alertas_nuevas': alertas_nuevas,
            'resumen_clientes': resumen_clientes,
            'activos_vulnerables': activos_vulnerables,
            'alertas_resueltas_hoy': alertas_resueltas_hoy,
            'alertas_resueltas_semana': alertas_resueltas_semana,
            'total_alertas_nuevas': total_alertas_nuevas,
            'total_alertas_en_proceso': total_alertas_en_proceso,
            'clientes_asignados': clientes_asignados,
        })
        
        return context 