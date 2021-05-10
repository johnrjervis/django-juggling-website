from django.shortcuts import render
#from django.http import HttpResponse
from vlog.models import JugglingVideo

# Create your views here.
def home_page(request):
    return render(request, 'index.html')
