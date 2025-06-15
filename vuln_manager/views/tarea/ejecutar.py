from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.services.task.task_executor import TaskExecutor

def ejecutar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    executor = TaskExecutor()
    try:
        executor.execute_task(tarea)
        messages.success(request, 'Tarea ejecutada correctamente.')
    except Exception as e:
        messages.error(request, f'Error al ejecutar la tarea: {str(e)}')
    return redirect('vuln_manager:tarea_detail', pk=pk) 