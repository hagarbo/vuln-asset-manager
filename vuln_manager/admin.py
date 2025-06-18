from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from vuln_manager.models import Usuario, Cliente, Activo, Vulnerabilidad, ActivoVulnerabilidad
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models.tarea.tipo_tarea import TipoTarea

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

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'programacion', 'estado', 'ultima_ejecucion', 'proxima_ejecucion', 'creada_por')
    list_filter = ('tipo', 'estado', 'ultima_ejecucion')
    search_fields = ('tipo__nombre', 'programacion')
    readonly_fields = ('ultima_ejecucion', 'proxima_ejecucion', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(TipoTarea)
class TipoTareaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'activo', 'created_at')
    list_filter = ('activo', 'created_at')
    search_fields = ('codigo', 'nombre', 'descripcion')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('nombre',)

# Register other models
admin.site.register(Cliente)
admin.site.register(Activo)
admin.site.register(Vulnerabilidad)
admin.site.register(ActivoVulnerabilidad)
