from django.test import TestCase
from django.core.exceptions import ValidationError
from vuln_manager.models import Cliente, Activo
from vuln_manager.forms.activo.update import ActivoUpdateForm

class ActivoUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Empresa de Prueba')
        cls.activo = Activo.objects.create(
            cliente=cls.cliente,
            nombre='Servidor Web',
            tipo='hardware',
            descripcion='Servidor de producción',
            palabras_clave='web, apache',
            ip='192.168.1.1',
            puerto=80,
            version='2.4.54'
        )

    def test_form_valid_data(self):
        form_data = {
            'nombre': 'Servidor Web Actualizado',
            'tipo': 'software',
            'descripcion': 'Servidor actualizado',
            'palabras_clave': 'web, nginx',
            'ip': '192.168.1.2',
            'puerto': 443,
            'version': '2.4.55'
        }
        form = ActivoUpdateForm(data=form_data, instance=self.activo)
        self.assertTrue(form.is_valid())

    def test_form_required_fields(self):
        form_data = {
            'nombre': '',
            'tipo': '',
            'palabras_clave': ''
        }
        form = ActivoUpdateForm(data=form_data, instance=self.activo)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('tipo', form.errors)
        self.assertIn('palabras_clave', form.errors)

    def test_form_optional_fields(self):
        form_data = {
            'nombre': 'Servidor Web Actualizado',
            'tipo': 'software',
            'palabras_clave': 'web, nginx'
        }
        form = ActivoUpdateForm(data=form_data, instance=self.activo)
        self.assertTrue(form.is_valid())

    def test_form_clean_palabras_clave(self):
        form_data = {
            'nombre': 'Servidor Web',
            'tipo': 'hardware',
            'palabras_clave': '  web , nginx , apache  '
        }
        form = ActivoUpdateForm(data=form_data, instance=self.activo)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['palabras_clave'], 'web, nginx, apache')

    def test_form_save(self):
        form_data = {
            'nombre': 'Servidor Web Actualizado',
            'tipo': 'software',
            'descripcion': 'Servidor actualizado',
            'palabras_clave': 'web, nginx',
            'ip': '192.168.1.2',
            'puerto': 443,
            'version': '2.4.55'
        }
        form = ActivoUpdateForm(data=form_data, instance=self.activo)
        self.assertTrue(form.is_valid())
        activo = form.save()
        self.assertEqual(activo.nombre, 'Servidor Web Actualizado')
        self.assertEqual(activo.tipo, 'software')
        self.assertEqual(activo.descripcion, 'Servidor actualizado')
        self.assertEqual(activo.palabras_clave, 'web, nginx')
        self.assertEqual(activo.ip, '192.168.1.2')
        self.assertEqual(activo.puerto, 443)
        self.assertEqual(activo.version, '2.4.55') 