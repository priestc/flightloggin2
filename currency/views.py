from annoying.decorators import render_to

from django.db.models import Q

from plane.models import Plane
from logbook.models import Flight
from currency.currbox import MediCurrBox, LandCurrBox, CertCurrBox, InstCurrBox
from FAA import FAA_Currency

@render_to('currency.html')
def currency(request, shared, display_user):
    currency = FAA_Currency(display_user)

    ############################################
    
    cert_currbox = CertCurrBox(cfi=currency.flight_instructor(), bfr=currency.flight_review())
    
    if not (currency.pilot or currency.cfi):
        del cert_currbox
    
    ############################################
    
    inst_out = []
    
    if Flight.objects.pseudo_category("fixed_wing").app().count() > 0:
        cb = InstCurrBox(cat="Fixed Wing", currency=currency.instrument("fixed_wing"))
        inst_out.append(cb)
        cb.render()
        
    if Flight.objects.pseudo_category("helicopter").app().count() > 0:
        cb = InstCurrBox(cat="Helicopter", currency=currency.instrument("helicopter"))
        inst_out.append(cb)
    
    if Flight.objects.pseudo_category("glider").app().count() > 0:
        cb = InstCurrBox(cat="Glider", currency=currency.instrument("glider"))
        inst_out.append(cb)
    
    ############################################
        
    cat_classes = Plane.objects.filter(user=display_user)\
                       .values_list('cat_class', flat=True)\
                       .order_by().distinct()
    cat_classes_out = []
    for item in cat_classes:
        currbox = LandCurrBox(cat_class=item)
        
        currbox.day = currency.landing(night=False, cat_class=item)
        currbox.night = currency.landing(night=True, cat_class=item)
        
        cat_classes_out.append(currbox)
    
    ############################################
    
    tailwheels = Plane.objects.filter(user=display_user)\
                              .filter( Q(tags__icontains="tailwheel"))\
                              .values_list('cat_class', flat=True)\
                              .order_by().distinct()
    tailwheels_out = []   
    for item in tailwheels:
        currbox = LandCurrBox(cat_class=item, tail=True)
        
        currbox.day = currency.landing(night=False, cat_class=item, tail=True)
        currbox.night = currency.landing(night=True, cat_class=item, tail=True)
        
        tailwheels_out.append(currbox)
        
    ############################################
    
    type_ratings = Plane.objects.filter(user=display_user)\
                                .filter( Q(tags__icontains="type rating") |
                                         Q(tags__icontains="currency"))\
                                .values_list('type', flat=True)\
                                .order_by().distinct()
    types_out = []
    for item in type_ratings:
        currbox = CurrBox(tr=item, method="landings")
        
        currbox.day = currency.landing(night=False, tr=item)
        currbox.night = currency.landing(night=True, tr=item)
        
        types_out.append(currbox)
    
    ##########################################
        
    medi_currbox = MediCurrBox()
    medi_currbox.first = currency.first_class()
    medi_currbox.second = currency.second_class()
    medi_currbox.third = currency.third_class()
    medi_currbox.medi_issued = currency.medical_class
    
    if not currency.medical_class:
        del medi_currbox                #if there are no medicals, then delete this box so it doesn't show up in the template
        
    ############################################

    return locals()

















