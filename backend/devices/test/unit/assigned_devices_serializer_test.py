from nose.tools import assert_equal
from devices.serializers import DeviceAssignmentSerializer
from devices import models


class TestDeviceAssignmentSerializer():

    def test_should_include_device_model(self):
        assert_equal(DeviceAssignmentSerializer.Meta.model, models.DeviceAssignment)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceAssignmentSerializer.Meta.fields, ('id', 'full_code', 'device_type_name', 'device_brand_name',
                                                              'return_date', 'life_start_date_or_assignment_date', 'life_end_date', 'assignee_name',
                                                              'project'))
