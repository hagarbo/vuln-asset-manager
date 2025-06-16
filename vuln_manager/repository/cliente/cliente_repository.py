from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.cliente.cliente import Cliente
from django.core.exceptions import ValidationError

class ClienteRepository(BaseRepository):
    """
    Repositorio para la entidad Cliente.
    Maneja todas las operaciones de base de datos relacionadas con clientes.
    """
    def __init__(self):
        super().__init__(Cliente)

    def get_all(self):
        return self.model.objects.all()

    def get_by_analista(self, analista):
        return self.model.objects.filter(analistas=analista)

    def get_by_usuario(self, usuario):
        return self.model.objects.filter(usuario=usuario)

    def get_none(self):
        return self.model.objects.none()

    def create_cliente(self, nombre, usuario):
        return self.model.objects.create(nombre=nombre, usuario=usuario)

    def get_analistas_by_cliente(self, cliente):
        """
        Obtiene los analistas asignados a un cliente.
        """
        return cliente.analistas.all()

    def asignar_analistas(self, cliente, analistas_ids):
        """
        Asigna analistas a un cliente.
        Valida roles y unicidad.
        """
        from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository
        usuario_repo = UsuarioRepository()
        analistas = usuario_repo.get_analistas().filter(id__in=analistas_ids)
        if len(analistas_ids) > 0 and analistas.count() != len(analistas_ids):
            raise ValidationError('Uno o más analistas no son válidos')
            
        # Asignar analistas usando la relación many-to-many directa
        cliente.analistas.set(analistas)
        return cliente 