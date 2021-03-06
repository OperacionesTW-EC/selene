# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-12 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0031_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceassignment',
            options={'ordering': ['-assignment_date', '-id'], 'verbose_name': 'Asignación de Dispositivos', 'verbose_name_plural': 'Asignaciones de Dispositivos'},
        ),
        migrations.AlterModelOptions(
            name='deviceendstatustype',
            options={'ordering': ['name'], 'verbose_name': 'Tipo de Baja', 'verbose_name_plural': 'Tipos de Baja'},
        ),
        migrations.AddField(
            model_name='device',
            name='device_end_status_comment',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='device_end_status_type',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deviceendstatustype',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
