from django import template
from django.utils.safestring import mark_safe
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo_vulnerabilidad import ActivoVulnerabilidad

register = template.Library()

@register.filter
def severity_to_css_class(severity):
    """
    Convierte la severidad de una vulnerabilidad en una clase CSS de Bootstrap personalizada.
    """
    severity_classes = {
        'critica': 'bg-severity-critical',
        'alta': 'bg-severity-high',
        'media': 'bg-severity-medium',
        'baja': 'bg-severity-low',
        'no establecida': 'bg-severity-none',
    }
    if not severity:
        return severity
    return severity_classes.get(severity.lower(), 'bg-severity-none')

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

@register.filter
def get_cvss(cvss_data, version):
    """
    Permite acceder a una versión específica de CVSS en un diccionario.
    Uso: {{ vulnerabilidad.cvss_data|get_cvss:'3.1' }}
    """
    if not isinstance(cvss_data, dict):
        return {}
    return cvss_data.get(version, {}) 