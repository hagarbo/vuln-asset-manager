from django import forms
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['tipo', 'programacion', 'parametros']
        widgets = {
            'programacion': forms.TextInput(
                attrs={'placeholder': "Ej: '0 0 * * *' para diario a medianoche"}
            ),
            'parametros': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo tipos de tarea activos
        self.fields['tipo'].queryset = TipoTarea.objects.filter(activo=True)
        # Si hay una instancia, mostrar los parámetros actuales
        if self.instance and self.instance.pk:
            self.fields['parametros'].initial = self.instance.parametros
        else:
            # Si es nueva, inicializar con valores por defecto según el tipo
            self.fields['parametros'].initial = {}

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        parametros = cleaned_data.get('parametros', {})
        # El estado se gestiona fuera del formulario, según la lógica de la vista
        if tipo and tipo.codigo == 'cve_collector':
            try:
                dias_atras = int(parametros.get('dias_atras', 1))
                if dias_atras > 30:
                    raise forms.ValidationError('No se pueden buscar CVEs de más de 30 días atrás')
            except (ValueError, TypeError):
                raise forms.ValidationError('El valor de días atrás debe ser un número entero')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance 