from django.db import models
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    file = models.FileField(upload_to='', default='some_path',
                            validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    time = models.DateTimeField(default=now, editable=False)
