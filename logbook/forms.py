from django import forms
from django.forms import ModelForm, ModelChoiceField
from models import *
from route.forms import RouteField
from plane.forms import PlaneField


class FlightForm(ModelForm):

    route = RouteField(widget=forms.TextInput, required=False, queryset=Route.objects.get_empty_query_set())
    plane = PlaneField(queryset=Plane.objects.get_empty_query_set(), required=True)
    
    def __init__(self, *args, **kwargs):
        custom_queryset = False    
        if kwargs.has_key('planes_queryset'):
            custom_queryset = kwargs['planes_queryset']
            del kwargs['planes_queryset']
            
        super(FlightForm, self).__init__(*args, **kwargs)
        if custom_queryset:
            self.fields['plane'].queryset = custom_queryset
            
    def clean_total(self):
        total = self.cleaned_data['total']
        if total <= 0:
            raise forms.ValidationError("'Total Time' must not be zero or negative")
        
        
        return self.cleaned_data

    class Meta:
        model = Flight
        exclude = ('user', )
