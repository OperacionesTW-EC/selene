from __future__ import unicode_literals
from django.db import migrations

# Even though the parameters are not used, they are required by django


def update_laptop_device_type(apps, schema_editor):
    from devices.models import DeviceType
    device = DeviceType.objects.get_or_create(code=DeviceType.LAPTOP_CODE, name=DeviceType.LAPTOP_NAME)[0]
    device.life_time = 3
    device.save()


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0016_merge'),
    ]
    operations = [
        migrations.RunPython(update_laptop_device_type),
    ]
