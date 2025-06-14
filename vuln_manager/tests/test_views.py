from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.auth.usuario import Usuario
from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
import datetime

class ViewTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        # Crear usuario admin
        cls.admin = Usuario.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass',
            rol='admin'
        )
        # Crear usuario analista
        cls.analista = Usuario.objects.create_user(
            username='analista',
            email='analista@example.com',
            password='analistapass',
            rol='analista'
        )
        # Crear usuario cliente
        cls.cliente_user = Usuario.objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='clientepass',
            rol='cliente'
        )
        # Crear cliente
        cls.cliente_test = Cliente.objects.create(nombre='Cliente de Prueba')
        # Asignar cliente al analista
        AnalistaCliente.objects.create(analista=cls.analista, cliente=cls.cliente_user)
        # Crear activo
        cls.activo_test = Activo.objects.create(
            cliente=cls.cliente_test,
            nombre='Activo de Prueba',
            tipo='software'
        )
        # Crear vulnerabilidad
        cls.vulnerabilidad_test = Vulnerabilidad.objects.create(
            cve_id='CVE-TEST-001',
            descripcion_en='Test Vulnerability',
            descripcion_es='Vulnerabilidad de Prueba',
            severidad='alta',
            status='published',
            fecha_publicacion=datetime.date(2023, 1, 1),
            fecha_modificacion=datetime.date(2023, 1, 1)
        )

class ClienteViewTest(ViewTestBase):
    def setUp(self):
        self.client.login(username='admin', password='adminpass')
        self.cliente = Cliente.objects.create(nombre='Cliente Test')

    def test_cliente_list_view(self):
        response = self.client.get(reverse('vuln_manager:cliente_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/cliente/list.html')
        self.assertContains(response, self.cliente.nombre)
        self.assertIn('clientes', response.context)
        self.assertIn(self.cliente, list(response.context['clientes']))

    def test_cliente_detail_view(self):
        response = self.client.get(reverse('vuln_manager:cliente_detail', args=[self.cliente.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/cliente/detail.html')
        self.assertContains(response, self.cliente.nombre)
        self.assertIn('object', response.context)
        self.assertEqual(response.context['object'], self.cliente)

class ActivoViewTest(ViewTestBase):
    def setUp(self):
        self.client.login(username='admin', password='adminpass')
        self.cliente = Cliente.objects.create(nombre='Cliente Test')
        self.activo = Activo.objects.create(
            cliente=self.cliente,
            nombre='Activo Test',
            tipo='hardware',
            palabras_clave='test'
        )

    def test_activo_list_view(self):
        response = self.client.get(reverse('vuln_manager:activo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activo/list.html')
        self.assertContains(response, self.activo.nombre)
        self.assertIn('activos', response.context)
        self.assertIn(self.activo, list(response.context['activos']))

    def test_activo_detail_view(self):
        response = self.client.get(reverse('vuln_manager:activo_detail', args=[self.activo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activo/detail.html')
        self.assertContains(response, self.activo.nombre)
        self.assertIn('object', response.context)
        self.assertEqual(response.context['object'], self.activo)

class VulnerabilidadViewTest(ViewTestBase):
    def setUp(self):
        self.client.login(username='admin', password='adminpass')
        self.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability',
            descripcion_es='Vulnerabilidad de prueba',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date()
        )

    def test_vulnerabilidad_list_view(self):
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/list.html')
        self.assertContains(response, self.vulnerabilidad.cve_id)
        self.assertIn('vulnerabilidades', response.context)
        self.assertIn(self.vulnerabilidad, list(response.context['vulnerabilidades']))

    def test_vulnerabilidad_detail_view(self):
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_detail', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/detail.html')
        self.assertContains(response, self.vulnerabilidad.cve_id)
        self.assertIn('object', response.context)
        self.assertEqual(response.context['object'], self.vulnerabilidad) 