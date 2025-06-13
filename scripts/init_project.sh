#!/bin/bash
set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Aplicando migraciones...${NC}"
python manage.py migrate --noinput

echo -e "${GREEN}Eliminando superusuario admin si existe...${NC}"
python << END
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@admin.com', 'Admin123!')
print('Superusuario creado correctamente')
END

echo -e "${GREEN}Cargando datos de fixtures...${NC}"
python manage.py loaddata vuln_manager/fixtures/initial_data.json || true

echo -e "${BLUE}Arrancando gunicorn...${NC}"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 120 