# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-23 22:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0008_auto_20160523_2114'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeviceState',
            new_name='DeviceStatus',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='device_state',
            new_name='device_status',
        ),
    ]
