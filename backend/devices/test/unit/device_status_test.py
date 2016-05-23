from django.core.exceptions import ValidationError
from nose.tools import *
from devices.models import DeviceStatus

class TestDeviceStatus:

    def setup(self):
        self.device_status = DeviceStatus(name='some_name')

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device_status.full_clean())

    def test_should_be_invalid_without_name(self):
        self.device_status.name = None
        assert_raises(ValidationError, self.device_status.full_clean)

    def test_name_should_be_unique(self):
        DeviceStatus(name='same_name').save()
        another_device = DeviceStatus(name='same_name')
        assert_raises(ValidationError, another_device.full_clean)

    def test_should_show_name_as_string_representation(self):
        assert_equal(str(self.device_status), 'some_name')

    def test_verbose_name(self):
        assert_equal(str(DeviceStatus._meta.verbose_name), "Estado de Dispositivo")

    def test_verbose_name_plural(self):
        assert_equal(str(DeviceStatus._meta.verbose_name_plural), "Estados de Dispositivo")

    def test_model_is_registered_in_admin(self):
        from django.contrib import admin
        assert_true(DeviceStatus in admin.site._registry)

