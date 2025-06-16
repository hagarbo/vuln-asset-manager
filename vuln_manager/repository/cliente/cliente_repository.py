from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
from vuln_manager.models.auth.usuario import Usuario
from django.core.exceptions import ValidationError

class ClienteRepository(BaseRepository):
    """
    Repositorio para la entidad Cliente.
    Maneja todas las operaciones de base de datos relacionadas con clientes.
    """
    def __init__(self):
        super().__init__(Cliente)

    def create_cliente(self, nombre, usuario):
        return self.model.objects.create(nombre=nombre, usuario=usuario)

    def asignar_analistas(self, cliente, analistas_ids):
        """
        Asigna analistas a un cliente usando el modelo intermedio AnalistaCliente.
        Valida roles y unicidad.
        """
        analistas = Usuario.objects.filter(id__in=analistas_ids, rol='analista')
        if len(analistas_ids) > 0 and analistas.count() != len(analistas_ids):
            raise ValidationError('Uno o más analistas no son válidos')
        # Limpiar relaciones previas
        cliente.analistas.clear()
        for analista in analistas:
            AnalistaCliente.objects.get_or_create(analista=analista, cliente=cliente)
        cliente.analistas.set(analistas)
        return cliente

    @staticmethod
    def exists_cliente_for_analista(analista_id, cliente_id):
        from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
        return AnalistaCliente.objects.filter(analista_id=analista_id, cliente_id=cliente_id).exists()

    @staticmethod
    def get_all():
        return Cliente.objects.all()

    @staticmethod
    def get_by_analista(analista):
        return Cliente.objects.filter(relaciones_analista_cliente__analista=analista)

    @staticmethod
    def get_by_usuario(usuario):
        return Cliente.objects.filter(usuario=usuario)

    @staticmethod
    def get_none():
        return Cliente.objects.none() 