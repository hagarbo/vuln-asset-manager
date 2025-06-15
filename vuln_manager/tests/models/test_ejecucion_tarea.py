from django.test import TestCase
from django.utils import timezone
from vuln_manager.models.tarea import Tarea, EjecucionTarea
from django.contrib.auth import get_user_model

class TestEjecucionTarea(TestCase):
    """Tests para el modelo EjecucionTarea."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear usuario de prueba
        User = get_user_model()
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Crear tarea de prueba
        self.tarea = Tarea.objects.create(
            nombre='Tarea Test',
            tipo='cve',
            descripcion='Descripción de la tarea de prueba',
            programacion='0 0 * * *',
            estado='programada',
            dias_atras=1,
            creada_por=self.usuario
        )

        # Datos de prueba para la ejecución
        self.ejecucion_data = {
            'tarea': self.tarea,
            'estado': 'exitoso',
            'resultado': 'Ejecución completada con éxito',
            'error': '',
            'cves_procesadas': 10,
            'cves_nuevas': 5,
            'cves_actualizadas': 3,
            'ejecutada_por': self.usuario
        }

    def test_crear_ejecucion(self):
        """Test para crear una ejecución con todos sus campos."""
        ejecucion = EjecucionTarea.objects.create(**self.ejecucion_data)
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(ejecucion.id)
        self.assertEqual(ejecucion.tarea, self.tarea)
        self.assertEqual(ejecucion.estado, self.ejecucion_data['estado'])
        self.assertEqual(ejecucion.resultado, self.ejecucion_data['resultado'])
        self.assertEqual(ejecucion.error, self.ejecucion_data['error'])
        self.assertEqual(ejecucion.cves_procesadas, self.ejecucion_data['cves_procesadas'])
        self.assertEqual(ejecucion.cves_nuevas, self.ejecucion_data['cves_nuevas'])
        self.assertEqual(ejecucion.cves_actualizadas, self.ejecucion_data['cves_actualizadas'])
        self.assertEqual(ejecucion.ejecutada_por, self.usuario)

    def test_fecha_inicio_automatica(self):
        """Test para verificar que la fecha de inicio se establece automáticamente."""
        ejecucion = EjecucionTarea.objects.create(**self.ejecucion_data)
        self.assertIsNotNone(ejecucion.fecha_inicio)
        self.assertIsNone(ejecucion.fecha_fin)

    def test_actualizar_fecha_fin(self):
        """Test para verificar la actualización de la fecha de fin."""
        ejecucion = EjecucionTarea.objects.create(**self.ejecucion_data)
        
        # Actualizar fecha de fin
        ahora = timezone.now()
        ejecucion.fecha_fin = ahora
        ejecucion.save()
        
        # Verificar que se actualizó correctamente
        ejecucion.refresh_from_db()
        self.assertEqual(ejecucion.fecha_fin, ahora)

    def test_estados_ejecucion(self):
        """Test para verificar los estados posibles de una ejecución."""
        ejecucion = EjecucionTarea.objects.create(**self.ejecucion_data)
        
        # Verificar estado inicial
        self.assertEqual(ejecucion.estado, 'exitoso')
        
        # Cambiar estados
        estados = ['error', 'cancelado']
        for estado in estados:
            ejecucion.estado = estado
            ejecucion.save()
            self.assertEqual(ejecucion.estado, estado)

    def test_str_representation(self):
        """Test para verificar la representación en string de la ejecución."""
        ejecucion = EjecucionTarea.objects.create(**self.ejecucion_data)
        expected_str = f"Ejecución de {self.tarea.nombre} - {ejecucion.fecha_inicio}"
        self.assertEqual(str(ejecucion), expected_str) 