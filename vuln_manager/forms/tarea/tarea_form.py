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
    
    # Campos dinámicos para parámetros
    severidad_minima = forms.ChoiceField(
        choices=[
            ('critica', 'Crítica'),
            ('alta', 'Alta'),
            ('media', 'Media'),
            ('baja', 'Baja'),
        ],
        required=False,
        label='Severidad Mínima',
        help_text='Severidad mínima para generar alertas',
        initial='critica'
    )
    
    dias_atras = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=30,
        label='Días hacia atrás',
        help_text='Número de días hacia atrás para buscar CVEs (1-30)',
        initial=7
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
            
            # Cargar valores de parámetros existentes
            parametros = self.instance.parametros or {}
            if 'severidad_minima' in parametros:
                self.fields['severidad_minima'].initial = parametros['severidad_minima']
            if 'dias_atras' in parametros:
                self.fields['dias_atras'].initial = parametros['dias_atras']
        else:
            # Si es nueva, inicializar con valores por defecto según el tipo
            self.fields['parametros'].initial = {}
        
        # Ocultar campos de parámetros inicialmente
        self.fields['severidad_minima'].widget.attrs.update({'style': 'display: none;'})
        self.fields['dias_atras'].widget.attrs.update({'style': 'display: none;'})

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        parametros = {}
        
        # Construir parámetros según el tipo de tarea
        if tipo:
            if tipo.codigo == 'cve_collector':
                dias_atras = cleaned_data.get('dias_atras')
                if dias_atras is not None:
                    if dias_atras > 30:
                        raise forms.ValidationError('No se pueden buscar CVEs de más de 30 días atrás')
                    if dias_atras < 1:
                        raise forms.ValidationError('El número de días debe ser mayor que 0')
                    parametros['dias_atras'] = dias_atras
                else:
                    raise forms.ValidationError('El campo "Días hacia atrás" es requerido para tareas de recolección de CVEs')
            
            elif tipo.codigo == 'cve_asset_correlation':
                severidad_minima = cleaned_data.get('severidad_minima')
                if severidad_minima:
                    parametros['severidad_minima'] = severidad_minima
                else:
                    raise forms.ValidationError('El campo "Severidad Mínima" es requerido para tareas de correlación')
        
        cleaned_data['parametros'] = parametros
        # Convertir el valor del checkbox en el estado correspondiente
        cleaned_data['estado'] = 'programada' if cleaned_data.get('activa') else 'pausada'
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.estado = 'programada' if self.cleaned_data.get('activa') else 'pausada'
        if commit:
            instance.save()
        return instance 