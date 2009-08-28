from django.forms import widgets
from django.forms import ModelChoiceField, CharField
from models import create_route_from_string, Route
from django.utils.safestring import mark_safe

class RouteWidget(widgets.TextInput):
    input_type = None
    def render(self, name, value, attrs=None):
        return mark_safe("<input class=\"route_line\" type=\"text\" value=\"" + str(value) + "\" name=\"" + name + "\"/>")
        
class RouteField(ModelChoiceField):
    widget = RouteWidget
    def clean(self, value):
        return create_route_from_string(value)
