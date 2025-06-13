from django.test import TestCase
from vuln_manager.repository.usuario import UsuarioRepository
from django.contrib.auth import get_user_model

class TestUsuarioRepository(TestCase):
    """
    Tests específicos para el repositorio de Usuarios.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = UsuarioRepository()
        
        # Datos de prueba para el usuario
        self.usuario_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
            'rol': 'cliente'
        }
        self.usuario = self.repository.create(**self.usuario_data)

    def test_create_usuario(self):
        """Test para crear un usuario con todos sus campos."""
        # Verificar que se creó correctamente
        self.assertIsNotNone(self.usuario.id)
        self.assertEqual(self.usuario.username, self.usuario_data['username'])
        self.assertEqual(self.usuario.email, self.usuario_data['email'])
        self.assertEqual(self.usuario.first_name, self.usuario_data['first_name'])
        self.assertEqual(self.usuario.last_name, self.usuario_data['last_name'])
        self.assertEqual(self.usuario.is_active, self.usuario_data['is_active'])
        self.assertEqual(self.usuario.rol, self.usuario_data['rol'])

    def test_get_usuario_by_id(self):
        """Test para obtener un usuario por su ID."""
        # Obtener el usuario por ID
        usuario = self.repository.get_by_id(self.usuario.id)
        
        # Verificar que es el usuario correcto
        self.assertEqual(usuario.username, self.usuario_data['username'])
        self.assertEqual(usuario.email, self.usuario_data['email'])

    def test_update_usuario(self):
        """Test para actualizar un usuario."""
        # Datos de actualización
        update_data = {
            'first_name': 'Test Updated',
            'last_name': 'User Updated',
            'email': 'updated@example.com'
        }
        
        # Actualizar el usuario
        updated_usuario = self.repository.update(self.usuario.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_usuario.first_name, update_data['first_name'])
        self.assertEqual(updated_usuario.last_name, update_data['last_name'])
        self.assertEqual(updated_usuario.email, update_data['email'])

    def test_delete_usuario(self):
        """Test para eliminar un usuario."""
        # Eliminar el usuario
        result = self.repository.delete(self.usuario.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(self.usuario.id)) 