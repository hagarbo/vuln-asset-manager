from django.db import models
from vuln_manager.models.activo.activo import Activo

class Vulnerabilidad(models.Model):
    SEVERIDAD_CHOICES = [
        ('critica', 'Crítica'),
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('no establecida', 'No Establecida'),
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
    
    # Datos de CVSS en formato dinámico
    cvss_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Datos CVSS",
        help_text="Datos de CVSS en formato original de la API"
    )
    
    # Campos derivados para uso común
    cvss_score = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name="Score CVSS"
    )
    cvss_severidad = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Severidad CVSS"
    )
    
    # Referencias
    referencias = models.JSONField(default=list, blank=True, verbose_name="URLs de Referencia")
    
    activos = models.ManyToManyField(Activo, through='vuln_manager.ActivoVulnerabilidad', related_name='vulnerabilidades_asociadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cve_id

    class Meta:
        verbose_name = 'Vulnerabilidad'
        verbose_name_plural = 'Vulnerabilidades' 