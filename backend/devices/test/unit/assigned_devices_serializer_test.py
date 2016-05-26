from nose.tools import *
from devices.serializers import *


class TestDeviceSerializer():

    def test_should_include_device_model(self):
        assert_equal(AssignedDeviceSerializer.Meta.model, Device)

    def test_should_include_fields_definition(self):
        assert_equal(AssignedDeviceSerializer.Meta.fields, ('id', 'full_code', 'device_type_name', 'device_brand_name',
                                                            'return_date', 'end_date', 'assignee_name',
                                                            'project', 'first_assignment_date', 'last_assignment_date'))


