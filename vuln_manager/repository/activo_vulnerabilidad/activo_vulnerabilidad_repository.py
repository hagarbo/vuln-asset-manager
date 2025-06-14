from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad
from django.db.models import Q

class ActivoVulnerabilidadRepository(BaseRepository):
    """
    Repositorio para la entidad ActivoVulnerabilidad.
    Maneja todas las operaciones de base de datos relacionadas con las relaciones entre activos y vulnerabilidades.
    """
    def __init__(self):
        super().__init__(ActivoVulnerabilidad)

    def get_by_activos_analista(self, analista_id):
        """
        Obtiene todas las relaciones de los activos asignados a un analista.
        """
        return self.model.objects.filter(
            activo__cliente__analistas__id=analista_id
        ).select_related('activo', 'vulnerabilidad')

    def get_by_activos_cliente(self, cliente_id):
        """
        Obtiene todas las relaciones de los activos de un cliente.
        """
        return self.model.objects.filter(
            activo__cliente_id=cliente_id
        ).select_related('activo', 'vulnerabilidad')

    def get_by_activo(self, activo_id):
        """
        Obtiene todas las vulnerabilidades asociadas a un activo.
        """
        return self.model.objects.filter(activo_id=activo_id).select_related('vulnerabilidad')

    def get_by_vulnerabilidad(self, vulnerabilidad_id):
        """
        Obtiene todos los activos afectados por una vulnerabilidad.
        """
        return self.model.objects.filter(vulnerabilidad_id=vulnerabilidad_id).select_related('activo')

    def get_by_estado(self, estado):
        """
        Obtiene todas las relaciones con un estado específico.
        """
        return self.model.objects.filter(estado=estado).select_related('activo', 'vulnerabilidad')

    def get_pendientes(self):
        """
        Obtiene todas las relaciones con estado PENDIENTE.
        """
        return self.get_by_estado('PENDIENTE')

    def get_en_progreso(self):
        """
        Obtiene todas las relaciones con estado EN_PROGRESO.
        """
        return self.get_by_estado('EN_PROGRESO')

    def get_resueltas(self):
        """
        Obtiene todas las relaciones con estado RESUELTO.
        """
        return self.get_by_estado('RESUELTO')

    def get_falsos_positivos(self):
        """
        Obtiene todas las relaciones marcadas como FALSO_POSITIVO.
        """
        return self.get_by_estado('FALSO_POSITIVO')

    def get_by_activo_y_vulnerabilidad(self, activo_id, vulnerabilidad_id):
        """
        Obtiene una relación específica entre un activo y una vulnerabilidad.
        """
        try:
            return self.model.objects.get(activo_id=activo_id, vulnerabilidad_id=vulnerabilidad_id)
        except self.model.DoesNotExist:
            return None

    def get_by_fecha_deteccion(self, fecha_inicio, fecha_fin=None):
        """
        Obtiene las relaciones detectadas en un rango de fechas.
        """
        query = Q(fecha_deteccion__gte=fecha_inicio)
        if fecha_fin:
            query &= Q(fecha_deteccion__lte=fecha_fin)
        return self.model.objects.filter(query).select_related('activo', 'vulnerabilidad') 