from django.core.exceptions import ValidationError
from nose.tools import *
from devices.models import DeviceEndStatusType

class TestDeviceStatus:

    def setup(self):
        self.device_end_status_type = DeviceEndStatusType(name='some_type')


    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device_end_status_type.full_clean())


    def test_should_be_invalid_without_name(self):
        self.device_end_status_type.name = None
        assert_raises(ValidationError, self.device_end_status_type.full_clean)


    def test_name_should_be_unique(self):
        DeviceEndStatusType(name='other_type').save()
        another_device_end_status_type = DeviceEndStatusType(name='other_type')
        assert_raises(ValidationError, another_device_end_status_type.full_clean)


    def test_should_show_name_as_string_representation(self):
        assert_equal(str(self.device_end_status_type), 'some_type')


    def test_verbose_name(self):
        assert_equal(str(DeviceEndStatusType._meta.verbose_name), "Tipo de Baja")


    def test_verbose_name_plural(self):
        assert_equal(str(DeviceEndStatusType._meta.verbose_name_plural), "Tipos de Baja")


    def test_model_is_registered_in_admin(self):
        from django.contrib import admin
        assert_true(DeviceEndStatusType in admin.site._registry)