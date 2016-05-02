# -*- coding: utf-8 -*-
from django.conf.urls import url
from devices import views

urlpatterns =[
                url(r'^devices$', views.devices, name='devices'),
                url(r'^device_form$', views.device_form, name='device_form'),
                url(r'^save_device$', views.save_device, name='save_device'),
            ]