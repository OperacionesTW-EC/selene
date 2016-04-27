from django.contrib import admin

# Register your models here.
from devices.models import DeviceType

admin.site.register(DeviceType)