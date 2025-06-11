from django.db import models
from .activo import Activo
from .vulnerabilidad import Vulnerabilidad

class ActivoVulnerabilidad(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    vulnerabilidad = models.ForeignKey(Vulnerabilidad, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=Vulnerabilidad.ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True)
    fecha_deteccion = models.DateField(auto_now_add=True)
    fecha_resolucion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vulnerabilidad de Activo'
        verbose_name_plural = 'Vulnerabilidades de Activos'
        unique_together = ['activo', 'vulnerabilidad'] 