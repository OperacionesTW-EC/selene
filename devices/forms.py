from django  import forms
from devices.models import *

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ()
    ownership = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=(('TW', 'TW'),('CL', 'CL')))
    asset = forms.CharField(widget= forms.HiddenInput())


