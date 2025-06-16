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

    def get_all(self):
        return self.model.objects.all()

    def get_by_analista(self, analista):
        return self.model.objects.filter(relaciones_analista_cliente__analista=analista)

    def get_by_usuario(self, usuario):
        return self.model.objects.filter(usuario=usuario)

    def get_none(self):
        return self.model.objects.none()

    def create_cliente(self, nombre, usuario):
        return self.model.objects.create(nombre=nombre, usuario=usuario)

    def get_or_create_analista_cliente(self, analista, cliente):
        """
        Obtiene o crea una relación entre un analista y un cliente.
        """
        return AnalistaCliente.objects.get_or_create(analista=analista, cliente=cliente)

    def exists_analista_cliente(self, analista_id, cliente_id):
        """
        Verifica si existe una relación entre un analista y un cliente.
        """
        return AnalistaCliente.objects.filter(analista_id=analista_id, cliente_id=cliente_id).exists()

    def get_analistas_by_cliente(self, cliente):
        """
        Obtiene los IDs de los analistas asignados a un cliente.
        """
        return AnalistaCliente.objects.filter(cliente=cliente).values_list('analista_id', flat=True)

    def asignar_analistas(self, cliente, analistas_ids):
        """
        Asigna analistas a un cliente usando el modelo intermedio AnalistaCliente.
        Valida roles y unicidad.
        """
        from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository
        usuario_repo = UsuarioRepository()
        analistas = usuario_repo.get_analistas().filter(id__in=analistas_ids)
        if len(analistas_ids) > 0 and analistas.count() != len(analistas_ids):
            raise ValidationError('Uno o más analistas no son válidos')
            
        # Limpiar relaciones previas
        AnalistaCliente.objects.filter(cliente=cliente).delete()
        
        # Crear nuevas relaciones usando el modelo intermedio
        for analista in analistas:
            self.get_or_create_analista_cliente(analista, cliente)
            
        return cliente 