import Image
import ImageFont
import ImageDraw

from logbook.constants import FIELD_TITLES, GRAPH_FIELDS

class Sig(object):
    """ Creates a little image with the user's logbook totals for
        linking in forum signatures and other uses
    """
    
    title_columns = []
    max_title_width = 0
    
    def __init__(self, user, columns, font="VeraMono", logo=False, size=12):
        import os
        from django.conf import settings
        
        self.user = user
        self.columns = columns
        self.data = {}
        
        assert int(size) <= 40, "Font size is too big"
        
        self.font_size = int(size)
        self.font = "%s.ttf" % font.replace('.', '').replace('/', '')
        
        if logo == 'logo':  ## logo will either be 'logo' or 'nologo'
            self.logo = True
        else:
            self.logo = False
        
        fontdir = os.path.join(settings.MEDIA_ROOT, "fonts", self.font)
        self.font = ImageFont.truetype(fontdir, self.font_size)
        
        self.line_height = self.font.getsize("TlIKOPgq")[1] + 2
        
        self.title_columns = [FIELD_TITLES[column] for column in columns]
    
    def get_data(self):
        """ Returns a dict with all the user's logbook totals
        """
        
        from logbook.models import Flight
        for column in self.columns:
            self.data[column] = Flight.objects.user(self.user).agg(column)
            
        print self.data
        
    
    def output(self):
        
        self.get_data()
        
        # the total width in pixels of the "title" section
        self.t_width = max(self.font.getsize("%s: " % text)[0]
                            for text in self.title_columns)
        
        # the total width in pixels of the numerical section
        self.d_width = max(self.font.getsize(" %.1f " % num)[0]
                            for num in self.data.values())
        
        width_padding = 0
        
        #scale the top/bottom margins with the font size
        height_padding = self.font_size / 3.0
        self.top_margin = self.font_size / 6.0
        
        # height in pixels of the entire image
        height = len(self.columns) * self.line_height + height_padding
        
        # wifth of the entire image in pixels
        img_width = width_padding + self.t_width + self.d_width
        
        self.im = Image.new("RGBA", (img_width, height))
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

