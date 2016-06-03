from nose.tools import assert_equal
from devices.serializers import DeviceAssignmentSerializer
from devices import models


class TestDeviceSerializer():

    def test_should_include_device_model(self):
        assert_equal(DeviceAssignmentSerializer.Meta.model, models.DeviceAssignment)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceAssignmentSerializer.Meta.fields, ('id', 'full_code', 'device_type_name', 'device_brand_name',
                                                            'return_date','laptop_begin_life', 'laptop_end_life', 'assignee_name',
                                                            'project'))
