# Script para poblar la base de datos con analistas, clientes y activos realistas
# Ejecutar en el shell de Django: exec(open('vuln_manager/fixtures/populate_demo_data.py').read())

from vuln_manager.models import Usuario, Cliente, Activo
from vuln_manager.models.tarea.tipo_tarea import TipoTarea
from vuln_manager.models.activo_vulnerabilidad.activo_vulnerabilidad import ActivoVulnerabilidad
from vuln_manager.models.alerta.alerta import Alerta
from vuln_manager.models.tarea.ejecucion_tarea import EjecucionTarea
from vuln_manager.models.tarea.tarea import Tarea
from django.contrib.auth.hashers import make_password
import random

def limpiar_base_datos():
    """Limpia la base de datos antes de crear nuevos datos de demo."""
    print("🧹 Limpiando base de datos antes de crear datos de demo...")
    
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
    
    print("✅ Limpieza completada\n")

print("Iniciando población de datos de demo...")

# Limpiar la base de datos antes de crear nuevos datos
limpiar_base_datos()

# Crear tipos de tarea
print("Creando tipos de tarea...")
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

# Crear tipos de tarea
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
        print(f"Tipo de tarea creado: {tipo_tarea.nombre}")
    else:
        print(f"Tipo de tarea ya existía: {tipo_tarea.nombre}")
    tipos_tarea.append(tipo_tarea)

# Datos de analistas
analistas_data = [
    {"username": "marta.garcia", "email": "marta.garcia@acme.com", "first_name": "Marta", "last_name": "García", "rol": "analista", "empresa": "ACME Security", "cargo": "Analista Senior"},
    {"username": "juan.perez", "email": "juan.perez@telefonica.com", "first_name": "Juan", "last_name": "Pérez", "rol": "analista", "empresa": "Telefónica", "cargo": "Especialista en Ciberseguridad"},
    {"username": "ana.rodriguez", "email": "ana.rodriguez@bbva.com", "first_name": "Ana", "last_name": "Rodríguez", "rol": "analista", "empresa": "BBVA", "cargo": "Analista de Vulnerabilidades"},
    {"username": "carlos.lopez", "email": "carlos.lopez@indra.com", "first_name": "Carlos", "last_name": "López", "rol": "analista", "empresa": "Indra", "cargo": "Consultor de Seguridad"},
    {"username": "lucia.martin", "email": "lucia.martin@everis.com", "first_name": "Lucía", "last_name": "Martín", "rol": "analista", "empresa": "Everis", "cargo": "Analista de Threat Intelligence"}
]

