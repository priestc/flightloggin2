from django.forms import ModelChoiceField, ModelForm, CharField
from models import *
from tagging.forms import TagField
from django import forms

class PlaneForm(ModelForm):
    
    tags = TagField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = Plane

class PlaneField(ModelChoiceField):
    pass
    #def label_from_instance(self, obj):
    #    return unicode(obj)
