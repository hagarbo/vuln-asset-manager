from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import PermissionDenied
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
        permissions = [
            # Permisos de administración de usuarios
            ("can_create_users", "Puede crear usuarios"),
            ("can_assign_clients", "Puede asignar clientes a analistas"),
            
            # Permisos de gestión de activos
            ("can_manage_assets", "Puede gestionar activos"),
            ("can_view_assets", "Puede ver activos"),
            
            # Permisos de gestión de vulnerabilidades
            ("can_manage_vulnerabilities", "Puede gestionar vulnerabilidades"),
            ("can_view_vulnerabilities", "Puede ver vulnerabilidades"),
        ]

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

    def get_clientes_asignados(self):
        from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
        return AnalistaCliente.objects.filter(analista=self).values_list('cliente', flat=True)

    def get_analistas_asignados(self):
        if not self.es_cliente:
            return Usuario.objects.none()
        from vuln_manager.models.cliente.analista_cliente import AnalistaCliente
        return Usuario.objects.filter(id__in=AnalistaCliente.objects.filter(cliente=self).values_list('analista_id', flat=True))

    def has_perm(self, perm, obj=None):
        """
        Implementa la lógica de permisos basada en roles.
        """
        # Los superusuarios tienen todos los permisos
        if self.is_superuser:
            return True

        # Permisos específicos por rol
        if self.es_admin:
            return perm in [
                "can_create_users",
                "can_assign_clients",
                "can_manage_assets",
                "can_view_assets",
                "can_manage_vulnerabilities",
                "can_view_vulnerabilities",
            ]

        if self.es_analista:
            return perm in [
                "can_manage_assets",
                "can_view_assets",
                "can_manage_vulnerabilities",
                "can_view_vulnerabilities",
            ]

        if self.es_cliente:
            return perm in [
                "can_view_assets",
                "can_view_vulnerabilities",
            ]

        return super().has_perm(perm, obj)

    def save(self, *args, **kwargs):
        """
        Validaciones adicionales antes de guardar.
        """
        if self.pk:  # Si el usuario ya existe
            old_user = Usuario.objects.get(pk=self.pk)
            if old_user.rol != self.rol:
                raise PermissionDenied("No se puede cambiar el rol de un usuario existente")
        super().save(*args, **kwargs)

    def es_admin(self):
        return self.rol == 'admin'

    def es_analista(self):
        return self.rol == 'analista'

    def es_cliente(self):
        return self.rol == 'cliente' 