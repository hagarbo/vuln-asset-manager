from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.cliente.cliente import Cliente

class ClienteRepository(BaseRepository):
    """
    Repositorio para la entidad Cliente.
    Maneja todas las operaciones de base de datos relacionadas con clientes.
    """
    def __init__(self):
        super().__init__(Cliente) 