from django import forms
from vuln_manager.models.cliente.cliente import Cliente
from vuln_manager.models.auth.usuario import Usuario

class ClienteUpdateForm(forms.ModelForm):
    analistas = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(rol='analista'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': 6}),
        label='Analistas asignados'
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'analistas']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['analistas'].widget.attrs['class'] = 'form-control'
        self.fields['analistas'].widget.attrs['size'] = 6 