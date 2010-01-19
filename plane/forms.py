import re

from django.forms import ModelChoiceField, ModelForm, CharField
from django import forms

from models import *
from tagging.forms import TagField


def clean_tailnumber(self):
    
    tn = self.cleaned_data.get('tailnumber', "")
    
    if " " in tn:
        raise forms.ValidationError("Spaces not allowed in Tailnumber")
    
    ## if more than one character matches this regex, raise error
    if re.subn(Plane.reverse_plane_regex(), 'X', tn)[1] > 0:
        raise forms.ValidationError("Invalid characters")
    
    return tn

def clean_type(self):
    
    ty = self.cleaned_data.get('type', "")
    
    if " " in ty:
        raise forms.ValidationError("Spaces not allowed in Type")
    
    ## if more than one character matches this regex, raise error
    if re.subn(Plane.reverse_plane_regex(), 'X', ty)[1] > 0:
        raise forms.ValidationError("Invalid characters")
    
    return ty

def clean(self):
    ty = self.cleaned_data.get('type', "")
    model = self.cleaned_data.get('model', "")
    
    if not ty and not model:
        raise forms.ValidationError("Must define either a Model name or a Type")
    
    return self.cleaned_data





class PopupPlaneForm(ModelForm):
    tags = TagField(widget=forms.Textarea, required=False)
    class Meta:
        model = Plane
    
    ## add these functions to the class this way so we don't have to duplicate
    ## code when adding them to the mass entry form as well...
    clean_tailnumber = clean_tailnumber
    clean_type = clean_type
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
    clean = clean
    
    
from django.forms.models import modelformset_factory

PlaneFormset = modelformset_factory(Plane,
                                    form=MassPlaneForm,
                                    extra=5,
                                    can_delete=False)
