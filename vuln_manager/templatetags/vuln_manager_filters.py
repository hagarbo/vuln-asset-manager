from django import template

register = template.Library()

@register.filter
def severity_to_css_class(severity_es):
    """
    Mapea la severidad en español a la clase CSS correspondiente en inglés.
    """
    mapping = {
        'critica': 'critical',
        'alta': 'high',
        'media': 'medium',
        'baja': 'low',
        'desconocida': 'none',
        # Asegurarse de que cualquier otro valor se mapee a 'none' por defecto
        'ninguna': 'none',
    }
    return mapping.get(severity_es.lower(), 'none') 