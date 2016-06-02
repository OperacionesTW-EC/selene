# coding=utf8
from model_mommy import mommy
from nose.tools import assert_equal, raises
from devices.models import DeviceAssignment
from devices.serializers import DeviceAssignmentSerializer


class TestDeviceAssignment:

    def setup(self):
        self.device_assignment = mommy.prepare_recipe('devices.device_assignment_recipe')

    def test_verbose_name(self):
        assert_equal(str(DeviceAssignment._meta.verbose_name), 'Asignación de Dispositivos')

    def test_verbose_name_plural(self):
        assert_equal(str(DeviceAssignment._meta.verbose_name_plural), "Asignaciones de Dispositivos")

    def test_should_be_valid_without_assignment_date(self):
        self.device_assignment.assignment_date = None
        assert_equal(True, DeviceAssignmentSerializer(data=self.device_assignment.__dict__).is_valid())

    @raises(ValueError)
    def test_should_be_invalid_without_device(self):
        self.device_assignment.device = None

    @raises(ValueError)
    def test_should_be_invalid_without_assignment(self):
        self.device_assignment.assignment = None

