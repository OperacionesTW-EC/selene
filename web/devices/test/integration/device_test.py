import WebTest as WebTest
from nose.tools import *
from django.core.urlresolvers import resolve
from devices import views
from django.test import Client
from devices.models import Device
from devices.factories import DeviceFactory

class TestDevice(WebTest):

    client = Client()

    def test_should_render_the_template(self):
        url = resolve('/device_form')
        assert_equal(url.func, views.device_form)
