from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class JugglingVideo(models.Model):
    filename = models.CharField(max_length = 60, default = '')
    title = models.CharField(max_length = 50, default = '')
    pub_date = models.DateTimeField(default = timezone.now)
    author_comment = models.TextField(default = '')

    @classmethod
    def get_homepage_video(cls):
        videos = JugglingVideo.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')

        return videos[0] if videos else ''

    @classmethod
    def get_archive_videos(cls):
        videos = JugglingVideo.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')

        return videos[1:] if (len(videos) > 1) else []

    def get_static_filename(self):
        return f'vlog/videos/{self.filename}'

    def get_approved_comments(self):
        return self.videocomment_set.filter(is_approved = True)

    def get_absolute_url(self):
        return reverse('vlog:detail', args = [self.id])

    def __str__(self):
        return self.filename

    def __repr__(self):
        return f'{self.__class__}: {self.filename}'


class VideoComment(models.Model):
    text = models.TextField(default = '')
    author = models.TextField(default = 'anonymous')
    video = models.ForeignKey(JugglingVideo, default = None, on_delete = models.SET_DEFAULT)
    date = models.DateTimeField(default = timezone.now)
    is_approved = models.BooleanField(default = True)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.__class__}: {self.text}'


class Acknowledgement(models.Model):
    name = models.TextField(default = '')
    link = models.TextField(default = '')
    description = models.TextField(default = '')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{self.__class__}: {self.name}'

