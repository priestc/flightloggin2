from django.db.models import Sum


class BarGraph(object):
    
    bar_color = 'y'
    
    def __init__(self, user, time):
        self.user = user
        self.time = time
        
        from logbook.models import Flight
        self.qs = Flight.objects.filter(user=user)
        
        self.fig = plt.figure(figsize=(10,10), dpi=1)
        self.ax = self.fig.add_subplot(111, frameon=True)
        
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
        titles, vals = self.get_data()
        
        top_m = 15     # top margin
        bottom_m = 15  # bottom margin
        side_m = 5     # side margin
        bar_pad = 3    # space between each bar
        bar_h = 7      # height of each bar
        
        width = 700
        
        num_bars = len(title)  #the total number of bars to plot
        
        height = top_m + bottom_m + (bar_h + bar_pad) * num_bars
        
        import Image
        
        self.im = Image.new("RGBA", (width, height))
        
        
        return self.im
    
    def split(self, qs, title):
        vals=[]
        vert=[]
        for item in qs:
            vert.append(item[title])            
            vals.append(item['val'])
        
        self.max = max(vals)    #find the maximum value for later
        self.len = len(vals)
            
        return vert, vals
    
    def get_column_title(self):
        from logbook.constants import FIELD_TITLES
        return FIELD_TITLES[self.time]
    
    def make_ytick(self, val):
        """Makes the values for the vertical ticks, some will subclass over
           this
        """
        return val

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
    
class FOBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_r(False).dual_g(False).pic().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By First Officer"
    
class CaptainBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_r(False).sic().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Captain"

   
class StudentBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_g().person().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Student"
    
class InstructorBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.dual_r().person().values('person')\
                    .order_by('val')\
                    .distinct()\
                    .annotate(val=Sum(self.time))
                    
        return self.split(qs, 'person')
    
    def title(self):
        return "By Instructor"
    
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
        
class PlaneTypeBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.values('plane__type')\
                    .distinct()\
                    .order_by('val')\
                    .annotate(val=Sum(self.time))        

        return self.split(qs, 'plane__type')
    
    def title(self):
        return "By Plane Type"    
        
class TailnumberBarGraph(BarGraph):
    
    def get_data(self):
        qs = self.qs.values('plane__tailnumber')\
                    .distinct()\
                    .order_by('val')\
                    .annotate(val=Sum(self.time))        

        return self.split(qs, 'plane__tailnumber')
    
    def title(self):
        return "By Tailnumber"    
