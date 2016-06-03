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


class DeviceStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DeviceStatus
        fields = ('id', 'name')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Project
        fields = ('id', 'name')


class DeviceAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeviceAssignment
        fields = ('id', 'full_code', 'device_type_name', 'device_brand_name',
                  'return_date', 'laptop_begin_life', 'laptop_end_life', 'assignee_name',
                  'project')


class DeviceSerializer(serializers.ModelSerializer):
    device_type_name = serializers.CharField(read_only=True)
    device_brand_name = serializers.CharField(read_only=True)
    device_status_name = serializers.CharField(read_only=True)
    full_code = serializers.CharField(read_only=True)
    purchase_date = serializers.DateField(required=False)
    laptop_begin_life = serializers.DateTimeField(required=False)
    laptop_end_life = serializers.DateTimeField(required=False)

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
                  'laptop_begin_life', 'laptop_end_life'
                  )


class AssignmentSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Assignment
        fields = ('id', 'assignee_name', 'assignment_date', 'project_name', 'project', 'devices', 'expected_return_date')
