from django.db import models
from vuln_manager.models.cliente.cliente import Cliente

class Activo(models.Model):
    TIPO_CHOICES = [
        ('hardware', 'Hardware'),
        ('software', 'Software'),
        ('servicio', 'Servicio'),
        ('red', 'Dispositivo de Red'),
        ('otro', 'Otro'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='activos')
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    palabras_clave = models.TextField(help_text="Palabras clave separadas por comas para búsqueda de CVEs")
    ip = models.GenericIPAddressField(null=True, blank=True)
    puerto = models.IntegerField(null=True, blank=True)
    version = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos' 