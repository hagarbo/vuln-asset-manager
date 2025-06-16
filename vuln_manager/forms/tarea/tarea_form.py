from django import forms
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea

class TareaForm(forms.ModelForm):
    activa = forms.BooleanField(
        required=False,
        initial=True,
        label='Tarea Activa',
        help_text='Si está marcada, la tarea se guardará como programada. Si no, se guardará como pausada.'
    )

    class Meta:
        model = Tarea
        fields = ['tipo', 'programacion', 'parametros']
        widgets = {
            'programacion': forms.TextInput(
                attrs={'placeholder': "Ej: '0 0 * * *' para diario a medianoche"}
            ),
            'parametros': forms.HiddenInput(
                attrs={'id': 'id_parametros'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo tipos de tarea activos
        self.fields['tipo'].queryset = TipoTarea.objects.filter(activo=True)
        # Si hay una instancia, mostrar los parámetros actuales y el estado
        if self.instance and self.instance.pk:
            self.fields['parametros'].initial = self.instance.parametros
            self.fields['activa'].initial = self.instance.estado == 'programada'
        else:
            # Si es nueva, inicializar con valores por defecto según el tipo
            self.fields['parametros'].initial = {}

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        parametros = cleaned_data.get('parametros', {})
        # Convertir el valor del checkbox en el estado correspondiente
        cleaned_data['estado'] = 'programada' if cleaned_data.get('activa') else 'pausada'
        
        if tipo and tipo.codigo == 'cve_collector':
            try:
                dias_atras = int(parametros.get('dias_atras', 1))
                if dias_atras > 30:
                    raise forms.ValidationError('No se pueden buscar CVEs de más de 30 días atrás')
                if dias_atras < 1:
                    raise forms.ValidationError('El número de días debe ser mayor que 0')
            except (ValueError, TypeError):
                raise forms.ValidationError('El valor de días atrás debe ser un número entero')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.estado = 'programada' if self.cleaned_data.get('activa') else 'pausada'
        if commit:
            instance.save()
        return instance 