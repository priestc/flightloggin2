from django import forms
from django.forms import widgets
from django.forms import ModelChoiceField, CharField
from models import create_route_from_string, Route
from django.utils.safestring import mark_safe

from django.forms.widgets import TextInput

class RouteWidget(TextInput):
    def _format_value_out(self, value):
        try:
            value = Route.objects.filter(pk=value).values_list('fallback_string')[0][0]
        except:
            value = ""
            
        return value

    def render(self, name, value, attrs=None):
        value = self._format_value_out(value)
        return super(RouteWidget, self).render(name, value, attrs={"class": "route_line"})
        
    def _has_changed(self, initial, data):
        return super(RouteWidget, self)._has_changed(self._format_value_out(initial), data)
        
       
class RouteField(ModelChoiceField):
    def clean(self, value):
        return create_route_from_string(value)
