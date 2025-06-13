from django.contrib.auth.forms import UserChangeForm
from django import forms
from vuln_manager.models import Usuario
from vuln_manager.repository.usuario.usuario_repository import UsuarioRepository

class UsuarioChangeForm(UserChangeForm):
    """
    Formulario para la modificación de usuarios existentes.
    Extiende UserChangeForm de Django para incluir campos personalizados.
    """
    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'telefono', 'empresa', 'cargo')
        exclude = ('password', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        # Asegurarnos de que los campos de contraseña no estén presentes
        if 'password' in self.fields:
            del self.fields['password']
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2'] 

    def save(self, commit=True):
        """
        Actualiza el usuario utilizando el patrón Repository.
        """
        data = self.cleaned_data.copy()
        repository = UsuarioRepository()
        instance = repository.update(self.instance.id, **data)
        return instance 
