from django.shortcuts import render
#from django.http import HttpResponse
from vlog.models import JugglingVideo

# Create your views here.

def index(request):
    videos = JugglingVideo.objects.all().order_by('-pub_date')
    latest_video = ''

    if videos:
        latest_video = videos[0]

    return render(request, 'vlog/index.html', {
        'latest_video' : latest_video,
    })

def detail(request, jugglingvideo_id):
    video = JugglingVideo.objects.get(id = jugglingvideo_id)

    return render(request, 'vlog/detail.html', {
        'video' : video,
    })
