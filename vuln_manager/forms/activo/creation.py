from django import forms
from vuln_manager.models import Activo, Cliente
from vuln_manager.repository.activo.activo_repository import ActivoRepository

class ActivoCreationForm(forms.ModelForm):
    """
    Formulario para la creación de nuevos activos.
    """
    class Meta:
        model = Activo
        fields = [
            'cliente',
            'nombre',
            'tipo',
            'descripcion',
            'palabras_clave',
            'ip',
            'puerto',
            'version'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'palabras_clave': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que todos los campos sean requeridos excepto descripción, ip, puerto y versión
        for field in ['cliente', 'nombre', 'tipo', 'palabras_clave']:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Campos opcionales
        for field in ['descripcion', 'ip', 'puerto', 'version']:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_puerto(self):
        puerto = self.cleaned_data.get('puerto')
        if puerto:
            try:
                return int(puerto)
            except (ValueError, TypeError):
                raise forms.ValidationError('El puerto debe ser un número entero válido.')
        return puerto

    def clean_palabras_clave(self):
        palabras = self.cleaned_data['palabras_clave']
        if palabras:
            # Dividir por comas, limpiar cada palabra y unir de nuevo sin espacios alrededor de las comas
            palabras_lista = [p.strip() for p in palabras.split(',') if p.strip()]
            return ','.join(palabras_lista)
        return palabras

    def save(self, commit=True):
        """
        Guarda el activo utilizando el patrón Repository.
        """
        data = self.cleaned_data.copy()
        repository = ActivoRepository()
        # El campo cliente puede ser un objeto o un id
        if 'cliente' in data and hasattr(data['cliente'], 'id'):
            data['cliente'] = data['cliente']
        instance = repository.create(**data)
        return instance 