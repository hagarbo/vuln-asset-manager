from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class VulnerabilidadDTO:
    cve_id: str
    descripcion_en: str
    descripcion_es: str
    severidad: str
    status: str
    fecha_publicacion: str  # ISO format
    fecha_modificacion: str  # ISO format
    # Datos de CVSS en formato dinámico
    cvss_data: Dict[str, Any]
    referencias: List[str]
    cvss_score: float = None  # Score de la versión más reciente de CVSS
    cvss_severidad: str = None  # Severidad de la versión más reciente de CVSS 