import re
from django import forms
from django.forms import ModelForm, ModelChoiceField
from models import *
from logbook.forms import FlightForm
from plane.forms import SimplePlaneField
from route.forms import SimpleRouteField

class ImportForm(forms.Form):
    file = forms.FileField()
    
class ImportFlight(FlightForm):
    route = SimpleRouteField()
    plane = SimplePlaneField()
