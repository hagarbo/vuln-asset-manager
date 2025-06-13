from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from vuln_manager.models import Usuario, Cliente, Activo, Vulnerabilidad, ActivoVulnerabilidad

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'empresa', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'empresa')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'empresa', 'cargo')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol', 'telefono', 'empresa', 'cargo'),
        }),
    )

# Register other models
admin.site.register(Cliente)
admin.site.register(Activo)
admin.site.register(Vulnerabilidad)
admin.site.register(ActivoVulnerabilidad)
