from django.urls import path
from . import views

urlpatterns = [
    path('video', views.stream_video, name='video'),
    path('play', views.player, name='player'),
    path('movies', views.list_movies, name='movies'),
]
