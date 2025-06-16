from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.auth.usuario import Usuario

class UsuarioRepository(BaseRepository):
    """
    Repositorio para la entidad Usuario.
    Maneja todas las operaciones de base de datos relacionadas con usuarios.
    """
    def __init__(self):
        super().__init__(Usuario) 

    def get_clientes_asignados(self, usuario):
        from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
        return AnalistaCliente.objects.filter(analista=usuario).values_list('cliente', flat=True)

    def get_analistas_asignados(self, usuario):
        if not usuario.es_cliente:
            return self.model.objects.none()
        from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
        from vuln_manager.models.cliente.cliente import Cliente
        cliente = Cliente.objects.filter(usuario=usuario).first()
        if not cliente:
            return self.model.objects.none()
        return self.model.objects.filter(id__in=AnalistaCliente.objects.filter(cliente=cliente).values_list('analista_id', flat=True))

    def get_analistas(self):
        return self.model.objects.filter(rol='analista') 