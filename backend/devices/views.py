from rest_framework import viewsets, generics
from devices import serializers
from rest_framework.response import Response
from rest_framework import status
from devices import models
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
        page = self.paginate_queryset(query_set)  # NOQA : page is necessary for the method below
        return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        return services.DeviceStatusService.get_filtered_device_statuses_without_assigned()

class DeviceStatusAllViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceStatus.objects.all()
    serializer_class = serializers.DeviceStatusSerializer



class DeviceEndStatusTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DeviceEndStatusType.objects.all()
    serializer_class = serializers.DeviceEndStatusTypeSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = models.Device.objects.all()
    serializer_class = serializers.DeviceSerializer


class ChangeDeviceStatus(generics.UpdateAPIView):
    def patch(self, request):
        device = models.Device.objects.get(pk=request.data['id'])
        if services.DeviceService.change_device_status(device, request.data['new_device_status']):
            message = 'El dispositivo: '+device.full_code()+' tiene el estado '+device.device_status.name
            return Response(status=status.HTTP_202_ACCEPTED, data={'message': message})

        return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': services.DeviceService.CHANGE_STATUS_ERROR_MESSAGE})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = models.Assignment.objects.all()
    serializer_class = serializers.AssignmentSerializer

    def create(self, request):
        assignment = self.get_assignment_by_request_data(request.data)
        assignment_service = services.AssignmentService(assignment, request.data['devices'])
        if assignment_service.create_assignment():
            return Response({'status': 'asignación creada', 'id': assignment_service.assignment.id})
        else:
            return Response(assignment_service.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_assignment_by_request_data(self, data):
        assignment = models.Assignment()
        assignment.assignee_name = data['assignee_name']
        if 'project' in data:
            assignment.project_id = data['project']
        if 'expected_return_date' in data:
            assignment.expected_return_date = data['expected_return_date']
        return assignment


class AssignedDeviceList(generics.ListCreateAPIView):

    serializer_class = serializers.DeviceAssignmentSerializer

    def list(self, request):
        serializer = serializers.DeviceAssignmentSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = models.DeviceAssignment.objects.filter(device__device_status__name=models.DeviceStatus.ASIGNADO,
                                                          actual_return_date=None)

        project = self.request.query_params.get('project', None)
        if project:
            if project == '0':
                project = None
            queryset = queryset.filter(assignment__project=project)

        assignee = str(self.request.query_params.get('assignee', '')).strip()
        if assignee:
            queryset = queryset.filter(assignment__assignee_name__icontains=assignee)

        return queryset
