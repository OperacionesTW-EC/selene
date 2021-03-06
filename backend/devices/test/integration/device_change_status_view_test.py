from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy
from devices import models
import datetime
from devices.services import DeviceService
from mock import patch


class TestChangeDeviceStatusView(APITestCase):
    @classmethod
    def setUpClass(self):
        self.device = mommy.prepare_recipe('devices.device_recipe')
        self.device.model = 'model'
        self.device.save()
        self.new_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.MANTENIMIENTO)
        self.new_status_dado_de_baja = models.DeviceStatus.objects.get(name=models.DeviceStatus.DADO_DE_BAJA)
        self.data = {'id': self.device.id, 'new_device_status': self.new_status.id, 'new_device_end_status_type': None,
                     'new_device_end_status_comment': None}
        self.data_dado_de_baja = {'id': self.device.id, 'new_device_status': self.new_status_dado_de_baja.id,
                                  'new_device_end_status_type': None, 'new_device_end_status_comment': None}

    @classmethod
    def tearDownClass(self):
        pass

    def date_with_format(self, date):
        fmt = "%d-%m-%Y"
        return date.strftime(fmt)

    def test_should_update_the_device_status(self):
        self.client.patch('/devices/change_status', self.data, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status, self.new_status)

    def test_should_return_202_if_the_device_is_successfully_updated(self):
        response = self.client.patch('/devices/change_status', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_should_return_the_success_message(self):
        response = self.client.patch('/devices/change_status', self.data, format='json')
        expected_message = 'El dispositivo: ' + self.device.full_code() + ' tiene el estado ' + models.DeviceStatus.MANTENIMIENTO
        self.assertEqual(response.data['message'], expected_message)

    def test_should_create_a_device_status_log_representing_the_change(self):
        change_date = self.date_with_format(datetime.date.today())
        self.client.patch('/devices/change_status', self.data, format='json')
        device_status_log = models.DeviceStatusLog.objects.get(device=self.device)
        self.assertEqual(device_status_log.device, self.device)
        self.assertEqual(device_status_log.device_status, self.new_status)
        self.assertEqual(self.date_with_format(device_status_log.status_change_datetime), change_date)

    def test_should_not_update_the_status_if_current_status_is_DADO_DE_BAJA(self):
        self.device.device_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.DADO_DE_BAJA)
        self.device.device_end_status_type = models.DeviceEndStatusType.objects.get(
            name=models.DeviceEndStatusType.DAÑADO)
        self.device.save()
        response = self.client.patch('/devices/change_status', self.data, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status.name, models.DeviceStatus.DADO_DE_BAJA)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], DeviceService.CHANGE_STATUS_ERROR_MESSAGE)

    def test_set_actual_return_date_if_the_device_is_assigned(self):
        expected_date = self.date_with_format(datetime.date.today())
        self.device.device_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.ASIGNADO)
        self.device.life_start_date = datetime.date.today()
        self.device.save()
        assignment = mommy.prepare_recipe('devices.assignment_recipe')
        assignment.save()
        device_assignment = models.DeviceAssignment(assignment=assignment, device=self.device)
        device_assignment.save()
        self.client.patch('/devices/change_status', self.data, format='json')
        device_assignment.refresh_from_db()
        self.assertEqual(expected_date, self.date_with_format(device_assignment.actual_return_date))

    def test_should_not_update_return_date_when_device_has_never_assigned(self):
        self.device.device_status = models.DeviceStatus.objects.get(name=models.DeviceStatus.DISPONIBLE)
        self.device.life_start_date = datetime.date.today()
        self.device.save()
        self.client.patch('/devices/change_status', self.data, format='json')
        device_assignment = DeviceService.get_last_device_assignment(self.device)
        self.assertIsNone(device_assignment)

    def test_should_not_update_the_status_DADO_DE_BAJA_if_end_status_type_is_empty(self):
        response = self.client.patch('/devices/change_status', self.data_dado_de_baja, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status.name, models.DeviceStatus.DISPONIBLE)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], DeviceService.CHANGE_STATUS_ERROR_MESSAGE)

    def test_should_update_the_status_DADO_DE_BAJA_if_end_status_type_is_not_empty(self):
        self.data_dado_de_baja.update({'new_device_end_status_type': 2})
        response = self.client.patch('/devices/change_status', self.data_dado_de_baja, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status.name, models.DeviceStatus.DADO_DE_BAJA)
        self.assertEqual(self.device.device_end_status_type.id, 2)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_should_update_the_status_DADO_DE_BAJA_if_end_status_type_is_not_empty_and_end_status_comment_is_not_empty(
            self):
        self.data_dado_de_baja.update({'new_device_end_status_type': 2, 'new_device_end_status_comment': 'Comentarios'})
        response = self.client.patch('/devices/change_status', self.data_dado_de_baja, format='json')
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_status.name, models.DeviceStatus.DADO_DE_BAJA)
        self.assertEqual(self.device.device_end_status_type.id, 2)
        self.assertEqual(self.device.device_end_status_comment, 'Comentarios')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
