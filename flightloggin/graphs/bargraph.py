from django.conf import settings

class BarGraph(object):
    
    color_profile = 1
    regular_font = ("VeraSe.ttf", 12)
    title_font =   ("VeraSeBd.ttf", 22)
    
    top_m = 50              # top margin
    bottom_m = 30           # bottom margin
    side_m = 5              # side margin
    bar_pad = 5             # space between each bar
    bar_h = 13              # height of each bar
    annotate_padding = 5    # the padding between the bar and the annotation
    width = 800
    
    class EmptyLogbook(Exception):
        pass
    
    def agg(self, *args, **kwargs):
        from django.db.models import Avg, Sum, Min, Max, StdDev
        return locals()[self.agg_type]( *args, **kwargs)
        
    def __init__(self, user, time, agg, func="Sum"):
        self.user = user
        self.time = time
        self.agg_type = func
        
        import ImageFont
        import os
        root = settings.MEDIA_ROOT
        
        font = os.path.join(root, "fonts", self.regular_font[0])
        self.font = ImageFont.truetype(font, self.regular_font[1])
        
        titlefont = os.path.join(root, "fonts", self.title_font[0])
        self.titlefont = ImageFont.truetype(font, self.title_font[1])
        
        from logbook.models import Flight
        self.qs = Flight.objects.filter(user=user)
        
        if self.time == 'day':
            self.qs = self.qs.add_column('day')
            
    def get_color(self):
        if self.color_profile == 1:
            self.color = (58,241,135)
        elif self.color_profile == 2:
            self.color = "#46B9ED"
        elif self.color_profile == 3:
            self.color = "#DA7E16" 
            
    def output(self):
        
        self.get_color()
        self.get_data()

        if not self.qs.extra(select={'a': 1}).values('a').order_by():
            return self.empty()
        
        self.num_bars = len(self.qs)  #the total number of bars to plot
        
        height = (
                    self.top_m +
                    self.bottom_m +
                    (self.bar_h * self.num_bars) +
                    (self.bar_pad * (self.num_bars - 1))
                )
        
        import Image, ImageDraw
        self.im = Image.new("RGBA", (self.width, height))
        self.draw = ImageDraw.Draw(self.im)
        
        try:
            self.draw_bars()
        except self.EmptyLogbook:
            return self.empty()
       
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
        if val == '':
            val='UNKNOWN'
            
        return val
    
    def format_annotation(self, value):
        """ Format the way the annotation on each bar is formatted
        """
        
        if self.time in ('app', 'day_l', 'night_l'):
            return "%s" % value
        
        else:
            return "%.1f" % value
    
    def draw_bars(self):
        i=0
        dict_key = self._field_title()
        self.t_max_width, v_max_width = self.find_max_label_widths(dict_key)
        bar_start = self.t_max_width + 10
        
        self.total_draw_space = self.width - (v_max_width +
                                              self.t_max_width +
                                              self.side_m*2 +
                                              self.annotate_padding*2 +
                                              10)
        
        #####
        
        for item in self.qs:
            text = item[dict_key]
            text = self.make_ytick(text)
            text_width = self.font.getsize(text)[0]
            
            draw_y = self.top_m + i * (self.bar_h + self.bar_pad)
            draw_x = self.side_m + self.t_max_width - text_width
            val = self.format_annotation(item['val'])
            
            #### draw the title for each bar
            self.draw.text(
                (draw_x, draw_y),
                "%s" % text,
                font=self.font,
                fill='black',
            )
            
            #### draw the bar
            yend = self.bar_h + draw_y
            length = (item['val'] / float(self.max)) * self.total_draw_space
            self.draw.rectangle(
                [(bar_start, draw_y),
                 (length + bar_start, yend)],
                fill=self.color,
                outline='black',
            )
            
            #### annotate each bar with the total
            self.draw.text(
                (bar_start + length + self.annotate_padding, draw_y),
                val,
                font=self.font,
                fill='black',
            )
            
            i += 1
    
    def draw_main_title(self):
        from logbook.constants import FIELD_TITLES
        time_title = FIELD_TITLES[self.time]
        agg_title = self.title()
        
        title = "%s %s %s" % (self.agg_type, time_title, agg_title)
        
        width = self.titlefont.getsize(title)[0]
        
        draw_x = self.total_draw_space/2.0 - width/2.0 + self.t_max_width
        
        self.draw.text(
                (draw_x,7),
                title,
                font=self.titlefont,
                fill='black',
        )
        
    def find_max_label_widths(self, dk):
        text_widths = []
        val_widths = []
        vals = []
        for item in self.qs:
            # run the y tick through this function so fields like cat_class
            # show "Single Engine" instead of "1"
            text = self.make_ytick(item[dk])
            val = self.format_annotation(item['val'])
            text_widths.append(self.font.getsize(text))
            val_widths.append(self.font.getsize(val))
            vals.append(item['val'])
        
        self.max = max(vals)
        if self.max == 0:
            raise self.EmptyLogbook
           
        return max(text_widths)[0], max(val_widths)[0]
    
    def empty(self):
        """ Returns a empty image for when there's nothing to show
        """
        
        import Image, ImageDraw
        self.im = Image.new("RGBA", (500, 200))
        self.draw = ImageDraw.Draw(self.im)
        
        self.draw.text((120,90),
                       'Nothing to show here',
                       font=self.titlefont,
                       fill='black')
        
        return self.im
        
