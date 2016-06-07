# coding=utf8
from model_mommy import mommy
from nose.tools import assert_equal, assert_not_equal
from nose.tools import assert_regexp_matches, assert_is_not_none, assert_true, assert_is_none
from devices import models
from devices import views
from django.test import RequestFactory
from datetime import date


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

    def test_should_set_life_start_date_on_device_for_new_laptop(self):
        assert_true(self.device.life_has_not_begun())
        self.get_response(self.build_request())
        device = models.DeviceAssignment.objects.filter(device__device_type__name='Laptop')[0].device
        assert_is_not_none(device.life_start_date)

    def test_should_not_set_life_start_date_on_device_for_non_laptop(self):
        device_type = models.DeviceType.objects.get_or_create(code='M', name='Mouse')[0]
        device_type.save()
        device = mommy.prepare_recipe('devices.non_asset_device_recipe')
        device.device_type = device_type
        device.save()
        self.get_response(self.build_request(devices=[device.id]))
        device = models.DeviceAssignment.objects.filter(device__device_type__name='Mouse')[0].device
        assert_is_none(device.life_start_date)

    def test_should_set_device_status_to_assigned(self):
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
        assignment_date = models.Assignment.objects.get(assignee_name='Name').assignment_date
        assert_equal(assignment_date, expected_date)

    def test_should_include_the_expected_return_date_if_any(self):
        response = self.get_response(self.build_request(expected_return_date='2010-05-30'))
        assignment = models.Assignment.objects.get(expected_return_date='2010-05-30')
        assert_equal(response.status_code, 200)
        assert_is_not_none(assignment)
