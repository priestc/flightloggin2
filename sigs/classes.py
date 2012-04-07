import datetime
import Image
import ImageFont
import ImageDraw

from logbook.constants import FIELD_TITLES, GRAPH_FIELDS

class BaseSig(object):
    
    def __init__(self, user, font="VeraMono", logo=False, size=12):
        import os
        from django.conf import settings
        
        self.user = user
        self.data = {}
        
        assert int(size) <= 40, "Font size is too big"
        
        self.font_size = int(size)
        self.font = "%s.ttf" % font.replace('.', '').replace('/', '')
        
        if logo == 'logo':  ## logo will either be 'logo' or 'nologo'
            self.logo = True
        else:
            self.logo = False
        
        fontdir = os.path.join(settings.PROJECT_ROOT, 'static_internal', "fonts", self.font)
        self.font = ImageFont.truetype(fontdir, self.font_size)
        
        self.line_height = self.font.getsize("TlIKOPgq")[1] + 2

class TotalsSig(BaseSig):
    """ Creates a little image with the user's logbook totals for
        linking in forum signatures and other uses
    """
    
    title_columns = []
    max_title_width = 0
    
    def __init__(self, *args, **kwargs):
        
        columns = kwargs.pop('columns')
        self.columns = columns
        self.title_columns = [FIELD_TITLES[column] for column in columns]
        
        super(TotalsSig, self).__init__(*args, **kwargs)
        
        
    
    def get_data(self):
        """
        Returns a dict with all the user's logbook totals
        """
        
        from logbook.models import Flight
        for column in self.columns:
            self.data[column] = Flight.objects.user(self.user).agg(column, float=True)
        
    
    def output(self):
        
        self.get_data()
        
        # the total width in pixels of the "title" section
        self.t_width = max(self.font.getsize("%s: " % text)[0]
                            for text in self.title_columns)
        
        # the total width in pixels of the numerical section
        self.d_width = max(self.font.getsize(" %.1f " % (num or 0))[0]
                            for num in self.data.values())
        
        width_padding = 0
        
        #scale the top/bottom margins with the font size
        height_padding = self.font_size / 3.0
        self.top_margin = self.font_size / 6.0
        
        # height in pixels of the entire image
        height = len(self.columns) * self.line_height + height_padding
        
        # wifth of the entire image in pixels
        img_width = width_padding + self.t_width + self.d_width
        
        self.im = Image.new("RGBA", (int(img_width), int(height)))
        self.draw = ImageDraw.Draw(self.im)
        
        self.put_all_columns()
        
        if self.logo:
            pass #self.put_logo()
        
        return self.im
    
    def put_all_columns(self):

        i=0
        
        # looping this way ensures all sigs are rendered in the same order
        # also it removes duplicates
        for key in GRAPH_FIELDS:
            if key in self.data.keys():
                disp = FIELD_TITLES[key]
                down_from_top = (i*self.line_height) + self.top_margin
                this_width = self.font.getsize("%s: " % disp)[0]
                title_over = self.t_width - this_width
                
                self.draw.text(
                                (title_over, down_from_top),
                                " %s: " % FIELD_TITLES[key],
                                font=self.font,
                                fill='black'
                )
                
                self.draw.text(
                                (self.t_width, down_from_top),
                                " %.1f" % self.data[key],
                                font=self.font,
                                fill='black'
                )
                               
                i += 1 #move the next line down one line width

class DaysSinceSig(BaseSig):
    def __init__(self, *args, **kwargs):
        
        self.mode = str(kwargs.pop('mode'))
        
        super(DaysSinceSig, self).__init__(*args, **kwargs)
        
    def figure_pre_text(self):
        if self.mode == 'total':
            title = ""
            
        elif self.mode == 'any':
            title = "logbook entry"
            
        else:
            title = FIELD_TITLES[self.mode]
            
        ##########################
            
        if self.mode == 'app':
            title = "Approach"
        
        elif self.mode == 'day_l':
            title = "Day Landing"
            
        elif self.mode == 'night_l':
            title = "Night Landing"
        
        elif self.mode == 'any':
            # do not do whats in the else block
            pass
        
        elif self.mode == 'total':
            ## to prevent a double space between 'last' and 'flight'
            title += "flight"
        
        else:
            title += " flight"
          
        
        self.pre_text = "Time since my last %s" % title

        
    def get_data(self):
        
        from logbook.models import Flight
        from logbook.constants import FIELD_TITLES    
        try:
            last = Flight.objects.user(self.user)\
                                 .filter_by_column(self.mode)\
                                 .latest()
                                 
        except Flight.DoesNotExist:
            last = None
            
        if last:
            self.days_ago = (datetime.date.today() - last.date).days
            self.unit = "days"
            
            if self.days_ago > 365:
                ## switch to years instead of days if it's
                ## been a really long time
                self.days_ago = "%.2f" % (self.days_ago / 365.0)
                self.unit = 'years'
                
            if self.days_ago < 0:
                self.days_ago = 'The future!'
                self.unit = ''
        else:
            self.days_ago = "Never"
            self.unit = ""
            
    
    def output(self):
        self.figure_pre_text()
        self.get_data()
        
        text = "%s: %s %s" % (self.pre_text, self.days_ago, self.unit)
        
        width, height = self.font.getsize(text)
        
        self.im = Image.new("RGBA", (width+10, height+2))
        self.draw = ImageDraw.Draw(self.im)
        
        self.draw.text(
            (5, 0),
            text,
            font=self.font,
            fill='black'
        )
        
        return self.im
    
