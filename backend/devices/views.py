from django.http import HttpResponse
from django.template import loader
from forms import DeviceForm
from django.contrib import messages
from rest_framework import viewsets
from devices.serializers import *

def devices(request):
    print request.GET
    template = loader.get_template('main/devices.html')
    context = {}
    return HttpResponse(template.render(context, request))


def device_form(request):
    template = loader.get_template('main/device_form.html')
    form = DeviceForm()
    if request.method == 'POST':
        print 'test', request.POST
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Dispositivo registrado correctamente')
        else:
            messages.add_message(request, messages.ERROR, 'El formulario tiene errores')
    context = {'form': form}
    return HttpResponse(template.render(context, request))


class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer

class DeviceBrandViewSet(viewsets.ModelViewSet):
    queryset = DeviceBrand.objects.all()
    serializer_class = DeviceBrandSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

