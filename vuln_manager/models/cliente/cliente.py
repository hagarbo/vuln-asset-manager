from django.db import models
from vuln_manager.models.auth.usuario import Usuario

class Cliente(models.Model):
    """
    Modelo que representa a un cliente en el sistema.
    """
    nombre = models.CharField(max_length=100)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente')
    analistas = models.ManyToManyField(Usuario, related_name='clientes_asignados', limit_choices_to={'rol': 'analista'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre'] 