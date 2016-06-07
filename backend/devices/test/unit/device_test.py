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
        self.device.device_type = DeviceType.objects.get_or_create(code='L', name='Laptop')[0]
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

    def test_should_be_valid_if_description_is_null(self):
        self.device.description = None
        assert_is_none(self.device.full_clean())

    def test_should_be_valid_if_description_is_blank(self):
        self.device.description = ''
        assert_is_none(self.device.full_clean())

    @raises(ValidationError)
    def test_should_be_invalid_if_description_is_longer_than_250_characters(self):
        self.device.description = ''
        for _ in range(251):
            self.device.description += 'A'
        self.device.full_clean()

    def test_should_be_valid_if_life_start_date_is_none(self):
        self.device.asset = 0
        self.device.life_start_date = None
        assert_is_none(self.device.full_clean())

    def test_should_say_if_has_lifetime(self):
        assert_true(self.device.has_lifetime())

    def test_should_not_say_that_has_lifetime(self):
        self.device.device_type = DeviceType.objects.get_or_create(code='Z', name='ZZZZZZZZZZZZZZZ')[0]
        assert_false(self.device.has_lifetime())

    def test_should_say_if_life_has_not_begun_for_device_with_lifetime(self):
        assert_true(self.device.life_has_not_begun())
        assert_false(self.device.life_has_begun())

    def test_should_say_if_life_has_begun_for_device_with_lifetime_and_start_date(self):
        self.device.life_start_date = datetime.date.today()
        assert_true(self.device.life_has_begun())
        assert_false(self.device.life_has_not_begun())

    def test_life_start_date_should_be_required_for_device_with_lifetime(self):
        self.device.mark_assigned()
        assert_raises(ValidationError, self.device.full_clean)

    def test_should_be_valid_if_has_lifetime_has_start_date_and_is_assigned(self):
        self.device.mark_assigned()
        self.device.life_start_date = datetime.date.today()
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

    def test_calculate_life_end_date_should_return_date_for_device_with_lifetime(self):
        self.device.save()
        self.device.device_type.life_time = 3
        self.device.life_start_date = datetime.date.today()
        actual_life_end_date = self.device.calculate_life_end_date()
        date_diff = actual_life_end_date - self.device.life_start_date
        assert_equal(date_diff.days, 3*365)

    def test_calculate_life_end_date_should_return_none_for_device_without_lifetime(self):
        self.device.life_start_date = datetime.date.today()
        self.device.device_type.life_time = None
        result = self.device.calculate_life_end_date()
        assert_is_none(result)

    def test_calculate_life_end_date_should_return_none_if_life_has_not_begun(self):
        self.device.life_start_date = None
        self.device.device_type.life_time = 3
        result = self.device.calculate_life_end_date()
        assert_is_none(result)

    def test_assign_should_set_life_start_date_for_device_with_lifetime_without_start_date(self):
        self.device.life_start_date = None
        self.device.device_type.life_time = 3
        self.device.assign()
        assert_equal(self.device.life_start_date, datetime.date.today())
        assert_equal(self.device.device_status_name(), DeviceStatus.ASIGNADO)

    def test_assign_should_not_set_life_start_date_for_device_with_start_date(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        self.device.life_start_date = yesterday
        self.device.device_type.life_time = 3
        self.device.assign()
        assert_equal(self.device.life_start_date, yesterday)
        assert_equal(self.device.device_status_name(), DeviceStatus.ASIGNADO)

    def test_assign_should_not_set_life_start_date_for_device_without_lifetime(self):
        self.device.life_start_date = None
        self.device.device_type.life_time = None
        self.device.assign()
        assert_is_none(self.device.life_start_date)
        assert_equal(self.device.device_status_name(), DeviceStatus.ASIGNADO)

    def test_mark_assigned_should_set_device_status_to_assigned(self):
        assert_equal(self.device.device_status_name(), DeviceStatus.DISPONIBLE)
        self.device.mark_assigned()
        assert_equal(self.device.device_status_name(), DeviceStatus.ASIGNADO)
