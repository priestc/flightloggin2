from django.test import TestCase

class SimpleTest(TestCase):
    def test_kml(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        
        self.failUnlessEqual(1 + 1, 2)
