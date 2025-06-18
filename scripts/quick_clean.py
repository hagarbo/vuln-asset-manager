#!/usr/bin/env python
"""
Script de limpieza rápida para desarrollo.
Solo limpia correlaciones y alertas, mantiene usuarios, clientes, activos y vulnerabilidades.
"""
# Este script debe ejecutarse con: python manage.py shell -c "exec(open('scripts/quick_clean.py').read())"

from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.tarea.ejecucion_tarea import EjecucionTarea

def quick_clean():
    """Limpia solo correlaciones y alertas para desarrollo."""
    print("🧹 Limpieza rápida para desarrollo...")
    
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
    
    print("\n✅ Limpieza rápida completada!")
    print("💡 Datos de usuarios, clientes, activos y vulnerabilidades mantenidos.")

# Ejecutar la función
quick_clean() 