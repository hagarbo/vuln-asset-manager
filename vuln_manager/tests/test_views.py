from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from vuln_manager.models import Cliente, Activo, Vulnerabilidad
import datetime

User = get_user_model()

class ViewTestBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.create_superuser('testuser', 'test@example.com', 'password')
        cls.cliente_test = Cliente.objects.create(nombre='Cliente de Prueba')
        cls.activo_test = Activo.objects.create(
            cliente=cls.cliente_test,
            nombre='Activo de Prueba',
            tipo='software'
        )
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
    def test_cliente_list_view(self):
        response = self.client.get(reverse('vuln_manager:cliente_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/clientes/list.html')
        self.assertContains(response, self.cliente_test.nombre)
        self.assertIn('clientes', response.context) # Check if 'clientes' is in context
        self.assertQuerysetEqual(response.context['clientes'], [self.cliente_test])

    def test_cliente_detail_view(self):
        response = self.client.get(reverse('vuln_manager:cliente_detail', args=[self.cliente_test.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/clientes/detail.html')
        self.assertContains(response, self.cliente_test.nombre)
        self.assertIn('object', response.context) # Check if 'object' is in context
        self.assertEqual(response.context['object'], self.cliente_test)

class ActivoViewTest(ViewTestBase):
    def test_activo_list_view(self):
        response = self.client.get(reverse('vuln_manager:activo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activos/list.html')
        self.assertContains(response, self.activo_test.nombre)
        self.assertIn('activos', response.context) # Check if 'activos' is in context
        self.assertQuerysetEqual(response.context['activos'], [self.activo_test])

    def test_activo_detail_view(self):
        response = self.client.get(reverse('vuln_manager:activo_detail', args=[self.activo_test.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activos/detail.html')
        self.assertContains(response, self.activo_test.nombre)
        self.assertIn('object', response.context) # Check if 'object' is in context
        self.assertEqual(response.context['object'], self.activo_test)

class VulnerabilidadViewTest(ViewTestBase):
    def test_vulnerabilidad_list_view(self):
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidades/list.html')
        self.assertContains(response, self.vulnerabilidad_test.cve_id)
        self.assertIn('vulnerabilidades', response.context) # Check if 'vulnerabilidades' is in context
        self.assertQuerysetEqual(response.context['vulnerabilidades'], [self.vulnerabilidad_test])

    def test_vulnerabilidad_detail_view(self):
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_detail', args=[self.vulnerabilidad_test.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidades/detail.html')
        self.assertContains(response, self.vulnerabilidad_test.cve_id)
        self.assertIn('object', response.context) # Check if 'object' is in context
        self.assertEqual(response.context['object'], self.vulnerabilidad_test) 