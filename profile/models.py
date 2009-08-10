from django.db import models
from django.contrib.auth.models import User
from constants import *
from plane.constants import CATEGORY_CLASSES, FAKE_CLASSES

class Profile(models.Model):
    user =           models.ForeignKey(User, primary_key=True)

    dob =            models.DateField(             "Date of Birth",             blank=True, default="1900-01-01")
    style =          models.IntegerField(                                       choices=STYLES, default=1)
    date_format =    models.IntegerField(          "Date Format",               choices=DATE_FORMATS, default=1)

    real_name =      models.CharField(             "Real Name",                 blank=True, max_length=32)
    per_page =       models.PositiveIntegerField(  "Logbook Entries Per Page",  default=50)
    backup_email =   models.EmailField(            "Backup Email",              blank=True, help_text="Leave blank to use the email listed above")
    backup_freq =    models.IntegerField(          "Backup Frequency",          choices=BACKUP_FREQUENCY, default=0)
    type_str =       models.CharField(                                          blank=True, max_length=128)

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.real_name)

    class Meta:
        pass

class Entries(models.Model):
    user =          models.ForeignKey(User, blank=False, primary_key=True)
    pic =           models.BooleanField(default=True)
    sic =           models.BooleanField(default=True)
    solo =          models.BooleanField(default=True)
    dual_r =        models.BooleanField(default=True)
    dual_g =        models.BooleanField(default=True)
    act_inst =      models.BooleanField(default=True)
    sim_inst =      models.BooleanField(default=True)
    xc =            models.BooleanField(default=True)
    night =         models.BooleanField(default=True)

    app =           models.BooleanField(default=True)
    day_l =         models.BooleanField(default=True)
    night_l =       models.BooleanField(default=True)

    student =       models.BooleanField(default=True)
    instructor =models.BooleanField(default=True)
    captain =       models.BooleanField(default=True)
    fo =            models.BooleanField(default=True)
    remarks =       models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.user, )

    def as_list(self):
        ret = []

        return ret


class AutoButton(models.Model):
    user =          models.ForeignKey(User, blank=False, primary_key=True)
    pic =           models.BooleanField(default=True)
    sic =           models.BooleanField(default=False)
    solo =          models.BooleanField(default=False)
    dual_r =        models.BooleanField(default=False)
    dual_g =        models.BooleanField(default=False)
    act_inst =      models.BooleanField(default=False)
    sim_inst =      models.BooleanField(default=False)
    xc =            models.BooleanField(default=False)
    night =         models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.user, )

class CurrencyDo(models.Model):
    user =          models.ForeignKey(User, blank=False, primary_key=True)

    faa_medical =   models.BooleanField("Medical")
    air_inst =      models.BooleanField("Instrument-Airplane")
    heli_inst =     models.BooleanField("Instrument-Helicopter")
    one35 =         models.BooleanField("Part 135 Minimums")
    atp =           models.BooleanField("ATP-Airplane Minimums")
    fr =            models.BooleanField("Flight Review")
    cfi =           models.BooleanField("CFI Expiration")

    d_1 =           models.BooleanField(CATEGORY_CLASSES[1][1], default=True)
    n_1 =           models.BooleanField()

    d_2 =           models.BooleanField(CATEGORY_CLASSES[2][1])
    n_2 =           models.BooleanField()

    d_3 =           models.BooleanField(CATEGORY_CLASSES[3][1])
    n_3 =           models.BooleanField()

    d_4 =           models.BooleanField(CATEGORY_CLASSES[4][1])
    n_4 =           models.BooleanField()

    d_5 =           models.BooleanField(CATEGORY_CLASSES[5][1])
    n_5 =           models.BooleanField()

    d_6 =           models.BooleanField(CATEGORY_CLASSES[6][1])
    n_6 =           models.BooleanField()

    d_7 =           models.BooleanField(CATEGORY_CLASSES[7][1])
    n_7 =           models.BooleanField()

    d_8 =           models.BooleanField(CATEGORY_CLASSES[8][1])
    n_8 =           models.BooleanField()

    d_9 =           models.BooleanField(CATEGORY_CLASSES[9][1])
    n_9 =           models.BooleanField()

    d_10 =          models.BooleanField(CATEGORY_CLASSES[10][1])
    n_10 =          models.BooleanField()

    d_11 =          models.BooleanField(CATEGORY_CLASSES[11][1])
    n_11 =          models.BooleanField()

    d_12 =          models.BooleanField(CATEGORY_CLASSES[12][1])
    n_12 =          models.BooleanField()

    d_13 =          models.BooleanField(CATEGORY_CLASSES[13][1])
    n_13 =          models.BooleanField()

    d_14 =          models.BooleanField(CATEGORY_CLASSES[14][1])
    n_14 =          models.BooleanField()

    d_20 =          models.BooleanField(FAKE_CLASSES[0][1])
    n_20 =          models.BooleanField()

    d_21 =          models.BooleanField(FAKE_CLASSES[1][1])
    n_21 =          models.BooleanField()

