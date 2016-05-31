from nose.tools import assert_equal
from devices.serializers import DeviceTypeSerializer
from devices import models


class TestDeviceTypeSerializer():

    def test_should_include_device_model(self):
        assert_equal(DeviceTypeSerializer.Meta.model, models.DeviceType)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceTypeSerializer.Meta.fields, ('id', 'name', 'code', 'life_time'))
