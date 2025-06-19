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

    def get_filtered(self, nombre=None, tipo=None, cliente=None):
        """
        Devuelve un queryset filtrado por nombre (parcial, insensible a mayúsculas), tipo y cliente.
        """
        qs = self.model.objects.all()
        if nombre:
            qs = qs.filter(nombre__icontains=nombre)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if cliente:
            qs = qs.filter(cliente=cliente)
        return qs 