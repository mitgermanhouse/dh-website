from django.shortcuts import render
from .models import Alumnus
from django.conf import settings

def index(request):
    alumni_by_year = {}
    alumni = Alumnus.objects.all().order_by('-year', 'last_name', 'first_name')
    
    for alum in alumni:
        year = alum.year
        if year not in alumni_by_year:
            alumni_by_year[year] = []
        alumni_by_year[year].append(alum)
    
    # Sort years descending
    years = sorted(alumni_by_year.keys(), reverse=True)
    
    context = {
        'alumni_by_year': [(year, alumni_by_year[year]) for year in years],
        'form_url': settings.ALUMNI_FORM_URL
    }
    return render(request, 'alumni/index.html', context)
