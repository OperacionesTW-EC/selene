from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def devices(request):
    template = loader.get_template('main/devices.html')
    context = {}
    return HttpResponse(template.render(context, request))

def device_form(request):
    template = loader.get_template('main/device_form.html')
    context = {}
    return HttpResponse(template.render(context, request))

