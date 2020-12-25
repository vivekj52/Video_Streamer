from django.contrib import admin
from .models import Video


class VideoAdmin(admin.ModelAdmin):
    fields = ['title', 'description']


admin.site.register(Video, VideoAdmin)
