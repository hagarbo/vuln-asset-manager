def get_severity_color(cvss_score):
    """
    Retorna el color CSS correspondiente a la severidad basada en el score CVSS.
    
    Args:
        cvss_score (float): Score CVSS de la vulnerabilidad
        
    Returns:
        str: Clase CSS para el color de severidad
    """
    if cvss_score is None:
        return 'severity-none'  # Blanco/Sin color
    
    if cvss_score >= 9.0:
        return 'severity-critical'  # Rojo oscuro/Rojo
    elif cvss_score >= 7.0:
        return 'severity-high'  # Oro/Naranja
    elif cvss_score >= 4.0:
        return 'severity-medium'  # Amarillo
    elif cvss_score >= 0.1:
        return 'severity-low'  # Gris/Azul
    else:
        return 'severity-none'  # Blanco/Sin color

def get_severity_text(cvss_score):
    """
    Retorna el texto de severidad en español basado en el score CVSS.
    
    Args:
        cvss_score (float): Score CVSS de la vulnerabilidad
        
    Returns:
        str: Texto de severidad en español
    """
    if cvss_score is None:
        return 'Desconocida'
    
    if cvss_score >= 9.0:
        return 'Crítica'
    elif cvss_score >= 7.0:
        return 'Alta'
    elif cvss_score >= 4.0:
        return 'Media'
    elif cvss_score >= 0.1:
        return 'Baja'
    else:
        return 'Desconocida' 