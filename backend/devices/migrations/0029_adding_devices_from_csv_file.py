from __future__ import unicode_literals

from django.db import migrations
from django.db import transaction
from devices.models import *  # NOQA
from datetime import date, datetime
import os
import sys


@transaction.atomic
def insert_from_csv(apps, schema_editor):
    try:
        FILE_PATH = os.environ['DEVICE_FILE_PATH']
    except Exception:
        migrations_abs_path = os.path.dirname(os.path.realpath(__file__))
        FILE_PATH = '%s/devices.csv' % migrations_abs_path

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
                    'assignment_date': 12,
                    'description': 16
                    }

    def create_assignment(parts, device):
        project = Project.objects.get_or_create(name=parts[FILE_COLUMNS['project_name']].strip().capitalize())[0]
        assignment_date = parts[FILE_COLUMNS['assignment_date']].strip()
        if assignment_date not in (None, ''):
            assignment_date = datetime.strptime(assignment_date, "%m/%d/%Y").date()
        else:
            assignment_date = date.today()
        assignee_name = parts[FILE_COLUMNS['assignee']].strip()
        assignment = Assignment(assignee_name=assignee_name, project=project)
        assignment.save()
        device.assign(assignment_date)
        device.save()
        device_assignment = DeviceAssignment(device=device, assignment=assignment, assignment_date=assignment_date)
        device_assignment.save()



    def print_device_errors(device):
        expected_code = device.generate_code()
        if expected_code != device.code:
            print('El dispositivo %s tiene inconsistencia en los datos, el código recibido fue: %s el generado es: %s' %
                  (device.full_code(), device.code,  expected_code))

    def create_device(parts):
        device_data = {}
        full_code = parts[FILE_COLUMNS['full_code']].strip()
        device_data['device_type'] = DeviceType.objects.get_or_create(name=parts[FILE_COLUMNS['device_type_name']].strip().capitalize(),
                                                                      code=parts[FILE_COLUMNS['device_type_code']].strip().upper())[0]
        device_data['device_brand'] = DeviceBrand.objects.get_or_create(name=parts[FILE_COLUMNS['device_brand_name']].strip().capitalize())[0]
        device_data['device_status'] = DeviceStatus.objects.get_or_create(name=parts[FILE_COLUMNS['device_status_name']].strip().capitalize())[0]
        device_data['code'] = full_code[0:4]
        device_data['sequence'] = int(full_code[4:])
        device_data['asset'] = 1 if parts[FILE_COLUMNS['asset']].strip().lower() == 'si' else 0
        device_data['ownership'] = parts[FILE_COLUMNS['ownership']].strip().upper()
        device_data['serial_number'] = parts[FILE_COLUMNS['serial_number']].strip()
        device_data['description'] = parts[FILE_COLUMNS['description']].strip()
        if parts[FILE_COLUMNS['model']].strip() in (None, ''):
            device_data['model'] = device_data['serial_number']
        else:
            device_data['model'] = parts[FILE_COLUMNS['model']].strip()
        purchase_date = parts[FILE_COLUMNS['purchase_date']].strip()
        if purchase_date not in (None, ''):
            device_data['purchase_date'] = datetime.strptime(purchase_date, '%m/%d/%Y')
        device = Device(**device_data)
        print_device_errors(device)
        return device

    def device_is_present(full_code):
        code = full_code[0:4]
        sequence = int(full_code[4:])
        device = Device.objects.filter(code=code, sequence=sequence)
        if device:
            print('El dispositivo con código %s no se insertó, ya está presente en la base de datos' % full_code)
            return True
        return False

    def parse_line(line):
        parts = line.split(",")
        full_code = parts[FILE_COLUMNS['full_code']].strip()
        if full_code in (None, '') or device_is_present(full_code):
            return
        device = create_device(parts)
        if device.device_status.name == DeviceStatus.ASIGNADO:
            create_assignment(parts, device)
        else:
            device.save()
    if 'test' in sys.argv:  # prevents running the migration when executing manage.py test
        return
    file = open(FILE_PATH, 'r')
    file.readline()
    for line in file:
        parse_line(line)
    file.close()


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0028_auto_20160608_2208'),
    ]
    operations = [
        migrations.RunPython(insert_from_csv),
    ]
