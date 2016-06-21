# coding=utf8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import datetime


class DeviceType(models.Model):
    name = models.CharField(verbose_name=_(u'Nombre'), max_length=50, unique=True)
    code = models.CharField(verbose_name=_(u'Código'), max_length=1, unique=True)
    life_time = models.IntegerField(verbose_name=_(u'Tiempo de Vida'), blank=True, null=True)
    LAPTOP_CODE = 'L'
    LAPTOP_NAME = 'Laptop'

    def has_lifetime(self):
        if self.life_time is None:
            return False
        return True

    class Meta:
        verbose_name = _(u'Tipo de Dispositivo')
        verbose_name_plural = _(u'Tipos de Dispositivo')
        ordering = ['name']

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)


class DeviceBrand(models.Model):
    name = models.CharField(verbose_name=_(u'Nombre'), max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Marca de Dispositivo')
        verbose_name_plural = _(u'Marcas de Dispositivo')


class DeviceStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    DISPONIBLE = 'Disponible'
    ASIGNADO = 'Asignado'
    MANTENIMIENTO = 'Mantenimiento'
    DADO_DE_BAJA = 'Dado de baja'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Estado de Dispositivo')
        verbose_name_plural = _(u'Estados de Dispositivo')


class Device(models.Model):

    def __check_required_asset_fields(self):
        return self.serial_number in (None, '') or self.model in (None, '') or self.purchase_date in (None, '')

    def validate_required_fields(self):
        if self.asset == 1 and self.__check_required_asset_fields():
            raise ValidationError(
                _('El número de serie, modelo y fecha de compra son obligatorios si selecciona el campo activo'),
                code='invalid')
        if self.life_start_date_required() and self.life_start_date in (None, ''):
            raise ValidationError(
                _('life_start_date required on an assigned device with a lifetime'),
                code='invalid')
        if not self.has_lifetime() and self.life_start_date not in (None, ''):
            raise ValidationError(
                _('life_start_date present on a device with no lifetime'),
                code='invalid')

    def clean(self):
        self.validate_required_fields()

    def assign(self, date=None):
        if self.has_lifetime_and_life_has_not_begun():
            self.life_start_date = date or datetime.date.today()
        self.mark_assigned()

    def life_start_date_required(self):
        return self.has_lifetime() and self.device_status_name() == DeviceStatus.ASIGNADO

    def mark_assigned(self):
        self.device_status = DeviceStatus.objects.get(name=DeviceStatus.ASIGNADO)

    def has_lifetime(self):
        return self.device_type.has_lifetime()

    def has_lifetime_and_life_has_begun(self):
        return self.has_lifetime() and self.life_start_date not in (None, '')

    def has_lifetime_and_life_has_not_begun(self):
        return self.has_lifetime() and self.life_start_date in (None, '')

    def device_type_name(self):
        return self.device_type.name

    def device_brand_name(self):
        return self.device_brand.name

    def device_status_name(self):
        return self.device_status.name

    def full_code(self):
        return self.generate_code() + '{0:04d}'.format(self.sequence)

    def calculate_life_end_date(self):
        if self.has_lifetime_and_life_has_begun():
            return self.life_start_date + datetime.timedelta(days=self.device_type.life_time * 365)

    def life_end_date(self):
        return self.calculate_life_end_date()

    def generate_code(self):
        return self.ownership.upper() + ("A" if self.asset else "E") + self.device_type.code.upper()

    def calculate_next_sequence_value(self):
        last_device_with_same_code = Device.objects.filter(code=self.code).order_by('-sequence')
        return 1 if len(last_device_with_same_code) == 0 else last_device_with_same_code[0].sequence + 1

    def life_start_date_or_assignment_date(self):
        """
        Para dispositivos con la vida limitada (DeviceType.life_time is not None, e.g. Laptop),
        se devuelve 'life_start_date' si hay.

        Para otros se devuelve la fecha de asignación más reciente, si hay
        """
        return self.life_start_date or self.get_last_assignment_date()

    def get_last_assignment_date(self):
        query_set = DeviceAssignment.objects.filter(device=self)
        if query_set:
            return query_set.first().assignment_date

    def save(self, *args, **kwargs):
        self.clean()
        if not self.pk:
            self.code = self.generate_code()
            self.sequence = self.calculate_next_sequence_value()
        super(Device, self).save(*args, **kwargs)

    class Meta:
        ordering = ['device_type']
        unique_together = (('code', 'sequence'),)

    device_type = models.ForeignKey('DeviceType')
    device_brand = models.ForeignKey('DeviceBrand')
    asset = models.IntegerField()
    ownership = models.CharField(max_length=2)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    sequence = models.IntegerField()
    code = models.CharField(max_length=10)
    device_status = models.ForeignKey('DeviceStatus')
    life_start_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Proyecto')
        verbose_name_plural = _(u'Proyectos')


class Assignment(models.Model):
    assignee_name = models.CharField(max_length=50)
    expected_return_date = models.DateField(blank=True, null=True)
    project = models.ForeignKey('Project', null=True, blank=True)
    devices = models.ManyToManyField(Device, through='DeviceAssignment')

    def assignment_date(self):
        query_set = DeviceAssignment.objects.filter(assignment=self)
        if query_set:
            return query_set.first().assignment_date

    def project_name(self):
        if self.project:
            return self.project.name

    class Meta:
        verbose_name = _(u'Asignación')
        verbose_name_plural = _(u'Asignaciones')


class DeviceAssignment(models.Model):
    device = models.ForeignKey('Device')
    assignment = models.ForeignKey('Assignment')
    assignment_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(null=True)

    def id(self):
        return self.device.id

    def full_code(self):
        return self.device.full_code()

    def device_type_name(self):
        return self.device.device_type.name

    def device_brand_name(self):
        return self.device.device_brand.name

    def device_description(self):
        return self.device.description

    def return_date(self):
        return self.assignment.expected_return_date

    def life_end_date(self):
        return self.device.calculate_life_end_date()

    def assignee_name(self):
        return self.assignment.assignee_name

    def project(self):
        if self.assignment.project:
            return self.assignment.project.name
        return ''

    def life_start_date_or_assignment_date(self):
        """
        Para dispositivos con la vida limitada (DeviceType.life_time is not None, e.g. Laptop),
        se devuelve 'life_start_date' si hay.

        Para otros se devuelve la fecha de asignación
        """
        return self.device.life_start_date or self.assignment_date

    class Meta:
        verbose_name = _(u'Asignación de Dispositivos')
        verbose_name_plural = _(u'Asignaciones de Dispositivos')
        ordering = ['-assignment_date', '-id']


class DeviceStatusLog(models.Model):
    device = models.ForeignKey('Device')
    device_status = models.ForeignKey('DeviceStatus')
    status_change_datetime = models.DateTimeField(blank=False, null=False, default=timezone.now)
