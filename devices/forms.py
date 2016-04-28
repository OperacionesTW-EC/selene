from django  import forms
from devices.models import *


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_type', 'device_brand', 'asset', 'serial_number', 'model', 'purchase_date', 'ownership']

    types = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=DeviceType.objects.all())
    brands = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=DeviceBrand.objects.all())
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    model = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    purchase_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control datepicker'}))
    ownership = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(('TW', 'TW'),('CL', 'CL')))
