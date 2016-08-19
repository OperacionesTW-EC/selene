from __future__ import unicode_literals

from django.db import migrations
from django.db import transaction
from devices.models import *;
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

    DeviceHistoric = apps.get_model("devices", "Device")
    ProjectHistoric = apps.get_model("devices", "Project")
    AssignmentHistoric = apps.get_model("devices", "Assignment")
    DeviceAssignmentHistoric = apps.get_model("devices", "DeviceAssignment")
    DeviceTypeHistoric = apps.get_model("devices", "DeviceType")
    DeviceBrandHistoric = apps.get_model("devices", "DeviceBrand")
    DeviceStatusHistoric = apps.get_model("devices", "DeviceStatus")


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

    def has_lifetime(device_type):
        if device_type.life_time is None:
            return False
        return True

    def has_lifetime_and_life_has_not_begun(device):
        return has_lifetime(device.device_type) and device.life_start_date in (None, '')

    def assign(device, date=None):
        if has_lifetime_and_life_has_not_begun(device):
            device.life_start_date = date or datetime.date.today()

    def create_assignment(parts, device):
        project = ProjectHistoric.objects.get_or_create(name=get_column_value(parts, 'project_name').capitalize())[0]
        assignment_date = get_column_value(parts, 'assignment_date')
        if assignment_date not in (None, ''):
            assignment_date = datetime.strptime(assignment_date, "%m/%d/%Y").date()
        else:
            assignment_date = date.today()
        assignee_name = get_column_value(parts, 'assignee')
        assignment = AssignmentHistoric(assignee_name=assignee_name, project=project)
        assignment.save()

        assign(device, assignment_date)

        device.save()
        device_assignment = DeviceAssignmentHistoric(device=device, assignment=assignment, assignment_date=assignment_date)
        device_assignment.save()

    def is_code_device_valid(device):
        expected_code = device.generate_code()
        is_valid = expected_code == device.code
        return is_valid

    def print_log_device_does_not_migrate(device):
        sequence_with_format = '{0:04d}'.format(device.sequence)
        print('El dispositivo con código %s%s no se insertó, ya que su código %s debe ser %s' % (device.code, sequence_with_format, device.code, device.full_code()))

    def create_device(parts):
        device_data = {}
        full_code = get_column_value(parts, 'full_code')
        device_data['device_type'] = create_device_type(parts)
        device_data['device_brand'] = create_device_brand(parts)
        device_data['device_status'] = create_devices_status(parts)
        device_data['code'] = full_code[0:4]
        device_data['sequence'] = int(full_code[4:])
        device_data['asset'] = 1 if get_column_value(parts,'asset').lower() == 'si' else 0
        device_data['ownership'] = get_column_value(parts,'ownership').upper()
        device_data['serial_number'] = get_column_value(parts,'serial_number')
        device_data['description'] = get_column_value(parts,'description')

        if get_column_value(parts,'model') in (None, ''):
            device_data['model'] = device_data['serial_number']
        else:
            device_data['model'] = get_column_value(parts,'model')
        purchase_date = get_column_value(parts,'purchase_date')

        if purchase_date not in (None, ''):
            device_data['purchase_date'] = datetime.strptime(purchase_date, '%m/%d/%Y')
        device = DeviceHistoric(**device_data)

        return device

    def get_column_value(parts, name_column):
        return parts[FILE_COLUMNS[name_column]].strip()

    def create_device_type(parts):
        return DeviceTypeHistoric.objects.get_or_create(name=get_column_value(parts, 'device_type_name').capitalize(),
                                         code=get_column_value(parts, 'device_type_code').upper())[0]

    def create_device_brand(parts):
        return DeviceBrandHistoric.objects.get_or_create(name=get_column_value(parts, 'device_brand_name').capitalize())[0]

    def create_devices_status(parts):
        return DeviceStatusHistoric.objects.get_or_create(name=get_column_value(parts, 'device_status_name').capitalize())[0]

    def device_is_present(full_code):
        code = full_code[0:4]
        sequence = int(full_code[4:])
        device = DeviceHistoric.objects.filter(code=code, sequence=sequence)
        if device:
            print('El dispositivo con código %s no se insertó, ya está presente en la base de datos' % full_code)
            return True
        return False

    def parse_line(line):
        parts = line.split(",")
        full_code = get_column_value(parts,'full_code')
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
