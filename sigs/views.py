import Image, ImageFont, ImageDraw
from annoying.decorators import render_to
from logbook.constants import FIELD_TITLES, GRAPH_FIELDS

@render_to('sigs.html')
def sigs(request, shared, display_user):
    from logbook.constants import all_agg_checkbox
    select = all_agg_checkbox()
    return locals()


def make_sig(request, shared, display_user, columns):
    
    columns = columns.split('-')
    
    sig = Sig(display_user, columns)
    
    from django.http import HttpResponse
    response = HttpResponse(mimetype="image/png")
    sig.output().save(response, "png")
    return response
    
    
class Sig(object):
    
    data = {}
    font_width = 6
    line_height = 16
    title_columns = []
    max_title_width = 0
    
    def __init__(self, user, columns):
        
        self.data = {}
        height = len(columns) * self.line_height
        self.title_columns = [FIELD_TITLES[column] for column in columns]
        self.max_title_width = max(len(text) for text in self.title_columns)
        
        width = (self.max_title_width + 9) * self.font_width + 2
        
        self.user = user
        self.im = Image.new("RGBA", (width, height))
        self.font = ImageFont.load_default()
        self.draw = ImageDraw.Draw(self.im)
        
        for column in columns:
            self.get_column(column)
        
    def get_column(self, column):
        from logbook.models import Flight
        self.data[column] = Flight.objects.user(self.user).agg(column)
    
    def put_all_columns(self):
        i=0
        for key in GRAPH_FIELDS:#self.number.keys()):
            if key in self.data.keys(): # = str(self.number[key])
                self.draw.text((1, (i*self.line_height)+1),
                               ("%*s: %s") % (self.max_title_width+1, " " + FIELD_TITLES[key], self.data[key]),
                               font=self.font,
                               fill='black')
                i += 1 #move the next line down one line width
    
    def output(self):
        self.put_all_columns()
        return self.im
