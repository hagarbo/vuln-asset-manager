from django.test import TestCase
from django.contrib.auth import get_user_model
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from django.utils import timezone

User = get_user_model()

class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Cliente Test'
        )

    def test_cliente_creation(self):
        self.assertEqual(self.cliente.nombre, 'Cliente Test')
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
            tipo='hardware',
            descripcion='Descripción de prueba',
            palabras_clave='test,prueba,ejemplo',
            ip='192.168.1.1',
            puerto=8080,
            version='1.0'
        )

    def test_activo_creation(self):
        self.assertEqual(self.activo.nombre, 'Activo Test')
        self.assertEqual(self.activo.tipo, 'hardware')
        self.assertEqual(self.activo.descripcion, 'Descripción de prueba')
        self.assertEqual(self.activo.palabras_clave, 'test,prueba,ejemplo')
        self.assertEqual(self.activo.ip, '192.168.1.1')
        self.assertEqual(self.activo.puerto, 8080)
        self.assertEqual(self.activo.version, '1.0')
        self.assertIsNotNone(self.activo.created_at)
        self.assertIsNotNone(self.activo.updated_at)

    def test_activo_str(self):
        self.assertEqual(str(self.activo), 'Activo Test (Hardware)')

class VulnerabilidadModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability description',
            descripcion_es='Descripción de vulnerabilidad de prueba',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date(),
            cvss_data={
                'v3.0': {
                    'score': 7.5,
                    'severidad': 'HIGH',
                    'vector': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H'
                }
            },
            referencias=['https://example.com/cve-2024-0001']
        )

    def test_vulnerabilidad_creation(self):
        self.assertEqual(self.vulnerabilidad.cve_id, 'CVE-2024-0001')
        self.assertEqual(self.vulnerabilidad.descripcion_en, 'Test vulnerability description')
        self.assertEqual(self.vulnerabilidad.descripcion_es, 'Descripción de vulnerabilidad de prueba')
        self.assertEqual(self.vulnerabilidad.severidad, 'high')
        self.assertEqual(self.vulnerabilidad.status, 'published')
        self.assertIsNotNone(self.vulnerabilidad.fecha_publicacion)
        self.assertIsNotNone(self.vulnerabilidad.fecha_modificacion)
        self.assertIsNotNone(self.vulnerabilidad.fecha_deteccion)
        self.assertEqual(self.vulnerabilidad.cvss_data['v3.0']['score'], 7.5)
        self.assertEqual(self.vulnerabilidad.referencias[0], 'https://example.com/cve-2024-0001')
        self.assertIsNotNone(self.vulnerabilidad.created_at)
        self.assertIsNotNone(self.vulnerabilidad.updated_at)

    def test_vulnerabilidad_str(self):
        self.assertEqual(str(self.vulnerabilidad), 'CVE-2024-0001')

class ActivoVulnerabilidadModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Cliente Test')
        cls.activo = Activo.objects.create(
            cliente=cls.cliente,
            nombre='Activo Test',
            tipo='hardware',
            palabras_clave='test'
        )
        cls.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability',
            descripcion_es='Vulnerabilidad de prueba',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date()
        )
        cls.activo_vulnerabilidad = ActivoVulnerabilidad.objects.create(
            activo=cls.activo,
            vulnerabilidad=cls.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas de prueba'
        )

    def test_activo_vulnerabilidad_creation(self):
        self.assertEqual(self.activo_vulnerabilidad.activo, self.activo)
        self.assertEqual(self.activo_vulnerabilidad.vulnerabilidad, self.vulnerabilidad)
        self.assertIsNotNone(self.activo_vulnerabilidad.fecha_deteccion)
        self.assertEqual(self.activo_vulnerabilidad.estado, 'PENDIENTE')
        self.assertEqual(self.activo_vulnerabilidad.notas, 'Notas de prueba')
        self.assertIsNotNone(self.activo_vulnerabilidad.created_at)
        self.assertIsNotNone(self.activo_vulnerabilidad.updated_at)

    def test_activo_vulnerabilidad_str(self):
        expected_str = f"{self.activo} - {self.vulnerabilidad}"
        self.assertEqual(str(self.activo_vulnerabilidad), expected_str) 