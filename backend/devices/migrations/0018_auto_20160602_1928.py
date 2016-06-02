# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-02 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0017_update_laptop_devices_life_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deviceassignment',
            options={'ordering': ['-assignment_date'], 'verbose_name': 'Asignación de Dispositivos', 'verbose_name_plural': 'Asignaciones de Dispositivos'},
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='assignment_datetime',
        ),
        migrations.AddField(
            model_name='device',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='first_assignment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='deviceassignment',
            name='assignment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
