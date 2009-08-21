from django.forms import ModelChoiceField, CharField
from models import create_route_from_string

class RouteField(ModelChoiceField):
    def clean(self, value):
        return create_route_from_string(value)
        
class SimpleRouteField(CharField):
    def clean(self, value):
        return Route(fallback_string=value)
