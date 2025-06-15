### [Fecha actual]

- Se eliminó el campo `activa` del modelo `Tarea`.
- El formulario de tareas ahora utiliza un checkbox que mapea a `estado` ('programada' o 'pausada').
- Se revisaron y adaptaron formularios, vistas y lógica asociada para reflejar este cambio.
- Se verificó que no quedan referencias a `activa` en el código, tests ni plantillas.

### 2024-06-15

- Añadida paginación (5 por página) al historial de ejecuciones en el detalle de la tarea (`TareaDetailView` y plantilla `tarea/detail.html`).
- Añadido botón de acción para ejecutar la tarea manualmente desde el detalle, con nueva vista `ejecutar_tarea` y URL asociada.
- Corregida la importación de la función `ejecutar_tarea` en `views/__init__.py` para evitar errores de importación.
- Se recomienda revisar la interfaz para comprobar la correcta visualización de la paginación y el funcionamiento del botón de ejecución manual.

- Eliminado `vuln_manager/celery.py` porque no se utiliza en la arquitectura actual de tareas programadas (se usa management commands en vez de Celery). 