# coding=utf8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeviceType(models.Model):
    name = models.CharField(verbose_name=_(u'Nombre'), max_length=50, unique=True)
    code = models.CharField(verbose_name=_(u'Código'), max_length=1, unique=True)

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


class Device(models.Model):
    def __check_required_fields(self):
        return self.serial_number in (None, '') or self.model in (None, '') or self.purchase_date in (None, '')

    def validate_required_fields(self):
        if self.asset == 1 and self.__check_required_fields():
            raise ValidationError(_('El número de serie, modelo y fecha de compra son obligatorios si selecciona el campo activo'), code='invalid')

    def clean(self):
        self.validate_required_fields()

    def device_type_name(self):
        return self.device_type.name

    def device_brand_name(self):
        return self.device_brand.name

    def full_code(self):
        return self.generate_code()+'{0:04d}'.format(self.sequence)

    def generate_code(self):
        return self.ownership.upper()+("A" if self.asset else "E")+self.device_type.code.upper()

    def calculate_next_sequence_value(self):
        last_device_with_same_code = Device.objects.filter(code=self.code).order_by('-sequence')
        return 1 if len(last_device_with_same_code) == 0 else last_device_with_same_code[0].sequence + 1

    def save(self, *args, **kwargs):
        self.clean()
        if not self.pk:
            self.code = self.generate_code()
            self.sequence = self.calculate_next_sequence_value()
        super(Device, self).save(*args, **kwargs)

    class Meta:
        ordering = ['device_type']

    device_type = models.ForeignKey('DeviceType')
    device_brand = models.ForeignKey('DeviceBrand')
    asset = models.IntegerField()
    ownership = models.CharField(max_length=2)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    sequence = models.IntegerField()
    code = models.CharField(max_length=10)


class Project(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Proyecto')
        verbose_name_plural = _(u'Proyectos')



