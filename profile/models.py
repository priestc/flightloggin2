from django.db import models
from django.contrib.auth.models import User
from constants import *
from plane.constants import CATEGORY_CLASSES, FAKE_CLASSES

class Profile(models.Model):
    user =           models.ForeignKey(User, primary_key=True)
    
    

    dob =            models.DateField(
                         "Date of Birth",
                         blank=True,
                         default="1900-01-01",
                     )
                     
    style =          models.IntegerField(
                         choices=STYLES,
                         default=2,
                     )
                         
    date_format =    models.CharField(
                         blank=True,
                         max_length=32,
                         default="Y-m-d",
                     )

    real_name =      models.CharField(
                         "Real Name",
                         blank=True,
                         max_length=32,
                     )
                         
    per_page =       models.PositiveIntegerField(
                         "Logbook Entries Per Page",
                         default=50,
                     )
                     
    backup_email =   models.EmailField(
                         "Backup Email",
                         blank=True,
                         help_text="Leave blank to use the email listed above",
                     )
                     
    backup_freq =    models.IntegerField(
                         "Backup Frequency",
                         choices=BACKUP_FREQUENCY,
                         default=0,
                     )
                     
    minutes =        models.BooleanField(
                         "Display times as HH:MM",
                         default=False,
                     )
                     
    text_plane =     models.BooleanField(
                         "Use text field for entering tailnumber",
                         default=False,
                     )
                     
    social =         models.BooleanField("Include me in site-wide stats and lists",
                         default=True,
                     )
                     
    logbook_share =  models.BooleanField("Share Basic Logbook",
                         default=True,
                         help_text='Allow other people to view your Flights, Locations, and Planes',
                     )
    
    events_share =   models.BooleanField("Share Events",
                         default=True,
                         help_text='Allow other people to view your Events',
                     )
    
    records_share =  models.BooleanField("Share Records",
                         default=True,
                         help_text='Allow other people to view your Records',
                     )
    
    other_share =    models.BooleanField("Share everything else",
                         default=True,
                         help_text='Allows people to view everything else; Maps, Graphs, Sigs, Currency...',
                     )
    
    secret_key =     models.CharField(
                         blank=False,
                         max_length=8,
                         default="",
                     )

    def __unicode__(self):
        return u"%s - %s" % (self.user, self.real_name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('logbook', [self.user.username], )

    class Meta:
        ordering = ('-user__date_joined', )
    
    @classmethod
    def get_for_user(cls, user):
        
        if user.is_authenticated():
            try:
                return cls.objects.get(user=user)
            
            except cls.DoesNotExist:
                p = cls(user=user)
                p.save()
                return p
            
        else:
            return cls()
        
    def get_num_format(self):
        if self.minutes:
            return "minutes"
        else:
            return "decimal"
        
    def get_date_format(self):
        if self.date_format:
            return self.date_format
        else:
            return "Y-m-d"
    
    def calc_secret_key(self):
        """
        calculate a secret key for use in facebook and twitter apps
        this key only needs to be calculated once per user account
        """
        
        from django.conf import settings
        from main.utils import hash_ten
        
        s = "%s%s%s" % (self.user.id,
                        self.user.date_joined,
                        settings.SECRET_KEY)
              
        return hash_ten(s, length=8)
        
    def save(self, *args, **kwargs):
        """
        add the secret key if it isn't already set, otherwise,
        just do save as normal
        """
        
        if self.secret_key == '':
            self.secret_key = self.calc_secret_key()
        super(Profile, self).save(*args, **kwargs)
       
        
    def get_email(self):
        if not self.user.email:
            return self.backup_email
        
        return self.user.email
    get_email.short_description="Email"
        
    def adminlink(self):
        """Puts a link in the admin page for the user's logbook"""
        
        return "<a target='_blank' href='http://beta.flightlogg.in%s'>Link</a>"\
                    % self.get_absolute_url()
    adminlink.allow_tags = True
    
    def date_registered(self):
        """Used in the admin interface to see when a user registered"""
        
        from django.utils.dateformat import format
        return format(self.user.date_joined, "M jS, Y")
    date_registered.admin_order_field = 'user__date_joined'


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
    instructor =    models.BooleanField(default=True)
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
    
    def as_jslist(self):
        """Prints out all columns the uer has selected into a javascript
           list
        """
        fields = ('pic','sic','solo','dual_g','dual_r',
                  'xc', 'night','sim_inst', 'act_inst')
        ret = []
        for field in fields:
            if getattr(self, field):
                ret.append(field)
        return ret
        

