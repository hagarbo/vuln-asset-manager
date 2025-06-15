from django import forms
from vuln_manager.models.tarea.tipo_tarea import TipoTarea

class TipoTareaForm(forms.ModelForm):
    class Meta:
        model = TipoTarea
        fields = ['codigo', 'nombre', 'descripcion', 'parametros', 'activo']
        widgets = {
            'parametros': forms.JSONField(
                widget=forms.Textarea(attrs={'rows': 4}),
                help_text="Configuración de parámetros en formato JSON"
            )
        } 