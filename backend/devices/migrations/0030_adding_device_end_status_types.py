from __future__ import unicode_literals
from django.db import migrations
from django.db import models


# Even though the parameters are not used, they are required by django


def create_device_end_status_type(apps, schema_editor):
    from devices.models import DeviceEndStatusType
    DeviceEndStatusType.objects.get_or_create(name=DeviceEndStatusType.DAÑADO)
    DeviceEndStatusType.objects.get_or_create(name=DeviceEndStatusType.VENDIDO)
    DeviceEndStatusType.objects.get_or_create(name=DeviceEndStatusType.ROBADO)
    DeviceEndStatusType.objects.get_or_create(name=DeviceEndStatusType.DONADO)
    DeviceEndStatusType.objects.get_or_create(name=DeviceEndStatusType.PERDIDO)


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0018_auto_20160602_1928'),
    ]
    operations = [
        migrations.CreateModel(
            name='DeviceEndStatusType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50))
            ],
            options={
                'verbose_name': u'Tipo de Baja',
                'verbose_name_plural': 'Tipos de Baja',
            },
        ),
        migrations.RunPython(create_device_end_status_type)
    ]
