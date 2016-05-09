from rest_framework import serializers
from devices.models import *


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType


class DeviceBrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceBrand


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    device_type = DeviceTypeSerializer(many=False, read_only=True)
    device_brand = DeviceBrandSerializer(many=False, read_only=True)
    class Meta:
        model = Device
        fields = ('id', 'device_type', 'device_brand', 'asset', 'ownership', 'serial_number', 'model', 'purchase_date')

