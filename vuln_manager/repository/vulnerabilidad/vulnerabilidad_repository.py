from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from datetime import datetime

class VulnerabilidadRepository(BaseRepository):
    """
    Repositorio para la entidad Vulnerabilidad.
    Maneja todas las operaciones de base de datos relacionadas con vulnerabilidades.
    """
    def __init__(self):
        super().__init__(Vulnerabilidad)

    def _parse_date(self, value):
        if not value:
            return None
        try:
            # Si ya es YYYY-MM-DD
            if len(value) == 10:
                return value
            # Si es formato ISO completo
            return datetime.fromisoformat(value).date().isoformat()
        except Exception:
            return None

    def _map_severidad(self, valor):
        mapping = {
            'CRITICAL': 'critica',
            'HIGH': 'alta',
            'MEDIUM': 'media',
            'LOW': 'baja',
        }
        return mapping.get(str(valor).strip().upper(), 'no establecida')

    def create_or_update_from_dto(self, dto):
        obj, created = Vulnerabilidad.objects.update_or_create(
            cve_id=dto.cve_id,
            defaults={
                "descripcion_en": dto.descripcion_en,
                "descripcion_es": dto.descripcion_es,
                "severidad": self._map_severidad(dto.severidad),
                "status": dto.status,
                "fecha_publicacion": self._parse_date(dto.fecha_publicacion),
                "fecha_modificacion": self._parse_date(dto.fecha_modificacion),
                "cvss_data": dto.cvss_data,
                "referencias": dto.referencias,
            }
        )
        return obj, created 