from rest_framework import viewsets, generics
from devices.serializers import *
from rest_framework.response import Response
from rest_framework import status
from devices.models import *
from devices.queries import Queries

class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class DeviceBrandViewSet(viewsets.ModelViewSet):
    queryset = DeviceBrand.objects.all()
    serializer_class = DeviceBrandSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Device.objects.all()
        [a.calculate_dates() for a in queryset]
        return queryset

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def create(self, request):
        assignment = self.get_assignment_by_request_data(request.data)
        devices_ids = request.data['devices']
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            assignment.save()
            for device_id in devices_ids:
                device = self.update_device_status(device_id)
                device_assignment = DeviceAssignment(device=device, assignment=assignment)
                device_assignment.save()
            return Response({'status': 'asignacion creada', 'id': assignment.id})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get_assignment_by_request_data(self, data):
        assignment = Assignment()
        assignment.assignee_name = data['assignee_name']
        if 'project' in data:
            assignment.project_id = data['project']
        return assignment

    def update_device_status(self, device_id):
        device = Device.objects.get(pk=device_id)
        device.device_status = DeviceStatus.objects.get(name=DeviceStatus.ASIGNADO)
        device.save()
        return device


class AssignedDeviceList(generics.ListCreateAPIView):

    serializer_class = AssignedDeviceSerializer

    def list(self, request):
        serializer = AssignedDeviceSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Queries().assigned_devices()
