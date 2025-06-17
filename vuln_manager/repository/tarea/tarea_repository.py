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

    def get_all(self):
        """Obtiene todas las tareas ordenadas por fecha de creación."""
        return self.model.objects.select_related('tipo').order_by('-created_at')

    def get_by_estado(self, estado):
        """Obtiene las tareas en un estado específico."""
        return self.model.objects.filter(estado=estado)

    def get_by_tipo(self, tipo_tarea):
        """Obtiene las tareas de un tipo específico."""
        return self.model.objects.filter(tipo=tipo_tarea)

    def get_by_creador(self, usuario):
        """Obtiene las tareas creadas por un usuario específico."""
        return self.model.objects.filter(creada_por=usuario)

    def get_by_fecha_creacion(self, fecha_inicio, fecha_fin):
        """Obtiene las tareas creadas en un rango de fechas."""
        return self.model.objects.filter(
            created_at__range=(fecha_inicio, fecha_fin)
        )

    def get_sin_ejecutar(self, dias):
        """Obtiene las tareas que no se han ejecutado en los últimos X días."""
        fecha_limite = timezone.now() - timedelta(days=dias)
        return self.model.objects.filter(
            ultima_ejecucion__lt=fecha_limite,
            estado='programada'
        )

    def update_ultima_ejecucion(self, tarea_id):
        """Actualiza la última ejecución de una tarea y calcula la próxima ejecución."""
        tarea = self.get_by_id(tarea_id)
        if tarea:
            ahora = timezone.now()
            self.update(tarea_id, {
                'ultima_ejecucion': ahora,
                'proxima_ejecucion': ahora + timedelta(days=1)
            })
        return tarea

    def count_programadas(self):
        """Cuenta el número de tareas programadas."""
        return self.model.objects.filter(estado='programada').count()

    def get_latest(self, limit=5):
        """Obtiene las últimas tareas ordenadas por fecha de creación."""
        return self.model.objects.select_related('tipo').order_by('-created_at')[:limit] 