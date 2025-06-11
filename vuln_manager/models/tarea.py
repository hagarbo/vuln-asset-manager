from django.db import models
from django.contrib.auth.models import User

class Tarea(models.Model):
    TIPO_CHOICES = [
        ('cve', 'Actualización de CVEs'),
        ('scan', 'Escaneo de Activos'),
    ]

    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('ejecutando', 'Ejecutando'),
        ('completada', 'Completada'),
        ('error', 'Error'),
        ('cancelada', 'Cancelada'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    programacion = models.CharField(max_length=100, help_text="Expresión cron (ej: '0 0 * * *' para diario a medianoche)")
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    proxima_ejecucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    activa = models.BooleanField(default=True)
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tareas_creadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = 'Tarea Programada'
        verbose_name_plural = 'Tareas Programadas'
        ordering = ['-created_at']

class EjecucionTarea(models.Model):
    ESTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('error', 'Error'),
        ('cancelado', 'Cancelado'),
    ]

    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='ejecuciones')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    resultado = models.TextField(blank=True)
    error = models.TextField(blank=True)
    ejecutada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ejecución de {self.tarea.nombre} - {self.fecha_inicio}"

    class Meta:
        verbose_name = 'Ejecución de Tarea'
        verbose_name_plural = 'Ejecuciones de Tareas'
        ordering = ['-fecha_inicio'] 