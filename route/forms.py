from django.forms import ModelChoiceField
from models import create_route_from_string

class RouteField(ModelChoiceField):
    def clean(self, string):
        return create_route_from_string(string)
