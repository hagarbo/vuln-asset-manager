from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.alerta.alerta import Alerta
from django.db.models import Q

class AlertaRepository(BaseRepository):
    """
    Repositorio para la entidad Alerta.
    Maneja todas las operaciones de base de datos relacionadas con alertas.
    """
    def __init__(self):
        super().__init__(Alerta)

    def get_by_activo_y_vulnerabilidad(self, activo_id, vulnerabilidad_id):
        """
        Obtiene una alerta específica entre un activo y una vulnerabilidad.
        """
        try:
            return self.model.objects.get(activo_id=activo_id, vulnerabilidad_id=vulnerabilidad_id)
        except self.model.DoesNotExist:
            return None

    def get_by_analista(self, analista):
        """
        Obtiene alertas de los clientes asignados al analista.
        """
        return self.model.objects.filter(
            activo__cliente__analistas=analista
        ).select_related('vulnerabilidad', 'activo', 'activo__cliente', 'analista_asignado')

    def get_by_cliente(self, cliente):
        """
        Obtiene alertas de un cliente específico.
        """
        return self.model.objects.filter(
            activo__cliente=cliente
        ).select_related('vulnerabilidad', 'activo', 'activo__cliente', 'analista_asignado')

    def get_filtered(self, user, cliente_filter=None, severidad_filter=None, estado_filter=None):
        """
        Obtiene alertas filtradas según el usuario y los filtros aplicados.
        """
        queryset = self.get_by_user(user)
        
        if cliente_filter:
            queryset = queryset.filter(activo__cliente__nombre__icontains=cliente_filter)
        
        if severidad_filter:
            queryset = queryset.filter(vulnerabilidad__severidad=severidad_filter)
        
        if estado_filter:
            queryset = queryset.filter(estado=estado_filter)
        
        return queryset

    def get_by_user(self, user):
        """
        Obtiene alertas según el rol del usuario.
        """
        if user.es_admin:
            return self.get_all().select_related('vulnerabilidad', 'activo', 'activo__cliente', 'analista_asignado')
        elif user.es_analista:
            return self.get_by_analista(user)
        else:
            return self.get_none()

    @staticmethod
    def get_none():
        from vuln_manager.models.alerta.alerta import Alerta
        return Alerta.objects.none() 