import os
import django
import time
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def wait_for_db():
    db_conn = None
    while not db_conn:
        try:
            db_conn = connections['default']
            db_conn.cursor()
            print('Base de datos disponible')
        except OperationalError:
            print('Esperando a que la base de datos esté disponible...')
            time.sleep(1)

print('Esperando a que la base de datos esté disponible...')
wait_for_db()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='Admin123!'  # Esta será la contraseña
    )
    print('Superusuario creado correctamente')
else:
    print('El superusuario ya existe') 