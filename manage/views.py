from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

from forms import ImportForm
from share.decorator import no_share

from import_class import PreviewImport, DatabaseImport, BaseImport
from handle_uploads import save_php, save_upload, get_last

from backupfromphp import PHPBackup, InvalidToken, InvalidURL

@render_to('export.html')
def export(request):
    return locals()

@render_to('import.html')
@no_share('NEVER')
def import_v(request):

    fileform = ImportForm()
    
    ## get the previous uploaded file
    ## p=file, previous=dict with some metadata
    p, previous = get_last(request.display_user.id)
    
    if not request.method == 'POST':
        return locals()
    
    # whether or not we just display the cotents, or actually commit the
    # changes depending on which submit button was clicked
    preview = request.POST.get('preview_p') or\
              request.POST.get('preview_u') or\
              request.POST.get('preview_f')
    
    if request.POST.get('import_f') or request.POST.get('preview_f'):
        #the file form was used
        f = request.FILES.get('file')
        url = None
        force_tsv = False
        
    elif request.POST.get('import_u') or request.POST.get('preview_u'):
        # the PHP backup thing was used, may throw errors
        url = request.POST.get('url')
        ba = PHPBackup(url)
        f = None
        force_tsv = True
        
    else:
        url = None
        f = None
        force_tsv = False
    
    locs = {}
    try:
        if f:
            save_upload(f, request.display_user)
        elif url:
            f = ba.get_file()
            save_php(f, request.display_user)
        
        #now it's go time   
        locs = do_import(preview, request.display_user, force_tsv)
        
    except BaseImport.InvalidCSVError:
        Error = "Not a valid CSV file"
        
    except BaseImport.NoFileError:
        Error = "Could not find File"
        
    except InvalidToken:
        Error = "Invalid Token"
        
    except InvalidURL:
        Error = "Invalid URL"
    
    else:
        # the import finished and there are no errors
        if not preview:
            from backup.models import edit_logbook
            edit_logbook.send(sender=request.display_user)
         
    locs2 = locals()
    locs2.update(locs)
    return locs2
    
    
def do_import(preview, user, force_tsv):
    """
    An auxiliary view function. Returns variables that will be added to the
    template context, but this function does not take a request object
    """
    
    f, previous = get_last(user.id)
    
    #######################################################

    if not preview:
        im = DatabaseImport(user, f, force_tsv)
        
    else:
        im = PreviewImport(user, f, force_tsv)
    
    # do the actual import routine now    
    im.action()

    from badges.utils import new_badge2
    new_badge2(users=[user])

    flight_out = im.flight_out
    non_out = im.non_out
    records_out = im.records_out
    plane_out = im.plane_out
    
    flight_header = im.flight_header
    non_flight_header = im.non_flight_header
    plane_header = im.plane_header
    
    del im
    
    return locals()
