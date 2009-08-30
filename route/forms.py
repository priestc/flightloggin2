from django import forms
from django.forms import widgets
from django.forms import ModelChoiceField, CharField
from models import create_route_from_string, Route
from django.utils.safestring import mark_safe

from django.forms.widgets import TextInput

class RouteWidget(TextInput):
     def _format_value(self, value):
         text = unicode(value)
         return text

     def render(self, name, value, attrs=None):
        value = Route.objects.filter(pk=value).values_list('fallback_string')[0][0]
        return super(RouteWidget, self).render(name, value, attrs={"class": "route_line"})
        
       
class RouteField(ModelChoiceField):
    def clean(self, value):
        return create_route_from_string(value)
