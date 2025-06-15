from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Tarea(models.Model):
    TIPO_CHOICES = [
        ('cve', 'Actualización de CVEs'),
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
    programacion = models.CharField(
        max_length=100,
        help_text="Expresión cron (ej: '0 0 * * *' para diario a medianoche)",
        validators=[RegexValidator(
            regex=r'^(\*|[0-9]{1,2}|\*\/[0-9]{1,2})(\s+(\*|[0-9]{1,2}|\*\/[0-9]{1,2})){4}$',
            message='Formato de expresión cron inválido'
        )]
    )
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    proxima_ejecucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    activa = models.BooleanField(default=True)
    
    # Campos específicos para tareas de CVE
    dias_atras = models.PositiveIntegerField(
        default=1,
        help_text='Número de días hacia atrás para buscar CVEs'
    )
    incluir_rechazadas = models.BooleanField(
        default=False,
        help_text='Incluir CVEs rechazadas en la búsqueda'
    )
    
    creada_por = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_creadas'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.tipo == 'cve':
            if self.dias_atras > 30:
                raise ValidationError('No se pueden buscar CVEs de más de 30 días atrás')
            if not self.programacion:
                raise ValidationError('La programación es requerida para tareas de CVE')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tarea Programada'
        verbose_name_plural = 'Tareas Programadas'
        ordering = ['-created_at'] 