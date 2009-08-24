from django.forms.models import modelformset_factory
from django.forms import ModelForm
from models import *

class NonFlightForm(ModelForm):
    class Meta:
        model = NonFlight
        exclude = ('user', )
        
NonFlightFormset = modelformset_factory(NonFlight, form=NonFlightForm, extra=1, can_delete=True)
