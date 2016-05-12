from nose.tools import *

from devices.models import Device
from devices.serializers import *

class TestDeviceSerializer():

    def test_should_include_device_type_model(self):
        assert_equal(DeviceSerializer.Meta.model, Device)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceSerializer.Meta.fields, ('id', 'device_type_name', 'device_brand_name', 'device_type', 'device_brand', 'asset',
                                                    'ownership', 'serial_number', 'model', 'purchase_date'))

