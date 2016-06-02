from django.core.exceptions import ValidationError
from nose.tools import *
from devices import models
from model_mommy import mommy

class TestDeviceStatusLog:

    def __init__(self):
        self.device_status_log = None

    def setup(self):
        device = mommy.prepare_recipe('devices.device_recipe')
        device.model = 'model'
        device.save()
        status = models.DeviceStatus.objects.get_or_create(name=models.DeviceStatus.DISPONIBLE)[0]
        self.device_status_log = models.DeviceStatusLog(device=device, device_status=status)

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device_status_log.full_clean())

    @raises(ValueError)
    def test_should_be_invalid_without_device(self):
        self.device_status_log.device = None

    @raises(ValueError)
    def test_should_be_invalid_without_device_status(self):
        self.device_status_log.device_status = None

    def test_should_set_status_change_datetime_by_default(self):
        self.device_status_log.save()
        assert_is_not_none(self.device_status_log.status_change_datetime)





