from django.contrib import admin

from .models import JugglingVideo, VideoComment

# Register your models here.
admin.site.register(JugglingVideo)
admin.site.register(VideoComment)
