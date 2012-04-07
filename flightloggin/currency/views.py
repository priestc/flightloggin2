from annoying.decorators import render_to
from flightloggin.share.decorator import no_share

from flightloggin.plane.models import Plane
from flightloggin.plane.constants import CURRENCIES
from logbook.models import Flight
from currbox import MediCurrBox, LandCurrBox, CertsCurrBox, InstCurrBox
from FAA import FAA_Landing, FAA_Medical, FAA_Instrument, FAA_Certs

@no_share('other')
@render_to('currency.html')
def currency(request):
    """
    Prepare the currency page
    """
    
    ############################################ instrument below
    
    inst_out = []                   
    for fake_class in ("fixed_wing", "helicopter", "glider"):
        inst = FAA_Instrument(request.display_user, fake_class=fake_class)
        if inst.eligible():
            inst.calculate()
            cb = InstCurrBox(inst)
            inst_out.append(cb)
    
    land_out = []    
    for curr in CURRENCIES:
        land = FAA_Landing(request.display_user, item=curr)
        if land.eligible():
            land.calculate()
            cb = LandCurrBox(land)
            land_out.append(cb)
    
    types = Plane.currency_types(request.display_user)
    type_out = []       
    for curr in types:
        land = FAA_Landing(request.display_user, item=curr)
        if land.eligible():
            land.calculate()
            cb = LandCurrBox(land)
            type_out.append(cb)
            
    medi = FAA_Medical(request.display_user)
    medi_out = []
    if medi.eligible():
        medi.calculate()
        cb = MediCurrBox(medi)
        medi_out.append(cb)
        
    cert = FAA_Certs(request.display_user)
    cert_out = []
    if cert.eligible():
        cert.calculate()
        cb = CertsCurrBox(cert)
        cert_out.append(cb)

    return locals()

















