from django.core.exceptions import ValidationError
from model_mommy import mommy
from nose.tools import assert_is_none, assert_raises, assert_equal, assert_true, assert_false
from nose.tools import raises
from devices.models import DeviceType
from devices.models import Device
from devices.models import DeviceStatus
import datetime


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

    def test_should_be_valid_if_purchase_date_is_null(self):
        self.device.asset = 0
        self.device.purchase_date = None
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_first_assignment_date_is_null(self):
        self.device.asset = 0
        self.device.first_assignment_date = None
        assert_is_none(self.device.full_clean())

    def test_mark_assigned_should_set_device_status_to_assigned(self):
        assert_equal(self.device.device_status_name(), DeviceStatus.DISPONIBLE)
        self.device.mark_assigned()
        assert_equal(self.device.device_status_name(), DeviceStatus.ASIGNADO)

    def test_should_identify_as_laptop(self):
        assert_true(self.device.is_laptop())

    def test_should_not_identify_as_laptop(self):
        self.device.device_type = DeviceType.objects.get_or_create(code='Z', name='ZZZZZZZZZZZZZZZ')[0]
        assert_false(self.device.is_laptop())

    def test_should_identify_as_new_laptop(self):
        assert_true(self.device.is_new_laptop())

    def test_should_not_identify_as_new_laptop(self):
        self.device.mark_assigned()
        assert_false(self.device.is_new_laptop())

    def test_should_not_identify_as_new_laptop_if_assigned(self):
        self.device.mark_assigned()
        self.device.first_assignment_date = datetime.date.today()
        self.device.end_date = datetime.date.today()
        assert_false(self.device.is_new_laptop())

    def test_should_not_identify_as_new_laptop_with_first_assignment_date(self):
        self.device.first_assignment_date = datetime.date.today()
        assert_false(self.device.is_new_laptop())

    def test_should_not_identify_as_new_laptop_with_end_date(self):
        self.device.end_date = datetime.date.today()
        assert_false(self.device.is_new_laptop())

    def test_first_assignment_date_should_be_required_if_assigned_laptop(self):
        self.device.mark_assigned()
        self.device.end_date = datetime.date.today()
        assert_raises(ValidationError, self.device.full_clean)

    def test_end_date_should_be_required_if_assigned_laptop(self):
        self.device.mark_assigned()
        self.device.first_assignment_date = datetime.date.today()
        assert_raises(ValidationError, self.device.full_clean)

    def test_should_be_valid_if_assigned_laptop_with_both_dates(self):
        self.device.mark_assigned()
        self.device.first_assignment_date = datetime.date.today()
        self.device.end_date = datetime.date.today()
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_end_date_is_null(self):
        self.device.asset = 0
        self.device.end_date = None
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
        assert_equal(str(Device._meta.ordering), "['device_type']")

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
        assert_equal(self.device.code, 'TWAL')

    def test_should_set_device_code_to_clme(self):
        self.device.device_type = DeviceType.objects.get_or_create(code='M', name='Mouse')[0]
        self.device.asset = 0
        self.device.ownership = 'CL'
        self.device.save()
        assert_equal(self.device.code, 'CLEM')

    def test_should_set_sequence_to_1(self):
        self.device.ownership = 'TW'
        self.device.save()
        assert_equal(self.device.sequence, 1)

    def test_should_set_sequence_to_2(self):
        self.device.ownership = 'TW'
        self.device.save()
        first_device = mommy.prepare_recipe('devices.device_recipe')
        first_device.model = 'model'
        first_device.ownership = 'TW'
        first_device.save()
        assert_equal(first_device.sequence, 2)

    def test_full_code_should_return_twla0001(self):
        self.device.ownership = 'TW'
        self.device.save()
        assert_equal(self.device.full_code(), 'TWAL0001')

    @raises(ValueError)
    def test_should_be_invalid_without_device_status(self):
        self.device.device_status = None

    @raises(ValueError)
    def test_should_be_invalid_without_device_brand(self):
        self.device.device_brand = None

    @raises(ValueError)
    def test_should_be_invalid_without_device_type(self):
        self.device.device_type = None

    def test_device_status_name_should_return_the_name_of_the_device_status(self):
        assert_equal(self.device.device_status_name(), self.device.device_status.name)

    def test_calculate_end_date_should_set_the_date_of_its_life_time(self):
        self.device.save()
        self.device.device_type.life_time = 3
        self.device.first_assignment_date = datetime.date.today()
        self.device.calculate_end_date()
        date_diff = self.device.end_date - self.device.first_assignment_date
        assert_equal(date_diff.days, 3*365)

    @raises(AssertionError)
    def test_calculate_end_dates_should_raise_if_device_type_life_time_is_none(self):
        self.device.first_assignment_date = datetime.date.today()
        self.device.device_type.life_time = None
        self.device.calculate_end_date()

    @raises(AssertionError)
    def test_calculate_end_dates_should_raise_if_device_type_first_assignment_date_is_none(self):
        self.device.first_assignment_date = None
        self.device.device_type.life_time = 3
        self.device.calculate_end_date()

