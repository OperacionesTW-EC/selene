from django.core.exceptions import ValidationError
from nose.tools import *
from devices.models import DeviceBrand

class TestDeviceBrand:

    def setup(self):
        self.device_brand = DeviceBrand(name='some_name')

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device_brand.full_clean())

    def test_should_be_invalid_without_name(self):
        self.device_brand.name = None
        assert_raises(ValidationError, self.device_brand.full_clean)

    def test_name_should_be_unique(self):
        DeviceBrand(name='same_name').save()
        another_device = DeviceBrand(name='same_name')
        assert_raises(ValidationError, another_device.full_clean)

    def test_should_be_invalid_with_name_too_long(self):
        self.device_brand.name = 'This name is too long and has more than 50 characters, so it is invalid'
        assert_raises(ValidationError, self.device_brand.full_clean)

    def test_should_show_name_as_string_representation(self):
        assert_equal(str(self.device_brand), 'some_name')

    def test_verbose_name(self):
        assert_equal(str(DeviceBrand._meta.verbose_name), "Marca de Dispositivo")

    def test_verbose_name_plural(self):
        assert_equal(str(DeviceBrand._meta.verbose_name_plural), "Marcas de Dispositivo")

    def test_model_is_registered_in_admin(self):
        from django.contrib import admin
        assert_true(DeviceBrand in admin.site._registry)