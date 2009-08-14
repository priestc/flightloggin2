from django.forms import ModelChoiceField, ModelForm
from models import *

class PlaneForm(ModelForm):
    class Meta:
        model = Plane

class PlaneField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.tailnumber, obj.type)
