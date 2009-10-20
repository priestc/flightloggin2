from annoying.decorators import render_to


class Airplane(object):
    total = "&nbsp;"
    dual_r = "&nbsp;"
    solo = "&nbsp;"
    pic = "&nbsp;"
    xc_dual_r = "&nbsp;"
    xc_solo = "&nbsp;"
    xc_pic = "&nbsp;"
    inst = "&nbsp;"
    night_dual_r = "&nbsp;"
    night_l = "&nbsp;"
    night_pic = "&nbsp;"
    night_l_pic = "&nbsp;"
    
    sic = "&nbsp;"
    six_xc = "&nbsp;"
    sic_night = "&nbsp;"
    sic_night_l = "&nbsp;"

@render_to('8710.html')
def auto8710(request, shared, display_user):
    
    airplane = Airplane()
    airplane.total = 200
    
    return locals()
