from django.http import HttpResponse
from django.template import loader
from forms import DeviceForm


def devices(request):
    template = loader.get_template('main/devices.html')
    context = {}
    return HttpResponse(template.render(context, request))


def device_form(request):
    template = loader.get_template('main/device_form.html')
    form = DeviceForm()
    context = {'form': form}
    return HttpResponse(template.render(context, request))

