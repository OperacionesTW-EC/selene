# coding=utf8
from model_mommy import mommy
from nose.tools import assert_equal, raises, assert_is_not_none, assert_is_none
from devices.models import DeviceAssignment
from datetime import date
import datetime


class TestDeviceAssignment:

    def setup(self):
        self.device_assignment = mommy.prepare_recipe('devices.device_assignment_recipe')

    def test_verbose_name(self):
        assert_equal(str(DeviceAssignment._meta.verbose_name), 'Asignación de Dispositivos')

    def test_verbose_name_plural(self):
        assert_equal(str(DeviceAssignment._meta.verbose_name_plural), "Asignaciones de Dispositivos")

    def test_should_be_ordered_by_assignment_date(self):
        assert_equal(DeviceAssignment._meta.ordering, ['-assignment_date', '-id'])

    @raises(ValueError)
    def test_should_be_invalid_without_device(self):
        self.device_assignment.device = None

    @raises(ValueError)
    def test_should_be_invalid_without_assignment(self):
        self.device_assignment.assignment = None

    def test_should_return_device_full_code(self):
        assert_is_not_none(self.device_assignment.full_code())

    def test_should_return_device_type_name(self):
        assert_is_not_none(self.device_assignment.device_type_name())

    def test_should_return_device_brand_name(self):
        assert_is_not_none(self.device_assignment.device_brand_name())

    def test_should_return_assignee_name(self):
        assert_is_not_none(self.device_assignment.assignee_name())

    def test_should_return_return_date(self):
        self.device_assignment.assignment.expected_return_date = date.today()
        assert_is_not_none(self.device_assignment.return_date())

    def test_should_return_life_end_date_for_devices_with_a_lifetime(self):
        self.device_assignment.device.device_type.life_time = 2
        self.device_assignment.device.life_start_date = date.today()
        assert_is_not_none(self.device_assignment.life_end_date())

    def test_should_not_return_life_end_date_for_devices_with_no_lifetime(self):
        self.device_assignment.device.device_type.life_time = None
        self.device_assignment.device.life_start_date = date.today()
        assert_is_none(self.device_assignment.life_end_date())

    def test_should_return_assignment_date_for_devices_with_no_lifetime(self):
        self.device_assignment.device.device_type.life_time = None
        assert_equal(self.device_assignment.life_start_date_or_assignment_date(), date.today())

    def test_should_return_life_start_date_for_devices_with_lifetime_and_start_date(self):
        yesterday = date.today() - datetime.timedelta(days=1)
        self.device_assignment.device.device_type.life_time = 2
        self.device_assignment.device.life_start_date = yesterday
        assert_equal(self.device_assignment.life_start_date_or_assignment_date(), yesterday)
