from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch
from devices import models
from devices import services
from datetime import date
import random
import datetime

NO_PROJECT = False
HAS_PROJECT = True


class TestAssignedDevicesView(APITestCase):

    def setUp(self):
        self.url = reverse('assigned_devices')

    def test_should_respond_with_200(self):
        response = self.client.get(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('devices.views.AssignedDeviceList.get_queryset')
    def test_should_return_a_list_of_devices(self, mock):
        mock.return_value = [{'id': '1',
                              'full_code': 'some_code',
                              'device_type_name': 'Laptop',
                              'device_brand_name': 'Apple'
                              }]
        response = self.client.get(self.url, {}, format='json')
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['full_code'], 'some_code')
        self.assertEqual(response.data[0]['device_type_name'], 'Laptop')
        self.assertEqual(response.data[0]['device_brand_name'], 'Apple')

    def test_should_filter_on_project_parameter(self):
        assignment = self.create_assignment()
        response = self.client.get(self.url, {'project': str(assignment.project.id)}, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['project'], assignment.project_name())

    def test_should_filter_on_none_project_parameter(self):
        self.create_assignment(NO_PROJECT)
        response = self.client.get(self.url, {'project': '0'}, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['project'], '')

    def test_should_filter_on_assignee_parameter(self):
        assignment = self.create_assignment()
        response = self.client.get(self.url, {'assignee': assignment.assignee_name}, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['assignee_name'], assignment.assignee_name)

    def test_should_not_show_devices_when_actual_return_date_is_not_none(self):
        active_assignment = self.create_device_assignment()
        ended_assignment = self.create_device_assignment()
        ended_assignment.actual_return_date = datetime.date.today()
        ended_assignment.save()
        response = self.client.get(self.url, {}, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], active_assignment.id)

    def create_assignment(self, has_project = True):
        project_name = 'UNIQUE PROJECT NAME FOR TEST 123456789'
        assignee_name = 'UNIQUE ASSIGNEE NAME FOR TEST 123456789'
        expected_project = None
        if has_project:
            expected_project = models.Project.objects.get_or_create(name=project_name)[0]
        assignment = models.Assignment(project=expected_project, assignee_name=assignee_name)
        device = self.create_device()
        assignment_service = services.AssignmentService(assignment, [str(device.id)])
        assignment_service.create_assignment()
        return assignment

    def create_device(self, status_name=models.DeviceStatus.DISPONIBLE):
        device_brand = models.DeviceBrand.objects.get_or_create(name='Some brand')[0]
        device_type = models.DeviceType.objects.get_or_create(code='L', name='Laptop')[0]
        device_status = models.DeviceStatus.objects.get_or_create(name=status_name)[0]

        device = models.Device.objects.get_or_create(
            device_type=device_type,
            device_brand=device_brand,
            device_status=device_status,
            asset=1,
            ownership=random.choice(['CL', 'TW']),
            serial_number='123123',
            purchase_date=date.today(),
            sequence=random.randint(0, 100),
            code='code', model="xyz",
            life_start_date=date.today()
        )[0]
        return device

    def create_device_assignment(self):
        device = self.create_device(models.DeviceStatus.ASIGNADO)
        assignment = models.Assignment.objects.get_or_create(
            assignee_name='Nombre Apellido'
        )[0]
        device_assignment = models.DeviceAssignment(assignment=assignment, device=device, assignment_date=date.today())
        device_assignment.save()
        return device_assignment

