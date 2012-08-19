import time

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from badges.utils import new_badge

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        users = User.objects.order_by('username')
        chunk = args[0]
        start = int(chunk) * 20
        end = ((int(chunk) + 1) * 20) -1
        new_badge(users=users[start:end])