# Datos de clientes
clientes_data = [
    {"username": "contacto_iberdrola", "email": "contacto@iberdrola.es", "first_name": "Contacto", "last_name": "Iberdrola", "rol": "cliente", "empresa": "Iberdrola", "cargo": "IT Manager"},
    {"username": "it_santander", "email": "it@santander.com", "first_name": "IT", "last_name": "Santander", "rol": "cliente", "empresa": "Banco Santander", "cargo": "Director IT"},
    {"username": "admin_endesa", "email": "admin@endesa.es", "first_name": "Admin", "last_name": "Endesa", "rol": "cliente", "empresa": "Endesa", "cargo": "CISO"},
    {"username": "security_repsol", "email": "security@repsol.com", "first_name": "Security", "last_name": "Repsol", "rol": "cliente", "empresa": "Repsol", "cargo": "Security Manager"},
    {"username": "tech_telefonica", "email": "tech@telefonica.com", "first_name": "Tech", "last_name": "Telefónica", "rol": "cliente", "empresa": "Telefónica", "cargo": "CTO"},
    {"username": "it_bbva", "email": "it@bbva.com", "first_name": "IT", "last_name": "BBVA", "rol": "cliente", "empresa": "BBVA", "cargo": "IT Director"},
    {"username": "admin_caixabank", "email": "admin@caixabank.es", "first_name": "Admin", "last_name": "CaixaBank", "rol": "cliente", "empresa": "CaixaBank", "cargo": "CISO"},
    {"username": "security_acs", "email": "security@acs.es", "first_name": "Security", "last_name": "ACS", "rol": "cliente", "empresa": "ACS", "cargo": "Security Director"},
    {"username": "it_ferrovial", "email": "it@ferrovial.com", "first_name": "IT", "last_name": "Ferrovial", "rol": "cliente", "empresa": "Ferrovial", "cargo": "IT Manager"},
    {"username": "admin_mapfre", "email": "admin@mapfre.com", "first_name": "Admin", "last_name": "Mapfre", "rol": "cliente", "empresa": "Mapfre", "cargo": "CISO"},
    {"username": "tech_inditex", "email": "tech@inditex.com", "first_name": "Tech", "last_name": "Inditex", "rol": "cliente", "empresa": "Inditex", "cargo": "CTO"},
    {"username": "it_mercadona", "email": "it@mercadona.es", "first_name": "IT", "last_name": "Mercadona", "rol": "cliente", "empresa": "Mercadona", "cargo": "IT Director"},
    {"username": "security_elcorteingles", "email": "security@elcorteingles.es", "first_name": "Security", "last_name": "El Corte Inglés", "rol": "cliente", "empresa": "El Corte Inglés", "cargo": "Security Manager"},
    {"username": "admin_iberia", "email": "admin@iberia.com", "first_name": "Admin", "last_name": "Iberia", "rol": "cliente", "empresa": "Iberia", "cargo": "CISO"},
    {"username": "tech_renfe", "email": "tech@renfe.es", "first_name": "Tech", "last_name": "Renfe", "rol": "cliente", "empresa": "Renfe", "cargo": "CTO"},
    {"username": "it_aeat", "email": "it@aeat.es", "first_name": "IT", "last_name": "AEAT", "rol": "cliente", "empresa": "Agencia Tributaria", "cargo": "IT Director"},
    {"username": "security_guardiacivil", "email": "security@guardiacivil.es", "first_name": "Security", "last_name": "Guardia Civil", "rol": "cliente", "empresa": "Guardia Civil", "cargo": "Security Manager"},
    {"username": "admin_ayuntamiento_madrid", "email": "admin@madrid.es", "first_name": "Admin", "last_name": "Ayuntamiento Madrid", "rol": "cliente", "empresa": "Ayuntamiento de Madrid", "cargo": "CISO"},
    {"username": "tech_ayuntamiento_barcelona", "email": "tech@barcelona.cat", "first_name": "Tech", "last_name": "Ayuntamiento Barcelona", "rol": "cliente", "empresa": "Ayuntamiento de Barcelona", "cargo": "CTO"},
    {"username": "it_universidad_complutense", "email": "it@ucm.es", "first_name": "IT", "last_name": "Universidad Complutense", "rol": "cliente", "empresa": "Universidad Complutense", "cargo": "IT Director"}
]

