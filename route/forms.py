from django import forms
from django.forms import widgets
from django.forms import ModelChoiceField, CharField
from models import Route
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
        attrs.update({"class": "route_field", "maxlength": 30})
        return super(RouteWidget, self).render(name, value, attrs)
        
    def _has_changed(self, initial, data):
        return super(RouteWidget, self)._has_changed(self._format_value_out(initial), data)
        
       
class RouteField(ModelChoiceField):
    widget = RouteWidget
    def clean(self, value):
        return Route.from_string(value)
