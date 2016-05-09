# -*- coding: utf-8 -*-
from django.conf.urls import url
from devices import views


urlpatterns =[
                url(r'^device_form$', views.device_form, name='device_form')
            ]