# Datos de activos inspirados en las vulnerabilidades
activos_templates = [
    # Servidores web
    {"nombre": "Servidor Web Principal", "tipo": "software", "descripcion": "Servidor web Apache con PHP y MySQL", "palabras_clave": "apache,php,mysql,web,servidor", "ip": "192.168.1.10", "puerto": 80, "version": "Apache 2.4 + PHP 8.1"},
    {"nombre": "Servidor Web Secundario", "tipo": "software", "descripcion": "Servidor web Nginx con Node.js", "palabras_clave": "nginx,nodejs,web,servidor", "ip": "192.168.1.11", "puerto": 80, "version": "Nginx 1.20 + Node.js 18"},
    {"nombre": "Servidor de Aplicaciones", "tipo": "software", "descripcion": "Servidor de aplicaciones Java con Tomcat", "palabras_clave": "java,tomcat,servidor,aplicacion", "ip": "192.168.1.12", "puerto": 8080, "version": "Apache Tomcat 9.0"},
    
    # Bases de datos
    {"nombre": "Base de Datos Principal", "tipo": "software", "descripcion": "Servidor de base de datos MySQL", "palabras_clave": "mysql,database,bbdd,servidor", "ip": "192.168.1.20", "puerto": 3306, "version": "MySQL 8.0"},
    {"nombre": "Base de Datos Secundaria", "tipo": "software", "descripcion": "Servidor de base de datos PostgreSQL", "palabras_clave": "postgresql,database,bbdd,servidor", "ip": "192.168.1.21", "puerto": 5432, "version": "PostgreSQL 14"},
    {"nombre": "Base de Datos Oracle", "tipo": "software", "descripcion": "Servidor de base de datos Oracle", "palabras_clave": "oracle,database,bbdd,servidor", "ip": "192.168.1.22", "puerto": 1521, "version": "Oracle 19c"},
    
    # Firewalls y seguridad
    {"nombre": "Firewall Perimetral", "tipo": "red", "descripcion": "Firewall Cisco ASA", "palabras_clave": "cisco,firewall,seguridad,perimetro", "ip": "192.168.1.1", "puerto": 443, "version": "Cisco ASA 9.12"},
    {"nombre": "Firewall Interno", "tipo": "red", "descripcion": "Firewall Fortinet FortiGate", "palabras_clave": "fortinet,firewall,seguridad,interno", "ip": "192.168.1.2", "puerto": 443, "version": "FortiGate 6.2"},
    {"nombre": "IPS/IDS", "tipo": "red", "descripcion": "Sistema de detección de intrusiones", "palabras_clave": "ips,ids,seguridad,deteccion", "ip": "192.168.1.3", "puerto": 22, "version": "Snort 3.0"},
    
    # Servidores de archivos
    {"nombre": "Servidor de Archivos", "tipo": "software", "descripcion": "Servidor de archivos Windows", "palabras_clave": "windows,archivos,servidor,smb", "ip": "192.168.1.30", "puerto": 445, "version": "Windows Server 2019"},
    {"nombre": "Servidor NAS", "tipo": "hardware", "descripcion": "Servidor de almacenamiento NAS", "palabras_clave": "nas,almacenamiento,servidor", "ip": "192.168.1.31", "puerto": 22, "version": "Synology DSM 7.0"},
    
    # Servidores de correo
    {"nombre": "Servidor de Correo", "tipo": "software", "descripcion": "Servidor de correo Exchange", "palabras_clave": "exchange,correo,email,servidor", "ip": "192.168.1.40", "puerto": 25, "version": "Microsoft Exchange 2019"},
    {"nombre": "Servidor SMTP", "tipo": "software", "descripcion": "Servidor SMTP Postfix", "palabras_clave": "postfix,smtp,correo,servidor", "ip": "192.168.1.41", "puerto": 25, "version": "Postfix 3.6"},
    
    # Servidores DNS
    {"nombre": "Servidor DNS Primario", "tipo": "software", "descripcion": "Servidor DNS BIND", "palabras_clave": "bind,dns,servidor", "ip": "192.168.1.50", "puerto": 53, "version": "BIND 9.16"},
    {"nombre": "Servidor DNS Secundario", "tipo": "software", "descripcion": "Servidor DNS secundario", "palabras_clave": "dns,servidor,secundario", "ip": "192.168.1.51", "puerto": 53, "version": "BIND 9.16"},
    
    # Estaciones de trabajo
    {"nombre": "Estación de Trabajo", "tipo": "hardware", "descripcion": "PC de usuario Windows 10", "palabras_clave": "windows,pc,usuario,oficina", "ip": "192.168.1.100", "puerto": None, "version": "Windows 10 Pro"},
    {"nombre": "Estación de Desarrollo", "tipo": "hardware", "descripcion": "PC de desarrollador Linux", "palabras_clave": "linux,desarrollo,pc,usuario", "ip": "192.168.1.101", "puerto": None, "version": "Ubuntu 22.04"},
    
    # Servidores de virtualización
    {"nombre": "Servidor de Virtualización", "tipo": "software", "descripcion": "Servidor VMware ESXi", "palabras_clave": "vmware,esxi,virtualizacion,servidor", "ip": "192.168.1.60", "puerto": 443, "version": "VMware ESXi 7.0"},
    {"nombre": "Servidor Hyper-V", "tipo": "software", "descripcion": "Servidor Microsoft Hyper-V", "palabras_clave": "hyper-v,microsoft,virtualizacion,servidor", "ip": "192.168.1.61", "puerto": 443, "version": "Windows Server 2019 Hyper-V"},
    
    # Servidores de backup
    {"nombre": "Servidor de Backup", "tipo": "software", "descripcion": "Servidor de respaldo Veeam", "palabras_clave": "veeam,backup,respaldo,servidor", "ip": "192.168.1.70", "puerto": 22, "version": "Veeam Backup & Replication 11"},
    
    # Servidores de monitoreo
    {"nombre": "Servidor de Monitoreo", "tipo": "software", "descripcion": "Servidor Nagios de monitoreo", "palabras_clave": "nagios,monitoreo,servidor", "ip": "192.168.1.80", "puerto": 80, "version": "Nagios Core 4.4"},
    
    # Routers y switches
    {"nombre": "Router Principal", "tipo": "red", "descripcion": "Router Cisco ISR", "palabras_clave": "cisco,router,red", "ip": "192.168.1.254", "puerto": 22, "version": "Cisco ISR 4321"},
    {"nombre": "Switch Core", "tipo": "red", "descripcion": "Switch de núcleo Cisco", "palabras_clave": "cisco,switch,red,core", "ip": "192.168.1.253", "puerto": 22, "version": "Cisco Catalyst 3850"}
]

