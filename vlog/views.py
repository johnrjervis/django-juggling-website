from django.shortcuts import render
#from django.http import HttpResponse
from vlog.models import JugglingVideo

# Create your views here.
def home_page(request):
    videos = JugglingVideo.objects.all()
    error_message = ''
    first_video_filename = ''

    if videos:
        first_video_filename = videos[0].filename
    else:
        error_message = 'No videos are available!'

    return render(request, 'index.html', {
        'first_video' : first_video_filename,
        'error_message': error_message
    })
