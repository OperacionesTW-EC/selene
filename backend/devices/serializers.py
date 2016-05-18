from rest_framework import serializers
from devices.models import *


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name', 'code')


class DeviceBrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = ('id', 'name')


class DeviceSerializer(serializers.ModelSerializer):
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    device_state_name = serializers.CharField(read_only=True)
    full_code = serializers.CharField(read_only=True)
    purchase_date = serializers.DateField(required=False)
    try:
        default_device_state = DeviceState.objects.get_or_create(name='Disponible')[0]
        device_state = serializers.ModelField(model_field=Device()._meta.get_field('device_state'), default=default_device_state)
    except Exception:
        print 'aaa'

    class Meta:
        model = Device
        fields = ('id', 'device_type_name', 'full_code', 'device_brand_name', 'device_type', 'device_brand', 'asset',
              'ownership', 'serial_number', 'model', 'purchase_date', 'device_state', 'device_state_name')
