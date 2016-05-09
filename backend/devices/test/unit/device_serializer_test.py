from nose.tools import *

from devices.models import Device
from devices.serializers import *

class TestDeviceSerializer():

    def test_should_include_device_type_model(self):
        assert_equal(DeviceSerializer.Meta.model, Device)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceSerializer.Meta.fields, ('id', 'device_type', 'device_brand', 'asset',
                                                    'ownership', 'serial_number', 'model', 'purchase_date'))

    def test_should_embed_device_type(self):
        assert_is_instance(DeviceSerializer().get_fields()['device_type'], DeviceTypeSerializer)

    def test_should_embed_device_brand(self):
        assert_is_instance(DeviceSerializer().get_fields()['device_brand'], DeviceBrandSerializer)