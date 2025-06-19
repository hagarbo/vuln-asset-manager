from django.views.generic import ListView
from django.urls import reverse
from django.core.paginator import Paginator
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.mixins.permissions import RoleRequiredMixin
from vuln_manager.repository.alerta.alerta_repository import AlertaRepository

class AlertaListView(RoleRequiredMixin, ListView):
    model = Alerta
    template_name = 'vuln_manager/alerta/list.html'
    context_object_name = 'alertas'
    paginate_by = 10
    allowed_roles = ['admin', 'analista', 'cliente']

    def get_queryset(self):
        ordering = self.request.GET.get('ordering', '-fecha_creacion')
        # Permitimos ordenar por fecha, estado, severidad, cliente y activo
        allowed_orderings = [
            'fecha_creacion', '-fecha_creacion', 
            'estado', '-estado',
            'vulnerabilidad__severidad', '-vulnerabilidad__severidad',
            'activo__cliente__nombre', '-activo__cliente__nombre',
            'activo__nombre', '-activo__nombre'
        ]
        if ordering not in allowed_orderings:
            ordering = '-fecha_creacion'
        
        user = self.request.user
        repository = AlertaRepository()
        
        # Obtener filtros
        cliente_filter = self.request.GET.get('cliente', '')
        severidad_filter = self.request.GET.get('severidad', '')
        estado_filter = self.request.GET.get('estado', '')
        
        # Aplicar filtros
        queryset = repository.get_filtered(
            user, 
            cliente_filter=cliente_filter if cliente_filter else None,
            severidad_filter=severidad_filter if severidad_filter else None,
            estado_filter=estado_filter if estado_filter else None
        )
        
        return queryset.order_by(ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener opciones de filtros para el template
        repository = AlertaRepository()
        all_alertas = repository.get_by_user(user)
        
        # Clientes disponibles para filtro
        if user.es_analista:
            # Para analistas, usar sus clientes asignados
            clientes = user.clientes_asignados.all().order_by('nombre')
        else:
            # Para admin, obtener clientes únicos de las alertas
            cliente_ids = set(all_alertas.values_list('activo__cliente__id', flat=True))
            clientes = Cliente.objects.filter(id__in=cliente_ids).order_by('nombre')
        
        # Estados disponibles - usar choices del modelo
        estados_disponibles = set(all_alertas.values_list('estado', flat=True))
        estados = [(estado, dict(Alerta.ESTADO_CHOICES).get(estado, estado)) 
                  for estado in estados_disponibles if estado]
        
        # Severidades disponibles - usar choices del modelo Vulnerabilidad
        from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
        severidades_disponibles = set(all_alertas.values_list('vulnerabilidad__severidad', flat=True))
        severidades = [(sev, dict(Vulnerabilidad.SEVERIDAD_CHOICES).get(sev, sev)) 
                      for sev in severidades_disponibles if sev]
        
        context.update({
            'ordering': self.request.GET.get('ordering', '-fecha_creacion'),
            'cliente_filter': self.request.GET.get('cliente', ''),
            'severidad_filter': self.request.GET.get('severidad', ''),
            'estado_filter': self.request.GET.get('estado', ''),
            'clientes': clientes,
            'estados': estados,
            'severidades': severidades,
            'total_alertas': all_alertas.count(),
            'alertas_nuevas': all_alertas.filter(estado='nueva').count(),
            'alertas_en_proceso': all_alertas.filter(estado='en_proceso').count(),
            'alertas_resueltas': all_alertas.filter(estado='resuelta').count(),
        })
        
        return context 