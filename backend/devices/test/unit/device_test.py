from django.core.exceptions import ValidationError
from model_mommy import mommy
from nose.tools import *
from devices.models import DeviceType
from devices.models import DeviceBrand
from devices.models import Device
from datetime import date


class TestDevice:

    def __init__(self):
        self.device = None
        self.device_brand = None
        self.device_type = None

    def setup(self):
        Device.objects.all().delete()
        self.device = mommy.prepare_recipe('devices.device_recipe')
        self.device.model = 'model'

    def test_should_be_valid_with_valid_field_values(self):
        assert_is_none(self.device.full_clean())

    def test_should_be_invalid_when_ownership_is_larger_than_2(self):
        self.device.ownership = 'qbc'
        assert_raises(ValidationError, self.device.full_clean)

    def test_should_be_valid_if_serial_is_null(self):
        self.device.asset = 0
        self.device.serial_number = None
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_model_is_null(self):
        self.device.asset = 0
        self.device.model = None
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_date_is_null(self):
        self.device.asset = 0
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

    def test_should_be_ordered_by_device_type(self):
        assert_equal(str(Device._meta.ordering), "[u'device_type']")

    def test_device_type_name_should_return_the_name_of_the_device_type(self):
        assert_equal(self.device.device_type_name(), self.device.device_type.name)

    def test_device_brand_name_should_return_the_name_of_the_device_brand(self):
        assert_equal(self.device.device_brand_name(), self.device.device_brand.name)

    def test_sequence_should_be_required(self):
        self.device.sequence = None
        assert_raises(ValidationError, self.device.full_clean)

    def test_code_should_be_required(self):
        self.device.code = None
        assert_raises(ValidationError, self.device.full_clean)

    def test_should_set_device_code_to_twla(self):
        self.device.ownership = 'TW'
        self.device.save()
        assert_equals(self.device.code, 'TWAL')

    def test_should_set_device_code_to_clme(self):
        self.device.device_type = DeviceType.objects.get_or_create(code='M', name='Mouse')[0]
        self.device.asset = 0
        self.device.ownership = 'CL'
        self.device.save()
        assert_equals(self.device.code, 'CLEM')

    def test_should_set_sequence_to_1(self):
        self.device.ownership = 'TW'
        self.device.save()
        assert_equals(self.device.sequence, 1)

    def test_should_set_sequence_to_2(self):
        self.device.ownership = 'TW'
        self.device.save()
        first_device = mommy.prepare_recipe('devices.device_recipe')
        first_device.model = 'model'
        first_device.ownership = 'TW'
        first_device.save()
        assert_equals(first_device.sequence, 2)

    def test_full_code_should_return_twla0001(self):
        self.device.ownership = 'TW'
        self.device.save()
        assert_equals(self.device.full_code(), 'TWAL0001')