from django.forms import ModelChoiceField, ModelForm, CharField
from django import forms

from models import *
from tagging.forms import TagField

class PopupPlaneForm(ModelForm):
    tags = TagField(widget=forms.Textarea, required=False)
    class Meta:
        model = Plane
    
    def clean(self):
        
        if " " in self.cleaned_data.get('tailnumber'):
            raise forms.ValidationError("Spaces not allowed in Tailnumber")
        
        return self.cleaned_data
        
class MassPlaneForm(ModelForm):
    description = CharField(required=False,
                            widget=forms.TextInput()
                  )
    class Meta:
        model = Plane
        exclude = ('user', )

class PlaneField(ModelChoiceField):
    pass
    #def label_from_instance(self, obj):
    #    return unicode(obj)
    
    
from django.forms.models import modelformset_factory

PlaneFormset = modelformset_factory(Plane,
                                    form=MassPlaneForm,
                                    extra=5,
                                    can_delete=False)
