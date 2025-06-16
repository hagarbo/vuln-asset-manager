from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """
    Modelo de Usuario personalizado que extiende AbstractUser.
    Implementa un sistema de roles jerárquico:
    - Admin: Gestiona toda la aplicación, crea cuentas y asigna clientes a analistas
    - Analista: Gestiona activos de sus clientes asignados
    - Cliente: Visualiza sus propios activos
    """
    ROLES = (
        ('admin', 'Administrador'),
        ('analista', 'Analista'),
        ('cliente', 'Cliente'),
    )
    
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='cliente',
        verbose_name='Rol'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    empresa = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Empresa'
    )
    cargo = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Cargo'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

    @property
    def es_admin(self):
        return self.rol == 'admin'

    @property
    def es_analista(self):
        return self.rol == 'analista'

    @property
    def es_cliente(self):
        return self.rol == 'cliente' 