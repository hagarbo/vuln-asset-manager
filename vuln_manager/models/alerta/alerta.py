from django.db import models
from django.contrib.auth.models import User
from vuln_manager.models.vulnerabilidad.vulnerabilidad import Vulnerabilidad
from vuln_manager.models.activo.activo import Activo
from django.conf import settings

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
    analista_asignado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertas_asignadas', verbose_name='Analista asignado')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nueva')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    resuelta_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alertas_resueltas',
        verbose_name='Resuelta por'
    )

    def __str__(self):
        return f"Alerta {self.vulnerabilidad.cve_id} - {self.activo.nombre}"

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_creacion'] 