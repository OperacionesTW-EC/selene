from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def devices(request):
    return HttpResponse("Hola")

