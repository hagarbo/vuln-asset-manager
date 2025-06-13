from django.db import models
from vuln_manager.models.activo.activo import Activo

class Vulnerabilidad(models.Model):
    SEVERIDAD_CHOICES = [
        ('critica', 'Crítica'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
        ('falso_positivo', 'Falso Positivo'),
    ]

    STATUS_CHOICES = [
        ('published', 'Publicado'),
        ('rejected', 'Rechazado'),
        ('draft', 'Borrador'),
    ]

    cve_id = models.CharField(max_length=20, unique=True)
    descripcion_en = models.TextField(verbose_name="Descripción (Inglés)")
    descripcion_es = models.TextField(verbose_name="Descripción (Español)")
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    fecha_publicacion = models.DateField()
    fecha_modificacion = models.DateField()
    fecha_deteccion = models.DateField(auto_now_add=True)
    
    # Campos CVSS v2
    cvss2_score = models.FloatField(null=True, blank=True, verbose_name="Score CVSS v2")
    cvss2_severidad = models.CharField(max_length=20, null=True, blank=True, verbose_name="Severidad CVSS v2")
    cvss2_vector = models.CharField(max_length=100, null=True, blank=True, verbose_name="Vector CVSS v2")
    
    # Campos CVSS v3
    cvss3_score = models.FloatField(null=True, blank=True, verbose_name="Score CVSS v3")
    cvss3_severidad = models.CharField(
        max_length=20, 
        null=True, 
        blank=True, 
        verbose_name="Severidad CVSS v3",
        choices=SEVERIDAD_CHOICES
    )
    cvss3_vector = models.CharField(max_length=100, null=True, blank=True, verbose_name="Vector CVSS v3")
    
    # Referencias
    referencias = models.JSONField(default=list, blank=True, verbose_name="URLs de Referencia")
    
    activos = models.ManyToManyField(Activo, through='ActivoVulnerabilidad', related_name='vulnerabilidades_asociadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cve_id

    class Meta:
        verbose_name = 'Vulnerabilidad'
        verbose_name_plural = 'Vulnerabilidades' 