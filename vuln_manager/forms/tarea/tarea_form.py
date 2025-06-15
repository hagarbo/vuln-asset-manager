from django import forms
from vuln_manager.models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'programacion', 'dias_atras', 'incluir_rechazadas']
        widgets = {
            'programacion': forms.TextInput(attrs={'placeholder': 'Ejemplo: 0 0 * * *'}),
            'dias_atras': forms.NumberInput(attrs={'min': 1, 'max': 30}),
        }

    def clean_programacion(self):
        programacion = self.cleaned_data.get('programacion')
        if not programacion:
            raise forms.ValidationError('La programación es obligatoria.')
        return programacion

    def clean_dias_atras(self):
        dias_atras = self.cleaned_data.get('dias_atras')
        if dias_atras is not None and (dias_atras < 1 or dias_atras > 30):
            raise forms.ValidationError('El número de días debe estar entre 1 y 30.')
        return dias_atras 