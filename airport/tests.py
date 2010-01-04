from django.test import TestCase

class SimpleTest(TestCase):
    fixtures = ['airport/test-fixtures/test-location.json',
                'airport/test-fixtures/test-country.json',
                'airport/test-fixtures/test-region.json',
                'airport/test-fixtures/test-worldborders.json',
                'airport/test-fixtures/test-usstates.json']
    
    def test_create_location(self):
        """
        Tests that a new location can be made and that the routine that
        finds which state the location is in is working
        """
        from models import *
        
        pt = (34.322631,-84.481517) # in georgia
        
        loc = Location(loc_class=3,
                       identifier='KCUS',
                       location="POINT (%s %s)" % (pt[1], pt[0]),
                       name="My Custom Point",
                       )
        
        loc.save()
        
        self.failUnlessEqual(loc.country.code, 'US')
        self.failUnlessEqual(loc.region.code, 'US-GA')
        
        
        
    
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
