from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.alerta.alerta import Alerta

class AlertaRepository(BaseRepository):
    """
    Repositorio para la entidad Alerta.
    Maneja todas las operaciones de base de datos relacionadas con alertas.
    """
    def __init__(self):
        super().__init__(Alerta) 