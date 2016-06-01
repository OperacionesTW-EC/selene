from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch
from devices.models import DeviceStatus


class TestDeviceStatusView(APITestCase):

    def test_should_respond_with_200(self):
        response = self.client.get('/device_status/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('devices.services.DeviceStatusService.get_filtered_device_statuses')
    def test_should_invoke_queries_filter_status(self, mock):
        mock.return_value = []
        self.client.get('/device_status/', {}, format='json')
        self.assertEqual(mock.called, True)

    def test_should_paginate_the_query(self):
        response = self.client.get('/device_status/', {}, format='json')
        self.assertIsNotNone(response.data['results'])

    def test_should_exclude_assigned_status(self):
        response = self.client.get('/device_status/', {}, format='json')
        for result in response.data['results']:
            assert DeviceStatus.ASIGNADO not in result['name']
