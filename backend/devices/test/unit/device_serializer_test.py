from nose.tools import assert_equal, assert_is_instance
from devices.serializers import DeviceSerializer
from devices import models


class TestDeviceSerializer():

    def test_should_include_device_type_model(self):
        assert_equal(DeviceSerializer.Meta.model, models.Device)

    def test_should_include_fields_definition(self):
        assert_equal(DeviceSerializer.Meta.fields, ('id', 'device_type_name', 'full_code', 'device_brand_name', 'device_type', 'device_brand', 'asset',
                                                    'ownership', 'serial_number', 'model', 'purchase_date', 'device_status', 'device_status_name',
                                                    'life_start_date_or_assignment_date', 'life_end_date', 'description'))

    def test_should_set_avaliable_device_status_as_default(self):
        assert_is_instance(DeviceSerializer().get_fields()['device_status'].default, models.DeviceStatus)
