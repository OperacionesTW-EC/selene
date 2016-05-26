from nose.tools import *
from devices.serializers import *


class TestDeviceTypeSerializer():

    def test_should_include_device_model(self):
        assert_equal(DeviceTypeSerializer.Meta.model, DeviceType)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceTypeSerializer.Meta.fields, ('id', 'name', 'code', 'life_time'))
