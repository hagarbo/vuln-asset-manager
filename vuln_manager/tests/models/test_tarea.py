from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from vuln_manager.models.tarea import Tarea
from django.contrib.auth import get_user_model

class TestTarea(TestCase):
    """Tests para el modelo Tarea."""

    def setUp(self):
        """Configuración inicial para cada test."""
        # Crear usuario de prueba
        User = get_user_model()
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Datos de prueba para la tarea
        self.tarea_data = {
            'tipo': self.tipo_tarea,
            'programacion': '0 0 * * *',
            'parametros': {'dias_atras': 1},
            'estado': 'programada',
            'creada_por': self.usuario
        }

    def test_crear_tarea(self):
        """Test para crear una tarea con todos sus campos."""
        tarea = Tarea.objects.create(**self.tarea_data)
        
        # Verificar que se creó correctamente
        self.assertIsNotNone(tarea.id)
        self.assertEqual(tarea.nombre, self.tarea_data['nombre'])
        self.assertEqual(tarea.tipo, self.tarea_data['tipo'])
        self.assertEqual(tarea.descripcion, self.tarea_data['descripcion'])
        self.assertEqual(tarea.programacion, self.tarea_data['programacion'])
        self.assertEqual(tarea.estado, self.tarea_data['estado'])
        self.assertEqual(tarea.activa, self.tarea_data['activa'])
        self.assertEqual(tarea.dias_atras, self.tarea_data['dias_atras'])
        self.assertEqual(tarea.creada_por, self.usuario)

    def test_validacion_programacion(self):
        """Test para validar el formato de la programación cron."""
        # Programación inválida
        self.tarea_data['programacion'] = 'invalid'
        tarea = Tarea(**self.tarea_data)
        with self.assertRaises(ValidationError):
            tarea.full_clean()

        # Programación válida
        self.tarea_data['programacion'] = '0 0 * * *'
        tarea = Tarea(**self.tarea_data)
        tarea.full_clean()  # No debe lanzar excepción

    def test_validacion_dias_atras(self):
        """Test para validar el límite de días hacia atrás."""
        # Días inválidos
        self.tarea_data['dias_atras'] = 31
        tarea = Tarea(**self.tarea_data)
        with self.assertRaises(ValidationError):
            tarea.clean()

        # Días válidos
        self.tarea_data['dias_atras'] = 30
        tarea = Tarea(**self.tarea_data)
        tarea.clean()  # No debe lanzar excepción

    def test_estados_tarea(self):
        """Test para verificar los estados posibles de una tarea."""
        tarea = Tarea.objects.create(**self.tarea_data)
        # Verificar estado inicial
        self.assertEqual(tarea.estado, 'programada')
        # Cambiar a pausada
        tarea.estado = 'pausada'
        tarea.save()
        self.assertEqual(tarea.estado, 'pausada')

    def test_ultima_ejecucion(self):
        """Test para verificar la actualización de última ejecución."""
        tarea = Tarea.objects.create(**self.tarea_data)
        
        # Verificar que inicialmente es None
        self.assertIsNone(tarea.ultima_ejecucion)
        
        # Actualizar última ejecución
        ahora = timezone.now()
        tarea.ultima_ejecucion = ahora
        tarea.save()
        
        # Verificar que se actualizó correctamente
        tarea.refresh_from_db()
        self.assertEqual(tarea.ultima_ejecucion, ahora)

    def test_str_representation(self):
        """Test para verificar la representación en string de la tarea."""
        tarea = Tarea.objects.create(**self.tarea_data)
        self.assertEqual(str(tarea), self.tarea_data['nombre']) 