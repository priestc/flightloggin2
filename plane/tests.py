from django.test import TestCase
from models import Plane

class SimpleTest(TestCase):
    def test_plane_profile_urls(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        p1 = Plane(type="C-172", tailnumber="N12\34334")
        p2 = Plane(type="C17#2", tailnumber="N??1234")
        p3 = Plane(type="C/172", tailnumber="N/1234")
        p4 = Plane(type="C ^72", tailnumber="N1234#")
        p5 = Plane(type="C=172", tailnumber="N1234.")
        p6 = Plane(type="C+17 ", tailnumber="N1234-2")
        p7 = Plane(type="C 172", tailnumber="N1234(1)")
        p8 = Plane(type="C-172", tailnumber="N1234[1]")
        p9 = Plane(type="C-172", tailnumber="N1234{1}")
        p10 = Plane(type=None, tailnumber=None)
        
        p1.save()
        p2.save()
        p3.save()
        p4.save()
        p5.save()
        p6.save()
        p7.save()
        p8.save()
        p9.save()
        p10.save()
        
        self.failUnlessEqual("%s" % p1, "N1234 (C-172)")
        self.failUnlessEqual("%s" % p2, "N1234 (C172)")
        self.failUnlessEqual("%s" % p3, "N1234 (C172)")
        self.failUnlessEqual("%s" % p4, "N1234 (C72)")
        self.failUnlessEqual("%s" % p5, "N1234 (C172)")
        self.failUnlessEqual("%s" % p6, "N1234-2 (C17)")
        self.failUnlessEqual("%s" % p7, "N1234(1) (C172)")
        self.failUnlessEqual("%s" % p8, "N1234[1] (C-172)")
        self.failUnlessEqual("%s" % p9, "N1234{1} (C-172)")
        self.failUnlessEqual("%s" % p10, "")
