import os
import django
import sys
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from vuln_manager.models import Vulnerabilidad

def test_vulnerabilidad():
    # Crear una vulnerabilidad de prueba
    vuln = Vulnerabilidad.objects.create(
        cve_id='CVE-2024-0001',
        descripcion_en='Test vulnerability description in English',
        descripcion_es='Descripción de vulnerabilidad de prueba en español',
        severidad='alta',
        status='published',
        fecha_publicacion=timezone.now().date(),
        fecha_modificacion=timezone.now().date(),
        cvss2_score=7.5,
        cvss2_severidad='alta',
        cvss2_vector='AV:N/AC:L/Au:N/C:P/I:P/A:P',
        cvss3_score=8.8,
        cvss3_severidad='alta',
        cvss3_vector='CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H',
        referencias=[
            'https://example.com/vuln1',
            'https://example.com/vuln2'
        ]
    )
    
    print(f"Vulnerabilidad creada: {vuln.cve_id}")
    print(f"CVSS v2 Score: {vuln.cvss2_score}")
    print(f"CVSS v3 Score: {vuln.cvss3_score}")
    print(f"Referencias: {vuln.referencias}")
    
    return vuln

if __name__ == '__main__':
    test_vulnerabilidad() 