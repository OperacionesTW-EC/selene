
from django.core.urlresolvers import  resolve
from django.test import TestCase
from main import views


class IndexViewTests(TestCase):
    def test_index_view_is_displayed_as_the_root_page(self):
        found = resolve('/')
        self.assertEqual(found.func, 1)