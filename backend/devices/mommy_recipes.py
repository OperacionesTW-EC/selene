from datetime import date
from model_mommy.recipe import Recipe
import random
from devices.models import *

device_recipe = Recipe(Device,
    device_type = DeviceType.objects.get_or_create(code='L', name='Laptop')[0],
    device_brand = DeviceBrand.objects.get_or_create(name='Some brand')[0],
    device_state = DeviceState.objects.get_or_create(name='Disponible3')[0],
    asset=1,
    ownership=random.choice(['CL', 'TW']),
    serial_number='123123',
    purchase_date=date.today(),
    sequence=random.randint(0, 100),
    code='code'
)