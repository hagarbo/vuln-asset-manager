from django.test import TestCase
from vuln_manager.repository.tarea import TareaRepository
from vuln_manager.models.tarea.tarea import Tarea
from django.contrib.auth import get_user_model

class TestTareaRepository(TestCase):
    """
    Tests específicos para el repositorio de Tareas.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = TareaRepository()
        
        # Crear usuario de prueba
        User = get_user_model()
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Datos de prueba para la tarea
        self.tarea_data = {
            'nombre': 'Tarea Test',
            'tipo': 'cve',
            'descripcion': 'Descripción de la tarea de prueba',
            'programacion': '0 0 * * *',
            'estado': 'programada',
            'activa': True,
            'creada_por': self.usuario
        }
        self.tarea = self.repository.create(**self.tarea_data)

    def test_create_tarea(self):
        """Test para crear una tarea con todos sus campos."""
        # Verificar que se creó correctamente
        self.assertIsNotNone(self.tarea.id)
        self.assertEqual(self.tarea.nombre, self.tarea_data['nombre'])
        self.assertEqual(self.tarea.tipo, self.tarea_data['tipo'])
        self.assertEqual(self.tarea.descripcion, self.tarea_data['descripcion'])
        self.assertEqual(self.tarea.programacion, self.tarea_data['programacion'])
        self.assertEqual(self.tarea.estado, self.tarea_data['estado'])
        self.assertEqual(self.tarea.activa, self.tarea_data['activa'])
        self.assertEqual(self.tarea.creada_por, self.usuario)

    def test_get_tarea_by_id(self):
        """Test para obtener una tarea por su ID."""
        # Obtener la tarea por ID
        tarea = self.repository.get_by_id(self.tarea.id)
        
        # Verificar que es la tarea correcta
        self.assertEqual(tarea.nombre, self.tarea_data['nombre'])
        self.assertEqual(tarea.tipo, self.tarea_data['tipo'])

    def test_update_tarea(self):
        """Test para actualizar una tarea."""
        # Datos de actualización
        update_data = {
            'nombre': 'Tarea Test Actualizada',
            'estado': 'ejecutando',
            'descripcion': 'Descripción actualizada'
        }
        
        # Actualizar la tarea
        updated_tarea = self.repository.update(self.tarea.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_tarea.nombre, update_data['nombre'])
        self.assertEqual(updated_tarea.estado, update_data['estado'])
        self.assertEqual(updated_tarea.descripcion, update_data['descripcion'])

    def test_delete_tarea(self):
        """Test para eliminar una tarea."""
        # Eliminar la tarea
        result = self.repository.delete(self.tarea.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(self.tarea.id)) 