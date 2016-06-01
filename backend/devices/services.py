from devices import models


class DeviceStatusService:

    @staticmethod
    def get_filtered_device_statuses():
        return models.DeviceStatus.objects.exclude(name=models.DeviceStatus.ASIGNADO)
