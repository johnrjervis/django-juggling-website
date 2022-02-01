from django.db import models
from django.utils import timezone

# Create your models here.


class JugglingVideo(models.Model):
    filename = models.CharField(max_length = 60, default = '')
    title = models.CharField(max_length = 50, default = '')
    pub_date = models.DateTimeField(default = timezone.now)
    author_comment = models.TextField(default = '')

    def __str__(self):
        return f'Juggling video: {self.filename}'

    def __repr__(self):
        return f'{self.__class__}: {self.filename}'


class VideoComment(models.Model):
    text = models.TextField(default = '')
    author = models.TextField(default = 'anonymous')
    video = models.ForeignKey(JugglingVideo, default = None, on_delete = models.SET_DEFAULT)
    date = models.DateTimeField(default = timezone.now)
    is_approved = models.BooleanField(default = True)

    def __str__(self):
        return f'Comment: {self.text}'

    def __repr__(self):
        return f'{self.__class__}: {self.text}'


class Acknowledgement(models.Model):
    name = models.TextField(default = '')
    link = models.TextField(default = '')
    description = models.TextField(default = '')

    def __str__(self):
        return f'Acknowledgement: {self.name}'

    def __repr__(self):
        return f'{self.__class__}: {self.name}'

