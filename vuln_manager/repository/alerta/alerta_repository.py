from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.alerta.alerta import Alerta

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