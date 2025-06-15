from django.db import models

class EjecucionTarea(models.Model):
    ESTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('error', 'Error'),
        ('cancelado', 'Cancelado'),
    ]

    tarea = models.ForeignKey(
        'Tarea',
        on_delete=models.CASCADE,
        related_name='ejecuciones'
    )
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    resultado = models.TextField(blank=True)
    error = models.TextField(blank=True)
    
    # Campos específicos para ejecuciones de tareas CVE
    cves_procesadas = models.PositiveIntegerField(default=0)
    cves_nuevas = models.PositiveIntegerField(default=0)
    cves_actualizadas = models.PositiveIntegerField(default=0)
    cves_rechazadas = models.PositiveIntegerField(default=0)
    
    ejecutada_por = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ejecuciones_tarea'
    )

    def __str__(self):
        return f"Ejecución de {self.tarea.nombre} - {self.fecha_inicio}"

    class Meta:
        verbose_name = 'Ejecución de Tarea'
        verbose_name_plural = 'Ejecuciones de Tareas'
        ordering = ['-fecha_inicio'] 