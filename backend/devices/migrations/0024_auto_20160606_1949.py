# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-06 19:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0023_auto_20160607_1348'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='laptop_begin_life',
            new_name='life_start_date',
        ),
        migrations.RemoveField(
            model_name='device',
            name='laptop_end_life',
        ),
        migrations.AlterField(
            model_name='devicestatuslog',
            name='status_change_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 6, 19, 49, 37, 229589, tzinfo=utc)),
        ),
    ]