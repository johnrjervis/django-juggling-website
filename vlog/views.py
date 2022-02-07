from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.utils import timezone
from django.core.exceptions import ValidationError
from vlog.models import JugglingVideo, VideoComment, Acknowledgement
from vlog.forms import CommentForm

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
    juggling_video = get_object_or_404(JugglingVideo.objects.filter(pub_date__lte = timezone.now()), id = jugglingvideo_id)
    error = None

    if request.method == 'POST':

        if request.POST['author']:
            comment = VideoComment(
                text = request.POST['text'],
                author = request.POST['author'],
                video = juggling_video
            )
        else:
            comment = VideoComment(text = request.POST['text'], video = juggling_video)

        try:
            comment.full_clean()
            comment.save()
            return redirect(juggling_video)

        except ValidationError:
            error = 'Blank comment was not submitted!'

    return render(
        request,
        'vlog/detail.html', 
        {
            'selected': 'Videos',
            'video': juggling_video,
            'form': CommentForm(),
            'error': error,
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
