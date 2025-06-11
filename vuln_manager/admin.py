from django.contrib import admin
from .models import Cliente, Activo, Vulnerabilidad, Tarea, Alerta, ActivoVulnerabilidad, EjecucionTarea

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Activo)
admin.site.register(Vulnerabilidad)
admin.site.register(Tarea)
admin.site.register(Alerta)
admin.site.register(ActivoVulnerabilidad)
admin.site.register(EjecucionTarea)
