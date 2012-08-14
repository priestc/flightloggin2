from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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

class ChangePasswordForm(forms.Form):
    old = forms.CharField(label="Old Password", widget=forms.PasswordInput)
    new = forms.CharField(label="New Password", widget=forms.PasswordInput)
    new2 = forms.CharField(label="Retype new password", widget=forms.PasswordInput)

    def __init__(self, *a, **k):
        self.user = k.pop('user', None)
        super(ChangePasswordForm, self).__init__(*a, **k)

    def clean_old(self):
        old = self.cleaned_data['old']
        user = authenticate(username=self.user.username, password=old)
        if user != self.user:
            raise forms.ValidationError('Invalid old password')
        return old

    def clean(self):
        new = self.cleaned_data['new']
        new2 = self.cleaned_data['new2']
        if new != new2:
            raise forms.ValidationError('Passwords must match')
        return self.cleaned_data

    def save(self):
        #user = User.objects.get(username=self.user.username)
        print "old", self.user.password
        self.user.set_password(self.cleaned_data['new'])
        self.user.save()
        #import debug
        #print user.password