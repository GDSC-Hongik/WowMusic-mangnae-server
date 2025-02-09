from django.urls import path
from . import views

app_name = 'keyword'

urlpatterns = [
    path("result/", views.get_song_view, name = 'get_song'),

]