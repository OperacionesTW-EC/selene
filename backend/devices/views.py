from rest_framework import viewsets, generics
from devices import serializers
from rest_framework.response import Response
from rest_framework import status
from devices import models
from datetime import date


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceType.objects.all()
    serializer_class = serializers.DeviceTypeSerializer


class DeviceBrandViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceBrand.objects.all()
    serializer_class = serializers.DeviceBrandSerializer


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
                device = self.update_device(device_id)
                self.create_device_assignment(device, assignment)
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

    def update_device(self, device_id):
        device = models.Device.objects.get(pk=device_id)
        if device.is_new_laptop():
            device.first_assignment_date = date.today()
            device.calculate_end_date()
        device.mark_assigned()
        device.save()
        return device

    def create_device_assignment(self, device, assignment):
        device_assignment = models.DeviceAssignment(device=device, assignment=assignment)
        if device.is_laptop():
            assert device.first_assignment_date and device.end_date
            device_assignment.assignment_date = device.first_assignment_date
        else:
            device_assignment.assignment_date = date.today()
        device_assignment.save()


class AssignedDeviceList(generics.ListCreateAPIView):

    serializer_class = serializers.DeviceAssignmentSerializer

    def list(self, request):
        serializer = serializers.DeviceAssignmentSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return models.DeviceAssignment.objects.filter(device__device_status__name=models.DeviceStatus.ASIGNADO)
