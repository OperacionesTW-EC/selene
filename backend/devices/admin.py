from django.contrib import admin

# Register your models here.
from devices.models import *

admin.site.register(DeviceType)
admin.site.register(DeviceBrand)
admin.site.register(Project)
admin.site.register(DeviceState)