# Crear analistas
print("Creando analistas...")
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
    print(f"Analista creado: {usuario.username}")

# Crear clientes y sus usuarios
print("Creando clientes y usuarios...")
clientes = []
for i, data in enumerate(clientes_data):
    # Crear usuario del cliente
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
    
    # Crear cliente
    cliente = Cliente.objects.create(
        nombre=data["empresa"],
        usuario=usuario
    )
    clientes.append(cliente)
    print(f"Cliente creado: {cliente.nombre}")

# Crear activos para cada cliente
print("Creando activos...")
activos_creados = 0
for cliente in clientes:
    # Cada cliente tendrá entre 18 y 22 activos
    num_activos = random.randint(18, 22)
    
    for i in range(num_activos):
        template = random.choice(activos_templates)
        
        # Personalizar el activo para el cliente
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
        activos_creados += 1
    
    print(f"Activos creados para {cliente.nombre}: {num_activos}")

# Asignar analistas aleatoriamente a los clientes
print("Asignando analistas a clientes...")
for cliente in clientes:
    # Asignar entre 1 y 2 analistas aleatoriamente
    num_analistas = random.randint(1, 2)
    analistas_asignados = random.sample(analistas, num_analistas)
    cliente.analistas.set(analistas_asignados)
    print(f"Analistas asignados a {cliente.nombre}: {[a.username for a in analistas_asignados]}")

print(f"\n¡Población completada!")
print(f"- Tipos de tarea creados: {len(tipos_tarea)}")
print(f"- Analistas creados: {len(analistas)}")
print(f"- Clientes creados: {len(clientes)}")
print(f"- Activos creados: {activos_creados}")
print(f"- Total de usuarios: {len(analistas) + len(clientes)}")
print(f"\nTodos los usuarios tienen la contraseña: renaido.")
print(f"\nTipos de tarea disponibles:")
for tipo in tipos_tarea:
    print(f"  - {tipo.codigo}: {tipo.nombre}") 