# Portal de Gestión de Activos y Vulnerabilidades

Sistema de gestión de activos tecnológicos y vulnerabilidades para PYMES, desarrollado como Proyecto Fin de Ciclo de DAW.

## Descripción

Este proyecto surge con el objetivo de desarrollar una plataforma que permita automatizar la detección, análisis y gestión de vulnerabilidades asociadas a los activos tecnológicos de una empresa. La motivación principal es dotar a los analistas de seguridad de una herramienta que facilite la toma de decisiones, reduzca los tiempos de reacción ante amenazas críticas y mejore la visibilidad de la postura de seguridad de cada cliente.

## Tecnologías utilizadas

- **Backend**: Django 4.2.10 (LTS)
- **Base de datos**: PostgreSQL 15
- **Frontend**: Django Templates + Bootstrap 5
- **Contenedores**: Docker

## Requisitos

- Docker y Docker Compose
- Git

## Instalación y configuración inicial

### 1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd vuln-asset-manager
```

### 2. Configuración del entorno
El proyecto utiliza Docker para su despliegue. Los archivos de configuración principales son:

#### requirements.txt
```
Django==4.2.10
psycopg2-binary==2.9.9
python-dotenv==1.0.1
```

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DJANGO_SETTINGS_MODULE=core.settings
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

### 3. Estructura del proyecto
```
vuln-asset-manager/
├── core/                    # Proyecto principal Django
│   ├── settings.py         # Configuración del proyecto
│   ├── urls.py            # Configuración de URLs
│   ├── wsgi.py
│   └── __init__.py
├── templates/             # Plantillas HTML
│   └── home.html         # Página inicial
├── static/               # Archivos estáticos (CSS, JS, imágenes)
├── requirements.txt      # Dependencias del proyecto
├── Dockerfile           # Configuración de Docker
└── docker-compose.yml   # Configuración de servicios Docker
```

### 4. Pasos para el despliegue inicial

1. Crear el proyecto Django:
```bash
docker-compose run --rm web django-admin startproject core .
```

2. Configurar settings.py:
- Configurar la base de datos PostgreSQL
- Configurar el idioma y zona horaria
- Configurar archivos estáticos y templates

3. Crear la página inicial (templates/home.html):
- Implementar una página básica con Bootstrap
- Configurar la navegación

4. Configurar URLs (core/urls.py):
- Configurar la ruta principal
- Configurar el panel de administración

5. Construir y ejecutar los contenedores:
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

6. Aplicar migraciones:
```bash
docker-compose exec web python manage.py migrate
```

### 5. Acceso a la aplicación

Una vez desplegada, la aplicación estará disponible en:
- http://localhost:8000 - Página inicial
- http://localhost:8000/admin - Panel de administración

## Próximos pasos

1. Configuración de la base de datos y modelos
2. Implementación del sistema de autenticación
3. Desarrollo de las aplicaciones principales:
   - Gestión de usuarios
   - Gestión de activos
   - Gestión de vulnerabilidades
   - Generación de informes

## Licencia

Este proyecto es parte de un Proyecto Fin de Ciclo y está sujeto a los términos de la licencia académica.

## Autor

## Autor - Adrián García Bouzas