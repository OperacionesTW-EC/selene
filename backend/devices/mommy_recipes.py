from datetime import date
from model_mommy.recipe import Recipe
import random
from model_mommy import mommy
from devices import models

assignment_recipe = Recipe(models.Assignment,
                           project=models.Project.objects.get_or_create(name='Some project')[0],
                           assignee_name='Nombre Apellido'
                           )

device_recipe = Recipe(models.Device,
                       device_type=models.DeviceType.objects.get_or_create(code='L', name='Laptop')[0],
                       device_brand=models.DeviceBrand.objects.get_or_create(name='Some brand')[0],
                       device_status=models.DeviceStatus.objects.get_or_create(name=models.DeviceStatus.DISPONIBLE)[0],
                       asset=1,
                       ownership=random.choice(['CL', 'TW']),
                       serial_number='123123',
                       purchase_date=date.today(),
                       sequence=None,
                       code=None
                       )


non_asset_device_recipe = Recipe(models.Device,
                                 device_type=models.DeviceType.objects.get_or_create(code='L', name='Laptop')[0],
                                 device_brand=models.DeviceBrand.objects.get_or_create(name='Some brand')[0],
                                 device_status=models.DeviceStatus.objects.get_or_create(name=models.DeviceStatus.DISPONIBLE)[0],
                                 asset=0,
                                 sequence=random.randint(0, 100),
                                 code='code'
                                 )

device_assignment_recipe = Recipe(models.DeviceAssignment,
                                  device=mommy.prepare_recipe('devices.non_asset_device_recipe'),
                                  assignment=mommy.prepare_recipe('devices.assignment_recipe'),
                                  assignment_date=date.today()
                                  )
