# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangoLogin
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect

def index(request):
    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def login(request):
    login = request.POST["login"]
    password = request.POST["password"]
    user = authenticate(username=login, password=password)

    if user is not None:
        if user.is_active:
            djangoLogin(request, user)
            return HttpResponseRedirect("/devices")
    return HttpResponseRedirect("/index")

def logout(request):
    logout()
    HttpResponseRedirect("/index")