from rest_framework import viewsets, generics
from devices import serializers
from rest_framework.response import Response
from rest_framework import status
from devices import models
from devices.queries import Queries
from devices import services


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceType.objects.all()
    serializer_class = serializers.DeviceTypeSerializer


class DeviceBrandViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceBrand.objects.all()
    serializer_class = serializers.DeviceBrandSerializer


class DeviceStatusViewSet(generics.ListCreateAPIView):
    serializer_class = serializers.DeviceStatusSerializer

    def list(self, request):
        query_set = self.get_queryset()
        serializer = serializers.DeviceStatusSerializer(query_set, many=True)
        page = self.paginate_queryset(query_set)  # page is necessary for the method bellow
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return services.DeviceStatusService.get_filtered_device_statuses()


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = models.Assignment.objects.all()
    serializer_class = serializers.AssignmentSerializer

    def create(self, request):
        assignment = self.get_assignment_by_request_data(request.data)
        devices_ids = request.data['devices']
        serializer = serializers.AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            assignment.save()
            for device_id in devices_ids:
                device = self.update_device_status(device_id)
                device_assignment = models.DeviceAssignment(device=device, assignment=assignment)
                device_assignment.save()
            return Response({'status': 'asignacion creada', 'id': assignment.id})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_assignment_by_request_data(self, data):
        assignment = models.Assignment()
        assignment.assignee_name = data['assignee_name']
        if 'project' in data:
            assignment.project_id = data['project']
        if 'expected_return_date' in data:
            assignment.expected_return_date = data['expected_return_date']
        return assignment

    def update_device_status(self, device_id):
        device = models.Device.objects.get(pk=device_id)
        device.device_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.ASIGNADO)
        device.save()
        return device


class AssignedDeviceList(generics.ListCreateAPIView):

    serializer_class = serializers.AssignedDeviceSerializer

    def list(self, request):
        serializer = serializers.AssignedDeviceSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Queries().assigned_devices()
