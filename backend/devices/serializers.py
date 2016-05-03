from rest_framework import serializers
from devices.models import *


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('name', 'code', 'id')
