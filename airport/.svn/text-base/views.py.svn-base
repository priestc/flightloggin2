from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.shortcuts import get_object_or_404

from models import *
from main.models import Company, Operation

################################

@render_to('view_airport.html')
def airport(request, pk):

    airport = get_object_or_404(Airport, pk=pk)

    company_base =  Company.objects.filter(operation__opbase__base=airport).distinct()         #ops where this airport is a base
    ops_fly =       Operation.objects.filter(opbase__route__bases=airport).distinct()          #ops where this airport is part of a route

    return locals()
