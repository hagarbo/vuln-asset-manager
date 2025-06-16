from django.db import migrations, models
import django.db.models.deletion

def migrar_tareas_existentes(apps, schema_editor):
    Tarea = apps.get_model('vuln_manager', 'Tarea')
    TipoTarea = apps.get_model('vuln_manager', 'TipoTarea')
    
    # Crear el tipo de tarea de CVEs si no existe
    tipo_cve, created = TipoTarea.objects.get_or_create(
        codigo='cve_collector',
        defaults={
            'nombre': 'Recolector de CVEs',
            'descripcion': 'Recolecta CVEs desde la API de NIST y las almacena en la base de datos.',
            'parametros': {"dias_atras": {"tipo": "integer", "min": 1, "max": 30, "default": 1, "descripcion": "Número de días hacia atrás para buscar CVEs"}},
            'activo': True,
        }
    )
    
    # Migrar tareas existentes
    for tarea in Tarea.objects.all():
        if tarea.tipo == 'cve':
            tarea.tipo = tipo_cve
            tarea.parametros = {'dias_atras': tarea.dias_atras}
            tarea.save()

class Migration(migrations.Migration):
    dependencies = [
        ('vuln_manager', '0010_add_tipo_tarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='parametros',
            field=models.JSONField(default=dict, help_text='Valores de los parámetros específicos de la tarea'),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='tipo',
            field=models.ForeignKey(
                help_text='Tipo de tarea a ejecutar',
                on_delete=django.db.models.deletion.PROTECT,
                to='vuln_manager.tipotarea'
            ),
        ),
        migrations.RunPython(migrar_tareas_existentes),
        migrations.RemoveField(
            model_name='tarea',
            name='dias_atras',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='nombre',
        ),
    ] 