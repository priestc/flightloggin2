def old_browser(request):
    ua = request.META.get('HTTP_USER_AGENT', "ff")
    
    if ("MSIE 7.0" in ua) or ("MSIE 6.0" in ua):
        old_browser = True
    else:
        old_browser = False
        
    return {'old_browser': old_browser}
