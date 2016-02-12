from django.core.urlresolvers import  resolve
from django.test import TestCase
from main import views


class DummyUnitTest(TestCase):
    def test_dummy_unit_test(self):
        self.assertEqual(1,1)

    def test_not_working(self):
        self.assertEqual(1,3)