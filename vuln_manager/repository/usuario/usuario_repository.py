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
        
        from vuln_manager.repository.cliente.cliente_repository import ClienteRepository
        cliente_repo = ClienteRepository()
        cliente = cliente_repo.get_by_usuario(usuario).first()
        
        if not cliente:
            return self.model.objects.none()
            
        from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
        return self.model.objects.filter(
            id__in=AnalistaCliente.objects.filter(cliente=cliente)
            .values_list('analista_id', flat=True)
        )

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
        print(f"Buscando analistas para cliente: {cliente.nombre}")
        # Usamos la relación many-to-many directa
        analistas = cliente.analistas.all()
        print(f"Analistas encontrados: {analistas.count()}")
        return analistas 