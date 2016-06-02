from rest_framework import serializers
from devices import models


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DeviceType
        fields = ('id', 'name', 'code', 'life_time')


class DeviceBrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DeviceBrand
        fields = ('id', 'name')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Project
        fields = ('id', 'name')


class DeviceAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeviceAssignment
        fields = ('id', 'full_code', 'device_type_name', 'device_brand_name',
                  'return_date', 'end_date', 'assignee_name',
                  'project', 'assignment_date')


class DeviceSerializer(serializers.ModelSerializer):
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    device_status_name = serializers.CharField(read_only=True)
    full_code = serializers.CharField(read_only=True)
    purchase_date = serializers.DateField(required=False)
    first_assignment_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

    try:
        default_device_status = models.DeviceStatus.objects.get_or_create(name=models.DeviceStatus.DISPONIBLE)[0]
        device_status = serializers.ModelField(model_field=models.Device()._meta.get_field('device_status'), default=default_device_status)
    except Exception:
        print('devicestatus Table does not exist')

    class Meta:
        model = models.Device
        fields = ('id', 'device_type_name', 'full_code', 'device_brand_name',
                  'device_type', 'device_brand', 'asset',
                  'ownership', 'serial_number', 'model', 'purchase_date',
                  'device_status', 'device_status_name',
                  'first_assignment_date', 'end_date'
                  )


class AssignmentSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Assignment
        fields = ('id', 'assignee_name', 'project_name', 'project', 'devices', 'expected_return_date')


class AssignedDeviceSerializer(serializers.ModelSerializer):
    full_code = serializers.CharField(read_only=True)
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    return_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    assignee_name = serializers.CharField(read_only=True)
    project = serializers.CharField(read_only=True)
    assignment_date = serializers.DateField(required=False)

    class Meta:
        model = models.Device
        fields = ('id', 'full_code', 'device_type_name', 'device_brand_name',
                  'return_date', 'end_date', 'assignee_name',
                  'project', 'assignment_date')
