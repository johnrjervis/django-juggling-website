from django.shortcuts import render, redirect, reverse, get_object_or_404 
from vlog.models import JugglingVideo, VideoComment
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
    juggling_video = get_object_or_404(JugglingVideo.objects.filter(pub_date__lte = timezone.now()), id = jugglingvideo_id)

    if request.method == 'POST':
        VideoComment.objects.create(text = request.POST['comment_text'], video = juggling_video)
        return redirect(reverse('vlog:detail', args = [juggling_video.id]))

    comments = VideoComment.objects.filter(video = juggling_video)

    return render(request, 'vlog/detail.html', {
        'selected': 'Videos',
        'video': juggling_video,
        'comments': comments,
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
