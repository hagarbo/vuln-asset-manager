from django.core.management.base import BaseCommand
from django.utils import timezone
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.services.task.task_executor import TaskExecutor
import croniter
from datetime import datetime

class Command(BaseCommand):
    help = 'Ejecuta las tareas programadas que están pendientes de ejecución.'

    def handle(self, *args, **options):
        executor = TaskExecutor()
        now = timezone.now()
        
        # Obtener tareas programadas
        tareas = Tarea.objects.filter(
            estado='programada'
        ).select_related('tipo')
        
        for tarea in tareas:
            try:
                # Verificar si la tarea debe ejecutarse según su programación
                if self._should_execute_task(tarea, now):
                    self.stdout.write(f'Ejecutando tarea: {tarea.tipo.nombre} (ID: {tarea.id})')
                    ejecucion = executor.execute_task(tarea)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Tarea completada: {tarea.tipo.nombre} (ID: {tarea.id})'
                        )
                    )
                else:
                    self.stdout.write(
                        f'Tarea {tarea.tipo.nombre} (ID: {tarea.id}) no programada para ejecución'
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error al ejecutar tarea {tarea.tipo.nombre} (ID: {tarea.id}): {str(e)}'
                    )
                )

    def _should_execute_task(self, tarea: Tarea, now: datetime) -> bool:
        """
        Determina si una tarea debe ejecutarse según su programación.
        
        Args:
            tarea: Instancia de Tarea a verificar
            now: Fecha y hora actual
            
        Returns:
            bool: True si la tarea debe ejecutarse, False en caso contrario
        """
        # Si es la primera ejecución o no tiene última ejecución
        if not tarea.ultima_ejecucion:
            return True
            
        # Crear iterador de cron
        cron = croniter.croniter(tarea.programacion, tarea.ultima_ejecucion)
        
        # Obtener próxima ejecución programada
        next_run = cron.get_next(datetime)
        
        # La tarea debe ejecutarse si la próxima ejecución programada es anterior o igual a ahora
        return next_run <= now 