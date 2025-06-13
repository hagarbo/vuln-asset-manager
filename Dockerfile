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
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/static /app/media

# Crear script de entrada
RUN echo '#!/bin/bash\n\
if [ "$RENDER" = "True" ]; then\n\
    echo "Running in production mode with gunicorn..."\n\
    python manage.py migrate\n\
    python manage.py collectstatic --noinput\n\
    gunicorn config.wsgi:application --bind 0.0.0.0:8000\n\
else\n\
    echo "Running in development mode..."\n\
    python manage.py runserver 0.0.0.0:8000\n\
fi' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Exponer el puerto
EXPOSE 8000

# Usar el script de entrada como comando
CMD ["/app/entrypoint.sh"] 