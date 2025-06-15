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
            tipo=self.tipo_tarea,
            programacion='0 0 * * *',
            parametros={'dias_atras': 1},
            estado='programada',
            creada_por=self.usuario
        )
        
        self.tarea2 = Tarea.objects.create(
            tipo=self.tipo_tarea,
            programacion='0 0 * * *',
            parametros={'dias_atras': 2},
            estado='programada',
            creada_por=self.usuario
        )
        
        self.tarea3 = Tarea.objects.create(
            tipo=self.tipo_tarea,
            programacion='0 0 * * *',
            parametros={'dias_atras': 3},
            estado='pausada',
            creada_por=self.usuario
        )

    def test_get_tareas_activas(self):
        """Test para obtener tareas activas."""
        tareas = self.repository.get_tareas_activas()
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
        tarea = self.repository.actualizar_estado(self.tarea1.id, 'pausada')
        self.assertEqual(tarea.estado, 'pausada')
        
        # Verificar en la base de datos
        tarea.refresh_from_db()
        self.assertEqual(tarea.estado, 'pausada')

    def test_actualizar_ultima_ejecucion(self):
        """Test para actualizar la última ejecución de una tarea."""
        tarea = self.repository.actualizar_ultima_ejecucion(self.tarea1.id)
        self.assertIsNotNone(tarea.ultima_ejecucion)
        
        # Verificar en la base de datos
        tarea.refresh_from_db()
        self.assertIsNotNone(tarea.ultima_ejecucion) 