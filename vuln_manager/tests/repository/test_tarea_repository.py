from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from vuln_manager.repository.tarea import TareaRepository
from vuln_manager.models.tarea import Tarea
from django.contrib.auth import get_user_model

class TestTareaRepository(TestCase):
    """Tests para el repositorio de Tareas."""

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
        
        # Crear tareas de prueba
        self.tarea1 = Tarea.objects.create(
            nombre='Tarea 1',
            tipo='cve',
            descripcion='Descripción de la tarea 1',
            programacion='0 0 * * *',
            estado='programada',
            activa=True,
            dias_atras=1,
            incluir_rechazadas=False,
            creada_por=self.usuario
        )
        
        self.tarea2 = Tarea.objects.create(
            nombre='Tarea 2',
            tipo='cve',
            descripcion='Descripción de la tarea 2',
            programacion='0 12 * * *',
            estado='ejecutando',
            activa=True,
            dias_atras=2,
            incluir_rechazadas=True,
            creada_por=self.usuario
        )
        
        self.tarea3 = Tarea.objects.create(
            nombre='Tarea 3',
            tipo='cve',
            descripcion='Descripción de la tarea 3',
            programacion='0 0 * * 1',
            estado='completada',
            activa=False,
            dias_atras=1,
            incluir_rechazadas=False,
            creada_por=self.usuario
        )

    def test_get_tareas_activas(self):
        """Test para obtener tareas activas."""
        tareas = self.repository.get_tareas_activas()
        self.assertEqual(tareas.count(), 2)
        self.assertIn(self.tarea1, tareas)
        self.assertIn(self.tarea2, tareas)
        self.assertNotIn(self.tarea3, tareas)

    def test_get_tareas_pendientes(self):
        """Test para obtener tareas pendientes."""
        tareas = self.repository.get_tareas_pendientes()
        self.assertEqual(tareas.count(), 1)
        self.assertIn(self.tarea1, tareas)
        self.assertNotIn(self.tarea2, tareas)
        self.assertNotIn(self.tarea3, tareas)

    def test_get_tareas_por_tipo(self):
        """Test para obtener tareas por tipo."""
        tareas = self.repository.get_tareas_por_tipo('cve')
        self.assertEqual(tareas.count(), 3)
        self.assertIn(self.tarea1, tareas)
        self.assertIn(self.tarea2, tareas)
        self.assertIn(self.tarea3, tareas)

    def test_get_tareas_por_estado(self):
        """Test para obtener tareas por estado."""
        tareas = self.repository.get_tareas_por_estado('programada')
        self.assertEqual(tareas.count(), 1)
        self.assertIn(self.tarea1, tareas)
        self.assertNotIn(self.tarea2, tareas)
        self.assertNotIn(self.tarea3, tareas)

    def test_get_tareas_por_creador(self):
        """Test para obtener tareas por creador."""
        tareas = self.repository.get_tareas_por_creador(self.usuario)
        self.assertEqual(tareas.count(), 3)
        self.assertIn(self.tarea1, tareas)
        self.assertIn(self.tarea2, tareas)
        self.assertIn(self.tarea3, tareas)

    def test_get_tareas_por_ultima_ejecucion(self):
        """Test para obtener tareas por última ejecución."""
        # Establecer última ejecución para tarea1
        self.tarea1.ultima_ejecucion = timezone.now() - timedelta(days=2)
        self.tarea1.save()
        
        tareas = self.repository.get_tareas_por_ultima_ejecucion(1)
        self.assertEqual(tareas.count(), 1)
        self.assertIn(self.tarea1, tareas)
        self.assertNotIn(self.tarea2, tareas)
        self.assertNotIn(self.tarea3, tareas)

    def test_actualizar_estado(self):
        """Test para actualizar el estado de una tarea."""
        tarea = self.repository.actualizar_estado(self.tarea1.id, 'ejecutando')
        self.assertEqual(tarea.estado, 'ejecutando')
        
        # Verificar en la base de datos
        tarea.refresh_from_db()
        self.assertEqual(tarea.estado, 'ejecutando')

    def test_actualizar_ultima_ejecucion(self):
        """Test para actualizar la última ejecución de una tarea."""
        tarea = self.repository.actualizar_ultima_ejecucion(self.tarea1.id)
        self.assertIsNotNone(tarea.ultima_ejecucion)
        
        # Verificar en la base de datos
        tarea.refresh_from_db()
        self.assertIsNotNone(tarea.ultima_ejecucion) 