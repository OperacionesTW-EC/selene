from django.http import HttpResponse
from django.template import loader

from selene import settings


def index(request):

    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
