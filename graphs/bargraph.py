from django.db.models import Sum
from django.conf import settings

class BarGraph(object):
    
    bar_color = 'y'
    font= "VeraSe.ttf"
    
    def __init__(self, user, time):
        self.user = user
        self.time = time
        
        import ImageFont
        #FIXME:make cross platform compatable
        font = settings.MEDIA_ROOT + "/fonts/" + self.font
        self.font = ImageFont.truetype(font, 12)
        
        from logbook.models import Flight
        self.qs = Flight.objects.filter(user=user)
        
    def annotate_bars(self, rects):
        """attach the text labels"""
        for rect in rects:
            width = rect.get_width() # the actual value as a float
            disp_value = '%.1f' % width #what gets displayed
            placement = width-(len(disp_value) * 20) #where it gets put (horizontal)
            if placement / self.max < 0.15:
                placement = 0.15 * self.max
            
            
            
            self.ax.text(width + 1.5*(self.max/100),
                         rect.get_y()+rect.get_height()/2., #height
                         disp_value,
                         ha='left',
                         va='center')

    def output(self):
        self.get_data()
        
        self.top_m = 50     # top margin
        self.bottom_m = 30  # bottom margin
        self.side_m = 5     # side margin
        self.bar_pad = 5    # space between each bar
        self.bar_h = 20     # height of each bar
        
        width = 800
        
        self.num_bars = len(self.qs)  #the total number of bars to plot
        
        height = self.top_m +\
                 self.bottom_m +\
                 (self.bar_h * self.num_bars) +\
                 (self.bar_pad * (self.num_bars - 1))
        
        import Image, ImageDraw
        self.im = Image.new("RGBA", (width, height))
        self.draw = ImageDraw.Draw(self.im)
        
        # bar titles need to be rendered first because they determine where to
        # start drawing the bar graphs
        self.draw_bar_titles()
        self.draw_bars()
        
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
    
    def draw_bar_titles(self):
        i=0
        dict_key = self._field_title()
        
        max_width = self.find_max_bar_label_width(dict_key)
        
        #####
        
        for item in self.qs:
            text = item[dict_key]
            text_width = self.font.getsize(text)[0]
            
            draw_y = self.top_m + i * (self.bar_h + self.bar_pad)
            draw_x = self.side_m + max_width - text_width
            
            self.draw.text(
                (draw_x, draw_y),
                "%s" % text,
                font=self.font,
                fill='black',
            )
            
            i += 1
        
    def find_max_bar_label_width(self, dk):
        text_widths = []
        for item in self.qs:
            text = item[dk]
            text_widths.append(self.font.getsize(text))
            
        return max(text_widths)[0]

###############################################################################

class PersonBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Person"
    
    def _field_title(self):
        return "person"
    
class FOBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_r(False).dual_g(False).pic().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By First Officer"
    
    def _field_title(self):
        return "person"
    
class CaptainBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_r(False).sic().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Captain"
    
    def _field_title(self):
        return "person"

   
class StudentBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_g().person().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Student"

    def _field_title(self):
        return "person"
        
class InstructorBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_r().person().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Instructor"

    def _field_title(self):
        return "person"
        
class CatClassBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.values('plane__cat_class')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'plane__cat_class')
    
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
        qs = self.qs.values('plane__tailnumber')\
                    .distinct()\
                    .order_by('val')\
                    .annotate(val=Sum(self.time))        

        return self.split(qs, 'plane__tailnumber')
    
    def title(self):
        return "By Tailnumber"
    
    def _field_title(self):
        return "plane__tailnumber"
