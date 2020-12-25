from django.db import models
from django.utils.timezone import now


class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    file = models.FileField(upload_to='', default='some_path')
    time = models.DateTimeField(default=now, editable=False)
