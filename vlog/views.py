import os
from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from vlog.models import JugglingVideo, VideoComment, Acknowledgement
from vlog.forms import CommentForm, EMPTY_COMMENT_ERROR

# Create your views here.

def index(request):

    return render(request, 'vlog/index.html', {
        'selected': 'Home',
        'video' : JugglingVideo.get_homepage_video(),
    })


def index_redirect(request):
    return redirect(reverse('vlog:index'))


def videos_list(request):

    return render(request, 'vlog/videos.html', {
        'selected': 'Videos',
        'videos_list': JugglingVideo.get_archive_videos()
    })


def video_detail(request, jugglingvideo_id):
    juggling_video = get_object_or_404(
        JugglingVideo.objects.filter(pub_date__lte = timezone.now()),
        id = jugglingvideo_id
    )
    form = CommentForm(for_video = juggling_video)

    if request.method == 'POST':

        form = CommentForm(for_video = juggling_video, data = request.POST)
        if form.is_valid():
            form.save()
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

def contact(request):
    return render(request, 'vlog/contact.html', {
        'selected': 'About',
    })

def send_message(request):
    sender = request.POST['sender_name']
    message = request.POST['message']
    send_mail(
        'A message via the juggling website',
        f'from: {sender}\nmessage: {message}',
        'jjs_juggling_videos@outlook.com',
        [os.environ.get('EMAIL_ADDRESS')]
    )
    return redirect(reverse('vlog:contact'))
