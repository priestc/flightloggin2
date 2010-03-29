import re

from django import forms
from django.conf import settings
from django.forms import ModelForm, ModelChoiceField
from django.contrib.admin import widgets
from django.forms.widgets import TextInput, HiddenInput
from django.forms.util import ValidationError

from models import *
from logbook.utils import from_minutes
from plane.models import Plane

#####################################

class BlankHourWidget(TextInput):
    def _format_value_out(self, value):
        """In: decimal number
           Out: a string formatted to HH:MM
           a zero value outputs an empty string"""
        
        if not value or value == 0:
            return ""

        return str(to_minutes(value))

    def render(self, name, value, attrs=None):
        value = self._format_value_out(value)
        attrs.update({"class": "float_line"})
        return super(BlankHourWidget, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        return super(BlankHourWidget, self).\
                    _has_changed(self._format_value_out(initial), data)
        
class BlankDecimalWidget(BlankHourWidget):
    def _format_value_out(self, value):
        """Prepare value for output in the mass entry form
           In: decimal number
           Out: a string of that decimal number
           a zero value outputs an empty string"""
        
        if not value or value == 0:
            return ""
        else:
            return value
    
class BlankIntWidget(BlankHourWidget):
    def _format_value_out(self, value):
        """Prepare value for outout in the mass entry form
           In: an int
           Out: a string of that int
           a zero value outputs an empty string"""
        
        if not value or value == 0:
            return ""
        else:
            return str(value)

class BlankHourField(forms.Field):
    widget = BlankHourWidget
    def clean(self, value):
        super(BlankHourField, self).clean(value)
        
        if not value:
            return 0
        
        value = value.replace(',','.')
        
        match = re.match("^([0-9]{1,5}):([0-9]{2})$", value)
        if match:
            dec = str(from_minutes(value))
        else:
            dec = str(value)
            
        try:
            ev = eval(dec)
        except:
            raise ValidationError("Invalid Formatting")
            
        return ev
        
    def __init__(self, *args, **kwargs):
        super(BlankHourField, self).__init__(required=False, *args, **kwargs)
        
class BlankDecimalField(BlankHourField):
    widget = BlankDecimalWidget

class BlankIntField(BlankHourField):
    widget = BlankIntWidget
    
###############################################################################

class PlaneTextInput(TextInput):
    def render(self, name, value, attrs=None):
        value = self._format_value_out(value)
        return super(PlaneTextInput, self).render(name, value, attrs)
    
    def _format_value_out(self, value):
        """
        In: plane pk
        Out: that plane's tailnumber
        """
        
        if not value or value == 0:
            return ""

        return Plane.objects.get(pk=value).tailnumber
    
    
    def _has_changed(self, initial, data):
        return super(PlaneTextInput, self).\
                    _has_changed(self._format_value_out(initial), data)

class TextPlaneField(ModelChoiceField):
    """
    A field that returns a plane instance and uses a text field widget 
    instead of a dropdown box.
    """
    
    widget = PlaneTextInput()
    
    def clean(self, val):
        """
        Turns the entered value (a tailnumber), into a plane instance
        """
        
        if val.startswith("pk:"):
            pk = val[3:]
            p = Plane.goon(pk=pk, user=self.user)
            if p:
                return p
            else:
                return Plane.objects.get(pk=settings.UNKNOWN_PLANE_ID)  
        
        if val == '':
            ## if input was blank, get and return the global unknown plane
            return Plane.objects.get(pk=settings.UNKNOWN_PLANE_ID)
        
        elif " " in val:
            tn, ty = val.split(' ')[:2]
            ty = ty.upper()
            kwarg = {"tailnumber": tn, "user": self.user, "type": ty}
        else:
            tn = val
            kwarg = {"tailnumber": tn, "user": self.user}
        
        try:
            return Plane.objects.filter(retired=False, **kwarg)[0]
        except IndexError:
            # couldn't find airplane, it either doesn't exist, or it's retired
            return Plane.objects.create(**kwarg)
    
###############################################################################

class PopupFlightForm(ModelForm):
    
    route_string = forms.CharField(label="Route", widget=TextInput(), required=False)
    
    total =    BlankDecimalField(label="Total Time")
    pic =      BlankDecimalField(label="PIC")
    sic =      BlankDecimalField(label="SIC")
    solo =     BlankDecimalField(label="Solo")
    dual_g =   BlankDecimalField(label="Dual Given")
    dual_r =   BlankDecimalField(label="Dual Received")
    xc =       BlankDecimalField(label="Cross Country")
    act_inst = BlankDecimalField(label="Actual Instrument")
    sim_inst = BlankDecimalField(label="Simulated Instrument")
    night =    BlankDecimalField(label="Night")
    
    day_l =    BlankIntField(label="Day Landings")
    night_l =  BlankIntField(label="Night Landings")
    app =      BlankIntField(label="Approaches")
    
    def __init__(self, *args, **kwargs):
        
        if kwargs.has_key('user'):
            self.user = kwargs.pop('user')
        else:
            from share.middleware import share
            self.user = share.get_display_user()
        
        super(PopupFlightForm, self).__init__(*args, **kwargs)

        self.fields['date'].widget = widgets.AdminDateWidget()
        
        from django.db.models import Max
        self.fields['plane'].queryset = \
                 Plane.objects\
                      .user_common(self.user)\
                      .exclude(retired=True)\
                      .annotate(fd=Max('flight__date'))\
                      .order_by('-fd')
        
        self.fields['plane'].user = self.user

    class Meta:
        model = Flight
        exclude = ('user', 'speed', 'gallons', 'gph', 'mpg', 'route')
        
    def clean_fuel_burn(self):
        from fuel_burn import FuelBurn
        value = self.cleaned_data['fuel_burn']
        
        if value == '':
            return ''
        
        ## this will raise the proper validation errors
        FuelBurn(input=value)
        
        return value
              
###############################################################################

class FormsetFlightForm(PopupFlightForm):
    """Form used for the mass entry section. It's the same as the normal flight
       form except that it renders the route field as a string, and the
       remarks are in a big textbox
    """
    
    remarks = forms.CharField(
                widget=forms.TextInput(attrs={"class": "remarks_line"}),
                required=False)
                
    person = forms.CharField(
                widget=forms.TextInput(attrs={"class": "person_line",
                                              "maxlength": 60}),
                required=False)
        
from django.forms.models import BaseModelFormSet
class MassEntryFormset(BaseModelFormSet):
    """
    An edited formset to deal with the custom plane queryset, as well as
    passing in the user instance to each form
    """
    
    def __init__(self, *args, **kwargs):
            

        self.user = kwargs.pop('user')
        self.text_plane = self.user.get_profile().text_plane
        
        super(MassEntryFormset, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        """
        Swaps out the plane field. If the user wants a text field, it drops in
        a TextPlane instance, otherwise it just overwrites the queryset
        with a queryset depicting all planes owned by the user
        """
        
        super(MassEntryFormset, self).add_fields(form, index)
        
        qs = Plane.objects.user_common(self.user)
        
        if self.text_plane:
            form.fields["plane"] = TextPlaneField(qs)
            form.fields["plane"].user=self.user
        else:
            form.fields["plane"] = ModelChoiceField(queryset=qs, required=True)
