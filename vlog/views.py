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

def videos(request):
    videos = JugglingVideo.objects.all().order_by('-pub_date')
    videos_list = ''

    if len(videos) > 1:
        videos_list = videos[1:]

    return render(request, 'vlog/videos.html', {
        'videos_list': videos_list
    })

def detail(request, jugglingvideo_id):
    video = JugglingVideo.objects.get(id = jugglingvideo_id)

    return render(request, 'vlog/detail.html', {
        'video' : video,
    })
