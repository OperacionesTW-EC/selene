# -*- coding: utf-8 -*-
from django.conf.urls import url
from devices import views

urlpatterns =[
                url(r'^devices$', views.devices, name='devices'),
            ]