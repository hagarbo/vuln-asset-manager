from django.db import models

class TipoTarea(models.Model):
    codigo = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único para identificar el tipo de tarea"
    )
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre descriptivo del tipo de tarea"
    )
    descripcion = models.TextField(
        help_text="Descripción detallada del tipo de tarea"
    )
    parametros = models.JSONField(
        default=dict,
        help_text="Configuración de parámetros específicos para este tipo de tarea"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Indica si este tipo de tarea está disponible para su uso"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de Tarea'
        verbose_name_plural = 'Tipos de Tarea'
        ordering = ['nombre'] 