from django.core.exceptions import ValidationError
from nose.tools import *
from devices.factories import *


class TestDevice:

    def setup(self):
        self.device = DeviceFactory.build(asset=0)

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device.full_clean())

    def test_should_be_invalidad_when_ownership_is_larger_than_2(self):
        self.device.ownership = 'qbc'
        assert_raises(ValidationError, self.device.full_clean)

    def test_should_be_valid_if_serial_is_null(self):
        self.device.serial_number = None
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_model_is_null(self):
        self.device.model = None
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_date_is_null(self):
        self.device.purchase_date = None
        assert_is_none(self.device.full_clean())

    def test_serial_number_should_be_required_if_device_is_an_asset(self):
        self.device.asset = 1
        self.device.serial_number = None
        assert_raises(ValidationError, self.device.full_clean)

    def test_model_should_be_required_if_device_is_an_asset(self):
        self.device.asset = 1
        self.device.model = None
        assert_raises(ValidationError, self.device.full_clean)

    def test_purchase_date_should_be_required_if_device_is_an_asset(self):
        self.device.asset = 1
        self.device.purchase_date = None
        assert_raises(ValidationError, self.device.full_clean)
