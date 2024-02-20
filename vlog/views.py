from os import environ as os_environ
from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
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
    if request.method == 'POST':
        email_body = f"From: {request.POST['sender_name']}\nMessage: {request.POST['message']}"
        if request.POST['message']:
            send_mail('A message from a website visitor', email_body, os_environ.get('OUTBOUND_EMAIL_ADDRESS'), [os_environ.get('EMAIL_ADDRESS')])
            messages.success(request, 'Your message has been sent!')
        else:
            messages.warning(request, 'Please enter a message.')
        return redirect('vlog:contact')

    return render(request, 'vlog/contact.html', {
        'selected': 'About',
    })
