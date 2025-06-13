from django.test import TestCase
from django.core.exceptions import ValidationError
from vuln_manager.models import Cliente
from vuln_manager.forms.activo.creation import ActivoCreationForm

class ActivoCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(nombre='Empresa de Prueba')

    def test_form_valid_data(self):
        form_data = {
            'cliente': self.cliente.id,
            'nombre': 'Servidor Web',
            'tipo': 'hardware',
            'descripcion': 'Servidor de producción',
            'palabras_clave': 'web, apache',
            'ip': '192.168.1.1',
            'puerto': 80,
            'version': '2.4.54'
        }
        form = ActivoCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_required_fields(self):
        form_data = {
            'cliente': self.cliente.id,
            'nombre': '',
            'tipo': '',
            'palabras_clave': ''
        }
        form = ActivoCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('tipo', form.errors)
        self.assertIn('palabras_clave', form.errors)

    def test_form_optional_fields(self):
        form_data = {
            'cliente': self.cliente.id,
            'nombre': 'Servidor Web',
            'tipo': 'hardware',
            'palabras_clave': 'web, apache'
        }
        form = ActivoCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_clean_palabras_clave(self):
        form_data = {
            'cliente': self.cliente.id,
            'nombre': 'Servidor Web',
            'tipo': 'hardware',
            'palabras_clave': '  web , apache , nginx  '
        }
        form = ActivoCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['palabras_clave'], 'web, apache, nginx')

    def test_form_save(self):
        form_data = {
            'cliente': self.cliente.id,
            'nombre': 'Servidor Web',
            'tipo': 'hardware',
            'palabras_clave': 'web, apache',
            'ip': '192.168.1.1',
            'puerto': 80,
            'version': '2.4.54'
        }
        form = ActivoCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        activo = form.save()
        self.assertEqual(activo.nombre, 'Servidor Web')
        self.assertEqual(activo.cliente, self.cliente)
        self.assertEqual(activo.tipo, 'hardware')
        self.assertEqual(activo.palabras_clave, 'web, apache')
        self.assertEqual(activo.ip, '192.168.1.1')
        self.assertEqual(activo.puerto, 80)
        self.assertEqual(activo.version, '2.4.54') 