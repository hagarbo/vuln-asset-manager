#!/bin/bash
set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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
User.objects.create_superuser('admin', 'admin@admin.com', 'Admin123!', rol='admin')
print('Superusuario creado correctamente con rol de administrador')
END

echo -e "${YELLOW}Verificando si la base de datos ya está inicializada...${NC}"

# Verificar variable de entorno para forzar inicialización
if [ "$FORCE_INIT" = "true" ]; then
    echo -e "${YELLOW}Forzando inicialización por variable de entorno FORCE_INIT=true${NC}"
    python manage.py shell -c "exec(open('scripts/init_production.py').read())"
else
    # Usar una variable para comunicar el resultado en lugar de exit()
    INIT_NEEDED=$(python << END
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from vuln_manager.models import Usuario, Cliente

# Verificar si ya hay datos
usuarios_count = Usuario.objects.count()
clientes_count = Cliente.objects.count()

if usuarios_count > 1 or clientes_count > 0:  # Más de 1 porque siempre hay admin
    print(f'✅ Base de datos ya inicializada: {usuarios_count} usuarios, {clientes_count} clientes')
    print('Skipping initialization...')
    print('NEED_INIT=false')
else:
    print('🔄 Base de datos vacía, procediendo con inicialización...')
    print('NEED_INIT=true')
END
)

    # Extraer el valor de NEED_INIT del output
    if echo "$INIT_NEEDED" | grep -q "NEED_INIT=true"; then
        echo -e "${YELLOW}Inicializando base de datos para producción...${NC}"
        python manage.py shell -c "exec(open('scripts/init_production.py').read())"
    else
        echo -e "${GREEN}Base de datos ya inicializada, saltando inicialización${NC}"
    fi
fi

echo -e "${GREEN}Cargando datos de fixtures...${NC}"
python manage.py loaddata vuln_manager/fixtures/initial_data.json || true

echo -e "${BLUE}Arrancando gunicorn...${NC}"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --timeout 120 