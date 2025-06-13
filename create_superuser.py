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
            # Mostrar información de conexión (sin la contraseña)
            db_settings = connections['default'].settings_dict
            print(f"Intentando conectar a la base de datos:")
            print(f"  Host: {db_settings['HOST']}")
            print(f"  Puerto: {db_settings['PORT']}")
            print(f"  Base de datos: {db_settings['NAME']}")
            print(f"  Usuario: {db_settings['USER']}")
            
            db_conn = connections['default']
            db_conn.cursor()
            print('Base de datos disponible')
        except OperationalError as e:
            print(f'Error al conectar: {str(e)}')
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