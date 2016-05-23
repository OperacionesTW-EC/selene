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


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')


class AssignmentSerializer(serializers.ModelSerializer):
    depth = 1


    class Meta:
        model = Assignment
        fields = ('id', 'assignee_name', 'project_name', 'project', 'devices')


class DeviceAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceAssignment
        fields = ('id', 'assignment', 'device')


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
        print 'devicestate Table does not exist'

    class Meta:
        model = Device
        fields = ('id', 'device_type_name', 'full_code', 'device_brand_name', 'device_type', 'device_brand', 'asset',
              'ownership', 'serial_number', 'model', 'purchase_date', 'device_state', 'device_state_name')


class AssignedDeviceSerializer(serializers.ModelSerializer):
    full_code = serializers.CharField(read_only=True)
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    assign_date = serializers.DateField(required=False)
    return_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    assignee_name = serializers.CharField(read_only=True)
    project = serializers.CharField(read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'full_code', 'device_type_name', 'device_brand_name',
                  'assign_date', 'return_date','end_date', 'assignee_name',
                  'project')
