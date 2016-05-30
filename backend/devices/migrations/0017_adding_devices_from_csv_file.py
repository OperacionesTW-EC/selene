from __future__ import unicode_literals
from django.db import migrations
from devices.models import *
from datetime import datetime
from django.utils import timezone
from dateutil import parser
import os


def insert_from_csv(apps, schema_editor):
    try:
        FILE_PATH = os.environ['DEVICE_FILE_PATH']
    except Exception:
        FILE_PATH = 'devices/migrations/devices.csv'

    FILE_COLUMNS = {'full_code': 0,
                    'device_type_name': 1,
                    'asset': 2,
                    'ownership': 3,
                    'serial_number': 4,
                    'device_type_code': 5,
                    'device_brand_name': 6,
                    'model': 7,
                    'purchase_date': 8,
                    'project_name': 9,
                    'device_status_name': 10,
                    'assignee': 11,
                    'assignment_date': 12
                    }

    def create_device(parts):
        device_data = {}
        full_code = parts[FILE_COLUMNS['full_code']].strip()
        device_data['device_type'] = DeviceType.objects.get_or_create(name=parts[FILE_COLUMNS['device_type_name']].strip().capitalize(), code=parts[FILE_COLUMNS['device_type_code']].strip().upper())[0]
        device_data['device_brand'] = DeviceBrand.objects.get_or_create(name=parts[FILE_COLUMNS['device_brand_name']].strip().capitalize())[0]
        device_data['device_status'] = DeviceStatus.objects.get_or_create(name=parts[FILE_COLUMNS['device_status_name']].strip().capitalize())[0]
        device_data['code'] = full_code[0:4]
        device_data['sequence'] = int(full_code[4:])
        device_data['asset'] = 1 if parts[FILE_COLUMNS['asset']].strip().lower() == 'si' else 0
        device_data['ownership'] = parts[FILE_COLUMNS['ownership']].strip().upper()
        device_data['serial_number'] = parts[FILE_COLUMNS['serial_number']].strip()
        if parts[FILE_COLUMNS['model']].strip() in (None, ''):
            device_data['model'] = device_data['serial_number']
        else:
            device_data['model'] = parts[FILE_COLUMNS['model']].strip()
        purchase_date = parts[FILE_COLUMNS['purchase_date']].strip()
        if purchase_date not in (None, ''):
            device_data['purchase_date'] = datetime.strptime(purchase_date, '%m/%d/%Y')
        device = Device.objects.get_or_create(**device_data)[0]
        return device

    def create_assignment(parts, device):
        project = Project.objects.get_or_create(name=parts[FILE_COLUMNS['project_name']].strip().capitalize())[0]
        assignment_date = parts[FILE_COLUMNS['assignment_date']].strip()
        if assignment_date not in (None, ''):
            assignment_date = parser.parse(assignment_date + ' 10:00:00 -0500')
        else:
            assignment_date = timezone.now()
        assignee_name = parts[FILE_COLUMNS['assignee']].strip()
        assignment = Assignment(assignee_name=assignee_name, assignment_datetime=assignment_date, project=project)
        assignment.save()
        device_assignment = DeviceAssignment(device=device, assignment=assignment)
        device_assignment.save()

    def parse_line(line):
        parts = line.decode('UTF-8').split(",")
        full_code = parts[FILE_COLUMNS['full_code']].strip()
        if full_code in (None, ''): return
        device = create_device(parts)
        if device.device_status.name == DeviceStatus.ASIGNADO:
            create_assignment(parts, device)

    file = open(FILE_PATH, 'r')
    file.readline()
    for line in file:
        parse_line(line)
    file.close()


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0016_merge'),
    ]
    operations = [
        migrations.RunPython(insert_from_csv),
    ]



