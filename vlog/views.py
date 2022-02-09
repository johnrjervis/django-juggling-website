from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.utils import timezone
from django.core.exceptions import ValidationError
from vlog.models import JugglingVideo, VideoComment, Acknowledgement
from vlog.forms import CommentForm, EMPTY_COMMENT_ERROR

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


def index_redirect(request):
    return redirect(reverse('vlog:index'))


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
    juggling_video = get_object_or_404(
        JugglingVideo.objects.filter(pub_date__lte = timezone.now()),
        id = jugglingvideo_id
    )
    form = CommentForm()

    if request.method == 'POST':

        form = CommentForm(data = request.POST)
        if form.is_valid():
            form.save(for_video = juggling_video)
            return redirect(juggling_video)

    return render(
        request,
        'vlog/detail.html', 
        {
            'selected': 'Videos',
            'video': juggling_video,
            'form': form,
        }
    )


def learn(request):
    return render(request, 'vlog/learn.html', {
        'selected': 'Learn',
    })


def about(request):
    return render(request, 'vlog/about.html', {
        'selected': 'About',
    })


def thanks(request):
    acknowledgements = Acknowledgement.objects.all()

    return render(request, 'vlog/thanks.html', {
        'acknowledgements': acknowledgements,
        'selected': 'About',
    })


def history(request):
    return render(request, 'vlog/history.html', {
        'selected': 'About',
    })
