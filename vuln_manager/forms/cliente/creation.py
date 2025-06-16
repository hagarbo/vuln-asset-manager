from django import forms
from django.contrib.auth import get_user_model
from vuln_manager.models.auth.usuario import Usuario

class ClienteCreationForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    nombre = forms.CharField(label='Nombre del cliente', max_length=100)
    archivo_activos = forms.FileField(label='Archivo de activos (CSV)', required=False)
    analistas = forms.ModelMultipleChoiceField(
        queryset=None,  # Se inyecta en __init__ obligatoriamente
        required=False,
        widget=forms.SelectMultiple,
        label='Analistas asignados'
    )

    def __init__(self, *args, **kwargs):
        analistas_queryset = kwargs.pop('analistas_queryset', None)
        if analistas_queryset is None:
            raise ValueError('Debe proporcionar el queryset de analistas (analistas_queryset) al formulario')
        super().__init__(*args, **kwargs)
        self.fields['analistas'].queryset = analistas_queryset
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['analistas'].widget.attrs['size'] = 6 