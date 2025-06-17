from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from vuln_manager.repository.tarea.tarea_repository import TareaRepository
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea
from vuln_manager.models.usuario.usuario import Usuario
from django.contrib.auth import get_user_model

class TestTareaRepository(TestCase):
    """Tests para el repositorio de Tareas."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.repository = TareaRepository()
        self.tipo_tarea = TipoTarea.objects.create(
            nombre='Test Tipo',
            codigo='test',
            descripcion='Test Descripción'
        )
        
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

    def test_get_all(self):
        """Test que verifica que get_all devuelve todas las tareas ordenadas."""
        tareas = self.repository.get_all()
        self.assertEqual(tareas.count(), 2)
        self.assertEqual(tareas[0], self.tarea2)  # Más reciente primero

    def test_get_by_estado(self):
        """Test que verifica que get_by_estado filtra correctamente."""
        tareas = self.repository.get_by_estado('programada')
        self.assertEqual(tareas.count(), 1)
        self.assertEqual(tareas[0], self.tarea1)

    def test_get_by_tipo(self):
        """Test que verifica que get_by_tipo filtra correctamente."""
        tareas = self.repository.get_by_tipo(self.tipo_tarea)
        self.assertEqual(tareas.count(), 2)

    def test_get_by_creador(self):
        """Test que verifica que get_by_creador filtra correctamente."""
        tareas = self.repository.get_by_creador(self.usuario)
        self.assertEqual(tareas.count(), 2)

    def test_get_by_fecha_creacion(self):
        """Test que verifica que get_by_fecha_creacion filtra correctamente."""
        fecha_inicio = timezone.now() - timezone.timedelta(days=1)
        fecha_fin = timezone.now() + timezone.timedelta(days=1)
        tareas = self.repository.get_by_fecha_creacion(fecha_inicio, fecha_fin)
        self.assertEqual(tareas.count(), 2)

    def test_get_sin_ejecutar(self):
        """Test que verifica que get_sin_ejecutar filtra correctamente."""
        tareas = self.repository.get_sin_ejecutar(1)
        self.assertEqual(tareas.count(), 1)
        self.assertEqual(tareas[0], self.tarea1)

    def test_update_ultima_ejecucion(self):
        """Test que verifica que update_ultima_ejecucion actualiza correctamente."""
        tarea = self.repository.update_ultima_ejecucion(self.tarea1.id)
        self.assertIsNotNone(tarea.ultima_ejecucion)
        self.assertIsNotNone(tarea.proxima_ejecucion)

    def test_count_programadas(self):
        """Test que verifica que count_programadas cuenta correctamente."""
        count = self.repository.count_programadas()
        self.assertEqual(count, 1)

    def test_get_latest(self):
        """Test que verifica que get_latest devuelve las últimas tareas."""
        tareas = self.repository.get_latest(1)
        self.assertEqual(tareas.count(), 1)
        self.assertEqual(tareas[0], self.tarea2)  # Más reciente primero

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