from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from devices import models
import datetime
from devices.services import DeviceService


class TestChangeDeviceStatusView(APITestCase):

    @classmethod
    def setUpClass(self):
        self.device = mommy.prepare_recipe('devices.device_recipe')
        self.device.model = 'model'
        self.device.save()
        self.new_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.MANTENIMIENTO)
        self.data = {'id': self.device.id, 'new_device_status': self.new_status.id}

    @classmethod
    def tearDownClass(self):
        pass

    def test_should_update_the_device_status(self):
        self.client.patch('/devices/change_status', self.data, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status, self.new_status)

    def test_should_return_202_if_the_device_is_successfully_updated(self):
        response = self.client.patch('/devices/change_status', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_should_return_the_success_message(self):
        response = self.client.patch('/devices/change_status', self.data, format='json')
        expected_message = 'El dispositivo: '+self.device.full_code()+' tiene el estado '+models.DeviceStatus.MANTENIMIENTO
        self.assertEqual(response.data['message'], expected_message)

    def test_should_create_a_device_status_log_representing_the_change(self):
        fmt = "%d-%m-%Y"
        change_date = datetime.date.today().strftime(fmt)
        self.client.patch('/devices/change_status', self.data, format='json')
        device_status_log = models.DeviceStatusLog.objects.get(device=self.device)
        self.assertEqual(device_status_log.device, self.device)
        self.assertEqual(device_status_log.device_status, self.new_status)
        self.assertEqual(device_status_log.status_change_datetime.strftime(fmt), change_date)

    def test_should_not_update_the_status_if_current_status_is_DADO_DE_BAJA(self):
        self.device.device_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.DADO_DE_BAJA)
        self.device.save()
        response = self.client.patch('/devices/change_status', self.data, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status.name, models.DeviceStatus.DADO_DE_BAJA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], DeviceService.CHANGE_STATUS_ERROR_MESSAGE)