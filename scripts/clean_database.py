#!/usr/bin/env python
"""
Script para limpiar las tablas de correlaciones y alertas.
Mantiene los datos básicos: usuarios, clientes, activos, vulnerabilidades, tareas.
Solo elimina ejecuciones de tareas de correlación, mantiene las del colector.
"""
# Este script debe ejecutarse con: python manage.py shell -c "exec(open('scripts/clean_database.py').read())"

from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.tarea.ejecucion_tarea import EjecucionTarea

def clean_correlation_data():
    """Limpia las tablas de correlaciones y alertas."""
    print("🧹 Limpiando datos de correlación...")
    
    # Contar registros antes de limpiar
    correlaciones_antes = ActivoVulnerabilidad.objects.count()
    alertas_antes = Alerta.objects.count()
    ejecuciones_correlacion_antes = EjecucionTarea.objects.filter(tarea__tipo__codigo='cve_asset_correlation').count()
    ejecuciones_colector_antes = EjecucionTarea.objects.filter(tarea__tipo__codigo='cve_collector').count()
    
    print(f"📊 Registros antes de limpiar:")
    print(f"   - Correlaciones: {correlaciones_antes}")
    print(f"   - Alertas: {alertas_antes}")
    print(f"   - Ejecuciones de correlación: {ejecuciones_correlacion_antes}")
    print(f"   - Ejecuciones del colector: {ejecuciones_colector_antes}")
    
    # Limpiar tablas
    print("\n🗑️  Eliminando registros...")
    
    # Eliminar correlaciones
    correlaciones_eliminadas = ActivoVulnerabilidad.objects.all().delete()[0]
    print(f"   ✅ Correlaciones eliminadas: {correlaciones_eliminadas}")
    
    # Eliminar alertas
    alertas_eliminadas = Alerta.objects.all().delete()[0]
    print(f"   ✅ Alertas eliminadas: {alertas_eliminadas}")
    
    # Eliminar solo ejecuciones de tareas de correlación
    ejecuciones_correlacion_eliminadas = EjecucionTarea.objects.filter(tarea__tipo__codigo='cve_asset_correlation').delete()[0]
    print(f"   ✅ Ejecuciones de correlación eliminadas: {ejecuciones_correlacion_eliminadas}")
    
    # Verificar limpieza
    correlaciones_despues = ActivoVulnerabilidad.objects.count()
    alertas_despues = Alerta.objects.count()
    ejecuciones_correlacion_despues = EjecucionTarea.objects.filter(tarea__tipo__codigo='cve_asset_correlation').count()
    ejecuciones_colector_despues = EjecucionTarea.objects.filter(tarea__tipo__codigo='cve_collector').count()
    
    print(f"\n📊 Registros después de limpiar:")
    print(f"   - Correlaciones: {correlaciones_despues}")
    print(f"   - Alertas: {alertas_despues}")
    print(f"   - Ejecuciones de correlación: {ejecuciones_correlacion_despues}")
    print(f"   - Ejecuciones del colector: {ejecuciones_colector_despues}")
    
    print("\n✅ Limpieza completada exitosamente!")
    print("💡 Ahora puedes ejecutar las tareas de correlación para generar nuevos datos.")

# Ejecutar la función
clean_correlation_data() 