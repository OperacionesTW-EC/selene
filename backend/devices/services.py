from django.core.exceptions import ValidationError
from devices import models
from datetime import date


class DeviceStatusService:
    @staticmethod
    def get_filtered_device_statuses_without_assigned   ():
        return models.DeviceStatus.objects.exclude(name=models.DeviceStatus.ASIGNADO)

    @staticmethod
    def create_status_change_log(device):
        device_status_log = models.DeviceStatusLog(device=device, device_status=device.device_status)
        device_status_log.save()
        return device_status_log


class DeviceEndStatusTypeService:
    @staticmethod
    def get_filtered_device_end_status_types():
        return models.DeviceEndStatusType.objects.order_by('id')


class DeviceService:
    CHANGE_STATUS_ERROR_MESSAGE = 'No se pudo cambiar el estado del dispositivo'

    @staticmethod
    def update_return_date_of_device_assignment(device):
        if device.is_Asignado():
            device_assignment = DeviceService.get_last_device_assignment(device)
            device_assignment.update_return_date_to_today()
            device_assignment.save()

    @staticmethod
    def get_last_device_assignment(device):
        device_assignments = models.DeviceAssignment.objects.filter(device=device).order_by('id')
        if device_assignments:
            return device_assignments.last()

    @staticmethod
    def change_device_status(device, new_status_id, new_device_end_status_type_id, new_device_end_status_type_comment):
        if not device.is_Dado_Baja():
            DeviceService.update_return_date_of_device_assignment(device)
            device.device_status = models.DeviceStatus.objects.get(pk=new_status_id)
            device.device_end_status_type = DeviceService.set_end_status_type(new_device_end_status_type_id)
            device.device_end_status_comment = new_device_end_status_type_comment
            device.save()
            DeviceStatusService.create_status_change_log(device)
        else:
            raise ValidationError(
                ('El dispositivo esta Dado de Baja no puede cambiar su estado'),
                code='invalid')

    @staticmethod
    def set_end_status_type(new_device_end_status_type_id):
        if new_device_end_status_type_id:
            return models.DeviceEndStatusType.objects.get(pk=new_device_end_status_type_id)
        else:
            return None



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
            device.assign()
            device.save()

    def create_device_assignment(self):
        for device in self.devices:
            device_assignment = models.DeviceAssignment(device=device, assignment=self.assignment,
                                                        assignment_date=date.today())
            device_assignment.save()