from django.db import models
from django.utils import timezone

# Create your models here.


class JugglingVideo(models.Model):
    filename = models.CharField(max_length = 60, default = '')
    title = models.CharField(max_length = 50, default = '')
    pub_date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f'Juggling video: {self.filename}'

    def __repr__(self):
        return f'{self.__class__}: {self.filename}'


class VideoComment(models.Model):
    text = models.TextField(default = '')
    author = models.TextField(default = 'anonymous')
    video = models.ForeignKey(JugglingVideo, default = None, on_delete = models.SET_DEFAULT)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f'Comment: {self.text}'

    def __repr__(self):
        return f'{self.__class__}: {self.text}'

