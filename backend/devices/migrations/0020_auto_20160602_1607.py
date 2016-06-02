# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-02 16:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0019_adding_device_statuses'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceStatusLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_change_datetime', models.DateTimeField(default=datetime.datetime(2016, 6, 2, 16, 7, 54, 991161, tzinfo=utc))),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Device')),
                ('device_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.DeviceStatus')),
            ],
        )
    ]