from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup

User = get_user_model()

class VulnerabilidadViewsTest(TestCase):
    def setUp(self):
        # Crear usuario administrador
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass',
            rol='admin'  # Asegurar que tiene el rol de admin
        )
        
        # Crear usuario analista
        self.analista = User.objects.create_user(
            username='analista',
            email='analista@example.com',
            password='analistapass',
            rol='analista'
        )
        
        # Crear vulnerabilidad de prueba
        self.vulnerabilidad = Vulnerabilidad.objects.create(
            cve_id='CVE-2024-0001',
            descripcion_en='Test vulnerability',
            descripcion_es='Vulnerabilidad de prueba',
            severidad='high',
            status='published',
            fecha_publicacion=timezone.now().date(),
            fecha_modificacion=timezone.now().date()
        )
        
        # Configurar cliente HTTP
        self.client = Client()

    def test_list_view_requires_login(self):
        """Test que verifica que se requiere login para ver la lista"""
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_list'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_list_view_accessible_by_all_roles(self):
        """Test que verifica que la lista es accesible por todos los roles"""
        # Probar con analista
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/list.html')
        
        # Probar con admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/list.html')

    def test_detail_view_requires_login(self):
        """Test que verifica que se requiere login para ver el detalle"""
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_detail', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_detail_view_accessible_by_all_roles(self):
        """Test que verifica que el detalle es accesible por todos los roles"""
        # Probar con analista
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_detail', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/detail.html')
        
        # Probar con admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_detail', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/detail.html')

    def test_update_view_requires_admin(self):
        """Test que verifica que solo los administradores pueden editar"""
        # Probar con analista
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_update', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 403)
        
        # Probar con admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_update', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/form.html')

    def test_delete_view_requires_admin(self):
        """Test que verifica que solo los administradores pueden eliminar"""
        # Probar con analista
        self.client.login(username='analista', password='analistapass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_delete', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 403)
        
        # Probar con admin
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('vuln_manager:vulnerabilidad_delete', args=[self.vulnerabilidad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vuln_manager/vulnerabilidad/confirm_delete.html')

    def test_update_vulnerabilidad(self):
        """Test que verifica la actualización de una vulnerabilidad"""
        self.client.login(username='admin', password='adminpass')
        # Datos para actualizar (solo los campos editables)
        data = {
            'cve_id': self.vulnerabilidad.cve_id,
            'descripcion_es': 'Descripción actualizada',
            'descripcion_en': 'Updated description',
            'severidad': 'critica',
            'status': 'published',
            'fecha_publicacion': self.vulnerabilidad.fecha_publicacion.strftime('%Y-%m-%d'),
            'fecha_modificacion': self.vulnerabilidad.fecha_modificacion.strftime('%Y-%m-%d')
        }
        # Enviar POST request
        response = self.client.post(
            reverse('vuln_manager:vulnerabilidad_update', args=[self.vulnerabilidad.id]),
            data
        )
        # Si no hay redirección, mostrar errores del formulario para depuración
        if response.status_code != 302:
            soup = BeautifulSoup(response.content, 'html.parser')
            errors = soup.find_all(class_='text-danger')
            print('ERRORES DEL FORMULARIO:')
            for e in errors:
                print(e.get_text(strip=True))
        # Verificar redirección
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('vuln_manager:vulnerabilidad_list')))
        # Verificar que se actualizó la vulnerabilidad
        self.vulnerabilidad.refresh_from_db()
        self.assertEqual(self.vulnerabilidad.descripcion_es, 'Descripción actualizada')
        self.assertEqual(self.vulnerabilidad.descripcion_en, 'Updated description')
        self.assertEqual(self.vulnerabilidad.severidad, 'critica')

    def test_delete_vulnerabilidad(self):
        """Test que verifica la eliminación de una vulnerabilidad"""
        self.client.login(username='admin', password='adminpass')
        
        # Enviar POST request
        response = self.client.post(
            reverse('vuln_manager:vulnerabilidad_delete', args=[self.vulnerabilidad.id])
        )
        
        # Verificar redirección
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('vuln_manager:vulnerabilidad_list')))
        
        # Verificar que se eliminó la vulnerabilidad
        self.assertFalse(Vulnerabilidad.objects.filter(id=self.vulnerabilidad.id).exists()) 