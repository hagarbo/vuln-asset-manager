from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .tipo_tarea import TipoTarea

class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('pausada', 'Pausada'),
    ]

    tipo = models.ForeignKey(
        TipoTarea,
        on_delete=models.PROTECT,
        help_text="Tipo de tarea a ejecutar"
    )
    programacion = models.CharField(
        max_length=100,
        help_text="Expresión cron (ej: '0 0 * * *' para diario a medianoche)",
        validators=[RegexValidator(
            regex=r'^(\*|[0-9]{1,2}|\*\/[0-9]{1,2})(\s+(\*|[0-9]{1,2}|\*\/[0-9]{1,2})){4}$',
            message='Formato de expresión cron inválido'
        )]
    )
    parametros = models.JSONField(
        default=dict,
        help_text="Valores de los parámetros específicos de la tarea"
    )
    ultima_ejecucion = models.DateTimeField(null=True, blank=True)
    proxima_ejecucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada', help_text='Estado general de la tarea: programada o pausada')
    
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
        if self.tipo and self.tipo.codigo == 'cve_collector':
            try:
                dias_atras = int(self.parametros.get('dias_atras', 1))
                if dias_atras > 30:
                    raise ValidationError('No se pueden buscar CVEs de más de 30 días atrás')
                if dias_atras < 1:
                    raise ValidationError('El número de días debe ser mayor que 0')
            except (ValueError, TypeError):
                raise ValidationError('El valor de días atrás debe ser un número entero válido')
            
            if not self.programacion:
                raise ValidationError('La programación es requerida para tareas de CVE')

    def __str__(self):
        return f"{self.tipo.nombre} - {self.programacion}"

    class Meta:
        verbose_name = 'Tarea Programada'
        verbose_name_plural = 'Tareas Programadas'
        ordering = ['-created_at'] 