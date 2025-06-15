from django.utils import timezone
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.repository.tarea.ejecucion_tarea_repository import EjecucionTareaRepository
from vuln_manager.repository.tarea.tarea_repository import TareaRepository
from vuln_manager.services.cve.nist_cve_collector import NISTCVECollector
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

class TaskExecutor:
    """
    Servicio para ejecutar tareas programadas.
    Maneja la ejecución de diferentes tipos de tareas y el registro de sus ejecuciones.
    """
    
    def __init__(self):
        self.ejecucion_repo = EjecucionTareaRepository()
        self.tarea_repo = TareaRepository()

    def execute_task(self, tarea: Tarea):
        """
        Ejecuta una tarea específica y registra su ejecución.
        Args:
            tarea: Instancia de Tarea a ejecutar
        Returns:
            EjecucionTarea: Registro de la ejecución
        """
        # Crear registro de ejecución usando el repositorio
        ejecucion = self.ejecucion_repo.create_ejecucion(
            tarea=tarea,
            estado='ejecutando',
            fecha_inicio=timezone.now(),
            ejecutada_por=tarea.creada_por
        )
        # La tarea permanece en estado 'programada' salvo que se pause manualmente
        try:
            if tarea.tipo.codigo == 'cve_collector':
                self._ejecutar_cve_collector(tarea, ejecucion)
            else:
                raise ValueError(f'Tipo de tarea no soportado: {tarea.tipo.codigo}')
            # Actualizar ejecución como completada usando el repositorio
            self.ejecucion_repo.update_ejecucion(
                ejecucion.id,
                estado='completada',
                fecha_fin=timezone.now()
            )
            # Actualizar última y próxima ejecución usando el repositorio
            self.tarea_repo.actualizar_ultima_ejecucion(tarea.id)
            return ejecucion
        except Exception as e:
            # Registrar error en la ejecución usando el repositorio
            self.ejecucion_repo.update_ejecucion(
                ejecucion.id,
                estado='error',
                fecha_fin=timezone.now(),
                error=str(e)
            )
            # Si se desea pausar la tarea tras error grave, aquí se podría poner:
            # tarea.estado = 'pausada'
            tarea.save()
            raise

    def _ejecutar_cve_collector(self, tarea, ejecucion):
        dias_atras = int(tarea.parametros.get('dias_atras', 1))
        collector = NISTCVECollector(days_back=dias_atras)
        cves = collector.fetch_cves()
        repo = VulnerabilidadRepository()
        nuevas, actualizadas = 0, 0
        for dto in cves:
            _, created = repo.create_or_update_from_dto(dto)
            if created:
                nuevas += 1
            else:
                actualizadas += 1
        # Actualizar los contadores en la ejecución
        self.ejecucion_repo.update_ejecucion(
            ejecucion.id,
            cves_procesadas=len(cves),
            cves_nuevas=nuevas,
            cves_actualizadas=actualizadas
        ) 