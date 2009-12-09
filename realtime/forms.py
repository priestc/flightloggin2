from django.forms import ModelForm
from models import Duty

class DutyForm(ModelForm):
    class Meta:
        model = Duty
