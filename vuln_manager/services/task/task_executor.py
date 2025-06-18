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
            elif tarea.tipo.codigo == 'cve_asset_correlation':
                self._ejecutar_cve_asset_correlation(tarea, ejecucion)
            else:
                raise ValueError(f'Tipo de tarea no soportado: {tarea.tipo.codigo}')
            # Actualizar ejecución como completada usando el repositorio
            self.ejecucion_repo.update_ejecucion(
                ejecucion.id,
                estado='completada',
                fecha_fin=timezone.now()
            )
            # Actualizar última ejecución
            self.tarea_repo.update_ultima_ejecucion(tarea.id)
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

    def _ejecutar_cve_asset_correlation(self, tarea, ejecucion):
        """
        Ejecuta la correlación entre CVEs y activos usando el servicio KeywordCorrelator.
        Solo procesa las CVEs nuevas/actualizadas desde la última ejecución del colector.
        """
        from vuln_manager.services.correlation import KeywordCorrelator
        from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository
        from vuln_manager.repository.tarea.ejecucion_tarea_repository import EjecucionTareaRepository

        # 1. Obtener la fecha de la última ejecución exitosa del colector
        ejecucion_repo = EjecucionTareaRepository()
        ultima_ejecucion_colector = ejecucion_repo.get_ultima_ejecucion_exitosa('cve_collector')
        fecha_corte = ultima_ejecucion_colector.fecha_fin if ultima_ejecucion_colector else None

        # 2. Obtener solo las CVEs nuevas/actualizadas
        cves = []
        if fecha_corte:
            cves = list(VulnerabilidadRepository().get_updated_since(fecha_corte))

        # 3. Pasar solo esas CVEs al correlador
        severidad_minima = tarea.parametros.get('severidad_minima', 'critica')
        correlator = KeywordCorrelator(severidad_minima=severidad_minima, cves=cves)
        result = correlator.correlate()

        # 4. Actualizar contadores en la ejecución
        self.ejecucion_repo.update_ejecucion(
            ejecucion.id,
            cves_procesadas=result.vulnerabilidades_procesadas,
            cves_nuevas=result.correlaciones_creadas,
            cves_actualizadas=result.alertas_generadas,
        ) 