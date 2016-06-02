from __future__ import unicode_literals
from django.db import migrations

# Even though the parameters are not used, they are required by django


def create_device_status(apps, schema_editor):
    from devices.models import DeviceStatus
    DeviceStatus.objects.get_or_create(name=DeviceStatus.MANTENIMIENTO)
    DeviceStatus.objects.get_or_create(name=DeviceStatus.DADO_DE_BAJA)


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0018_update_laptop_devices_life_time'),
    ]
    operations = [
        migrations.RunPython(create_device_status),
    ]
