# -*- coding: utf-8 -*-
from django.conf.urls import url
from main import views

urlpatterns =[
                url(r'^$', views.index, name='home'),
                url(r'^login', views.login, name='login'),
            ]