# Generated by Django 4.2.10 on 2025-06-16 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vuln_manager', '0014_remove_analista_cliente_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnalistaCliente',
        ),
    ]
