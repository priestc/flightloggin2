from django import forms
from django.forms import ModelChoiceField
from models import *
from logbook.forms import PopupFlightForm
from plane.models import Plane
       
###############################################################################

class ImportForm(forms.Form):
    file = forms.FileField(required=False)
    url = forms.CharField(required=False)
    
###############################################################################
###############################################################################

class ImportFlightForm(PopupFlightForm):
    plane = ModelChoiceField(queryset=Plane.objects.all(),
                             widget=forms.TextInput)

    #def save(self, *args, **kwargs):
   # 	# disable badges checking when adding flights via the import feature
    	# because after the import is done, we calculate badges once.
    #	kwargs['no_badges'] = True
   # 	return super(ImportFlightForm, self).save(*args, **kwargs)