# coding=utf8
from model_mommy import mommy
from nose.tools import assert_equal, assert_not_equal
from nose.tools import assert_regexp_matches, assert_is_not_none, assert_true, assert_is_none
from devices import models
from devices import views
from django.test import RequestFactory
from datetime import date
import datetime


class TestAssignmet:

    def __init__(self):
        self.device = None
        self.device_brand = None
        self.device_type = None

    def setup(self):
        self.project = models.Project(name='Selene')
        self.device = mommy.prepare_recipe('devices.non_asset_device_recipe')
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

    def test_should_set_dates_on_device_for_new_laptop(self):
        assert_true(self.device.is_new_laptop())
        self.get_response(self.build_request())
        device = models.DeviceAssignment.objects.filter(device__device_type__name='Laptop')[0].device
        assert_is_not_none(device.first_assignment_date)
        assert_is_not_none(device.end_date)

    def test_should_not_set_dates_on_device_for_non_laptop(self):
        device_type = models.DeviceType.objects.get_or_create(code='M', name='Mouse')[0]
        device_type.save()
        device = mommy.prepare_recipe('devices.non_asset_device_recipe')
        device.device_type = device_type
        device.save()
        self.get_response(self.build_request(devices=[device.id]))
        device = models.DeviceAssignment.objects.filter(device__device_type__name='Mouse')[0].device
        assert_is_none(device.first_assignment_date)
        assert_is_none(device.end_date)

    def test_should_retain_assignment_date_when_reassigning_laptop(self):
        expected_date = date.today() - datetime.timedelta(days=15)
        self.get_response(self.build_request(assignee_name='Original Assignee'))
        original_assignment = models.DeviceAssignment.objects.get(assignment__assignee_name='Original Assignee')
        original_assignment = self.manipulate_device_dates_to_simulate_old_assignment(original_assignment, expected_date)
        original_first_assignment_date = original_assignment.device.first_assignment_date
        original_end_date = original_assignment.device.end_date

        self.get_response(self.build_request(assignee_name='Reassignee', devices=[original_assignment.device.id]))
        re_assignment = models.DeviceAssignment.objects.get(assignment__assignee_name='Reassignee')
        assert_equal(re_assignment.assignment_date, expected_date)
        assert_equal(re_assignment.device.first_assignment_date, original_first_assignment_date)
        assert_equal(re_assignment.device.end_date, original_end_date)

    def manipulate_device_dates_to_simulate_old_assignment(self, device_assingment, older_date):
        device_assingment.assignment_date = older_date
        device_assingment.device.first_assignment_date = older_date
        device_assingment.device.calculate_end_date()
        device_assingment.device.save()
        device_assingment.save()
        return device_assingment

    def test_should_set_device_status_to_unavailable(self):
        device = mommy.prepare_recipe('devices.non_asset_device_recipe')
        uid = 'Hack to id the record: we should tear down!'
        device.model = uid
        device.save()
        self.get_response(self.build_request(devices=[device.id]))
        assert_equal((models.Device.objects.get(model=uid)).device_status.name,
                     (models.DeviceStatus.objects.get(name=models.DeviceStatus.ASIGNADO)).name)

    def test_project_should_not_be_required(self):
        request = self.build_request()
        del request.data['project']
        response = views.AssignmentViewSet().create(request)
        assert_equal(response.status_code, 200)

    def test_should_set_the_assignment_date(self):
        expected_date = date.today()
        self.get_response(self.build_request(assignee_name='Name'))
        assignment_date = models.DeviceAssignment.objects.get(assignment__assignee_name='Name').assignment_date
        assert_equal(assignment_date, expected_date)

    def test_should_include_the_expected_return_date_if_any(self):
        response = self.get_response(self.build_request(expected_return_date='2010-05-30'))
        assignment = models.Assignment.objects.get(expected_return_date='2010-05-30')
        assert_equal(response.status_code, 200)
        assert_is_not_none(assignment)
