from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


class LoginViewTests(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        User.objects.create_user('admin_test', 'temporary@gmail.com', 'admin_pass')
        self.incorrect_data = {
            'login': 'Rudolf',
            'password': '1234567890',
        }
        self.correct_data = {
            'login': 'admin_test',
            'password': 'admin_pass',
        }

    def test_successful_login_sends_to_device_page(self):
        response = self.client.post('/login', self.correct_data)
        self.assertEquals(response.url, "/devices")

    def test_unsuccessful_login_sends_to_home_page(self):
        response = self.client.post("/login", self.incorrect_data)
        self.assertEquals(response.url, "/index")


