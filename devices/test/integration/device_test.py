from nose.tools import *
from django.core.urlresolvers import resolve
from devices import views
from django.test import Client
from devices.models import Device
from devices.factories import DeviceFactory

class TestDevice:

    client = Client()

    def test_should_render_the_template(self):
        url = resolve('/device_form')
        assert_equal(url.func, views.device_form)

    def test_should_respond_200(self):
        resp = self.client.post('/save_device')
        assert_equal(resp.status_code, 200)

    def test_should_save_a_device(self):
        count = Device.objects.count()
        self.client.post('/save_device', DeviceFactory.build().__dict__)
        assert_equal(Device.objects.count(), count+1)