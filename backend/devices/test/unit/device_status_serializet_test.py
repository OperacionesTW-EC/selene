from nose.tools import assert_equal
from devices.serializers import DeviceStatusSerializer
from devices import models


class TestDeviceTypeSerializer():

    def test_should_include_device_model(self):
        assert_equal(DeviceStatusSerializer.Meta.model, models.DeviceStatus)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceStatusSerializer.Meta.fields, ('id', 'name'))
