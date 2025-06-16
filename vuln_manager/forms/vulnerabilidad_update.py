from django import forms
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

class VulnerabilidadUpdateForm(forms.ModelForm):
    class Meta:
        model = Vulnerabilidad
        fields = [
            'cve_id', 'descripcion_en', 'descripcion_es', 'severidad', 'status',
            'fecha_publicacion', 'fecha_modificacion'
        ]
        widgets = {
            'cve_id': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_en': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'descripcion_es': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'severidad': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'fecha_publicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_modificacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        """
        Actualiza la vulnerabilidad utilizando el patrón Repository.
        """
        data = self.cleaned_data.copy()
        repository = VulnerabilidadRepository()
        instance = repository.update(self.instance.id, **data)
        return instance 