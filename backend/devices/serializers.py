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


#class DeviceSerializer(serializers.HyperlinkedModelSerializer):
#    device_type = DeviceTypeSerializer(many=False, read_only=True)
#    device_brand = DeviceBrandSerializer(many=False, read_only=True)
#    class Meta:
#        model = Device
#        fields = ('id', 'device_type', 'device_brand', 'asset', 'ownership', 'serial_number', 'model', 'purchase_date')

class DeviceSerializer(serializers.ModelSerializer):
    device_type_name = serializers.CharField(read_only=True)
    class Meta:
        model = Device
        fields = ('id', 'device_type_name' , 'device_type', 'device_brand', 'asset', 'ownership', 'serial_number', 'model', 'purchase_date')
