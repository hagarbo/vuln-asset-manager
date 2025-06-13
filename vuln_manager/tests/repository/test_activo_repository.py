from django.test import TestCase
from vuln_manager.repository.activo import ActivoRepository
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.cliente.cliente import Cliente

class TestActivoRepository(TestCase):
    """
    Tests específicos para el repositorio de Activos.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = ActivoRepository()
        # Crear un cliente para las pruebas
        self.cliente = Cliente.objects.create(
            nombre="Cliente Test"
        )
        self.activo_data = {
            'nombre': 'Servidor Web',
            'tipo': 'hardware',  # Valor válido según TIPO_CHOICES
            'descripcion': 'Servidor web de producción',
            'palabras_clave': 'apache,nginx,web,server',  # Campo requerido
            'ip': '192.168.1.1',
            'puerto': 80,
            'version': '2.4.41',
            'cliente': self.cliente
        }
        self.activo = self.repository.create(**self.activo_data)

    def test_create_activo(self):
        """Test para crear un activo con todos sus campos."""
        # Verificar que se creó correctamente
        self.assertIsNotNone(self.activo.id)
        self.assertEqual(self.activo.nombre, self.activo_data['nombre'])
        self.assertEqual(self.activo.tipo, self.activo_data['tipo'])
        self.assertEqual(self.activo.descripcion, self.activo_data['descripcion'])
        self.assertEqual(self.activo.palabras_clave, self.activo_data['palabras_clave'])
        self.assertEqual(self.activo.ip, self.activo_data['ip'])
        self.assertEqual(self.activo.puerto, self.activo_data['puerto'])
        self.assertEqual(self.activo.version, self.activo_data['version'])
        self.assertEqual(self.activo.cliente, self.cliente)

    def test_get_activo_by_id(self):
        """Test para obtener un activo por su ID."""
        # Obtener el activo por ID
        activo = self.repository.get_by_id(self.activo.id)
        
        # Verificar que es el activo correcto
        self.assertEqual(activo.nombre, self.activo_data['nombre'])
        self.assertEqual(activo.tipo, self.activo_data['tipo'])
        self.assertEqual(activo.palabras_clave, self.activo_data['palabras_clave'])

    def test_update_activo(self):
        """Test para actualizar un activo."""
        # Datos de actualización
        update_data = {
            'nombre': 'Servidor Web Actualizado',
            'descripcion': 'Nueva descripción',
            'palabras_clave': 'apache,nginx,web,server,updated',
            'version': '2.4.42'
        }
        
        # Actualizar el activo
        updated_activo = self.repository.update(self.activo.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_activo.nombre, update_data['nombre'])
        self.assertEqual(updated_activo.descripcion, update_data['descripcion'])
        self.assertEqual(updated_activo.palabras_clave, update_data['palabras_clave'])
        self.assertEqual(updated_activo.version, update_data['version'])

    def test_delete_activo(self):
        """Test para eliminar un activo."""
        # Eliminar el activo
        result = self.repository.delete(self.activo.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(self.activo.id)) 