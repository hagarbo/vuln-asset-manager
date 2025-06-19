# Vuln-Asset-Manager

## Descripción
Sistema de gestión de activos tecnológicos y vulnerabilidades para PYMES, desarrollado como Proyecto Fin de Ciclo para el Ciclo Superior de Desarrollo de Aplicaciones Web.

## Estado Actual

### **1. Objetivo general y arquitectura**
- **Estado:** ✅ Completado
- El portal web está implementado en Django, con PostgreSQL, Docker y siguiendo el patrón Modelo-Vista-Plantilla (MVT).
- Se ha priorizado la separación de roles (admin, analista, cliente) y la escalabilidad, cumpliendo la arquitectura propuesta.

### **2. Objetivos específicos**

#### **Gestión de activos tecnológicos por cliente**
- ✅ CRUD completo de activos, asociados a clientes y gestionados por roles.

#### **Base de datos de vulnerabilidades CVE y activos**
- ✅ Modelos y relaciones implementados.
- ✅ Integración con fuentes oficiales (NIST) para importar CVEs.

#### **Extracción diaria de vulnerabilidades (NIST)**
- ✅ Implementada la recolección automática mediante comandos de gestión y servicios.
- ✅ **Nota:** Se gestionará mediante cron jobs en Render cuando el proyecto crezca (no se implementará Celery en esta fase).

#### **Cruce de información entre activos y CVEs**
- ✅ Lógica de correlación desarrollada y funcional, con vistas y repositorios específicos.

#### **Sistema de alertas ante vulnerabilidades críticas**
- ✅ Alertas automáticas generadas y asociadas a activos/clientes.
- ⏳ Pendiente: Envío de notificaciones por correo electrónico (la lógica está preparada, falta integración final y pruebas).

#### **Generación automática y personalizada de informes**
- ⏳ Parcial: Se generan resúmenes y métricas en dashboards, pero la exportación de informes PDF/Excel está pendiente de finalizar.

#### **Roles diferenciados y permisos**
- ✅ Implementados y revisados.
- ✅ Dashboards y vistas adaptadas a cada rol (admin, analista, cliente).

#### **Escalabilidad y seguridad**
- ✅ Uso de Docker, separación de servicios, y buenas prácticas de Django.
- ✅ Control de acceso y permisos revisados.

### **3. Historias de usuario (MVP)**

#### **Actualización automática de vulnerabilidades**
- ✅ Implementada (mediante comandos de gestión y servicios).

#### **Alta de clientes y activos desde archivo externo**
- ✅ Importación de activos desde CSV disponible.
- ✅ Alta de clientes funcional.

#### **Alta de analistas y asignación de clientes**
- ✅ Registro de analistas y asignación de clientes implementados.

#### **Visualización por parte del analista**
- ✅ Dashboards y listados para analistas con métricas, activos y vulnerabilidades asociadas.

#### **Alertas automáticas por vulnerabilidades críticas**
- ✅ Generación de alertas funcional.
- ⏳ Pendiente: Notificación por email.

#### **Consulta de histórico de vulnerabilidades (cliente)**
- ✅ El cliente puede consultar el histórico de vulnerabilidades de sus activos.

### **4. Fases técnicas y planificación**

#### **Análisis, diseño y configuración base**
- ✅ Completados.

#### **Desarrollo iterativo por módulos**
- ✅ CRUD de activos, clientes, usuarios, alertas y vulnerabilidades.
- ✅ Correlación y alertas.
- ✅ Dashboards diferenciados y visualmente integrados (Mazer).
- ⏳ Pendiente: Generación/exportación de informes.

#### **Pruebas y validación**
- ✅ Pruebas unitarias y de integración en modelos, formularios, repositorios y vistas.
- ⏳ Pendiente: Ampliar cobertura de tests en vistas específicas.

#### **Documentación y despliegue**
- ✅ Documentación técnica y de usuario en proceso (`docs/`, `README.md`).
- ✅ Despliegue en Docker funcional.
- ✅ Configuración para Render.com y despliegue automático desde GitHub.
- ⏳ Pendiente: Documentar el proceso de despliegue final y CI/CD completo.

### **5. Decisiones y mejoras adicionales**

#### **Unificación visual y experiencia de usuario**
- ✅ Dashboards y listados adaptados a cada rol, coherentes y visualmente integrados.
- ✅ Uso de Mazer, eliminación de Bootstrap innecesario.

