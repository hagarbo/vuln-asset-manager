from django.db import models
from django.utils import timezone

class ActivoVulnerabilidad(models.Model):
    activo = models.ForeignKey('vuln_manager.Activo', on_delete=models.CASCADE, related_name='relaciones_vulnerabilidad')
    vulnerabilidad = models.ForeignKey('vuln_manager.Vulnerabilidad', on_delete=models.CASCADE, related_name='activo_vulnerabilidad_set')
    fecha_deteccion = models.DateField()
    fecha_resolucion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En Progreso'),
        ('RESUELTO', 'Resuelto'),
        ('FALSO_POSITIVO', 'Falso Positivo')
    ])
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('activo', 'vulnerabilidad')
        verbose_name = 'Vulnerabilidad de Activo'
        verbose_name_plural = 'Vulnerabilidades de Activos'

    def __str__(self):
        return f"{self.activo} - {self.vulnerabilidad}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs) 