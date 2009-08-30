import re

from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.admin import widgets
from django.forms.widgets import TextInput

from models import *
from route.forms import RouteField, RouteWidget
from plane.forms import PlaneField
from logbook.utils import from_minutes

class BlankZeroWidget(TextInput):
     def _format_value(self, value):
         text = unicode(value)
         return text

     def render(self, name, value, attrs=None):
        if value == 0:
            value = ""
        return super(BlankZeroWidget, self).render(name, value, attrs={"class": "float_line"})
        
#####################################################################################################
        
class BlankFloatField(forms.CharField):

    widget=BlankZeroWidget
    
    def clean(self, value):
    
        if not value:
            return 0.0
            
        if re.match("^\d+:\d{2}$", value):
            value = from_minutes(value)
            
        try:
            value = eval(str(value))
        except:
            raise forms.ValidationError("Invalid formatting")
            
        if float(value) < 0:
            raise forms.ValidationError("Values can't be negative")
            
        return value
        
class BlankIntField(forms.IntegerField):
    
    widget=BlankZeroWidget
    
    def clean(self, value):
        if not value:
            return 0
            
        try:
            value = eval(value)
        except:
            raise forms.ValidationError("Invalid formatting")

        return int(value)
        
#####################################################################################################

class FlightForm(ModelForm):

    route = RouteField(widget=forms.TextInput, required=False, queryset=Route.objects.get_empty_query_set())
    plane = PlaneField(queryset=Plane.objects.get_empty_query_set(), required=True)
    
    total =    BlankFloatField(label="Total Time")
    pic =      BlankFloatField(label="PIC")
    sic =      BlankFloatField(label="SIC")
    solo =     BlankFloatField(label="Solo")
    dual_g =   BlankFloatField(label="Dual Given")
    dual_r =   BlankFloatField(label="Dual Received")
    xc =       BlankFloatField(label="Cross Country")
    act_inst = BlankFloatField(label="Actual Instrument")
    sim_inst = BlankFloatField(label="Simulated Instrument")
    night =    BlankFloatField(label="Night")
    
    day_l =    BlankIntField(label="Day Landings")
    night_l =  BlankIntField(label="Night Landings")
    app =      BlankIntField(label="Approaches")
    
    
    def __init__(self, *args, **kwargs):
        custom_queryset = False    
        if kwargs.has_key('planes_queryset'):
            custom_queryset = kwargs['planes_queryset']
            del kwargs['planes_queryset']
            
        super(FlightForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()
        if custom_queryset:
            self.fields['plane'].queryset = custom_queryset

    class Meta:
        model = Flight
        exclude = ('user', )

#############################################################################################################

class FormsetFlightForm(FlightForm):
        remarks = forms.CharField(widget=forms.TextInput(attrs={"class": "remarks_line"}))
        person = forms.CharField(widget=forms.TextInput(attrs={"class": "person_line"}))
        route = RouteField(queryset=Route.objects.get_empty_query_set(), widget=RouteWidget)
 
