import Image, ImageFont, ImageDraw
from annoying.decorators import render_to
from logbook.constants import FIELD_TITLES, GRAPH_FIELDS
from share.decorator import no_share

@no_share('other')
@render_to('sigs.html')
def sigs(request, shared, display_user):
    from logbook.constants import all_agg_checkbox
    checkbox_table = all_agg_checkbox()
    return locals()


@no_share('other')
def make_sig(request, shared, display_user, columns):
    
    columns = columns.split('-')
    
    sig = Sig(display_user, columns)
    
    from django.http import HttpResponse
    response = HttpResponse(mimetype="image/png")
    sig.output().save(response, "png")
    return response
    
    
class Sig(object):
    
    title_columns = []
    max_title_width = 0
    font = "VeraMono.ttf"
    font_size = 12
    line_height = 14
    
    def __init__(self, user, columns):
        import os
        from django.conf import settings
        
        self.user = user
        self.columns = columns
        self.data = {}
        
        print Image.VERSION
        
        fontdir = os.path.join(settings.MEDIA_ROOT, "fonts", self.font)
        self.font = ImageFont.truetype(fontdir, self.font_size)
        
        self.title_columns = [FIELD_TITLES[column] for column in columns]
    
    def get_data(self):
        for column in self.columns:
            self.get_column(column)
        
    def get_column(self, column):
        from logbook.models import Flight
        self.data[column] = Flight.objects.user(self.user).agg(column)
    
    def output(self):
        
        self.get_data()
        
        self.t_width = max(self.font.getsize("%s: " % text)[0]
                            for text in self.title_columns)
                            
        self.d_width = max(self.font.getsize(" %s " % num)[0]
                            for num in self.data)
                            
        height = len(self.columns) * self.line_height
        
        width_padding = 10
        
        img_width = width_padding + self.t_width + self.d_width
        
        self.im = Image.new("RGBA", (img_width, height))
        self.draw = ImageDraw.Draw(self.im)
        
        self.put_all_columns()
        return self.im
    
    
    def put_all_columns(self):
        
        i=0
        for key in GRAPH_FIELDS:
            if key in self.data.keys():
                disp = FIELD_TITLES[key]
                down_from_top = (i*self.line_height)+1
                this_width = self.font.getsize("%s: " % disp)[0]
                title_over = self.t_width - this_width
                
                self.draw.text((title_over, down_from_top),
                               " %s: " % FIELD_TITLES[key],
                               font=self.font,
                               fill='black')
                
                self.draw.text((self.t_width, down_from_top),
                               " %s" % self.data[key],
                               font=self.font,
                               fill='black')
                               
                i += 1 #move the next line down one line width






