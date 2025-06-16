from django.db import migrations

def ensure_cve_collector(apps, schema_editor):
    TipoTarea = apps.get_model('vuln_manager', 'TipoTarea')
    TipoTarea.objects.get_or_create(
        codigo='cve_collector',
        defaults={
            'nombre': 'Recolector de CVEs',
            'descripcion': 'Recolecta CVEs desde la API de NIST y las almacena en la base de datos.',
            'parametros': {
                'dias_atras': {
                    'tipo': 'number',
                    'label': 'Días hacia atrás',
                    'min': 1,
                    'max': 30,
                    'default': 1,
                    'requerido': True,
                    'descripcion': 'Número de días hacia atrás para buscar CVEs'
                }
            },
            'activo': True
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('vuln_manager', '0011_modify_tarea_model'),
    ]

    operations = [
        migrations.RunPython(ensure_cve_collector),
    ] 