from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.activo.activo import Activo

class ActivoRepository(BaseRepository):
    """
    Repositorio para la entidad Activo.
    Maneja todas las operaciones de base de datos relacionadas con activos.
    """
    def __init__(self):
        super().__init__(Activo) 