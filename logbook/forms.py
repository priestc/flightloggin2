from django import forms
from django.forms import ModelForm, ModelChoiceField
from models import *
from route.forms import RouteField
from plane.forms import PlaneField

class BlankFloatField(forms.FloatField):
    def clean(self, value):
        if not value:
            value = 0.0
        return float(value)
        
class BlankIntField(forms.IntegerField):
    def clean(self, value):
        if not value:
            value = 0
        return int(value)


class FlightForm(ModelForm):

    route = RouteField(widget=forms.TextInput, required=False, queryset=Route.objects.get_empty_query_set())
    plane = PlaneField(queryset=Plane.objects.get_empty_query_set(), required=True)
    
    pic =      BlankFloatField()
    sic =      BlankFloatField()
    solo =     BlankFloatField()
    dual_g =   BlankFloatField()
    dual_r =   BlankFloatField()
    xc =       BlankFloatField()
    act_inst = BlankFloatField()
    sim_inst = BlankFloatField()
    night =    BlankFloatField()
    
    day_l =    BlankIntField()
    night_l =  BlankIntField()
    app =      BlankIntField()
    
    
    def __init__(self, *args, **kwargs):
        custom_queryset = False    
        if kwargs.has_key('planes_queryset'):
            custom_queryset = kwargs['planes_queryset']
            del kwargs['planes_queryset']
            
        super(FlightForm, self).__init__(*args, **kwargs)
        if custom_queryset:
            self.fields['plane'].queryset = custom_queryset
            
    def clean(self):
        if self.cleaned_data.get('total',-1) <= 0.0:
            raise forms.ValidationError("'Total Time' must be positive")
        return self.cleaned_data

    class Meta:
        model = Flight
        exclude = ('user', )
