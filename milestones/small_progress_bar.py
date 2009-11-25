from django.conf import settings
import os
font_dir = os.path.join(settings.MEDIA_ROOT, 'fonts')

class SmallProgressBar(object):
    
    def __init__(self, value, max_value, width=100, height=10, outline=True,
                         color='green', font=False):
        
        assert not max_value == 0, "max value can't be 0"
        
        self.width = width
        self.height = height
        self.value = value
        self.max_value = max_value
        self.color = color
        self.font = font
        self.outline = outline
        
        self.percentage = self.value / float(self.max_value + 2)
        
        if self.value > self.max_value:
            self.value = self.max_value
            self.percentage = 1.0
        
    def output(self):
        import Image, ImageFont, ImageDraw

        im = Image.new("RGBA", (self.width, self.height))
        draw = ImageDraw.Draw(im)
        
        if self.outline:
            draw.rectangle([(0,0), (self.width-1, self.height-1)],
                                outline=self.color
            )
            
        # make the rectangle, according to the scale
        # +2 to account for the outline
        left = self.width * self.percentage
        
        draw.rectangle([(0,0), (left, self.height-1)], fill=self.color )
        
        return im
    
    def as_png(self):
        """ Returns the PNG as a django response object"""
        
        from django.http import HttpResponse
        response = HttpResponse(mimetype="image/png")
        self.output().save(response, "png")
        return response
        
