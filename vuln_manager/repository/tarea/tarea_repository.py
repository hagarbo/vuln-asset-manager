from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea
from django.utils import timezone
from datetime import timedelta

class TareaRepository(BaseRepository):
    """
    Repositorio para la entidad Tarea.
    Maneja todas las operaciones de base de datos relacionadas con tareas programadas.
    """
    def __init__(self):
        super().__init__(Tarea)

    def get_tareas_activas(self):
        """Obtiene todas las tareas programadas."""
        return self.model.objects.filter(estado='programada')

    def get_tareas_pendientes(self):
        """Obtiene las tareas que están programadas."""
        return self.model.objects.filter(estado='programada')

    def get_tareas_por_tipo(self, tipo_tarea):
        """Obtiene todas las tareas de un tipo específico."""
        return self.model.objects.filter(tipo=tipo_tarea)

    def get_tareas_por_estado(self, estado):
        """Obtiene todas las tareas en un estado específico."""
        return self.model.objects.filter(estado=estado)

    def get_tareas_por_creador(self, usuario):
        """Obtiene todas las tareas creadas por un usuario específico."""
        return self.model.objects.filter(creada_por=usuario)

    def get_tareas_por_fecha_creacion(self, fecha_inicio, fecha_fin):
        """Obtiene las tareas creadas en un rango de fechas."""
        return self.model.objects.filter(
            created_at__range=(fecha_inicio, fecha_fin)
        )

    def get_tareas_por_ultima_ejecucion(self, dias):
        """Obtiene las tareas que no se han ejecutado en los últimos X días."""
        fecha_limite = timezone.now() - timedelta(days=dias)
        return self.model.objects.filter(
            ultima_ejecucion__lt=fecha_limite,
            estado='programada'
        )

    def actualizar_estado(self, tarea_id, estado):
        """Actualiza el estado de una tarea."""
        tarea = self.get_by_id(tarea_id)
        if tarea:
            tarea.estado = estado
            tarea.save()
        return tarea

    def actualizar_ultima_ejecucion(self, tarea_id):
        """Actualiza la última ejecución de una tarea y calcula la próxima ejecución."""
        tarea = self.get_by_id(tarea_id)
        if tarea:
            ahora = timezone.now()
            tarea.ultima_ejecucion = ahora
            # Calcular la próxima ejecución para el día siguiente a la misma hora
            tarea.proxima_ejecucion = ahora + timedelta(days=1)
            tarea.save()
        return tarea

    def get_tareas_por_codigo_tipo(self, codigo_tipo):
        """Obtiene todas las tareas de un tipo específico por su código."""
        return self.model.objects.filter(tipo__codigo=codigo_tipo)

    def get_queryset(self):
        return self.model.objects.select_related('tipo').all().order_by('-created_at') 