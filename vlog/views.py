from django.shortcuts import render
#from django.http import HttpResponse
from vlog.models import JugglingVideo

# Create your views here.

def home_page(request):
    videos = JugglingVideo.objects.all()
    first_video = ''

    if videos:
        first_video = videos[0]

    return render(request, 'vlog/index.html', {
        'first_video' : first_video,
    })

def detail(request):
    videos = JugglingVideo.objects.all()
    first_video = ''

    if videos:
        first_video = videos[0]

    return render(request, 'vlog/detail.html', {
        'first_video' : first_video,
    })
