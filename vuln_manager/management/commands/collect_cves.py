from django.core.management.base import BaseCommand
from vuln_manager.services.task.task_executor import TaskExecutor
from vuln_manager.repository.tarea.tarea_repository import TareaRepository

class Command(BaseCommand):
    help = 'Recolecta CVEs desde NIST y las almacena en la base de datos usando el flujo service-repository.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tarea_id',
            type=int,
            help='ID de la tarea programada que ejecuta este comando'
        )

    def handle(self, *args, **options):
        tarea_id = options.get('tarea_id')
        if not tarea_id:
            self.stdout.write(self.style.ERROR('Debes proporcionar el ID de la tarea a ejecutar.'))
            return

        tarea_repo = TareaRepository()
        tarea = tarea_repo.get_by_id(tarea_id)
        if not tarea:
            self.stdout.write(self.style.ERROR(f'No se encontró la tarea con ID {tarea_id}'))
            return

        executor = TaskExecutor()
        try:
            ejecucion = executor.execute_task(tarea)
            self.stdout.write(self.style.SUCCESS(
                f'Tarea ejecutada correctamente. Ejecución ID: {ejecucion.id if ejecucion else "-"}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al ejecutar la tarea: {str(e)}'))