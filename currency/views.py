from annoying.decorators import render_to

from django.db.models import Q

from plane.models import Plane
from logbook.models import Flight
from currency.currbox import MediCurrBox, LandCurrBox, CertCurrBox, InstCurrBox
from FAA import FAA_Landing, FAA_Medical, FAA_Instrument

from share.decorator import no_share

@no_share('other')
@render_to('currency.html')
def currency(request):
    """
    Prepare the currency page
    """
    
    curr_land = FAA_Landing(request.display_user)
    curr_med = FAA_Medical(request.display_user)

    ############################################
    
    cert_currbox = CertCurrBox(cfi=curr_land.flight_instructor(),
                               bfr=curr_land.flight_review())
    
    if not (curr_land.has_bfr_event or curr_land.has_cfi_event):
        del cert_currbox
    
    ############################################ instrument below
    
    inst_out = []
    
    
    if Flight.objects.user(request.display_user)\
                     .pseudo_category("fixed_wing").app().count() > 5:
        curr_inst = FAA_Instrument(request.display_user)
        curr_inst.fake_class = "fixed_wing"
        cb = InstCurrBox(curr_inst, "Fixed Wing")
        inst_out.append(cb)
        cb.render()
        
    if Flight.objects.user(request.display_user)\
                     .pseudo_category("helicopter").app().count() > 5:
        curr_inst = FAA_Instrument(request.display_user)
        curr_inst.fake_class = "helicopter"
        cb = InstCurrBox(curr_inst, "Helicopter")
        inst_out.append(cb)
    
    if Flight.objects.user(request.display_user)\
                     .pseudo_category("glider").app().count() > 5:
        curr_inst = FAA_Instrument(request.display_user)
        curr_inst.fake_class = "glider"
        cb = InstCurrBox(curr_inst, "Glider")
        inst_out.append(cb)
    
    ############################################ landing below
        
    cat_classes = Plane.objects\
                       .user(request.display_user)\
                       .exclude(cat_class=0)\
                       .values_list('cat_class', flat=True)\
                       .order_by().distinct()
    cat_classes_out = []
    for item in cat_classes:
        currbox = LandCurrBox(cat_class=item)
        
        currbox.day = curr_land.landing(night=False, cat_class=item)
        currbox.night = curr_land.landing(night=True, cat_class=item)
        
        cat_classes_out.append(currbox)
    
    ############################################ tailwheel below
    
    tailwheels = Plane.objects.user(request.display_user)\
                              .tailwheel()\
                              .exclude(cat_class=0)\
                              .values_list('cat_class', flat=True)\
                              .order_by().distinct()
    tailwheels_out = []   
    for item in tailwheels:
        currbox = LandCurrBox(cat_class=item, tail=True)
        
        currbox.day = curr_land.landing(night=False, cat_class=item, tail=True)
        currbox.night = curr_land.landing(night=True, cat_class=item, tail=True)
        
        tailwheels_out.append(currbox)
        
    ############################################ type ratings below
    
    type_ratings = Plane.objects.user(request.display_user)\
                                .currency()\
                                .exclude(cat_class=0)\
                                .values_list('type', flat=True)\
                                .order_by().distinct()
    types_out = []
    for item in type_ratings:
        currbox = LandCurrBox(tr=item)
        
        currbox.day = curr_land.landing(night=False, tr=item)
        currbox.night = curr_land.landing(night=True, tr=item)
        
        types_out.append(currbox)
    
    ########################################## medical below
        
    medi_currbox = MediCurrBox()
    medi_currbox.first = curr_med.first_class()
    medi_currbox.second = curr_med.second_class()
    medi_currbox.third = curr_med.third_class()
    medi_currbox.medi_issued = curr_med.medical_class
    
    if not curr_med.medical_class:
        del medi_currbox                #if there are no medicals, then delete this box so it doesn't show up in the template
        
    ############################################

    return locals()

















