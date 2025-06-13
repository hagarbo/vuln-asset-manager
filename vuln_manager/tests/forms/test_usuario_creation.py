from django.test import TestCase
from django.core.exceptions import ValidationError
from vuln_manager.forms.usuario import UsuarioCreationForm
from vuln_manager.models import Usuario

class UsuarioCreationFormTest(TestCase):
    """Tests para el formulario de creación de usuario."""

    def setUp(self):
        """Configuración inicial para los tests."""
        self.form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'rol': 'cliente',
            'telefono': '123456789',
            'empresa': 'Test Company',
            'cargo': 'Test Position'
        }

    def test_form_valid_data(self):
        """Test que verifica que el formulario es válido con datos correctos."""
        form = UsuarioCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        """Test que verifica que el formulario es inválido con email incorrecto."""
        self.form_data['email'] = 'invalid-email'
        form = UsuarioCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_password_mismatch(self):
        """Test que verifica que el formulario es inválido cuando las contraseñas no coinciden."""
        self.form_data['password2'] = 'differentpass'
        form = UsuarioCreationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_required_fields(self):
        """Test que verifica que los campos requeridos son validados."""
        required_fields = ['username', 'email', 'rol', 'password1', 'password2']
        for field in required_fields:
            data = self.form_data.copy()
            data[field] = ''
            form = UsuarioCreationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)

    def test_form_save(self):
        """Test que verifica que el formulario guarda correctamente un usuario."""
        form = UsuarioCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertIsInstance(user, Usuario)
        self.assertEqual(user.username, self.form_data['username'])
        self.assertEqual(user.email, self.form_data['email'])
        self.assertEqual(user.rol, self.form_data['rol']) 