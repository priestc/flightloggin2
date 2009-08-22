from django.forms import ModelChoiceField, CharField
from models import create_route_from_string, Route

class RouteField(ModelChoiceField):
    def clean(self, value):
        return create_route_from_string(value)
