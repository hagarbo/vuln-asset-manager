from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer la variable de entorno por defecto para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('vuln_manager')

# Usar la configuración de Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas de todas las apps registradas
app.autodiscover_tasks() 