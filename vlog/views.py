from django.shortcuts import render
#from django.http import HttpResponse
from vlog.models import JugglingVideo

# Create your views here.

def index(request):
    videos = JugglingVideo.objects.all()
    first_video = ''

    if videos:
        first_video = videos[0]

    return render(request, 'vlog/index.html', {
        'first_video' : first_video,
    })

def detail(request, jugglingvideo_id):
    video = JugglingVideo.objects.get(id = jugglingvideo_id)

    return render(request, 'vlog/detail.html', {
        'video' : video,
    })
