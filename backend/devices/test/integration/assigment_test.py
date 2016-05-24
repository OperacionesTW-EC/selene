# coding=utf8
from django.core.exceptions import ValidationError
from model_mommy import mommy
from nose.tools import *
from devices.models import *
from devices.views import *
from django.test import RequestFactory
from rest_framework import status

class TestAssignmet:

    def __init__(self):
        self.device = None
        self.device_brand = None
        self.device_type = None

    def setup(self):
        self.assignment_view = AssignmentViewSet()
        self.project = Project(name='Selene')
        self.device = mommy.prepare_recipe('devices.device_recipe')
        self.device.model = 'model 200'
        self.device.save()
        self.project.save()
        self.factory = RequestFactory()
        self.request = self.factory.post('/assignment')
        self.request.data = {'assignee_name': 'Jose', 'project': self.project.id, 'devices': [self.device.id]}
        self.response = self.assignment_view.create(self.request)

    def test_good_request_should_return_success_message(self):
        assert_regexp_matches(self.response.data['status'], 'creada')

    def test_good_request_should_return_http_200(self):
        assert_equal(self.response.status_code, 200)

    def test_bad_request_should_not_return_http_200(self):
        self.request.data['project'] = 321321
        self.request.data['devices'] = [31213]
        self.response = self.assignment_view.create(self.request)
        assert_not_equal(self.response.status_code, 200)

    def test_should_save_a_new_assignment(self):
        self.request.data['assignee_name'] = 'Test'
        self.assignment_view.create(self.request)
        assignment = Assignment.objects.get(assignee_name='Test')
        assert_is_not_none(assignment)

    def test_should_set_device_status_to_unavailable(self):
        self.device.device_status = DeviceStatus.objects.get(name=DeviceStatus.DISPONIBLE)
        self.device.model = 'model 201'
        self.device.save()
        self.request.data = {'assignee_name': 'Jose', 'project': self.project.id, 'devices': [self.device.id]}
        self.assignment_view.create(self.request)
        assert_equal((Device.objects.get(model='model 201')).device_status.name, (DeviceStatus.objects.get(name=DeviceStatus.NO_DISPONIBLE)).name)

    def test_project_should_not_be_required(self):
        del self.request.data['project']
        self.assignment_view.create(self.request)
        assert_equal(self.response.status_code, 200)


