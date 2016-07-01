from nose.tools import assert_equal
from devices.serializers import DeviceEndStatusTypeSerializer
from devices import models


class TestDeviceEndStatusTypeSerializer():
    def test_should_include_device_end_status_type_model(self):
        assert_equal(DeviceEndStatusTypeSerializer.Meta.model, models.DeviceEndStatusType)


    def test_should_include_fields_definition(self):
        assert_equal(DeviceEndStatusTypeSerializer.Meta.fields, ('id', 'name'))
