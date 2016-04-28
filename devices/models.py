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
        return self.serial_number is None or self.model is None or self.purchase_date is None

    def required_if_asset(self):
        if self.asset == 1 and self.__check_required_fields():
            raise ValidationError(
                _('Serial Number field is required')
            )

    def clean(self):
        self.required_if_asset()

    device_type = models.ForeignKey('DeviceType')
    device_brand = models.ForeignKey('DeviceBrand')
    asset = models.IntegerField()
    ownership = models.CharField(max_length=2)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)



