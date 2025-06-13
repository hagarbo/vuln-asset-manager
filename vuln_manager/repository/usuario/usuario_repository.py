from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.auth.usuario import Usuario

class UsuarioRepository(BaseRepository):
    """
    Repositorio para la entidad Usuario.
    Maneja todas las operaciones de base de datos relacionadas con usuarios.
    """
    def __init__(self):
        super().__init__(Usuario) 