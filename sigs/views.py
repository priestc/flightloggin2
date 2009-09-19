import Image, ImageFont, ImageDraw
from annoying.decorators import render_to
from logbook.constants import FIELD_TITLES

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
    
    number = {}
    font_width = 6
    
    def __init__(self, user, columns):
        
        
        height = len(columns) * 15
        self.title_columns = [FIELD_TITLES[column] for column in columns]
        self.max_title_width = max(len(text) for text in self.title_columns)
        
        width = (self.max_title_width + 8) * self.font_width
        
        self.user = user
        self.im = Image.new("RGBA", (width, height))
        self.font = ImageFont.load_default()
        self.draw = ImageDraw.Draw(self.im)
        
        for column in columns:
            self.get_column(column)
        
    def get_column(self, column):
        from logbook.models import Flight
        self.number[column] = Flight.objects.user(self.user).agg(column)
    
    def put_all_columns(self):
        for i,key in enumerate(self.number.keys()):
            number = str(self.number[key])
            self.draw.text((0, i*15), ("%*s: %s") % (self.max_title_width, FIELD_TITLES[key], number), font=self.font, fill='black')
    
    def output(self):
        self.put_all_columns()
        return self.im
