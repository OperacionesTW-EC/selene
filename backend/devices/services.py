from django.core.exceptions import ValidationError

from devices import models
from datetime import date


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


class AssignmentService:

    def __init__(self, assignment, devices_ids):
        self.assignment = assignment
        self.devices = []
        self.errors = []
        self.load_devices(devices_ids)

    def load_devices(self, devices_ids):
        for device_id in devices_ids:
            try:
                self.devices.append(models.Device.objects.get(pk=device_id))
            except models.Device.DoesNotExist:
                self.errors.append({'error': 'No se encontró el dispositivo: %s' % device_id})

    def create_assignment(self):
        self.assignment.assignment_date = date.today()
        if self.save_assignment() and not self.errors:
            self.update_devices()
            self.create_device_assignment()
            return True
        return False

    def save_assignment(self):
        try:
            self.assignment.full_clean()
            self.assignment.save()
            return True
        except ValidationError as errors:
            self.errors = errors.message_dict
            return False

    def update_devices(self):
        for device in self.devices:
            if device.is_new_laptop():
                device.laptop_begin_life = date.today()
                device.calculate_laptop_end_life()
            device.mark_assigned()
            device.save()

    def create_device_assignment(self):
        for device in self.devices:
            device_assignment = models.DeviceAssignment(device=device, assignment=self.assignment)
            device_assignment.save()
