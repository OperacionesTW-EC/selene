from devices import models


class DeviceStatusService:

    @staticmethod
    def get_filtered_device_statuses():
        return models.DeviceStatus.objects.exclude(name=models.DeviceStatus.ASIGNADO)

    @staticmethod
    def create_status_change_log(device):
        device_status_log = models.DeviceStatusLog(device=device, device_status=device.device_status)
        device_status_log.save()
        return device_status_log


class DeviceService:
    CHANGE_STATUS_ERROR_MESSAGE = 'No se puede cambiar el estado de un dispositivo que está dado de baja'

    @staticmethod
    def change_device_status(device, new_status_id):
        if device.device_status.name != models.DeviceStatus.DADO_DE_BAJA:
            new_status = models.DeviceStatus.objects.get(pk=new_status_id)
            device.device_status = new_status
            device.save()
            DeviceStatusService.create_status_change_log(device)
            return True
        return False
