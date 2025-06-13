from django.test import TestCase
from django.contrib.auth import get_user_model
from vuln_manager.forms.usuario.creation import UsuarioCreationForm
from vuln_manager.forms.usuario.change import UsuarioChangeForm
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository
from unittest.mock import patch

User = get_user_model()

class TestUsuarioForms(TestCase):
    def setUp(self):
        # Datos de prueba para el formulario de creación
        self.creation_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'rol': 'admin',
            'telefono': '123456789',
            'empresa': 'Empresa Test',
            'cargo': 'Cargo Test',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        # Datos de prueba para el formulario de actualización
        self.update_data = {
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'telefono': '987654321',
            'empresa': 'Empresa Actualizada',
            'cargo': 'Cargo Actualizado'
        }

    @patch.object(UsuarioRepository, 'create')
    def test_usuario_creation_form_save(self, mock_create):
        # Crear una instancia del formulario con datos válidos
        form = UsuarioCreationForm(data=self.creation_data)
        self.assertTrue(form.is_valid())
        # Llamar al método save
        form.save()
        # Verificar que se llamó al método create del repositorio con los datos correctos
        mock_create.assert_called_once_with(**self.creation_data)

    @patch.object(UsuarioRepository, 'update')
    def test_usuario_change_form_save(self, mock_update):
        # Crear un usuario de prueba
        data_for_create = {k: v for k, v in self.creation_data.items() if k not in ['password1', 'password2']}
        usuario = UsuarioRepository().create(**data_for_create)
        # Crear una instancia del formulario con datos válidos y la instancia existente
        form = UsuarioChangeForm(data=self.update_data, instance=usuario)
        self.assertTrue(form.is_valid())
        # Llamar al método save
        form.save()
        # Verificar que se llamó al método update del repositorio con los datos correctos
        mock_update.assert_called_once_with(usuario.id, **self.update_data) 