# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-13 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0015_device_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='code',
            field=models.CharField(default='TW-N-A-000', max_length=10),
            preserve_default=False,
        ),
    ]
