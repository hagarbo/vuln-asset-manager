# Vuln-Asset-Manager

## Descripción
Sistema de gestión de activos tecnológicos y vulnerabilidades para PYMES, desarrollado como Proyecto Fin de Ciclo para el Ciclo Superior de Desarrollo de Aplicaciones Web.

## Estado Actual
- ✅ Configuración inicial del proyecto Django
- ✅ Configuración de Docker y Docker Compose
- ✅ Implementación de modelos de datos
- ✅ Configuración de la base de datos PostgreSQL
- ✅ Implementación de vistas básicas
- ✅ Creación de plantillas HTML
- ✅ Reorganización de vistas en archivos separados
- ⏳ Implementación de formularios
- ⏳ Sistema de autenticación
- ⏳ Sistema de búsqueda y filtrado
- ⏳ Pruebas unitarias
- ⏳ Despliegue en producción

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