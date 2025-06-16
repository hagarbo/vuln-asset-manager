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
        return usuario.clientes_asignados.all()

    def get_analistas_asignados(self, usuario):
        if not usuario.es_cliente:
            return self.model.objects.none()
        
        from vuln_manager.repository.cliente.cliente_repository import ClienteRepository
        cliente_repo = ClienteRepository()
        cliente = cliente_repo.get_by_usuario(usuario).first()
        
        if not cliente:
            return self.model.objects.none()
            
        return cliente.analistas.all()

    def get_analistas(self):
        return self.model.objects.filter(rol='analista')

    def get_analistas_by_cliente(self, cliente):
        """
        Obtiene los analistas asignados a un cliente específico.
        
        Args:
            cliente: Instancia del modelo Cliente
            
        Returns:
            QuerySet de Usuario con los analistas asignados al cliente
        """
        return cliente.analistas.all() 