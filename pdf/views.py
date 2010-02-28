from share.decorator import no_share
from pdf import PDF

@no_share('logbook')
def pdf(request):
    
    pdf = PDF(request.display_user)
    
    return pdf.as_response()
