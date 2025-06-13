from django.test import TestCase
from vuln_manager.repository.alerta import AlertaRepository
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.cliente.cliente import Cliente
from django.contrib.auth import get_user_model

class TestAlertaRepository(TestCase):
    """
    Tests específicos para el repositorio de Alertas.
    """
    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = AlertaRepository()
        
        # Crear usuario de prueba
        User = get_user_model()
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Crear vulnerabilidad de prueba
        self.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability EN',
            descripcion_es='Test vulnerabilidad ES',
            severidad='alta',
            status='published',
            fecha_publicacion='2024-01-01',
            fecha_modificacion='2024-01-01'
        )
        
        # Crear activo de prueba
        self.activo = Activo.objects.create(
            nombre='Activo Test',
            tipo='hardware',
            palabras_clave='test,activo',
            cliente=Cliente.objects.create(nombre='Cliente Test')
        )
        
        # Datos de prueba para la alerta
        self.alerta_data = {
            'vulnerabilidad': self.vulnerabilidad,
            'activo': self.activo,
            'analista_asignado': self.usuario,
            'estado': 'nueva',
            'notas': 'Notas de prueba'
        }
        self.alerta = self.repository.create(**self.alerta_data)

    def test_create_alerta(self):
        """Test para crear una alerta con todos sus campos."""
        # Verificar que se creó correctamente
        self.assertIsNotNone(self.alerta.id)
        self.assertEqual(self.alerta.vulnerabilidad, self.vulnerabilidad)
        self.assertEqual(self.alerta.activo, self.activo)
        self.assertEqual(self.alerta.analista_asignado, self.usuario)
        self.assertEqual(self.alerta.estado, self.alerta_data['estado'])
        self.assertEqual(self.alerta.notas, self.alerta_data['notas'])

    def test_get_alerta_by_id(self):
        """Test para obtener una alerta por su ID."""
        # Obtener la alerta por ID
        alerta = self.repository.get_by_id(self.alerta.id)
        
        # Verificar que es la alerta correcta
        self.assertEqual(alerta.vulnerabilidad, self.vulnerabilidad)
        self.assertEqual(alerta.activo, self.activo)

    def test_update_alerta(self):
        """Test para actualizar una alerta."""
        # Datos de actualización
        update_data = {
            'estado': 'en_proceso',
            'notas': 'Notas actualizadas'
        }
        
        # Actualizar la alerta
        updated_alerta = self.repository.update(self.alerta.id, **update_data)
        
        # Verificar que se actualizó correctamente
        self.assertEqual(updated_alerta.estado, update_data['estado'])
        self.assertEqual(updated_alerta.notas, update_data['notas'])

    def test_delete_alerta(self):
        """Test para eliminar una alerta."""
        # Eliminar la alerta
        result = self.repository.delete(self.alerta.id)
        
        # Verificar que se eliminó correctamente
        self.assertTrue(result)
        self.assertIsNone(self.repository.get_by_id(self.alerta.id)) 