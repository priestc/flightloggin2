import re

from django.forms import ModelChoiceField, ModelForm, CharField
from django import forms

from models import *
from logbook.fuel_burn import FuelBurn
from tagging.forms import TagField


def clean_tailnumber(self):
    
    tn = self.cleaned_data.get('tailnumber', "")
    
    if " " in tn:
        raise forms.ValidationError("Spaces not allowed in Tailnumber")
    
    ## if more than one character matches this regex, raise error
    if re.subn(r'[^A-Za-z0-9-\[\]\)\(}{\.]', 'X', tn)[1] > 0:
        raise forms.ValidationError("Invalid characters")
    
    return tn

def clean_type(self):
    
    ty = self.cleaned_data.get('type', "")
    
    if " " in ty:
        raise forms.ValidationError("Spaces not allowed in Type")
    
    ## if more than one character matches this regex, raise error
    if re.subn(r'[^A-Za-z0-9-\[\]\)\(}{\.]', 'X', ty)[1] > 0:
        raise forms.ValidationError("Invalid characters")
    
    return ty

def clean(self):
    ty = self.cleaned_data.get('type', "")
    model = self.cleaned_data.get('model', "")
    
    if not ty and not model:
        raise forms.ValidationError("Must define either a Model name or a Type")
    
    return self.cleaned_data

def clean_fuel_burn(self):
    fuel_burn = self.cleaned_data.get('fuel_burn', "")
    
    ## this will raise validation error if the units or w/e are incorrect
    FuelBurn.split_and_validate(fuel_burn)
    
    return fuel_burn

class PopupPlaneForm(ModelForm):
    tags = TagField(widget=forms.Textarea, required=False)
    class Meta:
        model = Plane
    
    ## add these functions to the class this way so we don't have to duplicate
    ## code when adding them to the mass entry form as well...
    clean_tailnumber = clean_tailnumber
    clean_type = clean_type
    clean_fuel_burn = clean_fuel_burn
    clean = clean
        
class MassPlaneForm(ModelForm):
    description = CharField(required=False,
                            widget=forms.TextInput()
                  )
    class Meta:
        model = Plane
        exclude = ('user', )
        
    clean_tailnumber = clean_tailnumber
    clean_type = clean_type
    clean_fuel_burn = clean_fuel_burn
    clean = clean
    
    
from django.forms.models import modelformset_factory

PlaneFormset = modelformset_factory(Plane,
                                    form=MassPlaneForm,
                                    extra=5,
                                    can_delete=False)
