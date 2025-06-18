from vuln_manager.models.activo.activo import Activo
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.models.alerta.alerta import Alerta
from django.utils import timezone
from vuln_manager.services.correlation.keyword_correlator import KeywordCorrelator

SEVERIDAD_ORDEN = {
    'critica': 4,
    'alta': 3,
    'media': 2,
    'baja': 1,
    'no establecida': 0,
}

class CVEAssetCorrelator(KeywordCorrelator):
    """
    Correlador de CVEs con activos usando palabras clave.
    Mantiene compatibilidad con el código existente mientras usa la nueva arquitectura.
    """
    
    def __init__(self, severidad_minima='critica'):
        super().__init__(severidad_minima=severidad_minima)
    
    def correlacionar(self):
        """
        Método de compatibilidad con el código existente.
        Ejecuta la correlación y retorna el resultado.
        """
        result = self.correlate()
        return result

    def correlate(self):
        """
        Ejecuta la correlación entre CVEs y activos.
        """
        activos = Activo.objects.all()
        cves = Vulnerabilidad.objects.all()
        for activo in activos:
            palabras = [p.strip().lower() for p in activo.palabras_clave.split(',') if p.strip()]
            for cve in cves:
                desc = (cve.descripcion_en or '').lower()
                if any(palabra in desc for palabra in palabras):
                    # Comprobar duplicidad de relación
                    relacion, creada = ActivoVulnerabilidad.objects.get_or_create(
                        activo=activo,
                        vulnerabilidad=cve,
                        defaults={
                            'fecha_deteccion': timezone.now().date(),
                            'estado': 'PENDIENTE',
                            'notas': ''
                        }
                    )
                    # Comprobar severidad para alerta
                    sev_cve = (cve.severidad or '').lower().replace('á', 'a')
                    if SEVERIDAD_ORDEN.get(sev_cve, 0) >= SEVERIDAD_ORDEN.get(self.severidad_minima, 0):
                        # Comprobar duplicidad de alerta
                        Alerta.objects.get_or_create(
                            activo=activo,
                            vulnerabilidad=cve,
                            defaults={
                                'estado': 'nueva',
                                'notas': ''
                            }
                        ) 