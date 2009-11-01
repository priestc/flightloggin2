from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

from forms import ImportForm
from share.decorator import no_share

@login_required()
@render_to('import.html')
@no_share
def import_v(request, shared, display_user):

    if not request.method == 'POST':
        fileform = ImportForm()
        p, previous = get_last(display_user)
        return locals()
        
    from import_class import PreviewImport, DatabaseImport, BaseImport
    from handle_uploads import save_php, save_upload
    
    if request.POST.get('import_f') or request.POST.get('preview_f'):
        f = request.FILES['file']
        save_upload(f, display_user)
        if not f:
            NoFile=True
            return locals()
        
    if request.POST.get('import_u') or request.POST.get('preview_u'):
        from backupfromphp import PHPBackup
        f = PHPBackup(request.POST['url']).get_file()
        save_php(f, display_user)
        
    if request.POST.get('import_p') or request.POST.get('preview_p'):   
        pass
    
    
    f, previous = get_last(display_user)
        
    #######################################################
    
    if not f:
        NoFile = True
        return locals()
    
    #######################################################
        
    preview = request.POST.get('preview_p') or\
              request.POST.get('preview_u') or\
              request.POST.get('preview_f')
    
    import_ = request.POST.get('import_p') or\
              request.POST.get('import_u') or\
              request.POST.get('import_f')

    if import_:
        im = DatabaseImport(display_user, f)
        
    else:
        im = PreviewImport(display_user, f)
        
    try:
        im.action()

    except BaseImport.InvalidCSVError:
        InvalidError = True
        return locals()

    flight_out = im.flight_out
    non_out = im.non_out
    records_out = im.records_out
    plane_out = im.plane_out
    
    flight_header = im.flight_header
    non_flight_header = im.non_flight_header
    plane_header = im.plane_header
    
    del im
        
    fileform = ImportForm()
    return locals()


@render_to('export.html')
def export(request, shared, display_user):
    return locals()


def get_last(user):
    from handle_uploads import find_already_uploaded_file
    p, mod, size = find_already_uploaded_file(user.id)
    
    if p:
        previous = {}
        previous['age'] = "Uploaded %s Ago" % mod
        previous['size'] = "%s KB<br>" % size
    else:
        previous = {}
        previous['age'] = "<i>You have not uploaded anything yet</i>"
        previous['size'] = ""
        
    return p, previous


