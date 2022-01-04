from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from vlog.models import JugglingVideo
from django.utils import timezone

# Create your views here.

def index(request):
    videos = JugglingVideo.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')
    videos_list = ''

    if videos:
        videos_list = [videos[0]]

    return render(request, 'vlog/index.html', {
        'selected': 'Home',
        'videos_list' : videos_list,
    })

def videos_list(request):
    videos = JugglingVideo.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')
    videos_list = ''

    if len(videos) > 1:
        videos_list = videos[1:]

    return render(request, 'vlog/videos.html', {
        'selected': 'Videos',
        'videos_list': videos_list
    })

def video_detail(request, jugglingvideo_id):
    video = get_object_or_404(JugglingVideo.objects.filter(pub_date__lte = timezone.now()), id = jugglingvideo_id)

    return render(request, 'vlog/detail.html', {
        'selected': 'Videos',
        'video': video,
        'new_comment_text': request.POST.get('comment_text', ''),
    })

def learn(request):
    return render(request, 'vlog/learn.html', {
        'selected': 'Learn',
    })

def about(request):
    return render(request, 'vlog/about.html', {
        'selected': 'About',
    })

def thanks(request):
    return render(request, 'vlog/thanks.html', {
        'selected': 'About',
    })

def history(request):
    return render(request, 'vlog/history.html', {
        'selected': 'About',
    })
