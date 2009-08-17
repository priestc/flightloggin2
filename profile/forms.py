from django.forms import ModelForm
from models import *
from logbook.models import Columns
from profile.models import CurrencyDo

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )

class ColumnsForm(ModelForm):
    class Meta:
        model = Columns
        exclude = ('user', )

class AutoForm(ModelForm):
    class Meta:
        model = AutoButton
        exclude = ('user', )

class Currency(ModelForm):
    class Meta:
        model = CurrencyDo
        exclude = ('user', )
