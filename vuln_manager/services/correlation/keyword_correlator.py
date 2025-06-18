from vuln_manager.services.correlation.correlator_base import CorrelatorBase, CorrelationResult
from vuln_manager.repository.activo.activo_repository import ActivoRepository
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository
from vuln_manager.repository.activo_vulnerabilidad.activo_vulnerabilidad_repository import ActivoVulnerabilidadRepository
from vuln_manager.repository.alerta.alerta_repository import AlertaRepository
from django.utils import timezone
from typing import Dict

SEVERIDAD_ORDEN = {
    'critica': 4,
    'alta': 3,
    'media': 2,
    'baja': 1,
    'no establecida': 0,
}

class KeywordCorrelator(CorrelatorBase):
    """
    Correlador basado en palabras clave.
    Correlaciona activos con vulnerabilidades comparando palabras clave de los activos
    con las descripciones de las vulnerabilidades.
    """
    
    def __init__(self, severidad_minima='critica', cves=None):
        self.severidad_minima = severidad_minima.lower()
        self.cves = cves
        self.activo_repo = ActivoRepository()
        self.vulnerabilidad_repo = VulnerabilidadRepository()
        self.activo_vulnerabilidad_repo = ActivoVulnerabilidadRepository()
        self.alerta_repo = AlertaRepository()

    def correlate(self, **kwargs) -> CorrelationResult:
        """
        Ejecuta la correlación basada en palabras clave.
        
        Args:
            **kwargs: Parámetros adicionales (no utilizados en esta implementación)
            
        Returns:
            CorrelationResult: Resultado con métricas de la correlación
        """
        result = CorrelationResult()
        
        try:
            activos = self.activo_repo.get_all()
            cves = self.cves if self.cves and len(self.cves) > 0 else self.vulnerabilidad_repo.get_all()
            
            result.activos_procesados = activos.count()
            result.vulnerabilidades_procesadas = len(cves) if isinstance(cves, list) else cves.count()
            
            for activo in activos:
                palabras = [p.strip().lower() for p in activo.palabras_clave.split(',') if p.strip()]
                
                for cve in cves:
                    desc = (cve.descripcion_en or '').lower()
                    
                    if any(palabra in desc for palabra in palabras):
                        # Crear o actualizar relación ActivoVulnerabilidad
                        relacion_existente = self.activo_vulnerabilidad_repo.get_by_activo_y_vulnerabilidad(activo.id, cve.id)
                        if relacion_existente:
                            result.correlaciones_existentes += 1
                        else:
                            self.activo_vulnerabilidad_repo.create(
                                activo=activo,
                                vulnerabilidad=cve,
                                fecha_deteccion=timezone.now().date(),
                                estado='PENDIENTE',
                                notas=''
                            )
                            result.correlaciones_creadas += 1
                        
                        # Comprobar severidad para generar alerta
                        sev_cve = (cve.severidad or '').lower().replace('á', 'a')
                        if SEVERIDAD_ORDEN.get(sev_cve, 0) >= SEVERIDAD_ORDEN.get(self.severidad_minima, 0):
                            # Crear o verificar alerta
                            alerta_existente = self.alerta_repo.get_by_activo_y_vulnerabilidad(activo.id, cve.id)
                            if alerta_existente:
                                result.alertas_existentes += 1
                            else:
                                self.alerta_repo.create(
                                    activo=activo,
                                    vulnerabilidad=cve,
                                    estado='nueva',
                                    notas=''
                                )
                                result.alertas_generadas += 1
                                
        except Exception as e:
            result.errores.append(f"Error en correlación: {str(e)}")
            
        return result

    def get_supported_parameters(self) -> Dict:
        """
        Retorna los parámetros soportados por este correlador.
        
        Returns:
            Dict: Configuración de parámetros
        """
        return {
            "severidad_minima": {
                "tipo": "choice",
                "opciones": ["critica", "alta", "media", "baja"],
                "default": "critica",
                "descripcion": "Severidad mínima para generar alertas"
            }
        } 