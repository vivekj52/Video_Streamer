from .models import Video
from django import forms


class UploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'description', 'file', )
