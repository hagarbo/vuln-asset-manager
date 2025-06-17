from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            existing_classes = visible.field.widget.attrs.get('class', '')
            # Añadir 'form-control' solo si no está ya presente
            if 'form-control' not in existing_classes:
                visible.field.widget.attrs['class'] = (existing_classes + ' form-control').strip() 