from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad

class VulnerabilidadRepository(BaseRepository):
    """
    Repositorio para la entidad Vulnerabilidad.
    Maneja todas las operaciones de base de datos relacionadas con vulnerabilidades.
    """
    def __init__(self):
        super().__init__(Vulnerabilidad) 