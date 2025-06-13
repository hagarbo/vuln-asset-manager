from django.contrib.auth.forms import UserCreationForm
from django import forms
from vuln_manager.models import Usuario
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository

class UsuarioCreationForm(UserCreationForm):
    """
    Formulario para la creación de nuevos usuarios.
    Extiende UserCreationForm de Django para incluir campos personalizados.
    """
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'rol', 'telefono', 'empresa', 'cargo', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['rol'].required = True

    def save(self, commit=True):
        """
        Guarda el usuario utilizando el patrón Repository.
        """
        data = self.cleaned_data.copy()
        repository = UsuarioRepository()
        instance = repository.create(**data)
        return instance 
