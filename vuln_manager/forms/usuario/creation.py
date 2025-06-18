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
        Guarda el usuario utilizando el método seguro de Django, validando que las contraseñas coinciden.
        """
        data = self.cleaned_data.copy()
        password1 = data.pop('password1', None)
        password2 = data.pop('password2', None)
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        data.pop('password', None)
        instance = Usuario.objects.create_user(password=password1, **data)
        return instance 
