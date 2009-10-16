from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

from forms import ImportForm
from share.decorator import no_share

@login_required()
@render_to('import.html')
@no_share
def import_v(request, shared, display_user):

    if request.method == 'POST':
        
        from import_class import PreviewImport, DatabaseImport
        
        fileform = ImportForm(request.POST, request.FILES)
        
        if fileform.is_valid():
            f = request.FILES['file']
        
        if request.POST['submit'] == 'Import':
            im = DatabaseImport(display_user, f)

        elif request.POST['submit'] == 'Preview':
            im = PreviewImport(display_user, f)
            
        im.action()
        flight_out = im.flight_out
        non_out = im.non_out
        records_out = im.records_out
        plane_out = im.plane_out
        
    else:
        fileform = ImportForm()

    return locals()
