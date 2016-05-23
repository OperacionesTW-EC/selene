from datetime import date
from model_mommy.recipe import Recipe
import random
from model_mommy import mommy
from devices.models import *

assignment_recipe = Recipe(Assignment,
                           project=Project.objects.get_or_create(name='Futbolmatch')[0],
                           assignee_name='Nombre Apellido'
                           )

device_recipe = Recipe(Device,
                       device_type=DeviceType.objects.get_or_create(code='L', name='Laptop')[0],
                       device_brand=DeviceBrand.objects.get_or_create(name='Some brand')[0],
                       device_status=DeviceStatus.objects.get_or_create(name='Disponible3')[0],
                       asset=1,
                       ownership=random.choice(['CL', 'TW']),
                       serial_number='123123',
                       purchase_date=date.today(),
                       sequence=random.randint(0, 100),
                       code='code'
                       )

device_assignment_recipe = Recipe(DeviceAssignment,
                                  device=mommy.prepare_recipe('devices.device_recipe'),
                                  assignment=mommy.prepare_recipe('devices.assignment_recipe')
                                  )
