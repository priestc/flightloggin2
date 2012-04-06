from django.test import TestCase
from models import Route

class SimpleTest(TestCase):
    
    fixtures = ['airport/test-fixtures/test-location.json',
                'airport/test-fixtures/test-country.json',
                'airport/test-fixtures/test-region.json',]
    
    
    def test_route_distance(self):
        r = Route.from_string('SNTR SSBT')
        
        ## 3 decimal places (forgive rounding errors)
        s = "%3.3f"
        real_val = 959.70030329462986
        
        self.failUnlessEqual(s % r.max_start_all, s % real_val)
        
    def test_profile_page(self):
        r = Route.from_string('SNTR SSBT')
        response = self.client.get('/route-%s.html' % r.pk)
        self.failUnlessEqual(response.status_code, 200)
        
        r = Route.from_string('SNTR derp SSBT')
        response = self.client.get('/route-%s.html' % r.pk)
        self.failUnlessEqual(response.status_code, 200)
        
        r = Route.from_string('SNTR @derp SSBT')
        response = self.client.get('/route-%s.html' % r.pk)
        self.failUnlessEqual(response.status_code, 200)

