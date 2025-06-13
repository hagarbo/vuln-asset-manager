from django.db import models
from django.core.exceptions import ValidationError

class AnalistaCliente(models.Model):
    """
    Modelo para gestionar la relación entre analistas y clientes.
    """
    analista = models.ForeignKey(
        'vuln_manager.Usuario',
        on_delete=models.CASCADE,
        related_name='relaciones_analista',
        verbose_name='Analista'
    )
    cliente = models.ForeignKey(
        'vuln_manager.Usuario',
        on_delete=models.CASCADE,
        related_name='relaciones_cliente',
        verbose_name='Cliente'
    )
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de asignación'
    )

    class Meta:
        verbose_name = 'Relación Analista-Cliente'
        verbose_name_plural = 'Relaciones Analista-Cliente'
        unique_together = ['analista', 'cliente']
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.analista.username} -> {self.cliente.username}"

    def clean(self):
        from vuln_manager.models import Usuario
        if not self.analista.es_analista():
            raise ValidationError({'analista': 'El usuario debe ser un analista'})
        if not self.cliente.es_cliente():
            raise ValidationError({'cliente': 'El usuario debe ser un cliente'})
        if self.analista == self.cliente:
            raise ValidationError('Un usuario no puede ser asignado a sí mismo')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs) 