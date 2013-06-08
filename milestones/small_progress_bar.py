from PIL import Image, ImageFont, ImageDraw

from django.conf import settings
import os
font_dir = os.path.join(settings.MEDIA_ROOT, 'fonts')

class SmallProgressBar(object):
    
    def __init__(self, value, max_value, width=100, height=10, outline=True,
                         color='green'):
        
        assert max_value != 0, "max value can't be 0"
        
        self.width = width
        self.height = height
        self.value = value
        self.max_value = max_value
        self.color = color
        self.outline = outline
        
        self.percentage = self.value / float(self.max_value)
        
        if self.value > self.max_value:
            self.value = self.max_value
            self.percentage = 1.0
    
    def draw_outline(self, draw):
        """
        Drawl a one pixel border around the progressbar
        """
        
        top_right = (0,0)
        bottom_left = (self.width-1, self.height-1)
        
        draw.rectangle([top_right, bottom_left], outline=self.color) 
    
    def output(self):
        im = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(im)
        
        if self.outline:
            self.draw_outline(draw)
            
        # make the rectangle, according to the scale
        # -2 to account for the outline
        left = (self.width - 2) * self.percentage
        
        if left:
            top_right = (1,1)
            bottom_left = (left, self.height-2)
            draw.rectangle([top_right, bottom_left], fill=self.color )
        
        return im
    
    def as_png(self):
        """Returns the PNG as a django response object"""
        
        from django.http import HttpResponse
        response = HttpResponse(mimetype="image/png")
        self.output().save(response, "png")
        return response
