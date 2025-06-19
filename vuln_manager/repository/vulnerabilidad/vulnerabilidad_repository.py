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

    def count(self):
        """Cuenta el número total de vulnerabilidades."""
        return self.model.objects.count()

    def get_updated_since(self, fecha):
        """
        Devuelve las vulnerabilidades creadas o modificadas desde la fecha dada.
        :param fecha: datetime o string en formato ISO/fecha
        :return: QuerySet de Vulnerabilidad
        """
        if not fecha:
            return self.model.objects.none()
        if isinstance(fecha, str):
            try:
                fecha = datetime.fromisoformat(fecha)
            except Exception:
                return self.model.objects.none()
        return self.model.objects.filter(
            fecha_modificacion__gte=fecha
        )

    def get_filtered(self, severidad=None, cve_id=None, descripcion_en=None, fecha_inicio=None, fecha_fin=None):
        """
        Devuelve un queryset filtrado por severidad, cve_id (parcial), descripcion_en (parcial, insensible a mayúsculas),
        y rango de fecha_publicacion (inicio y fin, inclusivo).
        """
        qs = self.model.objects.all()
        if severidad:
            qs = qs.filter(severidad=severidad)
        if cve_id:
            qs = qs.filter(cve_id__icontains=cve_id)
        if descripcion_en:
            qs = qs.filter(descripcion_en__icontains=descripcion_en)
        if fecha_inicio:
            qs = qs.filter(fecha_publicacion__gte=fecha_inicio)
        if fecha_fin:
            qs = qs.filter(fecha_publicacion__lte=fecha_fin)
        return qs 