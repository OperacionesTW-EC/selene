# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-27 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_devicetype_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicetype',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre'),
        ),
    ]
