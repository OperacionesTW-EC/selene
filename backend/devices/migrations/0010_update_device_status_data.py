# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-23 22:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_auto_20160523_2208'),
    ]

    operations = [
        migrations.RunSQL("update devices_devicestatus set name = 'No Disponible' WHERE name = 'No disponible'"),
    ]