from django.test import TestCase
from vuln_manager.repository.cliente import ClienteRepository
from vuln_manager.models.cliente.cliente import Cliente

class TestClienteRepository(TestCase):
    """
    Tests específicos para el repositorio de Clientes.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = ClienteRepository()
        self.cliente_data = {
            'nombre': 'Empresa Test'
        }
        self.cliente = self.repository.create(**self.cliente_data)

    def test_create_cliente(self):
        """Test para crear un cliente con todos sus campos."""
        # Verificar que se creó correctamente
        self.assertIsNotNone(self.cliente.id)
        self.assertEqual(self.cliente.nombre, self.cliente_data['nombre'])

    def test_get_cliente_by_id(self):
        """Test para obtener un cliente por su ID."""
        # Obtener el cliente por ID
        cliente = self.repository.get_by_id(self.cliente.id)
        
        # Verificar que es el cliente correcto
        self.assertEqual(cliente.nombre, self.cliente_data['nombre'])

    def test_update_cliente(self):
        """Test para actualizar un cliente."""
        # Datos de actualización
        update_data = {
            'nombre': 'Empresa Test Actualizada'
        }
        
        # Actualizar el cliente
        updated_cliente = self.repository.update(self.cliente.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_cliente.nombre, update_data['nombre'])

    def test_delete_cliente(self):
        """Test para eliminar un cliente."""
        # Eliminar el cliente
        result = self.repository.delete(self.cliente.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(self.cliente.id)) 