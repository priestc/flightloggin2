from django.test import TestCase

class SimpleTest(TestCase):
    fixtures = ['airport/test-fixtures/test-location.json',
                'airport/test-fixtures/test-country.json',
                'airport/test-fixtures/test-region.json',
                'airport/test-fixtures/test-worldborders.json',
                'airport/test-fixtures/test-usstates.json']
    
    def test_location_in_georgia(self):
        """
        Tests that a new location can be made and that the routine that
        finds which state the location is in is working
        """
        from models import Location
        
        pt = (34.322631,-84.481517) # in georgia
        
        loc = Location(
                       loc_class=3,
                       identifier='KCUS',
                       location="POINT (%s %s)" % (pt[1], pt[0]),
                       name="My Custom Point",
                      )
        
        loc.save()
        
        self.failUnlessEqual(loc.country.code, 'US')
        self.failUnlessEqual(loc.region.code, 'US-GA')
        
    def test_location_in_the_ocean(self):
        """
        Tests that a new location can be made and that the routine that
        finds which state the location is in is working
        """
        from models import Location
        
        pt = (-2.4,2.1) # in the middle of the ocean
        
        loc = Location(
                       loc_class=3,
                       identifier='KCUS',
                       location="POINT (%s %s)" % (pt[1], pt[0]),
                       name="My Custom Point in the ocean",
                      )
        
        loc.save()
        
        self.failUnlessEqual(loc.country.code, '')
        self.failUnlessEqual(loc.region, None)
        
    def test_profile_page(self):
        response = self.client.get('/airport-SNTR.html')
        self.failUnlessEqual(response.status_code, 200)
        
    def test_profile_redirect(self):
        response = self.client.get('/location-SNTR.html')
        self.failUnlessEqual(response.status_code, 302)  
    
