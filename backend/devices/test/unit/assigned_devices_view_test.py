from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch


class TestAssignedDevicesView(APITestCase):

    def test_should_respond_with_200(self):
        url = reverse('assigned_devices')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('devices.views.AssignedDeviceList.get_queryset')
    def test_should_return_a_list_of_devices(self, mock):
        url = reverse('assigned_devices')
        mock.return_value = [{'id': '1',
                              'full_code': 'some_code',
                                'device_type_name': 'Laptop',
                                'device_brand_name': 'Apple'
                              }]
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['full_code'], 'some_code')
        self.assertEqual(response.data[0]['device_type_name'], 'Laptop')
        self.assertEqual(response.data[0]['device_brand_name'], 'Apple')
