from django.contrib import admin
from .models import JugglingVideo, VideoComment, Acknowledgement


# Register your models here.

class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'video_id', 'video', 'is_approved')

admin.site.register(JugglingVideo)
admin.site.register(VideoComment, VideoCommentAdmin)
admin.site.register(Acknowledgement)
