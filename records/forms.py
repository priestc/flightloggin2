from django.forms.models import modelformset_factory
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.contrib.auth.models import User

from django import forms
from models import *

class NonFlightForm(ModelForm):
    #user = forms.ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput)
    class Meta:
        model = NonFlight
        exclude = ('user' )
        
NonFlightFormset = modelformset_factory(NonFlight, form=NonFlightForm, extra=1, can_delete=True)
