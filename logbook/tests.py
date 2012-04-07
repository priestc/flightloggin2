from django.test import TestCase

from django.conf import settings

from models import Flight
from plane.models import Plane
from route.models import Route
from django.contrib.auth.models import User

class ColumnsTest(TestCase):
    
    fixtures = ['airport/test-fixtures/ohio.json',
                'airport/test-fixtures/test-region.json',
                'airport/test-fixtures/test-country.json']
    
    def setUp(self):
        import datetime
        today = datetime.date.today()
        
        self.u = User(username='test')
        self.u.save()
        
        self.baron = Plane(tailnumber="N1234", type='BE-55')
        self.baron.save()
        
        self.seaplane = Plane(tailnumber="N5678", cat_class=3)
        self.seaplane.save()
        
        self.local_route = Route.from_string('kvta kvta')
        
        self.more50nm_route = Route.from_string('kvta kluk')
        self.no_land_more50nm_route = Route.from_string('kvta @kluk kvta')
        
        self.less50nm_route = Route.from_string('kvta kcmh')
        self.no_land_less50nm_route = Route.from_string('kvta @kcmh kvta')
        
        self.f = Flight(total=11.0,
                        pic=10.0,
                        date=today,
                        route=self.local_route)
        
        
    def test_cat_class_columns(self):
        """
        Tests that all the columns that deal with category/class
        output the correct value
        """
        
        # multi engine land
        #########################################################
        
        self.f.plane = self.baron
        self.f.save()
        
        self.failUnlessEqual(self.f.column('single'), "")
        self.failUnlessEqual(self.f.column('m_pic'), "10.0")
        self.failUnlessEqual(self.f.column('m_t'), "")
                
        # multi-sea local
        #########################################################
        
        self.f.plane = self.seaplane
        self.f.save()
        
        self.failUnlessEqual(self.f.column('single'), "11.0")
        self.failUnlessEqual(self.f.column('m_pic'), "")
        self.failUnlessEqual(self.f.column('m_t'), "")
    
    def test_local_route_columns(self):
        """
        Tests the columns that depend on the properties of the route
        when the route is a local flight
        """
        
        self.f.route = self.local_route     # vta vta
        self.f.save()
        
        self.failUnlessEqual(self.f.column('p2p'), "")
        self.failUnlessEqual(self.f.column('atp_xc'), "")
        self.failUnlessEqual(self.f.column('max_width'), "")
        self.failUnlessEqual(self.f.column('line_dist'), "")
    
    def test_less_50_nm_route(self):
        """
        Tests the columns that depend on the properties of the route
        when the route is greater than 50nm
        """
        
        self.f.route = self.less50nm_route   # vta cmh
        self.f.save()
        
        self.failUnlessEqual(self.f.column('p2p'), "11.0")
        self.failUnlessEqual(self.f.column('atp_xc'), "")
        self.failUnlessEqual(self.f.column('max_width'), "19.9")
        self.failUnlessEqual(self.f.column('line_dist'), "19.9")
        
        self.f.route = self.no_land_less50nm_route  # vta @cmh vta
        self.f.save()
        
        self.failUnlessEqual(self.f.column('p2p'), "")
        self.failUnlessEqual(self.f.column('atp_xc'), "")
        self.failUnlessEqual(self.f.column('max_width'), "19.9")
        self.failUnlessEqual(self.f.column('line_dist'), "39.7")
        
    def test_more_50_nm_route(self):
        """
        Tests the columns that depend on the properties of the route
        when the route is less than 50nm
        """
        
        self.f.route = self.no_land_more50nm_route  # vta @luk vta
        self.f.save()
        
        self.failUnlessEqual(self.f.column('p2p'), "")
        self.failUnlessEqual(self.f.column('atp_xc'), "11.0")
        self.failUnlessEqual(self.f.column('max_width'), "106.5")
        self.failUnlessEqual(self.f.column('line_dist'), "212.5")
        
        self.f.route = self.more50nm_route     # vta luk
        self.f.save()
        
        self.failUnlessEqual(self.f.column('p2p'), "11.0")
        self.failUnlessEqual(self.f.column('atp_xc'), "11.0")
        self.failUnlessEqual(self.f.column('max_width'), "106.5")
        self.failUnlessEqual(self.f.column('line_dist'), "106.2")
        
    #def test_empty_logbook_page(self):
    #    response = self.client.get('/test/logbook.html')
    #    self.failUnlessEqual(response.status_code, 200)

class FuelBurnTest(TestCase): 

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


















