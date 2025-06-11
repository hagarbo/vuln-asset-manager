from django.db import models
from django.contrib.auth.models import User
from .vulnerabilidad import Vulnerabilidad
from .activo import Activo

class Alerta(models.Model):
    ESTADO_CHOICES = [
        ('nueva', 'Nueva'),
        ('vista', 'Vista'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
        ('ignorada', 'Ignorada'),
    ]

    vulnerabilidad = models.ForeignKey(Vulnerabilidad, on_delete=models.CASCADE)
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    analista_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nueva')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    resuelta_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alertas_resueltas'
    )

    def __str__(self):
        return f"Alerta {self.vulnerabilidad.cve_id} - {self.activo.nombre}"

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_creacion'] 