#### **Permisos y rutas**
- ✅ Separación clara de rutas y vistas para cada rol.
- ✅ Eliminación de referencias a roles no usados ("gestor").

#### **Patrón repositorio y servicios**
- ✅ Adoptado para lógica compleja y reutilizable, siguiendo buenas prácticas.

#### **Contenerización y portabilidad**
- ✅ Docker y Docker Compose configurados y en uso.

### **6. Pendientes y próximos pasos**
- **Finalizar y probar el envío de notificaciones por correo electrónico.**
- **Completar la exportación/generación de informes automáticos y personalizados.**
- **Revisar y ampliar la cobertura de tests, especialmente en vistas.**
- **Documentar el proceso de despliegue y CI/CD.**
- **Decidir y personalizar la información mostrada en el dashboard del cliente.**

### **Resumen**
El proyecto cumple la mayoría de los hitos y objetivos definidos en el anteproyecto, especialmente en cuanto a la gestión de activos, usuarios, roles, correlación de vulnerabilidades y visualización adaptada.  
Quedan pendientes principalmente el envío de notificaciones por email, la exportación de informes y la documentación/despliegue final.  
El desarrollo sigue las buenas prácticas y la planificación establecida, con una base sólida para su ampliación y entrega final.

## Estructura del Proyecto
```
vuln-asset-manager/
├── config/                # Configuración principal de Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── vuln_manager/         # Aplicación principal
│   ├── models/           # Modelos de datos
│   │   ├── __init__.py
│   │   ├── cliente.py
│   │   ├── activo.py
│   │   └── vulnerabilidad.py
│   ├── views/            # Vistas
│   │   ├── __init__.py
│   │   ├── cliente_views.py
│   │   ├── activo_views.py
│   │   └── vulnerabilidad_views.py
│   └── urls.py
├── templates/            # Plantillas HTML
│   ├── base.html
│   └── vuln_manager/
│       ├── cliente_list.html
│       ├── cliente_detail.html
│       ├── activo_list.html
│       ├── activo_detail.html
│       ├── vulnerabilidades/
│       │   ├── list.html
│       │   ├── detail.html
│       │   ├── form.html
│       │   └── confirm_delete.html
│       └── vulnerabilidad_detail.html
├── static/              # Archivos estáticos
├── docs/               # Documentación
│   ├── ESTADO.md
│   └── PROYECTO.md
├── docker-compose.yml
└── Dockerfile
```

## Tecnologías Utilizadas
- Python 3.11
- Django 4.2
- PostgreSQL 15
- Docker y Docker Compose
- Bootstrap 5
- HTML5/CSS3

## Próximos Pasos
1. Implementar formularios para crear/editar entidades
2. Añadir sistema de autenticación y autorización
3. Implementar búsqueda y filtrado de datos
4. Añadir validaciones de datos
5. Implementar pruebas unitarias
6. Configurar despliegue en producción

## Notas de Desarrollo
- El proyecto está configurado para desarrollo local con Docker
- Se utiliza PostgreSQL como base de datos
- Las vistas están organizadas en archivos separados para mejor mantenimiento
- Las plantillas utilizan Bootstrap para el diseño responsivo

## Configuración del Entorno
- **Docker**: Sí
- **Base de datos**: PostgreSQL
- **Framework**: Django 4.2.10
- **Frontend**: Bootstrap 5

## Dependencias Principales
- Django 4.2.10
- psycopg2-binary 2.9.9
- python-dotenv 1.0.1

## Modelos Principales

### Vulnerabilidad
- Campos CVSS v2/v3
- Sistema de referencias
- Estado y seguimiento

### Activo
- Gestión de activos tecnológicos
- Relación con vulnerabilidades

### Cliente
- Gestión de clientes
- Asignación de analistas

### Tarea
- Gestión de tareas programadas (actualización de CVEs, escaneo de activos)
- Registro de ejecuciones, estados y programación tipo cron
- Relación con usuarios (creador, ejecutor)

### Alerta
- Gestión de alertas asociadas a vulnerabilidades y activos
- Estados de alerta (nueva, vista, en proceso, resuelta, ignorada)
- Asignación de analista y seguimiento de resolución

## Cambios Recientes
1. Implementación del modelo de Vulnerabilidades con soporte para:
   - CVSS v2 y v3
   - Sistema de referencias
   - Estados de vulnerabilidad

## Comandos Útiles
```bash
# Iniciar contenedores
docker-compose up -d

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Acceder al shell de Django
docker-compose exec web python manage.py shell
``` 