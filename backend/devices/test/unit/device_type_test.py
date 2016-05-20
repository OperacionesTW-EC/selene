from django.core.exceptions import ValidationError
from nose.tools import *
from devices.models import DeviceType
from model_mommy import mommy


class TestDeviceType:

    def setup(self):
        self.device_type, _ = DeviceType.objects.get_or_create(code='L', name='Laptop')

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device_type.full_clean())

    def test_should_be_invalid_without_name(self):
        self.device_type.name = None
        assert_raises(ValidationError, self.device_type.full_clean)

    def test_should_be_invalid_with_name_too_long(self):
        self.device_type.name = 'This name is too long and has more than 50 characters, so it is invalid'
        assert_raises(ValidationError, self.device_type.full_clean)

    def test_name_should_be_unique(self):
        mommy.make('DeviceType', name='Some name', code='X')
        another_device = mommy.prepare('DeviceType', name='Some name', code='X')
        assert_raises(ValidationError, another_device.full_clean)

    def test_should_be_invalid_without_code(self):
        self.device_type.code = None
        assert_raises(ValidationError, self.device_type.full_clean)

    def test_should_be_invalid_with_code_too_long(self):
        self.device_type.code = 'AB'
        assert_raises(ValidationError, self.device_type.full_clean)

    def test_code_should_be_unique(self):
        mommy.make('DeviceType', code='D')
        another_device = mommy.prepare('DeviceType', code='D')
        assert_raises(ValidationError, another_device.full_clean)

    def test_should_show_name_and_code_as_string_representation(self):
        assert_equal(str(self.device_type), '%s (%s)' % (self.device_type.name, self.device_type.code))

    def test_model_is_registered_in_admin(self):
        from django.contrib import admin
        assert_true(DeviceType in admin.site._registry)

    def test_verbose_name(self):
        assert_equal(str(DeviceType._meta.verbose_name), "Tipo de Dispositivo")

    def test_verbose_name_plural(self):
        assert_equal(str(DeviceType._meta.verbose_name_plural), "Tipos de Dispositivo")
