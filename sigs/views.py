import Image, ImageFont, ImageDraw
from annoying.decorators import render_to
from logbook.constants import FIELD_TITLES, GRAPH_FIELDS
from share.decorator import no_share

from main.table import html_table

def all_agg_checkbox(prefix=""):
    out = []
    for field in GRAPH_FIELDS:
        if field == 'total' or field == 'pic':
            sel='checked="checked"'
        else:
            sel = ""
        
        out.append(
        """<input %(sel)s type="checkbox" id="%(field)s">
           <label for="%(field)s">%(display)s</label>""" %
                {'sel': sel, 'field': field, 'display': FIELD_TITLES[field]}
        )
    
    return html_table(out, 5, "checktable")

@no_share('other')
@render_to('sigs.html')
def sigs(request, shared, display_user):
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
    #font = "Verdana.ttf"
    font = "VeraMono.ttf"
    font_size = 12
    line_height = 14
    
    def __init__(self, user, columns):
        import os
        from django.conf import settings
        
        self.user = user
        self.columns = columns
        self.data = {}
        
        fontdir = os.path.join(settings.MEDIA_ROOT, "fonts", self.font)
        self.font = ImageFont.truetype(fontdir, self.font_size)
        
        self.title_columns = [FIELD_TITLES[column] for column in columns]
    
    def get_data(self):
        from logbook.models import Flight
        for column in self.columns:
            self.data[column] = Flight.objects.user(self.user).agg(column)
            
        print self.data
        
    
    def output(self):
        
        self.get_data()
        
        self.t_width = max(self.font.getsize("%s: " % text)[0]
                            for text in self.title_columns)
                            
        self.d_width = max(self.font.getsize(" %.1f " % num)[0]
                            for num in self.data.values())
        
        width_padding = 0
        height_padding = 3
        
        height = len(self.columns) * self.line_height + height_padding
        
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
                               " %.1f" % self.data[key],
                               font=self.font,
                               fill='black')
                               
                i += 1 #move the next line down one line width






