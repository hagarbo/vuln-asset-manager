from vuln_manager.repository.base_repository import BaseRepository
from vuln_manager.models.tarea.ejecucion_tarea import EjecucionTarea

class EjecucionTareaRepository(BaseRepository):
    """
    Repositorio para la entidad EjecucionTarea.
    Maneja todas las operaciones de base de datos relacionadas con ejecuciones de tareas.
    """
    def __init__(self):
        super().__init__(EjecucionTarea)

    def create_ejecucion(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update_ejecucion(self, ejecucion_id, **kwargs):
        ejecucion = self.get_by_id(ejecucion_id)
        if ejecucion:
            for key, value in kwargs.items():
                setattr(ejecucion, key, value)
            ejecucion.save()
        return ejecucion

    def get_by_tarea(self, tarea):
        return self.model.objects.filter(tarea=tarea)

    def get_ultima_ejecucion_exitosa(self, tipo_codigo):
        """
        Devuelve la última ejecución exitosa (completada) de una tarea de un tipo dado.
        :param tipo_codigo: Código del tipo de tarea (str)
        :return: EjecucionTarea o None
        """
        return self.model.objects.filter(
            tarea__tipo__codigo=tipo_codigo,
            estado='completada'
        ).order_by('-fecha_fin').first() 