###############################################################################

class PersonBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .values('person')
                    .exclude(person='')
                    .order_by('-val')
                    .distinct()
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By Person"
    
    def _field_title(self):
        return "person"
    
class FOBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .dual_r(False)
                    .dual_g(False)
                    .pic()
                    .values('person')
                    .exclude(person='')
                    .order_by('-val')
                    .distinct()
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By First Officer"
    
    def _field_title(self):
        return "person"
    
class CaptainBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .dual_r(False)
                    .sic()
                    .values('person')
                    .exclude(person='')
                    .order_by('-val')
                    .distinct()
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By Captain"
    
    def _field_title(self):
        return "person"

   
class StudentBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .dual_g()
                    .values('person')
                    .exclude(person='')
                    .order_by('-val')
                    .distinct()
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By Student"

    def _field_title(self):
        return "person"
        
class InstructorBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .dual_r().values('person')
                    .exclude(person='')
                    .order_by('-val')
                    .distinct()
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By Instructor"

    def _field_title(self):
        return "person"
        
class CatClassBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .values('plane__cat_class')
                    .order_by('-val')
                    .distinct()
                    .annotate(val=self.agg(self.time)))
    
    def make_ytick(self, val):
        from plane.constants import CATEGORY_CLASSES
        return CATEGORY_CLASSES[val][1]
    
    def title(self):
        return "By Category/Class"

    def _field_title(self):
        return "plane__cat_class"

class PlaneTypeBarGraph(BarGraph):
    
    def get_data(self):
        
        time = self.time
        
        self.qs = (self.qs.filter_by_column(self.time)
                    .values('plane__type')
                    .distinct()
                    .order_by('-val')
                    .select_related()
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By Plane Type"

    def _field_title(self):
        return "plane__type"
        
class TailnumberBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .values('plane__tailnumber')
                    .distinct()
                    .order_by('-val')
                    .annotate(val=self.agg(self.time)))
    
    def title(self):
        return "By Tailnumber"
    
    def _field_title(self):
        return "plane__tailnumber"

class ManufacturerBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .values('plane__manufacturer')
                    .distinct()
                    .annotate(val=self.agg(self.time))
                    .order_by('-val'))
    
    def title(self):
        return "By Manufacturer"
    
    def _field_title(self):
        return "plane__manufacturer"
    
class ModelBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.filter_by_column(self.time)
                    .values('plane__model')
                    .distinct()
                    .annotate(val=self.agg(self.time))
                    .order_by('-val'))
    
    def title(self):
        return "By Model"
    
    def _field_title(self):
        return "plane__model"
    
class YearBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.extra(select={'year':'EXTRACT (YEAR FROM date)' })
                         .filter_by_column(self.time)
                         .values('year')
                         .distinct()
                         .order_by()
                         .annotate(val=self.agg(self.time))
                         .order_by('-val'))
    
    def make_ytick(self, val):
        #convert to int to get rid of ".0", then to string for printing
        return "%s" % int(val)
    
    def title(self):
        return "By Year"
    
    def _field_title(self):
        return "year"
    
class MonthBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.extra(select={'month':'EXTRACT (MONTH FROM date)' })
                         .filter_by_column(self.time)
                         .values('month')
                         .distinct()
                         .order_by()
                         .annotate(val=self.agg(self.time))
                         .order_by('-val'))
    
    def make_ytick(self, val):
        #convert number to month name
        MONTHS = ('dummy', 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December')
        return MONTHS[int(val)]
    
    def title(self):
        return "By Month"
    
    def _field_title(self):
        return "month"
    
class DOWBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.extra(select={'dow':'EXTRACT (DOW FROM date)' })
                         .filter_by_column(self.time)
                         .values('dow')
                         .distinct()
                         .order_by()
                         .annotate(val=self.agg(self.time))
                         .order_by('-val'))
    
    def make_ytick(self, val):
        #convert number to month name
        DOW = ('Sunday', 'Monday', 'Tuesday', 'Wendsday', 'Thursday',
                  'Friday', 'Saturday')
        return DOW[int(val)]
    
    def title(self):
        return "By Day of the Week"
    
    def _field_title(self):
        return "dow"
    
class MonthYearBarGraph(BarGraph):
    
    def get_data(self):
        self.qs = (self.qs.extra(select={'my':"to_char(date, 'FMMonth YYYY')"})
                         .filter_by_column(self.time)
                         .values('my')
                         .distinct()
                         .order_by()
                         .annotate(val=self.agg(self.time))
                         .order_by('-val'))
    
    def title(self):
        return "By Month/Year"
    
    def _field_title(self):
        return "my"
