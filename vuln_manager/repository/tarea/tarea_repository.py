from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.tarea.tarea import Tarea

class TareaRepository(BaseRepository):
    """
    Repositorio para la entidad Tarea.
    Maneja todas las operaciones de base de datos relacionadas con tareas.
    """
    def __init__(self):
        super().__init__(Tarea) 