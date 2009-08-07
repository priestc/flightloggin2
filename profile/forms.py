from django.forms import ModelForm
from models import *
from logbook.models import Columns
from currency.models import CurrencyDo

class ProfileForm(ModelForm):
    class Meta:
        model = Profile

class ColumnsForm(ModelForm):
    class Meta:
        model = Columns

class AutoForm(ModelForm):
    class Meta:
        model = AutoButton

class Currency(ModelForm):
    class Meta:
        model = CurrencyDo
