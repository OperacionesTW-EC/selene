# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-08 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0027_adding_devices_from_csv_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceassignment',
            options={'ordering': ['-assignment__assignment_date', '-id'], 'verbose_name': 'Asignación de Dispositivos', 'verbose_name_plural': 'Asignaciones de Dispositivos'},
        ),
        migrations.AlterField(
            model_name='devicestatuslog',
            name='status_change_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
