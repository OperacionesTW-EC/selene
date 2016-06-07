from __future__ import unicode_literals
from django.db import migrations
from devices.models import *  # NOQA
from datetime import date, datetime
import os


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
                    'assignment_date': 12
                    }

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
        if parts[FILE_COLUMNS['model']].strip() in (None, ''):
            device_data['model'] = device_data['serial_number']
        else:
            device_data['model'] = parts[FILE_COLUMNS['model']].strip()
        purchase_date = parts[FILE_COLUMNS['purchase_date']].strip()
        if purchase_date not in (None, ''):
            device_data['purchase_date'] = datetime.strptime(purchase_date, '%m/%d/%Y')
        device = Device(**device_data)
        return device

    def create_assignment(parts, device):
        project = Project.objects.get_or_create(name=parts[FILE_COLUMNS['project_name']].strip().capitalize())[0]
        assignment_date = parts[FILE_COLUMNS['assignment_date']].strip()
        if assignment_date not in (None, ''):
            assignment_date = datetime.strptime(assignment_date, "%m/%d/%Y").date()  
        else:
            assignment_date = date.today()
        assignee_name = parts[FILE_COLUMNS['assignee']].strip()
        assignment = Assignment(assignee_name=assignee_name, project=project, assignment_date=assignment_date)
        validate(assignment)
        assignment.save()
        device.assign(assignment_date)
        validate(device)
        device.save()
        device_assignment = DeviceAssignment(device=device, assignment=assignment)
        validate(device_assignment)
        device_assignment.save()

    def validate(model):
        try:
            getattr(model, 'full_clean')()
        except ValidationError as e:
            print(model.__dict__)
            raise e

    def composite_key_parts(full_code):
        c, s = full_code[0:4], int(full_code[4:])
        return c, s

    def exists(code, sequence, serial):
        if Device.objects.filter(code=code, sequence=sequence):
            return True
        if serial not in (None, '') and Device.objects.filter(serial_number=serial):
            return True

    def should_skip(full_code, serial):
        if full_code in (None, ''):
            return True
        #  if exists(full_code, serial):
            #  return True

    def parse_line(line):
        parts = line.split(",")
        full_code = parts[FILE_COLUMNS['full_code']].strip()
        code, seq = composite_key_parts(full_code)
        serial = parts[FILE_COLUMNS['serial_number']].strip()
        if full_code in (None, ''):
            return
        #  if exists(code, seq):
            #  return
        print('Loading: %s %s %s, %s' % (full_code, code, seq, serial))

        device = create_device(parts)
        if device.device_status.name == DeviceStatus.ASIGNADO:
            create_assignment(parts, device)
        else:
            validate(device)
            device.save()

    print('\n_______ BEGIN _______')
    with open(FILE_PATH, 'r') as f:
        f.readline()
        for line in f:
            parse_line(line.rstrip())


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0024_auto_20160607_1326'),
    ]
    operations = [
        migrations.RunPython(insert_from_csv),
    ]

