from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class CorrelationResult:
    """
    Resultado de una correlación entre activos y vulnerabilidades.
    """
    def __init__(self):
        self.correlaciones_creadas: int = 0
        self.correlaciones_existentes: int = 0
        self.alertas_generadas: int = 0
        self.alertas_existentes: int = 0
        self.activos_procesados: int = 0
        self.vulnerabilidades_procesadas: int = 0
        self.errores: List[str] = []

class CorrelatorBase(ABC):
    """
    Interfaz base para correladores de activos y vulnerabilidades.
    Define los métodos que deben implementar todas las estrategias de correlación.
    """
    
    @abstractmethod
    def correlate(self, **kwargs) -> CorrelationResult:
        """
        Ejecuta la correlación entre activos y vulnerabilidades.
        
        Args:
            **kwargs: Parámetros específicos de la implementación
            
        Returns:
            CorrelationResult: Resultado de la correlación con métricas
        """
        pass
    
    @abstractmethod
    def get_supported_parameters(self) -> Dict:
        """
        Retorna los parámetros soportados por este correlador.
        
        Returns:
            Dict: Diccionario con parámetros y sus configuraciones
        """
        pass 