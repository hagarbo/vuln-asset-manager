from django import template
from django.utils.safestring import mark_safe
from vuln_manager.models import ActivoVulnerabilidad, Vulnerabilidad

register = template.Library()

@register.filter
def severity_to_css_class(severity):
    """
    Convierte la severidad de una vulnerabilidad en una clase CSS de Bootstrap.
    """
    severity_classes = {
        'critica': 'severity-critical',
        'alta': 'severity-high',
        'media': 'severity-medium',
        'baja': 'severity-low',
        'ninguna': 'severity-none',
    }
    return severity_classes.get(severity.lower(), 'bg-secondary')

@register.filter
def status_to_css_class(estado):
    """
    Convierte el estado de una vulnerabilidad en una clase CSS de Bootstrap.
    Maneja tanto los estados de ActivoVulnerabilidad como los estados de Vulnerabilidad.
    """
    estado_classes = {
        # Estados de ActivoVulnerabilidad
        'pendiente': 'warning',
        'en_proceso': 'info',
        'resuelta': 'success',
        'falso_positivo': 'secondary',
        
        # Estados de Vulnerabilidad
        'published': 'success',
        'draft': 'warning',
        'rejected': 'danger',
    }
    return estado_classes.get(str(estado).lower(), 'secondary') 