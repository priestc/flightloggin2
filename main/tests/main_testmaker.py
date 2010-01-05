
from django.test import TestCase
from django.test import Client
from django import template
from django.db.models import get_model

class Testmaker(TestCase):

    fixtures = ["/srv/flightloggin/main/fixtures/test-user.json",]


    def test_chrislogbookhtml_126266092883(self):
        r = self.client.get('/chris/logbook.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrisplaneshtml_126266093305(self):
        r = self.client.get('/chris/planes.html', {})
        self.assertEqual(r.status_code, 200)
        print r.context[-1]
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chriseventshtml_126266093483(self):
        r = self.client.get('/chris/events.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrislocationshtml_126266093651(self):
        r = self.client.get('/chris/locations.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrisrecordshtml_126266093799(self):
        r = self.client.get('/chris/records.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrislinegraphshtml_126266094001(self):
        r = self.client.get('/chris/linegraphs.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrislinegraphtotalnorate_spikespng_126266094086(self):
        r = self.client.get('/chris/linegraph/total/norate-spikes.png', {})
        self.assertEqual(r.status_code, 200)
    def test_chrisbargraphshtml_126266094191(self):
        r = self.client.get('/chris/bargraphs.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrisbargraphtotalsumby_typepng_126266094261(self):
        r = self.client.get('/chris/bargraph/total/Sum/by-type.png', {})
        self.assertEqual(r.status_code, 200)
    def test_chrismapshtml_126266094424(self):
        r = self.client.get('/chris/maps.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_states90states_coloredpng_126266094481(self):
        r = self.client.get('/states/90/states-colored.png', {})
        self.assertEqual(r.status_code, 404)
    def test_states90states_countpng_126266094487(self):
        r = self.client.get('/states/90/states-count.png', {})
        self.assertEqual(r.status_code, 404)
    def test_states90states_uniquepng_126266094495(self):
        r = self.client.get('/states/90/states-unique.png', {})
        self.assertEqual(r.status_code, 404)
    def test_chris8710html_126266094558(self):
        r = self.client.get('/chris/8710.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrissigshtml_126266094863(self):
        r = self.client.get('/chris/sigs.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrissigspicpng_126266094927(self):
        r = self.client.get('/chris/sigs/pic.png', {})
        self.assertEqual(r.status_code, 200)
    def test_chrisnologo_sigsveramono_10total_picpng_126266094942(self):
        r = self.client.get('/chris/nologo-sigs/VeraMono-10/total-pic.png', {})
        self.assertEqual(r.status_code, 200)
    def test_chriscurrencyhtml_126266095017(self):
        r = self.client.get('/chris/currency.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrismilestoneshtml_126266095266(self):
        r = self.client.get('/chris/milestones.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_smallbar00_1200png_126266095427(self):
        r = self.client.get('/smallbar/0.0--1200.png', {})
        self.assertEqual(r.status_code, 200)
    def test_smallbar00_100png_126266095428(self):
        r = self.client.get('/smallbar/0.0--100.png', {})
        self.assertEqual(r.status_code, 200)
    def test_smallbar00_500png_126266095429(self):
        r = self.client.get('/smallbar/0.0--500.png', {})
        self.assertEqual(r.status_code, 200)
    def test_smallbar0_75png_126266095431(self):
        r = self.client.get('/smallbar/0--75.png', {})
        self.assertEqual(r.status_code, 200)
    def test_smallbar00_25png_126266095432(self):
        r = self.client.get('/smallbar/0.0--25.png', {})
        self.assertEqual(r.status_code, 200)
    def test_smallbar00_1500png_126266095432(self):
        r = self.client.get('/smallbar/0.0--1500.png', {})
        self.assertEqual(r.status_code, 200)
    def test_smallbar00_250png_126266095434(self):
        r = self.client.get('/smallbar/0.0--250.png', {})
        self.assertEqual(r.status_code, 200)
    def test_chrismassentryhtml_126266095563(self):
        r = self.client.get('/chris/massentry.html', {})
        self.assertEqual(r.status_code, 302)
    def test_chrisimporthtml_126266096101(self):
        r = self.client.get('/chris/import.html', {})
        self.assertEqual(r.status_code, 302)
    def test_chrisexporthtml_126266096234(self):
        r = self.client.get('/chris/export.html', {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(unicode(r.context[-1]['records']), u'[]')
    def test_chrispreferenceshtml_12626609636(self):
        r = self.client.get('/chris/preferences.html', {})
        self.assertEqual(r.status_code, 302)
