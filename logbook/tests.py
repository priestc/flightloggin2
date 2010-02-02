from django.test import TestCase

from django.conf import settings

from models import Flight
from plane.models import Plane
from route.models import Route
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    
    fixtures = ['airport/test-fixtures/test-location.json']
    
    def test_logbook_columns(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        import datetime
        today = datetime.date.today()
        
        # multi engine land p2p > 50nm
        #########################################################
        
        p = Plane(tailnumber="N1234", cat_class=2, type='BE-55')
        p.save()
        
        r = Route.from_string('SNTR SSBT')
        
        f = Flight(plane=p, total=11.0, pic=10.0, date=today, route=r)
        f.save()
        
        self.failUnlessEqual(f.column('single'), "")
        self.failUnlessEqual(f.column('p2p'), "11.0")
        self.failUnlessEqual(f.column('m_pic'), "10.0")
        self.failUnlessEqual(f.column('plane'), "N1234 (BE-55)")
        self.failUnlessEqual(f.column('line_dist'), "959.7")
        self.failUnlessEqual(f.column('atp_xc'), "11.0")
                
        # multi-sea local
        #########################################################
        
        p = Plane(tailnumber="N5678", cat_class=4)
        p.save()
        
        r = Route.from_string('SNTR SNTR')
        
        f = Flight(plane=p, total=11.0, pic=10.0, date=today, route=r)
        f.save()
        
        self.failUnlessEqual(f.column('p2p'), "")
        self.failUnlessEqual(f.column('atp_xc'), "")
        self.failUnlessEqual(f.column('sea_pic'), "10.0")
        self.failUnlessEqual(f.column('tailnumber'), "N5678")
        
        # special remarks and events
        #########################################################
        
        
        
        r = Route.from_string('SNTR SNTR')
        
        f = Flight(plane=p,
                   total=11.0,
                   pic=10.0,
                   date=today,
                   route=r,
                   app=5,
                   holding=True,
                   tracking=True,
                   remarks="remarks derp",
                   ipc=True,
                   cfi_checkride=True)
        f.save()
        
        self.failUnlessEqual(f.column('type'), "TYPE")
        self.failUnlessEqual(f.column('app'), "5 HT")
        self.failUnlessEqual(f.column('sea_pic'), "10.0")
        self.failUnlessEqual(f.column('tailnumber'), "N444444")
        self.failUnlessEqual(f.column('remarks'), "<span class=\"flying_event\">[IPC][Instructor Checkride]</span> remarks derp")
        
    def test_empty_logbook_page(self):
        u = User(username='test')
        u.save()
        
        response = self.client.get('/test/logbook.html')
        self.failUnlessEqual(response.status_code, 200)

class FuelBurn(TestCase): 

    def setUp(self):
        self.p = Plane(tailnumber="N444444", cat_class=4, type="TYPE")
        self.p.save()
        
        self.u = User(username='bob')
        self.u.save()
        
        self.f = Flight(plane=self.p,
                   route=Route.from_string('mer-lga'),
                   user=self.u,
                   date='2009-01-05',
                   total=10.0,
                 )
        self.f.save()
        
    def test_regular_fuel_burn(self):
        
        self.f.fuel_burn = '98gph'
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 980.0)
        self.failUnlessEqual(self.f.gph, 98)
        
        self.f.fuel_burn = '874.5 g'
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 874.5)
        self.failUnlessEqual(self.f.gph, 87.45)
        
    def test_conversion(self):
        """
        Test that teh conversion routines are accurate
        """
        
        self.f.fuel_burn = '10 l'
        self.f.save()
        
        self.failUnlessEqual("%.2f" % self.f.gallons, "%.2f" % 2.64172052)
        
        self.f.fuel_burn = '60 pll'
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 360)
        
        self.f.fuel_burn = '60p'
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 408.0)

    def test_zero_fuel_burn(self):
        """
        Test that the routine can handle fuel burns that are zero
        and where the time is zero
        """
        
        self.f.fuel_burn = '0 gph'
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 0)
        self.failUnlessEqual(self.f.gph, 0)
        
        self.f.fuel_burn = '56 g'
        self.f.total = 0
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 56)
        self.failUnlessEqual(self.f.gph, 0)


        self.f.fuel_burn = '56 gph'
        self.f.total = 0
        self.f.save()
        
        self.failUnlessEqual(self.f.gallons, 0)
        self.failUnlessEqual(self.f.gph, 56)


















