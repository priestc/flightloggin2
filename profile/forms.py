from django.forms import ModelForm
from django.contrib.auth.models import User

from logbook.models import Columns
from models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'facebook_uid', 'secret_key')

class ColumnsForm(ModelForm):
    class Meta:
        model = Columns
        exclude = ('user', )

class AutoForm(ModelForm):
    class Meta:
        model = AutoButton
        exclude = ('user', )
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
