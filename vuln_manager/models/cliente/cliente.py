from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cliente', verbose_name='Usuario')
    analistas = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='clientes', blank=True, verbose_name='Analistas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes' 