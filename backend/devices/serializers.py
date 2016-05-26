from rest_framework import serializers
from devices.models import *



class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name', 'code', 'life_time')


class DeviceBrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = ('id', 'name')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name')


class DeviceAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceAssignment
        fields = ('id', 'assignment', 'device')


class DeviceSerializer(serializers.ModelSerializer):
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    device_status_name = serializers.CharField(read_only=True)
    full_code = serializers.CharField(read_only=True)
    purchase_date = serializers.DateField(required=False)
    try:
        default_device_status = DeviceStatus.objects.get_or_create(name=DeviceStatus.DISPONIBLE)[0]
        device_status = serializers.ModelField(model_field=Device()._meta.get_field('device_status'), default=default_device_status)
    except Exception:
        print 'devicestatus Table does not exist'

    class Meta:
        model = Device
        fields = ('id', 'device_type_name', 'full_code', 'device_brand_name', 'device_type', 'device_brand', 'asset',
                  'ownership', 'serial_number', 'model', 'purchase_date', 'device_status', 'device_status_name')


class AssignmentSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = ('id', 'assignee_name', 'project_name', 'project', 'devices', 'assignment_datetime')


class AssignedDeviceSerializer(serializers.ModelSerializer):
    full_code = serializers.CharField(read_only=True)
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    return_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    assignee_name = serializers.CharField(read_only=True)
    project = serializers.CharField(read_only=True)
    first_assignment_date = serializers.DateField(required=False)
    last_assignment_date = serializers.DateField(required=False)

    class Meta:
        model = Device
        fields = ('id', 'full_code', 'device_type_name', 'device_brand_name',
                  'return_date', 'end_date', 'assignee_name',
                  'project', 'first_assignment_date', 'last_assignment_date')
