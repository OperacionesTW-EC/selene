from rest_framework import status
from rest_framework.test import APITestCase
from mock import patch
from devices.models import DeviceEndStatusType


class TestDeviceStatusView(APITestCase):

    def test_should_respond_with_200(self):
        response = self.client.get('/device_end_status_type/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_paginate_the_query(self):
        response = self.client.get('/device_end_status_type/', {}, format='json')
        self.assertIsNotNone(response.data['results'])