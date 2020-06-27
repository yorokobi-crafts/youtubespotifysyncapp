from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yssync/callback/', views.callback, name='callback'),
    path('yssync/ajax/', views.create_playlist_spotify, name='create_playlist_spotify'),
    path('yssync/ajax_url/', views.retrieve_playlist_url, name='retrieve_playlist_url'),
    path('yssync/ajax_videos/', views.retrieve_video_list, name='retrieve_video_list'),
    path('yssync/logout/', views.deleteCookie, name='deleteCookie'),
    path('login/', views.login, name='login'),
    path('google583e06e36e583b27.html/', views.comprobation, name='html')
]
