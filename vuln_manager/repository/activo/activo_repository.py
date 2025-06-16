from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.activo.activo import Activo

class ActivoRepository(BaseRepository):
    """
    Repositorio para la entidad Activo.
    Maneja todas las operaciones de base de datos relacionadas con activos.
    """
    def __init__(self):
        super().__init__(Activo)

    def get_by_cliente(self, cliente):
        """
        Obtiene todos los activos de un cliente específico.
        """
        return self.model.objects.filter(cliente=cliente)

    def get_by_analista(self, analista):
        """
        Obtiene los activos asignados a un analista a través de sus clientes.
        """
        return self.model.objects.filter(cliente__analistas=analista) 