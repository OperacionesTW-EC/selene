# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-26 16:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0014_auto_20160524_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='life_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tiempo de Vida'),
        )
    ]
