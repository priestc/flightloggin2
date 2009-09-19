import Image, ImageFont, ImageDraw

def sigs(request, shared, display_user):
    return make_sig(display_user, 256,256, "ff")


def make_sig(user, width, height, columns):
    im = Image.new("RGBA", (width, height))
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(im)
    
    draw.text((10, 150), "lol hy", font=font, fill='black')
    
    from django.http import HttpResponse
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response
