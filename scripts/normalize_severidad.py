import os
import sys
import django

# Añadir la raíz del proyecto al PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vuln_manager.models import Vulnerabilidad
from vuln_manager.repository.vulnerabilidad.vulnerabilidad_repository import VulnerabilidadRepository

repo = VulnerabilidadRepository()

count = 0
for v in Vulnerabilidad.objects.all():
    nueva = repo._map_severidad(v.severidad)
    if v.severidad != nueva:
        v.severidad = nueva
        v.save(update_fields=["severidad"])
        count += 1

print(f"Valores de severidad normalizados en {count} vulnerabilidades.") 