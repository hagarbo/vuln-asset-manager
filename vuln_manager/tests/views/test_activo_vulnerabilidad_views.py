from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from django.contrib.auth import get_user_model

User = get_user_model()

class ActivoVulnerabilidadViewsTest(TestCase):
    def setUp(self):
        # Crear usuario administrador
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        
        # Crear usuario analista
        self.analista = User.objects.create_user(
            username='analista',
            email='analista@example.com',
            password='analistapass',
            rol='analista'
        )
        
        # Crear cliente
        self.cliente = Cliente.objects.create(nombre='Cliente Test')
        self.cliente.analistas.add(self.analista)
        
        # Crear activo
        self.activo = Activo.objects.create(
            cliente=self.cliente,
            nombre='Activo Test',
            tipo='hardware',
            palabras_clave='test'
        )
        
        # Crear vulnerabilidad
        self.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability',
            descripcion_es='Vulnerabilidad de prueba',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date()
        )
        
        # Crear relación activo-vulnerabilidad
        self.activo_vulnerabilidad = ActivoVulnerabilidad.objects.create(
            activo=self.activo,
            vulnerabilidad=self.vulnerabilidad,
            fecha_deteccion=timezone.now().date(),
            estado='PENDIENTE',
            notas='Notas de prueba'
        )
        
        # Configurar cliente HTTP
        self.client = Client()

    def test_list_view_requires_login(self):
        """Test que verifica que se requiere login para ver la lista"""
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_requires_permission(self):
        """Test que verifica que se requiere permiso para ver la lista"""
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activo_vulnerabilidad/list.html')

    def test_create_view_requires_login(self):
        """Test que verifica que se requiere login para crear"""
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_create_view_requires_permission(self):
        """Test que verifica que se requiere permiso para crear"""
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activo_vulnerabilidad/create.html')

    def test_update_view_requires_login(self):
        """Test que verifica que se requiere login para actualizar"""
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_update', args=[self.activo_vulnerabilidad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_view_requires_permission(self):
        """Test que verifica que se requiere permiso para actualizar"""
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_update', args=[self.activo_vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activo_vulnerabilidad/update.html')

    def test_delete_view_requires_login(self):
        """Test que verifica que se requiere login para eliminar"""
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_delete', args=[self.activo_vulnerabilidad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_view_requires_permission(self):
        """Test que verifica que se requiere permiso para eliminar"""
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:activo_vulnerabilidad_delete', args=[self.activo_vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/activo_vulnerabilidad/delete.html')

    def test_create_activo_vulnerabilidad(self):
        """Test que verifica la creación de una relación activo-vulnerabilidad"""
        self.client.login(username='analista', password='analistapass')
        
        # Datos para crear una nueva relación
        data = {
            'activo': self.activo.id,
            'vulnerabilidad': self.vulnerabilidad.id,
            'fecha_deteccion': timezone.now().date(),
            'estado': 'PENDIENTE',
            'notas': 'Nueva relación de prueba'
        }
        
        # Enviar POST request
        response = self.client.post(reverse('vuln_manager:activo_vulnerabilidad_create'), data)
        
        # Verificar redirección
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('vuln_manager:activo_vulnerabilidad_list')))
        
        # Verificar que se creó la relación
        self.assertTrue(ActivoVulnerabilidad.objects.filter(notas='Nueva relación de prueba').exists())

    def test_update_activo_vulnerabilidad(self):
        """Test que verifica la actualización de una relación activo-vulnerabilidad"""
        self.client.login(username='analista', password='analistapass')
        
        # Datos para actualizar
        data = {
            'activo': self.activo.id,
            'vulnerabilidad': self.vulnerabilidad.id,
            'fecha_deteccion': timezone.now().date(),
            'estado': 'EN_PROGRESO',
            'notas': 'Notas actualizadas'
        }
        
        # Enviar POST request
        response = self.client.post(
            reverse('vuln_manager:activo_vulnerabilidad_update', args=[self.activo_vulnerabilidad.id]),
            data
        )
        
        # Verificar redirección
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('vuln_manager:activo_vulnerabilidad_list')))
        
        # Verificar que se actualizó la relación
        self.activo_vulnerabilidad.refresh_from_db()
        self.assertEqual(self.activo_vulnerabilidad.estado, 'EN_PROGRESO')
        self.assertEqual(self.activo_vulnerabilidad.notas, 'Notas actualizadas')

    def test_delete_activo_vulnerabilidad(self):
        """Test que verifica la eliminación de una relación activo-vulnerabilidad"""
        self.client.login(username='analista', password='analistapass')
        
        # Enviar POST request
        response = self.client.post(
            reverse('vuln_manager:activo_vulnerabilidad_delete', args=[self.activo_vulnerabilidad.id])
        )
        
        # Verificar redirección
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('vuln_manager:activo_vulnerabilidad_list')))
        
        # Verificar que se eliminó la relación
        self.assertFalse(ActivoVulnerabilidad.objects.filter(id=self.activo_vulnerabilidad.id).exists()) 