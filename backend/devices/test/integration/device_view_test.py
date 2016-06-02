from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy


class TestDeviceView(APITestCase):

    @classmethod
    def setUpClass(self):
        self.device = mommy.prepare_recipe('devices.device_recipe')
        self.device.model = 'model'
        self.device.save()

    @classmethod
    def tearDownClass(self):
        self.device.delete()

    def test_should_respond_with_200(self):
        response = self.client.get('/devices/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

