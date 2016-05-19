# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-19 21:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignee_name', models.CharField(max_length=50)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.Assignment')),
            ],
            options={
                'verbose_name': u'Asignación',
                'verbose_name_plural': 'Asignaciones',
            },
        ),
    ]
