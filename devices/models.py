# coding=utf8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeviceType(models.Model):
    name = models.CharField(verbose_name=_(u'Nombre'), max_length=50, unique=True)
    code = models.CharField(verbose_name=_(u'Código'), max_length=1, unique=True)

    class Meta:
        verbose_name = _(u'Tipo de Dispositivo')
        verbose_name_plural = _(u'Tipos de Dispositivo')

    def __str__(self):
        return '%s(%s)' % (self.name, self.code)

class DeviceBrand(models.Model):
    name = models.CharField(verbose_name=_(u'Nombre'), max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Marca de Dispositivo')
        verbose_name_plural = _(u'Marcas de Dispositivo')