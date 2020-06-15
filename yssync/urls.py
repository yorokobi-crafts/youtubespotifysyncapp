from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('yssync/callback/', views.callback, name='callback'),
    path('yssync/ajax/', views.create_playlist_spotify, name='create_playlist_spotify'),
    path('yssync/ajax_url/', views.retrieve_playlist_url, name='retrieve_playlist_url'),
    path('yssync/ajax_videos/', views.retrieve_video_list, name='retrieve_video_list'),
    path('yssync/ajax_logout/', views.logout_session, name='logout_session'),
    path('yssync/cookietest_set/', views.cookietest_set, name='cookietest_set'),
    path('yssync/cookietest_get/', views.cookietest_get, name='cookietest_get')
]
