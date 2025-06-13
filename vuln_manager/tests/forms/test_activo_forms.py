from django.test import TestCase
from django.contrib.auth import get_user_model
from vuln_manager.models import Cliente
from vuln_manager.forms.activo.creation import ActivoCreationForm
from vuln_manager.forms.activo.update import ActivoUpdateForm
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from unittest.mock import patch

User = get_user_model()

class TestActivoForms(TestCase):
    def setUp(self):
        # Crear un cliente de prueba
        self.cliente = Cliente.objects.create(nombre='Cliente Test')
        # Crear un usuario de prueba
        self.usuario = User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')
        # Datos de prueba para el formulario de creación
        self.creation_data = {
            'cliente': self.cliente,
            'nombre': 'Activo Test',
            'tipo': 'hardware',
            'descripcion': 'Descripción de prueba',
            'palabras_clave': 'test,activo',
            'ip': '192.168.1.1',
            'puerto': 80,
            'version': '1.0'
        }
        # Datos de prueba para el formulario de actualización
        self.update_data = {
            'nombre': 'Activo Actualizado',
            'tipo': 'software',
            'descripcion': 'Descripción actualizada',
            'palabras_clave': 'test,actualizado',
            'ip': '192.168.1.2',
            'puerto': 443,
            'version': '2.0'
        }

    @patch.object(ActivoRepository, 'create')
    def test_activo_creation_form_save(self, mock_create):
        # Crear una instancia del formulario con datos válidos
        form = ActivoCreationForm(data=self.creation_data)
        self.assertTrue(form.is_valid())
        # Llamar al método save
        form.save()
        # Verificar que se llamó al método create del repositorio con los datos correctos
        mock_create.assert_called_once_with(**self.creation_data)

    @patch.object(ActivoRepository, 'update')
    def test_activo_update_form_save(self, mock_update):
        # Crear un activo de prueba
        activo = ActivoRepository().create(**self.creation_data)
        # Crear una instancia del formulario con datos válidos y la instancia existente
        form = ActivoUpdateForm(data=self.update_data, instance=activo)
        self.assertTrue(form.is_valid())
        # Llamar al método save
        form.save()
        # Verificar que se llamó al método update del repositorio con los datos correctos
        mock_update.assert_called_once_with(activo.id, **self.update_data) 