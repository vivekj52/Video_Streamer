from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView

from . import views

urlpatterns = [
    path('video', views.stream_video, name='video'),
    path('play', views.player, name='player'),
    path('movies', views.list_movies, name='movies'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup')
]