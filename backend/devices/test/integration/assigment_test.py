# coding=utf8
from mock import MagicMock
from model_mommy import mommy
from nose.tools import assert_regexp_matches, assert_equal, assert_not_equal, assert_is_not_none
from devices import models
from devices import views
from django.test import RequestFactory
from django.utils import timezone


class TestAssignmet:

    def __init__(self):
        self.device = None
        self.device_brand = None
        self.device_type = None

    def setup(self):
        self.project = models.Project(name='Selene')
        self.device = mommy.prepare_recipe('devices.device_recipe')
        self.device.model = 'model 200'
        self.device.save()
        self.project.save()

    def build_request(self, **request_options):
        request = RequestFactory().post('/assignment')
        request.data = {'assignee_name': 'Jose', 'project': self.project.id, 'devices': [self.device.id]}
        request.data.update(request_options)
        return request

    def get_response(self, request):
        return views.AssignmentViewSet().create(request)

    def test_good_request_should_return_success_message(self):
        assert_regexp_matches(self.get_response(self.build_request()).data['status'], 'creada')

    def test_good_request_should_return_http_200(self):
        assert_equal(self.get_response(self.build_request()).status_code, 200)

    def test_bad_request_should_not_return_http_200(self):
        request = self.build_request(project=4324234, devices=[434234])
        assert_not_equal(self.get_response(request).status_code, 200)

    def test_should_save_a_new_assignment(self):
        self.get_response(self.build_request(assignee_name='Test'))
        assignment = models.Assignment.objects.get(assignee_name='Test')
        assert_is_not_none(assignment)

    def test_should_set_device_status_to_unavailable(self):
        device = mommy.prepare_recipe('devices.device_recipe')
        device.model = 'model 201'
        device.save()
        self.get_response(self.build_request(devices=[device.id]))
        assert_equal((models.Device.objects.get(model='model 201')).device_status.name, (models.DeviceStatus.objects.get(name=models.DeviceStatus.ASIGNADO)).name)

    def test_project_should_not_be_required(self):
        request = self.build_request()
        del request.data['project']
        response = views.AssignmentViewSet().create(request)
        assert_equal(response.status_code, 200)

    def test_should_set_the_assignment_date(self):
        expected_time = timezone.now()
        timezone.now = MagicMock(return_value=expected_time)
        fmt = "%d-%m-%Y %H:%M"
        self.get_response(self.build_request(assignee_name='Name'))
        assignment_datetime = models.Assignment.objects.get(assignee_name='Name').assignment_datetime
        assert_equal(assignment_datetime.strftime(fmt), expected_time.strftime(fmt))

    def test_should_include_the_expected_return_date_if_any(self):
        response = self.get_response(self.build_request(expected_return_date='2010-05-30'))
        assignment = models.Assignment.objects.get(expected_return_date='2010-05-30')
        assert_equal(response.status_code, 200)
        assert_is_not_none(assignment)
