from django import forms
from django.forms import ModelChoiceField
from models import *
from logbook.forms import FlightForm
from plane.models import Plane
       
###############################################################################

class ImportForm(forms.Form):
    file = forms.FileField(required=False)
    url = forms.CharField(required=False)
    
###############################################################################
###############################################################################

class ImportFlightForm(FlightForm):
    plane = ModelChoiceField(queryset=Plane.objects.all(),
                             widget=forms.TextInput)
