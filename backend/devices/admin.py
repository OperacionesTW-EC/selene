from django.contrib import admin

# Register your models here.
from devices import models

admin.site.register(models.DeviceType)
admin.site.register(models.DeviceBrand)
admin.site.register(models.Project)
admin.site.register(models.DeviceStatus)
admin.site.register(models.DeviceEndStatusType)
