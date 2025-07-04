FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
COPY requirements-dev.txt .
ARG INSTALL_DEV=false
RUN pip install --no-cache-dir -r requirements.txt \
    && if [ "$INSTALL_DEV" = "true" ]; then pip install --no-cache-dir -r requirements-dev.txt; fi

# Copiar el proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/static /app/media

# Crear script de entrada
RUN echo '#!/bin/bash\n\
if [ "$RENDER" = "True" ]; then\n\
    echo "Running in production mode with gunicorn..."\n\
    echo "Waiting for database..."\n\
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do\n\
        sleep 0.1\n\
    done\n\
    echo "Database is up!"\n\
    python manage.py migrate\n\
    python manage.py collectstatic --noinput\n\
    exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 0\n\
else\n\
    echo "Running in development mode..."\n\
    python manage.py runserver 0.0.0.0:8000\n\
fi' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Instalar netcat para el health check
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Exponer el puerto
EXPOSE 8000

# Usar el script de entrada como comando
CMD ["/app/entrypoint.sh"]

# Temporalmente cambiamos el CMD para crear un superusuario
CMD ["python", "create_superuser.py"]

COPY scripts/init_project.sh /app/init_project.sh
RUN chmod +x /app/init_project.sh

CMD ["/app/init_project.sh"] 