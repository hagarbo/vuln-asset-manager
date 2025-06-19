#!/usr/bin/env python
"""
Script de inicialización para producción.
Limpia la base de datos y la puebla con datos iniciales.
"""
# Este script debe ejecutarse con: python manage.py shell -c "exec(open('scripts/init_production.py').read())"

from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.tarea.ejecucion_tarea import EjecucionTarea
from vuln_manager.models.tarea.tarea import Tarea
from vuln_manager.models import Usuario, Cliente, Activo
from vuln_manager.models.tarea.tipo_tarea import TipoTarea
from django.contrib.auth.hashers import make_password
import random

def init_production():
    """Inicializa la base de datos para producción."""
    print("🚀 Inicializando base de datos para producción...")
    
    # 1. Limpiar datos existentes
    print("\n🧹 Limpiando datos existentes...")
    
    # Contar registros antes de limpiar
    correlaciones_antes = ActivoVulnerabilidad.objects.count()
    alertas_antes = Alerta.objects.count()
    ejecuciones_antes = EjecucionTarea.objects.count()
    tareas_antes = Tarea.objects.count()
    usuarios_antes = Usuario.objects.count()
    clientes_antes = Cliente.objects.count()
    activos_antes = Activo.objects.count()
    
    print(f"📊 Registros antes de limpiar:")
    print(f"   - Correlaciones: {correlaciones_antes}")
    print(f"   - Alertas: {alertas_antes}")
    print(f"   - Ejecuciones de tareas: {ejecuciones_antes}")
    print(f"   - Tareas: {tareas_antes}")
    print(f"   - Usuarios: {usuarios_antes}")
    print(f"   - Clientes: {clientes_antes}")
    print(f"   - Activos: {activos_antes}")
    
    # Limpiar tablas
    print("\n🗑️  Eliminando registros...")
    
    # Eliminar correlaciones y alertas
    correlaciones_eliminadas = ActivoVulnerabilidad.objects.all().delete()[0]
    alertas_eliminadas = Alerta.objects.all().delete()[0]
    print(f"   ✅ Correlaciones eliminadas: {correlaciones_eliminadas}")
    print(f"   ✅ Alertas eliminadas: {alertas_eliminadas}")
    
    # Eliminar ejecuciones de tareas
    ejecuciones_eliminadas = EjecucionTarea.objects.all().delete()[0]
    print(f"   ✅ Ejecuciones de tareas eliminadas: {ejecuciones_eliminadas}")
    
    # Eliminar tareas
    tareas_eliminadas = Tarea.objects.all().delete()[0]
    print(f"   ✅ Tareas eliminadas: {tareas_eliminadas}")
    
    # Eliminar activos
    activos_eliminadas = Activo.objects.all().delete()[0]
    print(f"   ✅ Activos eliminados: {activos_eliminadas}")
    
    # Eliminar clientes (esto también eliminará los usuarios de cliente)
    clientes_eliminadas = Cliente.objects.all().delete()[0]
    print(f"   ✅ Clientes eliminados: {clientes_eliminadas}")
    
    # Eliminar usuarios que no sean admin
    usuarios_eliminadas = Usuario.objects.exclude(username='admin').delete()[0]
    print(f"   ✅ Usuarios eliminados: {usuarios_eliminadas}")
    
    # 2. Crear tipos de tarea
    print("\n📋 Creando tipos de tarea...")
    tipos_tarea_data = [
        {
            "codigo": "cve_collector",
            "nombre": "Recolector de CVEs",
            "descripcion": "Recolecta vulnerabilidades desde fuentes externas como NIST NVD",
            "parametros": {
                "dias_atras": {
                    "tipo": "integer",
                    "min": 1,
                    "max": 30,
                    "default": 7,
                    "descripcion": "Número de días hacia atrás para buscar CVEs"
                }
            },
            "activo": True
        },
        {
            "codigo": "cve_asset_correlation",
            "nombre": "Correlación CVE-Activos",
            "descripcion": "Correlaciona vulnerabilidades con activos basándose en palabras clave",
            "parametros": {
                "severidad_minima": {
                    "tipo": "choice",
                    "opciones": ["critica", "alta", "media", "baja"],
                    "default": "critica",
                    "descripcion": "Severidad mínima para generar alertas"
                }
            },
            "activo": True
        }
    ]
    
    tipos_tarea = []
    for data in tipos_tarea_data:
        tipo_tarea, created = TipoTarea.objects.get_or_create(
            codigo=data["codigo"],
            defaults={
                "nombre": data["nombre"],
                "descripcion": data["descripcion"],
                "parametros": data["parametros"],
                "activo": data["activo"]
            }
        )
        if created:
            print(f"   ✅ Tipo de tarea creado: {tipo_tarea.nombre}")
        else:
            print(f"   ℹ️  Tipo de tarea ya existía: {tipo_tarea.nombre}")
        tipos_tarea.append(tipo_tarea)
    
    # 3. Crear datos de demo
    print("\n👥 Creando datos de demo...")
    
    # Datos de analistas
    analistas_data = [
        {"username": "marta.garcia", "email": "marta.garcia@acme.com", "first_name": "Marta", "last_name": "García", "rol": "analista", "empresa": "ACME Security", "cargo": "Analista Senior"},
        {"username": "juan.perez", "email": "juan.perez@telefonica.com", "first_name": "Juan", "last_name": "Pérez", "rol": "analista", "empresa": "Telefónica", "cargo": "Especialista en Ciberseguridad"},
        {"username": "ana.rodriguez", "email": "ana.rodriguez@bbva.com", "first_name": "Ana", "last_name": "Rodríguez", "rol": "analista", "empresa": "BBVA", "cargo": "Analista de Vulnerabilidades"},
    ]
    
    # Datos de clientes
    clientes_data = [
        {"username": "contacto_iberdrola", "email": "contacto@iberdrola.es", "first_name": "Contacto", "last_name": "Iberdrola", "rol": "cliente", "empresa": "Iberdrola", "cargo": "IT Manager"},
        {"username": "it_santander", "email": "it@santander.com", "first_name": "IT", "last_name": "Santander", "rol": "cliente", "empresa": "Banco Santander", "cargo": "Director IT"},
        {"username": "admin_endesa", "email": "admin@endesa.es", "first_name": "Admin", "last_name": "Endesa", "rol": "cliente", "empresa": "Endesa", "cargo": "CISO"},
    ]
    
    # Crear analistas
    print("   👨‍💼 Creando analistas...")
    analistas = []
    for data in analistas_data:
        usuario = Usuario.objects.create_user(
            username=data["username"],
            email=data["email"],
            password="renaido.",
            first_name=data["first_name"],
            last_name=data["last_name"],
            rol=data["rol"],
            empresa=data["empresa"],
            cargo=data["cargo"]
        )
        analistas.append(usuario)
        print(f"      ✅ Analista creado: {usuario.username}")
    
    # Crear clientes
    print("   🏢 Creando clientes...")
    clientes = []
    for data in clientes_data:
        usuario = Usuario.objects.create_user(
            username=data["username"],
            email=data["email"],
            password="renaido.",
            first_name=data["first_name"],
            last_name=data["last_name"],
            rol=data["rol"],
            empresa=data["empresa"],
            cargo=data["cargo"]
        )
        
        cliente = Cliente.objects.create(
            nombre=data["empresa"],
            usuario=usuario
        )
        clientes.append(cliente)
        print(f"      ✅ Cliente creado: {cliente.nombre}")
    
    # Crear algunos activos de ejemplo
    print("   💻 Creando activos de ejemplo...")
    activos_templates = [
        {"nombre": "Servidor Web Principal", "tipo": "software", "descripcion": "Servidor web Apache con PHP y MySQL", "palabras_clave": "apache,php,mysql,web,servidor", "ip": "192.168.1.10", "puerto": 80, "version": "Apache 2.4 + PHP 8.1"},
        {"nombre": "Base de Datos Principal", "tipo": "software", "descripcion": "Servidor de base de datos MySQL", "palabras_clave": "mysql,database,bbdd,servidor", "ip": "192.168.1.20", "puerto": 3306, "version": "MySQL 8.0"},
        {"nombre": "Firewall Perimetral", "tipo": "red", "descripcion": "Firewall Cisco ASA", "palabras_clave": "cisco,firewall,seguridad,perimetro", "ip": "192.168.1.1", "puerto": 443, "version": "Cisco ASA 9.12"},
    ]
    
    for cliente in clientes:
        for i, template in enumerate(activos_templates):
            activo = Activo.objects.create(
                nombre=f"{template['nombre']} - {cliente.nombre}",
                descripcion=f"{template['descripcion']} para {cliente.nombre}",
                palabras_clave=template['palabras_clave'],
                ip=f"10.{cliente.id}.{i+1}.{random.randint(1, 254)}",
                puerto=template['puerto'],
                tipo=template['tipo'],
                version=template['version'],
                cliente=cliente
            )
        print(f"      ✅ Activos creados para {cliente.nombre}")
    
    # Asignar analistas aleatoriamente a los clientes
    print("   👥 Asignando analistas a clientes...")
    for cliente in clientes:
        # Asignar entre 1 y 2 analistas aleatoriamente
        num_analistas = random.randint(1, 2)
        analistas_asignados = random.sample(analistas, num_analistas)
        cliente.analistas.set(analistas_asignados)
        print(f"      ✅ Analistas asignados a {cliente.nombre}: {[a.username for a in analistas_asignados]}")
    
    # 4. Verificar inicialización
    print("\n📊 Verificación final:")
    correlaciones_final = ActivoVulnerabilidad.objects.count()
    alertas_final = Alerta.objects.count()
    ejecuciones_final = EjecucionTarea.objects.count()
    tareas_final = Tarea.objects.count()
    usuarios_final = Usuario.objects.count()
    clientes_final = Cliente.objects.count()
    activos_final = Activo.objects.count()
    tipos_final = TipoTarea.objects.count()
    
    print(f"   - Correlaciones: {correlaciones_final}")
    print(f"   - Alertas: {alertas_final}")
    print(f"   - Ejecuciones de tareas: {ejecuciones_final}")
    print(f"   - Tareas: {tareas_final}")
    print(f"   - Usuarios: {usuarios_final}")
    print(f"   - Clientes: {clientes_final}")
    print(f"   - Activos: {activos_final}")
    print(f"   - Tipos de tarea: {tipos_final}")
    
    print("\n✅ Inicialización completada exitosamente!")
    print("🎯 La base de datos está lista para producción.")
    print("💡 Credenciales de acceso:")
    print("   - Admin: admin / Admin123!")
    print("   - Analistas: marta.garcia, juan.perez, ana.rodriguez / renaido.")
    print("   - Clientes: contacto_iberdrola, it_santander, admin_endesa / renaido.")

# Ejecutar la función
init_production() 