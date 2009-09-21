import settings

def css_path(request):
    try:
        style = request.user.get_profile().style
    except:
        style = 1
        
    CSS_URL = settings.MEDIA_URL + "/css/style" + str(style)
        
        
    return {"CSS_URL": CSS_URL}
