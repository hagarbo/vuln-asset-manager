from django.test import TestCase
from django.contrib.auth import get_user_model
from vuln_manager.models import (
    Usuario,
    Cliente,
    Activo,
    Vulnerabilidad,
    ActivoVulnerabilidad,
    Tarea,
    EjecucionTarea,
    Alerta,
)
import datetime

User = get_user_model()

class ClienteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.cliente = Cliente.objects.create(
            nombre='Cliente Test',
            email='cliente@test.com',
            telefono='123456789',
            direccion='Dirección Test'
        )
        cls.cliente.analistas.add(cls.user)

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nombre, 'Cliente Test')
        self.assertEqual(self.cliente.email, 'cliente@test.com')
        self.assertEqual(self.cliente.telefono, '123456789')
        self.assertEqual(self.cliente.direccion, 'Dirección Test')
        self.assertIn(self.user, self.cliente.analistas.all())
        self.assertIsNotNone(self.cliente.created_at)
        self.assertIsNotNone(self.cliente.updated_at)

    def test_cliente_str(self):
        self.assertEqual(str(self.cliente), 'Cliente Test')

class ActivoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.activo = Activo.objects.create(
            cliente=cls.cliente,
            nombre='Activo Test',
            tipo='SERVIDOR',
            descripcion='Descripción Test',
            estado='ACTIVO'
        )

    def test_activo_creation(self):
        self.assertEqual(self.activo.nombre, 'Activo Test')
        self.assertEqual(self.activo.cliente, self.cliente)
        self.assertEqual(self.activo.get_tipo_display(), 'Servidor')
        self.assertEqual(self.activo.descripcion, 'Descripción Test')
        self.assertEqual(self.activo.estado, 'ACTIVO')
        self.assertIsNotNone(self.activo.created_at)
        self.assertIsNotNone(self.activo.updated_at)

    def test_activo_str(self):
        self.assertEqual(str(self.activo), 'Activo Test (Servidor)')

class VulnerabilidadModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vulnerabilidad = Vulnerabilidad.objects.create(
            nombre='Vulnerabilidad Test',
            descripcion='Descripción Test',
            severidad='ALTA',
            estado='ACTIVA'
        )

    def test_vulnerabilidad_creation(self):
        self.assertEqual(self.vulnerabilidad.nombre, 'Vulnerabilidad Test')
        self.assertEqual(self.vulnerabilidad.descripcion, 'Descripción Test')
        self.assertEqual(self.vulnerabilidad.get_severidad_display(), 'Alta')
        self.assertEqual(self.vulnerabilidad.estado, 'ACTIVA')

    def test_vulnerabilidad_str(self):
        self.assertEqual(str(self.vulnerabilidad), 'Vulnerabilidad Test')

class TareaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.tarea = Tarea.objects.create(
            nombre='Tarea Test',
            descripcion='Descripción Test',
            tipo='ESCANEO',
            estado='PENDIENTE',
            creada_por=cls.user
        )

    def test_tarea_creation(self):
        self.assertEqual(self.tarea.nombre, 'Tarea Test')
        self.assertEqual(self.tarea.descripcion, 'Descripción Test')
        self.assertEqual(self.tarea.get_tipo_display(), 'Escaneo')
        self.assertEqual(self.tarea.creada_por, self.user)

    def test_tarea_str(self):
        self.assertEqual(str(self.tarea), 'Tarea Test (Escaneo)')

class AlertaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.activo = Activo.objects.create(
            cliente=cls.cliente,
            nombre='Activo Test',
            tipo='SERVIDOR',
            palabras_clave='web'
        )
        cls.vulnerabilidad = Vulnerabilidad.objects.create(
            nombre='Vulnerabilidad Test',
            descripcion='Descripción Test',
            severidad='ALTA',
            estado='ACTIVA'
        )
        cls.alerta = Alerta.objects.create(
            vulnerabilidad=cls.vulnerabilidad,
            activo=cls.activo,
            analista_asignado=cls.user,
            mensaje='Mensaje Test',
            severidad='ALTA',
            estado='ACTIVA'
        )

    def test_alerta_creation(self):
        self.assertEqual(self.alerta.vulnerabilidad, self.vulnerabilidad)
        self.assertEqual(self.alerta.activo, self.activo)
        self.assertEqual(self.alerta.analista_asignado, self.user)
        self.assertEqual(self.alerta.get_estado_display(), 'Activa')
        self.assertEqual(self.alerta.mensaje, 'Mensaje Test')
        self.assertEqual(self.alerta.severidad, 'ALTA')

    def test_alerta_str(self):
        self.assertEqual(str(self.alerta), f"Alerta {self.vulnerabilidad.nombre} - {self.activo.nombre}")

class ActivoVulnerabilidadModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.activo = Activo.objects.create(
            cliente=cls.cliente,
            nombre='Activo Test',
            tipo='SERVIDOR',
            palabras_clave='web'
        )
        cls.vulnerabilidad = Vulnerabilidad.objects.create(
            nombre='Vulnerabilidad Test',
            descripcion='Descripción Test',
            severidad='ALTA',
            estado='ACTIVA'
        )
        cls.activo_vulnerabilidad = ActivoVulnerabilidad.objects.create(
            activo=cls.activo,
            vulnerabilidad=cls.vulnerabilidad,
            estado='DETECTADA',
            notas='Notas Test'
        )

    def test_activo_vulnerabilidad_creation(self):
        self.assertEqual(self.activo_vulnerabilidad.activo, self.activo)
        self.assertEqual(self.activo_vulnerabilidad.vulnerabilidad, self.vulnerabilidad)
        self.assertEqual(self.activo_vulnerabilidad.get_estado_display(), 'Detectada')
        self.assertEqual(self.activo_vulnerabilidad.notas, 'Notas Test')

class EjecucionTareaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.tarea = Tarea.objects.create(
            nombre='Tarea Test',
            descripcion='Descripción Test',
            tipo='ESCANEO',
            estado='PENDIENTE',
            creada_por=cls.user
        )
        cls.ejecucion_tarea = EjecucionTarea.objects.create(
            tarea=cls.tarea,
            estado='EN_PROGRESO',
            ejecutada_por=cls.user
        )

    def test_ejecucion_tarea_creation(self):
        self.assertEqual(self.ejecucion_tarea.tarea, self.tarea)
        self.assertEqual(self.ejecucion_tarea.get_estado_display(), 'En Progreso')
        self.assertEqual(self.ejecucion_tarea.ejecutada_por, self.user) 