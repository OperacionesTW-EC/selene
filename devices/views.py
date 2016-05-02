from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from forms import DeviceForm


def devices(request):
    print request.GET
    template = loader.get_template('main/devices.html')
    context = {}
    return HttpResponse(template.render(context, request))


def device_form(request):
    template = loader.get_template('main/device_form.html')
    form = DeviceForm()
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def save_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect("/devices", {'algo': True})
