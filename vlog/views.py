from django.shortcuts import render
#from django.http import HttpResponse
from vlog.models import JugglingVideo

# Create your views here.
def home_page(request):
    videos = JugglingVideo.objects.all()
    first_video_filename = ''

    if videos:
        first_video_filename = videos[0].filename

    return render(request, 'index.html', {
        'first_video' : first_video_filename,
    })
