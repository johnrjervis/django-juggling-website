from django.contrib import admin

from .models import JugglingVideo, VideoComment, Acknowledgement

# Register your models here.
admin.site.register(JugglingVideo)
admin.site.register(VideoComment)
admin.site.register(Acknowledgement)
