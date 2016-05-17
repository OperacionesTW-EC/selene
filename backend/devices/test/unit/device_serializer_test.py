from nose.tools import *

from devices.models import *
from devices.serializers import *

class TestDeviceSerializer():

    def test_should_include_device_type_model(self):
        assert_equal(DeviceSerializer.Meta.model, Device)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceSerializer.Meta.fields, ('id', 'device_type_name', 'full_code', 'device_brand_name', 'device_type', 'device_brand', 'asset',
                                                    'ownership', 'serial_number', 'model', 'purchase_date', 'device_state', 'device_state_name'))

    def test_should_set_avaliable_device_state_as_default(self):
        assert_is_instance(DeviceSerializer().get_fields()['device_state'].default, DeviceState)