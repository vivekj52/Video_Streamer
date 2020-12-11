from django.urls import path

from . import views

urlpatterns = [
    path('', views.stream_video, name='index'),
    path('play', views.player, name='index'),
]