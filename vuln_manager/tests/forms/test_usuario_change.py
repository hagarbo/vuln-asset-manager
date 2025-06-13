from django.test import TestCase
from django.contrib.auth import get_user_model
from vuln_manager.forms.usuario import UsuarioChangeForm
from vuln_manager.models import Usuario

class UsuarioChangeFormTest(TestCase):
    """Tests para el formulario de modificación de usuario."""

    def setUp(self):
        """Configuración inicial para los tests."""
        self.user = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            rol='cliente'
        )
        self.form_data = {
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'telefono': '987654321',
            'empresa': 'Updated Company',
            'cargo': 'Updated Position'
        }

    def test_form_valid_data(self):
        """Test que verifica que el formulario es válido con datos correctos."""
        form = UsuarioChangeForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        """Test que verifica que el formulario es inválido con email incorrecto."""
        self.form_data['email'] = 'invalid-email'
        form = UsuarioChangeForm(data=self.form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_required_email(self):
        """Test que verifica que el email es un campo requerido."""
        self.form_data['email'] = ''
        form = UsuarioChangeForm(data=self.form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_save(self):
        """Test que verifica que el formulario guarda correctamente los cambios."""
        form = UsuarioChangeForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, self.form_data['email'])
        self.assertEqual(updated_user.first_name, self.form_data['first_name'])
        self.assertEqual(updated_user.last_name, self.form_data['last_name'])
        self.assertEqual(updated_user.telefono, self.form_data['telefono'])
        self.assertEqual(updated_user.empresa, self.form_data['empresa'])
        self.assertEqual(updated_user.cargo, self.form_data['cargo'])

    def test_form_excludes_password(self):
        """Test que verifica que el campo password está excluido del formulario."""
        form = UsuarioChangeForm(instance=self.user)
        self.assertNotIn('password', form.fields) 