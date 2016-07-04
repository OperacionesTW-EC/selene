from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch
from devices.models import DeviceStatus


class TestDeviceStatusAllView(APITestCase):
    def test_should_respond_with_200(self):
        response = self.client.get('/device_status_all/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_all_state(self):
        response = self.client.get('/device_status_all/', {}, format='json')
        expected_data = ['Asignado','Disponible', 'Mantenimiento','Dado de baja']
        data = []
        for state in response.data['results']:
            data.append(state['name'])
        self.assertEqual(expected_data.sort(), data.sort())
