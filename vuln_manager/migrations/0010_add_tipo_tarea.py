from django.db import migrations, models
import django.db.models.deletion

def crear_tipo_tarea_cve(apps, schema_editor):
    TipoTarea = apps.get_model('vuln_manager', 'TipoTarea')
    TipoTarea.objects.create(
        codigo='cve_collector',
        nombre='Recolector de CVEs',
        descripcion='Recolecta CVEs desde la API de NIST y las almacena en la base de datos.',
        parametros={
            'dias_atras': {
                'tipo': 'integer',
                'min': 1,
                'max': 30,
                'default': 1,
                'descripcion': 'Número de días hacia atrás para buscar CVEs'
            }
        },
        activo=True
    )

class Migration(migrations.Migration):
    dependencies = [
        ('vuln_manager', '0009_remove_ejecuciontarea_cves_rechazadas'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoTarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(help_text='Código único para identificar el tipo de tarea', max_length=50, unique=True)),
                ('nombre', models.CharField(help_text='Nombre descriptivo del tipo de tarea', max_length=100)),
                ('descripcion', models.TextField(help_text='Descripción detallada del tipo de tarea')),
                ('parametros', models.JSONField(default=dict, help_text='Configuración de parámetros específicos para este tipo de tarea')),
                ('activo', models.BooleanField(default=True, help_text='Indica si este tipo de tarea está disponible para su uso')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Tipo de Tarea',
                'verbose_name_plural': 'Tipos de Tarea',
                'ordering': ['nombre'],
            },
        ),
        migrations.RunPython(crear_tipo_tarea_cve),
    ] 