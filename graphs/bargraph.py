from django.db.models import Sum
from django.conf import settings

class BarGraph(object):
    
    bar_color = 'y'
    regular_font = ("VeraSe.ttf", 12)
    title_font =   ("VeraSeBd.ttf", 22)
    
    def __init__(self, user, time):
        self.user = user
        self.time = time
        
        import ImageFont
        #FIXME:make cross platform compatable
        font = settings.MEDIA_ROOT + "/fonts/" + self.regular_font[0]
        self.font = ImageFont.truetype(font, self.regular_font[1])
        
        titlefont = settings.MEDIA_ROOT + "/fonts/" + self.title_font[0]
        self.titlefont = ImageFont.truetype(font, self.title_font[1])
        
        from logbook.models import Flight
        self.qs = Flight.objects.filter(user=user)

    def output(self):
        self.get_data()
        
        self.top_m = 50           # top margin
        self.bottom_m = 30        # bottom margin
        self.side_m = 5           # side margin
        self.bar_pad = 5          # space between each bar
        self.bar_h = 13           # height of each bar
        self.annotate_padding = 5 # the padding between the bar and the annotation
        
        self.width = 800
        
        self.num_bars = len(self.qs)  #the total number of bars to plot
        
        height = self.top_m +\
                 self.bottom_m +\
                 (self.bar_h * self.num_bars) +\
                 (self.bar_pad * (self.num_bars - 1))
        
        import Image, ImageDraw
        self.im = Image.new("RGBA", (self.width, height))
        self.draw = ImageDraw.Draw(self.im)
        
        self.draw_bars()
        self.draw_main_title()
        
        
        return self.im
    
    def as_png(self):
        from django.http import HttpResponse
        response = HttpResponse(mimetype="image/png")
        self.output().save(response, "png")
        return response
    
    def get_column_title(self):
        from logbook.constants import FIELD_TITLES
        return FIELD_TITLES[self.time]
    
    def make_ytick(self, val):
        """Makes the values for the vertical ticks, some will subclass over
           this
        """
        return val
    
    def draw_bars(self):
        i=0
        dict_key = self._field_title()
        title_max_width, val_max_width = self.find_max_label_widths(dict_key)
        bar_start = title_max_width + 10
        
        total_draw_space = self.width - (val_max_width +
                                         title_max_width +
                                         self.side_m*2 +
                                         self.annotate_padding*2 +
                                         10)
        
        #####
        
        for item in self.qs.order_by('-val'):
            text = item[dict_key]
            text_width = self.font.getsize(text)[0]
            
            draw_y = self.top_m + i * (self.bar_h + self.bar_pad)
            draw_x = self.side_m + title_max_width - text_width
            
            #### draw the title for each bar
            self.draw.text(
                (draw_x, draw_y),
                "%s" % text,
                font=self.font,
                fill='black',
            )
            
            #### draw the bar
            yend = self.bar_h + draw_y
            length = (item['val'] / self.max) * total_draw_space
            self.draw.rectangle(
                [(bar_start, draw_y),
                 (length + bar_start, yend)],
                fill=(58,241,135),
                outline='black',
            )
            
            #### draw the total for each bar
            self.draw.text(
                (bar_start + length + self.annotate_padding, draw_y),
                "%s" % item['val'],
                font=self.font,
                fill='black',
                
            )
            
            i += 1
    
    def draw_main_title(self):
        from logbook.constants import FIELD_TITLES
        time_title = FIELD_TITLES[self.time]
        agg_title = self.title()
        
        title = "%s %s" % (time_title, agg_title)
        
        width = self.titlefont.getsize(title)[0]
        
        draw_x = self.width/2 - width/2
        
        self.draw.text(
                (draw_x,5),
                title,
                font=self.titlefont,
                fill='black',
        )
        
    def find_max_label_widths(self, dk):
        text_widths = []
        val_widths = []
        vals = []
        for item in self.qs:
            text = item[dk]
            val = item['val']
            text_widths.append(self.font.getsize(text))
            val_widths.append(self.font.getsize("%.1d" % val))
            vals.append(item['val'])
        
        self.max = max(vals)
           
        return max(text_widths)[0], max(val_widths)[0]

###############################################################################

class PersonBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By Person"
    
    def _field_title(self):
        return "person"
    
class FOBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.dual_r(False).dual_g(False).pic().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By First Officer"
    
    def _field_title(self):
        return "person"
    
class CaptainBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.dual_r(False).sic().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By Captain"
    
    def _field_title(self):
        return "person"

   
class StudentBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.dual_g().person().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By Student"

    def _field_title(self):
        return "person"
        
class InstructorBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.dual_r().person().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By Instructor"

    def _field_title(self):
        return "person"
        
class CatClassBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.values('plane__cat_class')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
    
    def make_ytick(self, val):
        from plane.constants import CATEGORY_CLASSES
        return CATEGORY_CLASSES[val][1]
    
    def title(self):
        return "By Category/Class"

    def _field_title(self):
        return "plane__cat_class"

class PlaneTypeBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.values('plane__type')\
                    .distinct()\
                    .order_by('val')\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By Plane Type"

    def _field_title(self):
        return "plane__type"
        
class TailnumberBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = self.qs.values('plane__tailnumber')\
                    .distinct()\
                    .order_by('val')\
                    .annotate(val=Sum(self.time))
    
    def title(self):
        return "By Tailnumber"
    
    def _field_title(self):
        return "plane__tailnumber"
