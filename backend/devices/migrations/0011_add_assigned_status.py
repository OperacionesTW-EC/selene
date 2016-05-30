from __future__ import unicode_literals
from django.db import migrations

# Even though the parameters are not used, they are required by django


def insert_assigned_status(apps, schema_editor):
    from devices.models import DeviceStatus
    DeviceStatus.objects.get_or_create(name=DeviceStatus.ASIGNADO)


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_auto_20160523_2208'),
    ]
    operations = [
        migrations.RunPython(insert_assigned_status),
    ]



