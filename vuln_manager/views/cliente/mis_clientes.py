from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Avg, F, ExpressionWrapper, fields, Subquery, OuterRef
from django.utils import timezone
from datetime import timedelta
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad

class MisClientesView(RoleRequiredMixin, TemplateView):
    template_name = 'vuln_manager/cliente/mis_clientes.html'
    allowed_roles = ['analista']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener clientes asignados al analista
        clientes_asignados = user.clientes_asignados.all()
        
        # Cliente seleccionado (por defecto el primero, o por URL)
        cliente_id = self.request.GET.get('cliente')
        if cliente_id:
            cliente_seleccionado = get_object_or_404(Cliente, id=cliente_id, analistas=user)
        else:
            cliente_seleccionado = clientes_asignados.first() if clientes_asignados.exists() else None
        
        # Sección activa
        seccion = self.request.GET.get('seccion', 'resumen')
        
        context.update({
            'page_title': 'Mis Clientes',
            'clientes_asignados': clientes_asignados,
            'cliente_seleccionado': cliente_seleccionado,
            'seccion_activa': seccion,
        })
        
        # Si hay cliente seleccionado, obtener datos específicos
        if cliente_seleccionado:
            context.update(self._get_datos_cliente(cliente_seleccionado))
        
        return context
    
    def _get_datos_cliente(self, cliente):
        """Obtiene todos los datos específicos del cliente"""
        # Fechas para cálculos
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        inicio_semana = hoy - timedelta(days=7)
        
        # Alertas del cliente
        alertas_cliente = Alerta.objects.filter(activo__cliente=cliente)
        
        # Métricas principales
        metricas = {
            'total_alertas': alertas_cliente.count(),
            'alertas_criticas': alertas_cliente.filter(vulnerabilidad__severidad='critica').count(),
            'alertas_altas': alertas_cliente.filter(vulnerabilidad__severidad='alta').count(),
            'alertas_nuevas': alertas_cliente.filter(estado='nueva').count(),
            'alertas_en_proceso': alertas_cliente.filter(estado='en_proceso').count(),
            'alertas_resueltas_mes': alertas_cliente.filter(
                estado='resuelta',
                fecha_resolucion__date__gte=inicio_mes
            ).count(),
            'alertas_resueltas_semana': alertas_cliente.filter(
                estado='resuelta',
                fecha_resolucion__date__gte=inicio_semana
            ).count(),
        }
        
        # Tiempo promedio de resolución (últimos 30 días)
        alertas_resueltas_recientes = alertas_cliente.filter(
            estado='resuelta',
            fecha_resolucion__date__gte=hoy - timedelta(days=30)
        )
        if alertas_resueltas_recientes.exists():
            # Usar ExpressionWrapper para calcular la diferencia de fechas
            tiempo_promedio = alertas_resueltas_recientes.annotate(
                tiempo_resolucion=ExpressionWrapper(
                    F('fecha_resolucion') - F('fecha_creacion'),
                    output_field=fields.DurationField()
                )
            ).aggregate(
                tiempo_promedio=Avg('tiempo_resolucion')
            )['tiempo_promedio']
            metricas['tiempo_promedio_dias'] = tiempo_promedio.days if tiempo_promedio else 0
        else:
            metricas['tiempo_promedio_dias'] = 0
        
        # Activos del cliente
        activos_cliente = Activo.objects.filter(cliente=cliente)
        
        # Subconsulta para obtener la fecha de la última alerta
        ultima_alerta_subquery = Alerta.objects.filter(
            activo=OuterRef('pk')
        ).order_by('-fecha_creacion').values('fecha_creacion')[:1]
        
        activos_vulnerables = activos_cliente.annotate(
            num_alertas=Count('alerta'),
            ultima_alerta_fecha=Subquery(ultima_alerta_subquery)
        ).filter(num_alertas__gt=0).order_by('-num_alertas')[:5]
        
        # Alertas prioritarias (críticas y altas, ordenadas por fecha)
        alertas_prioritarias = alertas_cliente.filter(
            vulnerabilidad__severidad__in=['critica', 'alta']
        ).select_related('vulnerabilidad', 'activo').order_by('-fecha_creacion')[:10]
        
        # Datos para gráficos (últimos 6 meses)
        datos_grafico = []
        for i in range(6):
            fecha = hoy - timedelta(days=30*i)
            inicio_mes_grafico = fecha.replace(day=1)
            fin_mes_grafico = (inicio_mes_grafico + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            alertas_mes = alertas_cliente.filter(
                fecha_creacion__date__gte=inicio_mes_grafico,
                fecha_creacion__date__lte=fin_mes_grafico
            ).count()
            
            alertas_resueltas_mes = alertas_cliente.filter(
                estado='resuelta',
                fecha_resolucion__date__gte=inicio_mes_grafico,
                fecha_resolucion__date__lte=fin_mes_grafico
            ).count()
            
            datos_grafico.append({
                'mes': fecha.strftime('%b %Y'),
                'alertas_nuevas': alertas_mes,
                'alertas_resueltas': alertas_resueltas_mes,
            })
        
        return {
            'metricas': metricas,
            'activos_vulnerables': activos_vulnerables,
            'alertas_prioritarias': alertas_prioritarias,
            'datos_grafico': list(reversed(datos_grafico)),  # Orden cronológico
            'total_activos': activos_cliente.count(),
            'activos_con_alertas': activos_cliente.filter(alerta__isnull=False).distinct().count(),
        } 