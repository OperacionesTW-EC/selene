from nose.tools import assert_equal
from devices.serializers import AssignedDeviceSerializer
from devices import models


class TestDeviceSerializer():

    def test_should_include_device_model(self):
        assert_equal(AssignedDeviceSerializer.Meta.model, models.Device)

    def test_should_include_fields_definition(self):
        assert_equal(AssignedDeviceSerializer.Meta.fields, ('id', 'full_code', 'device_type_name', 'device_brand_name',
                                                            'return_date', 'laptop_end_life', 'assignee_name',
                                                            'project'))


