import re
from django import forms
from django.forms import ModelForm, ModelChoiceField
from models import *
from logbook.forms import FlightForm
from plane.forms import SimplePlaneField
from route.forms import SimpleRouteField
from route.models import Route
from plane.models import Plane

class ImportForm(forms.Form):
    file = forms.FileField()
    
class ImportFlightForm(FlightForm):
    #route = ModelChoiceField(queryset=Route.objects.all(), required=False, widget=forms.TextInput)
    #route = ModelChoiceField(queryset=Airport.objects.all(), widget=forms.TextInput)
    plane = ModelChoiceField(queryset=Plane.objects.all(), widget=forms.TextInput)
