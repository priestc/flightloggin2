from annoying.decorators import render_to
from logbook.constants import FIELD_TITLES, GRAPH_FIELDS
from share.decorator import no_share

from main.table import html_table

def all_agg_checkbox(prefix=""):
    out = []
    for field in GRAPH_FIELDS:
        if field == 'total' or field == 'pic':
            sel='checked="checked"'
        else:
            sel = ""
        
        out.append(
        """<input %(sel)s type="checkbox" id="c_%(field)s">
           <label for="c_%(field)s">%(display)s</label>""" %
                {'sel': sel, 'field': field, 'display': FIELD_TITLES[field]}
        )
    
    return html_table(out, 5, "checktable")

def all_agg_radiobox(any_=False, prefix="", name='radio'):
    out = []
    
    #grab from global scope so we can add to it
    fields = list(GRAPH_FIELDS)
    
    if any_:
        fields += ['any']
    
    for field in fields:
        if field == 'any':
            sel='checked="checked"'
        else:
            sel = ""
            
        out.append(
        """<input %(sel)s type="radio" id="r_%(field)s" name="%(name)s">
           <label for="r_%(field)s">%(display)s</label>""" %
                {'name': name,
                 'sel': sel,
                 'field': field,
                 'display': FIELD_TITLES[field]}
        )
    
    return html_table(out, 5, "radiotable")

@no_share('other')
@render_to('sigs.html')
def sigs(request):
    checkbox_table = all_agg_checkbox()
    radiobox_table = all_agg_radiobox(any_=True, name='lastx')
    return locals()


@no_share('other')
def make_totals_sig(request, columns, logo, font, size=12):
    from classes import TotalsSig
    columns = columns.split('-')
    
    sig = TotalsSig(request.display_user,
                    columns=columns,
                    font=font,
                    logo=logo,
                    size=size)
    
    from django.http import HttpResponse
    response = HttpResponse(mimetype="image/png")
    sig.output().save(response, "png")
    return response

@no_share('other')
def make_days_since_sig(request, mode, font, size=12):
    from classes import DaysSinceSig
    
    sig = DaysSinceSig(request.display_user,
                       mode=mode,
                       font=font,
                       size=size)
    
    from django.http import HttpResponse
    response = HttpResponse(mimetype="image/png")
    sig.output().save(response, "png")
    return response
