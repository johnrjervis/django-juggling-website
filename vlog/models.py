from django.db import models

# Create your models here.

class JugglingVideo(models.Model):
    filename = models.CharField(max_length=60, default='')
