import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User

from logbook.forms import PopupFlightForm
from backup.models import edit_logbook
from plane.models import Plane

class Command(BaseCommand):
    help = "Erase All demo information, and rese to defaults"

    def handle(self, *args, **options):
    	demo_user = User.objects.get(id=settings.DEMO_USER_ID)
        
        Flight.objects.filter(user=demo_user).delete()
        Plane.objects.filter(user=demo_user).delete()

        plane1 = Plane.objects.create(user=demo_user, tailnumber="N1234", type='C-172')
        plane2 = Plane.objects.create(user=demo_user, tailnumber="N5555", type='B-737')

        form = PopupFlightForm(dict(
        	user=demo_user,
        	plane=plane2,
        	date=datetime.datetime.now(),
        	route_string='KLGA-KBOS',
        	total=3.2,
        	pic=3.2,
        	remarks="picked up dave"
        ))

        form.save()

        edit_logbook.send(sender=demo_user)