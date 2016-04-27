from nose.tools import *
from django.core.urlresolvers import resolve
from devices import views

class TestDevice:

    def test_should_render_the_template(self):
        url = resolve('/device_form')
        assert_equal(url.func, views.device_form)