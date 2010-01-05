from django.test import TestCase

class SimpleTest(TestCase):
    
    fixtures = ['airport/test-fixtures/test-location.json',
                'airport/test-fixtures/test-country.json',
                'airport/test-fixtures/test-region.json',]
    
    
    def test_route_distance(self):
        from models import Route
        
        r = Route.from_string('SNTR SSBT')
        
        ## 3 decimal places (forgive rounding errors)
        s = "%3.3f"
        real_val = 959.70030329462986
        
        self.failUnlessEqual(s % r.max_start_all, s % real_val)

