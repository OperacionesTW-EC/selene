from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client


class LoginFunctionalTests(TestCase):

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        user = User.objects.create_user('admin_test', 'temporary@gmail.com', 'admin_pass') #Esta linea nos faltaba!!, en la base de datos de prueba no existe el usuario que creamos por comandos
        self.incorrect_data = {
            'login': 'Rudolf',
            'password': '1234567890',
        }
        self.correct_data = {
            'login': 'admin_test',
            'password': 'admin_pass',
        }

    #response = self.client.get("index")


    def test_successful_login_sends_to_device_page(self):
        response = self.client.post('/login', self.correct_data,follow=True)
        self.assertRedirects(response,"/devices") #Aqui se puede assertRedirects usar xq el redirect es diferente de /


    def test_unsuccessful_login_sends_to_home_page(self):
        response = self.client.post("/login", self.incorrect_data)
        self.assertEquals(response.url,"/index")


