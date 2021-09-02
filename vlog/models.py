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
